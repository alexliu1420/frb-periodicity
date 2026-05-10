"""Reusable physical calculations for the stage scripts.

Inputs:
    Periods, drift rates, observing frequencies, apertures, burst energetics,
    and synthetic or real polarization-angle arrays.

Outputs:
    Dataclass result records for orbital-aberration, active-tracking,
    energy-budget, duty-cycle, and RVM-fitting calculations.

Pipeline role:
    Centralizes the physics and mathematics so every stage uses the same
    equations and unit conversions. Code license: MIT -- see LICENSE for details.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi, sqrt

import numpy as np
from scipy.optimize import curve_fit

from .constants import (
    AU_M,
    C_M_S,
    DAYS_PER_YEAR,
    G_M3_KG_S2,
    L_SUN_ERG_S,
    M_SUN_KG,
    SECONDS_PER_DAY,
    FIDUCIAL_FOCAL_DISTANCE_AU,
    SOLAR_DIAMETER_M,
    hz_per_s_to_mhz_per_ms,
    mhz_per_ms_to_hz_per_s,
)


@dataclass(frozen=True)
class PassiveAberrationResult:
    period_days: float
    orbital_radius_au: float
    orbital_velocity_km_s: float
    orbital_acceleration_m_s2: float
    sweep_rate_rad_s: float
    required_aperture_km: float | None
    predicted_dfdt_mhz_ms: float


@dataclass(frozen=True)
class ActiveTrackingResult:
    dfdt_mhz_ms: float
    frequency_mhz: float
    aperture_km: float
    focal_distance_au: float
    sweep_rate_rad_s: float
    transverse_velocity_km_s: float


@dataclass(frozen=True)
class EnergyBudgetResult:
    beam_divergence_rad: float
    beam_solid_angle_sr: float
    beaming_fraction: float
    true_energy_erg: float
    true_power_erg_s: float
    true_power_l_sun: float


@dataclass(frozen=True)
class RVMFitResult:
    reduced_chi_squared: float
    chi_squared: float
    dof: int
    fitted_parameters: tuple[float, float, float, float]
    note: str


def kepler_period_days(radius_au: float, star_mass_sol: float = 1.0) -> float:
    """Keplerian circular-orbit period in days for AU and solar masses."""
    # In solar units Kepler's third law is P^2 = a^3 / M, where P is years,
    # a is AU, and M is solar masses.
    return sqrt(radius_au**3 / star_mass_sol) * DAYS_PER_YEAR


def observed_orbital_period_range(
    redshift: float,
    min_radius_au: float = 0.1,
    max_radius_au: float = 50.0,
    star_mass_sol: float = 1.0,
) -> tuple[float, float]:
    """Return observed-frame Keplerian period bounds in days."""
    rest_min = kepler_period_days(min_radius_au, star_mass_sol)
    rest_max = kepler_period_days(max_radius_au, star_mass_sol)
    # Cosmological time dilation stretches source-frame periods by (1 + z).
    return rest_min * (1.0 + redshift), rest_max * (1.0 + redshift)


def circular_orbit_from_period(period_days: float, star_mass_sol: float = 1.0) -> tuple[float, float, float]:
    """Return radius in meters, orbital velocity in m/s, and acceleration in m/s^2."""
    period_s = period_days * SECONDS_PER_DAY
    star_mass_kg = star_mass_sol * M_SUN_KG
    # Rearranged circular Kepler law: a = (G M P^2 / 4pi^2)^(1/3).
    radius_m = (G_M3_KG_S2 * star_mass_kg * period_s**2 / (4.0 * pi**2)) ** (1.0 / 3.0)
    velocity_m_s = 2.0 * pi * radius_m / period_s
    # Centripetal acceleration sets the aberration sweep scale in this model.
    acceleration_m_s2 = velocity_m_s**2 / radius_m
    return radius_m, velocity_m_s, acceleration_m_s2


def passive_aberration_result(
    period_days: float,
    dfdt_mhz_ms: float | None,
    frequency_mhz: float,
    aperture_m: float = SOLAR_DIAMETER_M,
    star_mass_sol: float = 1.0,
) -> PassiveAberrationResult:
    """Compute passive orbital-aberration predictions for a fixed aperture."""
    radius_m, velocity_m_s, acceleration_m_s2 = circular_orbit_from_period(period_days, star_mass_sol)
    # Small-angle aberration changes at approximately a_orb / c.
    sweep_rate = acceleration_m_s2 / C_M_S
    frequency_hz = frequency_mhz * 1e6
    # Beam-width model: theta ~ lambda/D = c/(fD), so df/dt = -f^2 D Omega/c.
    predicted_hz_s = -(aperture_m * frequency_hz**2 * sweep_rate) / C_M_S
    required_aperture_km = None
    if dfdt_mhz_ms is not None:
        # Invert the same relation to ask what aperture would reproduce an
        # observed drift under passive orbital aberration.
        required_aperture_m = abs(mhz_per_ms_to_hz_per_s(dfdt_mhz_ms)) * C_M_S / (
            frequency_hz**2 * sweep_rate
        )
        required_aperture_km = required_aperture_m / 1000.0
    return PassiveAberrationResult(
        period_days=period_days,
        orbital_radius_au=radius_m / AU_M,
        orbital_velocity_km_s=velocity_m_s / 1000.0,
        orbital_acceleration_m_s2=acceleration_m_s2,
        sweep_rate_rad_s=sweep_rate,
        required_aperture_km=required_aperture_km,
        predicted_dfdt_mhz_ms=hz_per_s_to_mhz_per_ms(predicted_hz_s),
    )


def active_tracking_result(
    dfdt_mhz_ms: float,
    frequency_mhz: float,
    aperture_m: float = SOLAR_DIAMETER_M,
    focal_distance_au: float = FIDUCIAL_FOCAL_DISTANCE_AU,
) -> ActiveTrackingResult:
    """Compute the sweep rate and transverse velocity implied by active tracking."""
    frequency_hz = frequency_mhz * 1e6
    # Active tracking keeps the beam-width relation but treats Omega as a free
    # tracking rate rather than tying it to the macroscopic activity period.
    sweep_rate = abs(mhz_per_ms_to_hz_per_s(dfdt_mhz_ms)) * C_M_S / (frequency_hz**2 * aperture_m)
    transverse_velocity_km_s = sweep_rate * focal_distance_au * AU_M / 1000.0
    return ActiveTrackingResult(
        dfdt_mhz_ms=dfdt_mhz_ms,
        frequency_mhz=frequency_mhz,
        aperture_km=aperture_m / 1000.0,
        focal_distance_au=focal_distance_au,
        sweep_rate_rad_s=sweep_rate,
        transverse_velocity_km_s=transverse_velocity_km_s,
    )


def energy_budget(
    isotropic_energy_erg: float,
    duration_ms: float,
    frequency_mhz: float = 600.0,
    aperture_m: float = SOLAR_DIAMETER_M,
) -> EnergyBudgetResult:
    """Estimate beaming-corrected energy under a simple circular-cone aperture.

    This uses theta = lambda / D as an order-of-magnitude divergence angle. A
    textbook Airy first-null estimate would introduce a 1.22 factor and change
    the beaming fraction by about 50 percent.
    """
    wavelength_m = C_M_S / (frequency_mhz * 1e6)
    divergence_rad = wavelength_m / aperture_m
    # Approximate a narrow circular cone with solid angle pi(theta/2)^2.
    solid_angle_sr = pi * (divergence_rad / 2.0) ** 2
    beaming_fraction = solid_angle_sr / (4.0 * pi)
    true_energy_erg = isotropic_energy_erg * beaming_fraction
    true_power_erg_s = true_energy_erg / (duration_ms / 1000.0)
    return EnergyBudgetResult(
        beam_divergence_rad=divergence_rad,
        beam_solid_angle_sr=solid_angle_sr,
        beaming_fraction=beaming_fraction,
        true_energy_erg=true_energy_erg,
        true_power_erg_s=true_power_erg_s,
        true_power_l_sun=true_power_erg_s / L_SUN_ERG_S,
    )


def duty_cycle(period_days: float, window_days: float) -> tuple[float, float]:
    """Return duty cycle and equivalent visible longitude angle in degrees."""
    duty = window_days / period_days
    return duty, duty * 360.0


def rvm_model(phi: np.ndarray, alpha: float, zeta: float, psi0: float, phi0: float) -> np.ndarray:
    """Rotating Vector Model polarization angle, in radians."""
    # Standard RVM form using atan2 to preserve the correct quadrant of the
    # polarization-angle swing.
    num = np.sin(alpha) * np.sin(phi - phi0)
    den = np.sin(zeta) * np.cos(alpha) - np.cos(zeta) * np.sin(alpha) * np.cos(phi - phi0)
    return np.arctan2(num, den) + psi0


def angle_residual(observed: np.ndarray, predicted: np.ndarray) -> np.ndarray:
    """Return wrapped PA residuals in radians."""
    # Polarization angle is periodic; wrapping avoids false large residuals near
    # the +/-pi boundary.
    return np.arctan2(np.sin(observed - predicted), np.cos(observed - predicted))


def fit_rvm_to_pa(phases: np.ndarray, observed_pa: np.ndarray, pa_error: np.ndarray) -> RVMFitResult:
    """Fit an RVM curve to PA data.

    This is suitable for synthetic or real PA arrays, but scientific claims require
    real burst-level PA measurements and uncertainties.
    """

    def fit_func(phi: np.ndarray, alpha: float, zeta: float, psi0: float, phi0: float) -> np.ndarray:
        return rvm_model(phi, alpha, zeta, psi0, phi0)

    bounds = ([0.0, 0.0, -np.pi, phases.min() - np.pi], [np.pi, np.pi, np.pi, phases.max() + np.pi])
    initial = (np.pi / 4.0, np.pi / 3.0, float(np.median(observed_pa)), 0.0)
    # Weighted nonlinear least squares using provided PA errors; real analyses
    # should add physically motivated priors and compare multiple model classes.
    popt, _ = curve_fit(
        fit_func,
        phases,
        observed_pa,
        p0=initial,
        sigma=pa_error,
        absolute_sigma=True,
        bounds=bounds,
        maxfev=20000,
    )
    residual = angle_residual(observed_pa, fit_func(phases, *popt))
    chi_squared = float(np.sum((residual / pa_error) ** 2))
    dof = max(1, len(phases) - len(popt))
    return RVMFitResult(
        reduced_chi_squared=chi_squared / dof,
        chi_squared=chi_squared,
        dof=dof,
        fitted_parameters=tuple(float(value) for value in popt),
        note="Fit quality alone does not reject natural models without real PA data, priors, and model comparison.",
    )
