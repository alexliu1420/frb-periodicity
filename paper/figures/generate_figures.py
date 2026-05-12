"""Generate the two figures for the FRB periodicity preprint.

Inputs:
    Curated source values from frb/data.py and physical equations from
    frb/models.py. The script imports rather than re-deriving so any
    future data correction propagates automatically.

Outputs:
    paper/figures/figure1_joint_test.{pdf,png}
    paper/figures/figure2_rfocal_contours.{pdf,png}

Pipeline role:
    Visualizes (1) the passive sub-case failure under joint period +
    frequency comparison with explicit Brown et al. 2024 alpha
    uncertainty bands, and (2) the active-tracking model's family of
    consistencies parameterized by R_focal. The numerical content
    matches the paper's Section 3.1 sensitivity table and Section 4.3
    table; a sanity-check print pass at the end verifies consistency.

Code license: MIT -- see LICENSE for details.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Add repo root to path so we can import frb.* when running from paper/figures/.
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from frb.constants import AU_M, C_M_S, SOLAR_DIAMETER_M
from frb.data import sources_with_dfdt
from frb.models import active_tracking_result, passive_aberration_result


# ----- Configuration -----------------------------------------------------------

ALPHA_CENTRAL = 2.0
ALPHA_SIGMA = 0.2  # Brown et al. 2024 1-sigma uncertainty on the power-law exponent
FAILURE_THRESHOLD = 5.0  # Pre-declared scaling failure factor from stage5
FIDUCIAL_R_FOCAL_AU = 550.0
R_FOCAL_CONTOURS_AU = [55.0, 550.0, 5500.0, 50000.0]

FIGURE_DIR = Path(__file__).resolve().parent
FIGURE1_BASENAME = "figure1_joint_test"
FIGURE2_BASENAME = "figure2_rfocal_contours"

# Color palette (colorblind-safe selections from matplotlib's "tab10").
COLOR_PREDICTION = "#d62728"
COLOR_BAND_1SIGMA = "#fbb4ae"
COLOR_BAND_2SIGMA = "#fde0dd"
COLOR_THRESHOLD = "#7f7f7f"
COLOR_FIDUCIAL = "#d62728"
COLOR_OTHER_CONTOUR = "#999999"
COLOR_BAND_PLAUSIBLE = "#e6f0ff"

# Per-source identity (used consistently across Figure 1 and Figure 2).
SOURCE_STYLES = {
    "FRB 20180916B": {"color": "#1f77b4", "marker": "o"},  # blue circle
    "FRB 20121102A": {"color": "#2ca02c", "marker": "s"},  # green square
}


# ----- Data prep ---------------------------------------------------------------

def get_anchor_records() -> dict[str, dict[str, float]]:
    """Return curated anchor source values indexed by source name."""
    anchors: dict[str, dict[str, float]] = {}
    for source in sources_with_dfdt():
        anchors[source.name] = {
            "period_days": source.period_days,
            "dfdt_mhz_ms": source.dfdt_mhz_ms,
            "frequency_mhz": source.dfdt_frequency_mhz,
        }
    return anchors


def predicted_ratio(alpha: float, anchor_1: dict[str, float], anchor_2: dict[str, float]) -> float:
    """Cross-source predicted |df/dt| ratio under df/dt = C f^alpha P^(-4/3)."""
    freq_ratio = anchor_2["frequency_mhz"] / anchor_1["frequency_mhz"]
    period_ratio = anchor_1["period_days"] / anchor_2["period_days"]
    return (freq_ratio**alpha) * (period_ratio ** (4.0 / 3.0))


def observed_ratio(anchor_1: dict[str, float], anchor_2: dict[str, float]) -> float:
    """Observed |df/dt| ratio (raw, native frequencies)."""
    return abs(anchor_2["dfdt_mhz_ms"]) / abs(anchor_1["dfdt_mhz_ms"])


def discrepancy_factor(alpha: float, anchor_1: dict[str, float], anchor_2: dict[str, float]) -> float:
    return observed_ratio(anchor_1, anchor_2) / predicted_ratio(alpha, anchor_1, anchor_2)


# ----- Figure 1: joint period+frequency falsification --------------------------

def generate_figure_1(anchors: dict[str, dict[str, float]]) -> None:
    """|df/dt|/f^2 versus P with Brown et al. 2024 alpha uncertainty bands."""
    anchor_short = anchors["FRB 20180916B"]
    anchor_long = anchors["FRB 20121102A"]

    # Convert frequencies to GHz for cleaner y-axis units (MHz/(ms*GHz^2)).
    f_short_ghz = anchor_short["frequency_mhz"] / 1000.0
    f_long_ghz = anchor_long["frequency_mhz"] / 1000.0

    # Observed values normalized by f^2.
    y_short_obs = abs(anchor_short["dfdt_mhz_ms"]) / f_short_ghz**2
    y_long_obs = abs(anchor_long["dfdt_mhz_ms"]) / f_long_ghz**2

    # Prediction line: P^(-4/3) normalized to FRB 20180916B's f^2-normalized
    # observed value. At each P, the predicted |df/dt|/f^2 follows
    # y(P) = y_short_obs * (P_short / P)^(4/3).
    p_short = anchor_short["period_days"]
    p_long = anchor_long["period_days"]
    p_grid = np.logspace(np.log10(p_short * 0.5), np.log10(p_long * 1.4), 200)
    y_pred_line = y_short_obs * (p_short / p_grid) ** (4.0 / 3.0)

    # Predicted value at the long-period anchor under various alpha. With
    # y-axis = |df/dt|/f^2, propagating the anchor with alpha != 2 adds an
    # extra factor (f_long/f_short)^(alpha-2).
    def predicted_at_long(alpha: float) -> float:
        return (
            y_short_obs
            * (f_long_ghz / f_short_ghz) ** (alpha - 2.0)
            * (p_short / p_long) ** (4.0 / 3.0)
        )

    y_pred_central = predicted_at_long(ALPHA_CENTRAL)
    y_pred_1sigma_low = predicted_at_long(ALPHA_CENTRAL + ALPHA_SIGMA)  # higher alpha -> larger prediction
    y_pred_1sigma_high = predicted_at_long(ALPHA_CENTRAL - ALPHA_SIGMA)  # lower alpha -> smaller prediction
    y_pred_2sigma_low = predicted_at_long(ALPHA_CENTRAL + 2 * ALPHA_SIGMA)
    y_pred_2sigma_high = predicted_at_long(ALPHA_CENTRAL - 2 * ALPHA_SIGMA)

    # The failure-threshold reference: 5x the central prediction at long-period anchor.
    y_threshold_at_long = y_pred_central * FAILURE_THRESHOLD
    y_threshold_line = y_pred_line * FAILURE_THRESHOLD

    fig, ax = plt.subplots(figsize=(7.2, 5.4))

    # 2-sigma band first (lighter, drawn underneath).
    ax.fill_betweenx(
        [y_pred_2sigma_low, y_pred_2sigma_high],
        p_long * 0.93,
        p_long * 1.07,
        color=COLOR_BAND_2SIGMA,
        alpha=0.7,
        label=r"$2\sigma$ on $\alpha=2.0\pm0.4$ (Brown+ 2024)",
    )
    # 1-sigma band.
    ax.fill_betweenx(
        [y_pred_1sigma_low, y_pred_1sigma_high],
        p_long * 0.93,
        p_long * 1.07,
        color=COLOR_BAND_1SIGMA,
        alpha=0.9,
        label=r"$1\sigma$ on $\alpha=2.0\pm0.2$ (Brown+ 2024)",
    )

    # Prediction line.
    ax.plot(
        p_grid,
        y_pred_line,
        color=COLOR_PREDICTION,
        linestyle="-",
        linewidth=1.8,
        label=r"Passive prediction: $|df/dt|/f^2 \propto P^{-4/3}$ (anchored)",
    )

    # 5x failure threshold reference line.
    ax.plot(
        p_grid,
        y_threshold_line,
        color=COLOR_THRESHOLD,
        linestyle="--",
        linewidth=1.2,
        alpha=0.7,
        label=rf"$5\times$ failure threshold (stage5_scaling_test)",
    )

    # Data points -- per-source color/marker matches Figure 2 for cross-figure
    # consistency: FRB 20180916B = blue circle, FRB 20121102A = green square.
    style_short = SOURCE_STYLES["FRB 20180916B"]
    style_long = SOURCE_STYLES["FRB 20121102A"]
    ax.scatter(
        [p_short],
        [y_short_obs],
        color=style_short["color"],
        marker=style_short["marker"],
        s=80,
        zorder=5,
        edgecolors="black",
        linewidths=0.8,
        label=f"FRB 20180916B (f = {f_short_ghz*1000:.0f} MHz, observed)",
    )
    ax.scatter(
        [p_long],
        [y_long_obs],
        color=style_long["color"],
        marker=style_long["marker"],
        s=80,
        zorder=5,
        edgecolors="black",
        linewidths=0.8,
        label=f"FRB 20121102A (f = {f_long_ghz*1000:.0f} MHz, observed)",
    )

    # Annotations for source names (frequencies are already in legend).
    ax.annotate(
        "FRB 20180916B",
        xy=(p_short, y_short_obs),
        xytext=(p_short * 0.55, y_short_obs * 1.35),
        fontsize=9,
        ha="center",
    )
    ax.annotate(
        "FRB 20121102A",
        xy=(p_long, y_long_obs),
        xytext=(p_long * 1.05, y_long_obs * 1.5),
        fontsize=9,
        ha="left",
    )

    # Discrepancy arrow from prediction (central) to observation at long-period anchor.
    discrepancy_central = y_long_obs / y_pred_central
    ax.annotate(
        rf"$\approx {discrepancy_central:.1f}\times$ discrepancy",
        xy=(p_long, y_long_obs),
        xytext=(p_long * 1.05, y_pred_central * 1.7),
        fontsize=10,
        ha="left",
        arrowprops=dict(arrowstyle="->", color="black", lw=0.7),
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(p_short * 0.4, p_long * 1.5)
    ax.set_ylim(y_pred_2sigma_low * 0.5, y_short_obs * 2.5)
    ax.set_xlabel("Activity period $P$ (days)", fontsize=11)
    ax.set_ylabel(r"$|df/dt|\,/\,f^{2}$  (MHz/(ms$\cdot$GHz$^{2}$))", fontsize=11)
    ax.set_title("Joint period + frequency falsification of the passive sub-case", fontsize=11)
    ax.grid(True, which="both", linestyle=":", linewidth=0.4, alpha=0.6)
    ax.legend(loc="lower left", fontsize=8, framealpha=0.9)

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"{FIGURE1_BASENAME}.pdf")
    fig.savefig(FIGURE_DIR / f"{FIGURE1_BASENAME}.png", dpi=200)
    plt.close(fig)

    # Sanity check.
    print("--- Figure 1 sanity check ---")
    print(f"  FRB 20180916B observed |df/dt|/f^2: {y_short_obs:.3f} MHz/(ms*GHz^2)")
    print(f"  FRB 20121102A observed |df/dt|/f^2: {y_long_obs:.3f} MHz/(ms*GHz^2)")
    print(f"  Predicted at long-period anchor (alpha=2.0): {y_pred_central:.3f}")
    print(f"  1-sigma band: {y_pred_1sigma_low:.3f} to {y_pred_1sigma_high:.3f}")
    print(f"  2-sigma band: {y_pred_2sigma_low:.3f} to {y_pred_2sigma_high:.3f}")
    print(f"  Discrepancy at central alpha: {discrepancy_central:.2f}x")
    print(f"  Discrepancy at +1-sigma alpha: {y_long_obs/y_pred_1sigma_high:.2f}x")
    print(f"  Discrepancy at -1-sigma alpha: {y_long_obs/y_pred_1sigma_low:.2f}x")
    print(f"  Discrepancy at +2-sigma alpha: {y_long_obs/y_pred_2sigma_high:.2f}x")
    print(f"  Discrepancy at -2-sigma alpha: {y_long_obs/y_pred_2sigma_low:.2f}x")


# ----- Figure 2: active-tracking R_focal contours ------------------------------

def generate_figure_2(anchors: dict[str, dict[str, float]], with_plausible_band: bool) -> None:
    """v_perp versus Omega with R_focal contours and anchor points."""
    omega_grid = np.logspace(-11, -8, 200)
    fig, ax = plt.subplots(figsize=(7.2, 5.4))

    # Optional plausible kinematic regime band (10 to 1000 km/s).
    if with_plausible_band:
        ax.fill_between(
            omega_grid,
            10,
            1000,
            color=COLOR_BAND_PLAUSIBLE,
            alpha=0.7,
            zorder=0,
            label="Non-relativistic kinematic regime (illustrative)",
        )

    # Relativistic-velocity hatch region (> ~30000 km/s, ~0.1c).
    relativistic_threshold = 30000.0
    ax.fill_between(
        omega_grid,
        relativistic_threshold,
        1e6,
        color="#ffcccc",
        alpha=0.4,
        hatch="//",
        edgecolor="#999999",
        linewidth=0.0,
        zorder=0,
        label=r"Approaches relativistic ($v_{\perp} \gtrsim 0.1c$)",
    )

    # R_focal contours.
    for r_au in R_FOCAL_CONTOURS_AU:
        v_grid = omega_grid * r_au * AU_M / 1000.0  # km/s
        is_fiducial = abs(r_au - FIDUCIAL_R_FOCAL_AU) < 1e-6
        color = COLOR_FIDUCIAL if is_fiducial else COLOR_OTHER_CONTOUR
        linewidth = 2.2 if is_fiducial else 1.0
        linestyle = "-" if is_fiducial else "--"
        label = (
            rf"$R_\mathrm{{focal}} = {r_au:.0f}$ AU (fiducial)"
            if is_fiducial
            else rf"$R_\mathrm{{focal}} = {r_au:.0f}$ AU"
        )
        ax.plot(omega_grid, v_grid, color=color, linewidth=linewidth, linestyle=linestyle, label=label)

    # Anchor points at fiducial R_focal (550 AU). Color/marker shared with
    # Figure 1 via SOURCE_STYLES so the two figures stay visually consistent.
    for name in ["FRB 20180916B", "FRB 20121102A"]:
        style = SOURCE_STYLES[name]
        rec = anchors[name]
        result = active_tracking_result(
            dfdt_mhz_ms=rec["dfdt_mhz_ms"],
            frequency_mhz=rec["frequency_mhz"],
            aperture_m=SOLAR_DIAMETER_M,
            focal_distance_au=FIDUCIAL_R_FOCAL_AU,
        )
        ax.scatter(
            [result.sweep_rate_rad_s],
            [result.transverse_velocity_km_s],
            color=style["color"],
            marker=style["marker"],
            s=90,
            zorder=5,
            edgecolors="black",
            linewidths=0.8,
            label=f"{name} (f = {rec['frequency_mhz']:.0f} MHz)",
        )
        ax.annotate(
            f"{name}\nv⊥ = {result.transverse_velocity_km_s:.1f} km/s",
            xy=(result.sweep_rate_rad_s, result.transverse_velocity_km_s),
            xytext=(result.sweep_rate_rad_s * 0.45, result.transverse_velocity_km_s * 0.35),
            fontsize=9,
            ha="left",
            arrowprops=dict(arrowstyle="->", color=style["color"], lw=0.6),
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-11, 1e-8)
    ax.set_ylim(0.1, 1e5)
    ax.set_xlabel(r"Implied sweep rate $\Omega_\mathrm{active}$ (rad/s)", fontsize=11)
    ax.set_ylabel(r"Implied transverse velocity $v_{\perp}$ (km/s)", fontsize=11)
    ax.set_title("Active-tracking family of consistencies parameterized by $R_\\mathrm{focal}$", fontsize=11)
    ax.grid(True, which="both", linestyle=":", linewidth=0.4, alpha=0.6)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.92, ncol=1)

    fig.tight_layout()
    # The "no band" version (contours alone) was chosen as the published variant;
    # the alternative is kept available for experimentation by passing
    # with_plausible_band=True from a caller.
    suffix = "_with_band" if with_plausible_band else ""
    fig.savefig(FIGURE_DIR / f"{FIGURE2_BASENAME}{suffix}.pdf")
    fig.savefig(FIGURE_DIR / f"{FIGURE2_BASENAME}{suffix}.png", dpi=200)
    plt.close(fig)

    # Sanity check.
    print(f"--- Figure 2 sanity check (with_plausible_band={with_plausible_band}) ---")
    for name in ["FRB 20180916B", "FRB 20121102A"]:
        rec = anchors[name]
        result = active_tracking_result(
            dfdt_mhz_ms=rec["dfdt_mhz_ms"],
            frequency_mhz=rec["frequency_mhz"],
            aperture_m=SOLAR_DIAMETER_M,
            focal_distance_au=FIDUCIAL_R_FOCAL_AU,
        )
        print(
            f"  {name}: Omega = {result.sweep_rate_rad_s:.3e} rad/s,"
            f" v_perp at 550 AU = {result.transverse_velocity_km_s:.2f} km/s"
        )


# ----- Driver ------------------------------------------------------------------

def main() -> None:
    anchors = get_anchor_records()
    print("Anchor source values (from frb/data.py):")
    for name, rec in anchors.items():
        print(
            f"  {name}: P = {rec['period_days']} d, "
            f"df/dt = {rec['dfdt_mhz_ms']} MHz/ms, "
            f"f = {rec['frequency_mhz']} MHz"
        )

    anchor_short = anchors["FRB 20180916B"]
    anchor_long = anchors["FRB 20121102A"]
    print("\nCross-source observed ratio:", round(observed_ratio(anchor_short, anchor_long), 3))
    for alpha in [1.6, 1.8, ALPHA_CENTRAL, 2.2, 2.4]:
        pr = predicted_ratio(alpha, anchor_short, anchor_long)
        df = discrepancy_factor(alpha, anchor_short, anchor_long)
        print(f"  alpha = {alpha}: predicted_ratio = {pr:.4f}, discrepancy = {df:.2f}x")

    print()
    generate_figure_1(anchors)
    print()
    generate_figure_2(anchors, with_plausible_band=False)
    print(f"\nFigures written to {FIGURE_DIR}.")


if __name__ == "__main__":
    main()
