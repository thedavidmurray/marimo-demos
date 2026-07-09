# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy==2.4.6",
#     "matplotlib==3.11.0",
# ]
# ///

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full", app_title="Hermes Signal Infographic")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Hermes Signal Infographic

    A simpler, poster-style companion to the animated demo.

    The slider acts like a phase dial for the Hermes control plane: each position shifts the signal
    orbit, dispatch lanes, and threshold bands into a new snapshot.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    phase_slider = mo.ui.slider(
        start=0.0,
        stop=1.0,
        step=0.001,
        value=0.28,
        label="Signal phase",
        full_width=True,
    )
    phase_slider
    return (phase_slider,)


@app.cell(hide_code=True)
def _(phase_slider):
    phase_value = phase_slider.value
    return (phase_value,)


@app.cell(hide_code=True)
def _(np, phase_value):
    n = 280
    theta = np.linspace(0, 2 * np.pi, n)
    core_radius = 1.0 + 0.16 * np.sin(4 * theta + phase_value * 2 * np.pi)
    core_radius += 0.05 * np.sin(11 * theta - phase_value * 5)
    orbit_x = core_radius * np.cos(theta)
    orbit_y = core_radius * np.sin(theta)

    dispatch_angles = np.linspace(0, 2 * np.pi, 7, endpoint=False) + phase_value * 2 * np.pi
    dispatch_radius = 1.28 + 0.08 * np.sin(dispatch_angles * 3 - phase_value * 4)
    dispatch_x = dispatch_radius * np.cos(dispatch_angles)
    dispatch_y = dispatch_radius * np.sin(dispatch_angles)

    trace_theta = np.linspace(phase_value * 2 * np.pi - 1.9, phase_value * 2 * np.pi, 110)
    trace_radius = 1.36 + 0.14 * np.sin(trace_theta * 2.2)
    trace_x = trace_radius * np.cos(trace_theta)
    trace_y = trace_radius * np.sin(trace_theta)

    band_x = np.linspace(0, 1, 240)
    dispatch_band = 0.50 + 0.24 * np.sin(2 * np.pi * (band_x + phase_value))
    moa_band = 0.13 * np.sin(2 * np.pi * (band_x * 2 - phase_value * 1.3))
    judge_band = 0.65 + 0.17 * np.cos(2 * np.pi * (band_x * 0.5 - phase_value * 0.6))
    return (
        band_x,
        dispatch_band,
        dispatch_x,
        dispatch_y,
        judge_band,
        moa_band,
        orbit_x,
        orbit_y,
        trace_x,
        trace_y,
    )


@app.cell(hide_code=True)
def _(
    band_x,
    dispatch_band,
    dispatch_x,
    dispatch_y,
    judge_band,
    moa_band,
    orbit_x,
    orbit_y,
    phase_value,
    plt,
    trace_x,
    trace_y,
):
    theme = {
        "bg": "#070b14",
        "panel": "#0b1220",
        "ink": "#f4ecdc",
        "muted": "#a9b2c5",
        "amber": "#ffb74d",
        "cyan": "#67d9ff",
        "violet": "#8f9aff",
        "green": "#7ff1b5",
        "line": "#253149",
    }

    fig = plt.figure(figsize=(14, 9), facecolor=theme["bg"])
    gs = fig.add_gridspec(2, 3, width_ratios=[1.35, 1.0, 0.85], height_ratios=[1.0, 0.8])

    ax_orbit = fig.add_subplot(gs[:, 0])
    ax_wave = fig.add_subplot(gs[0, 1:])
    ax_cards = fig.add_subplot(gs[1, 1:])

    for ax in (ax_orbit, ax_wave, ax_cards):
        ax.set_facecolor(theme["bg"])

    ax_orbit.set_aspect("equal")
    ax_orbit.axis("off")
    ax_orbit.set_xlim(-1.9, 1.9)
    ax_orbit.set_ylim(-1.9, 1.9)

    ax_orbit.add_patch(plt.Circle((0, 0), 1.48, fill=False, color=theme["cyan"], alpha=0.18, linewidth=2.0))
    ax_orbit.add_patch(plt.Circle((0, 0), 1.0, fill=False, color=theme["amber"], alpha=0.18, linewidth=1.8))
    ax_orbit.plot(trace_x, trace_y, color=theme["violet"], alpha=0.30, linewidth=2.3)
    ax_orbit.plot(orbit_x, orbit_y, color=theme["amber"], linewidth=2.8)
    ax_orbit.fill(orbit_x, orbit_y, color=theme["amber"], alpha=0.08)

    ax_orbit.scatter([0], [0], s=900, color=theme["amber"], alpha=0.08)
    ax_orbit.scatter([0], [0], s=280, color=theme["amber"], edgecolors=theme["ink"], linewidths=1.2)
    ax_orbit.text(0, 0.02, "HERMES", color=theme["bg"], fontsize=15, fontweight="bold", ha="center", va="center")
    ax_orbit.text(0, -0.22, "control plane", color=theme["bg"], fontsize=8, ha="center", va="center")

    ax_orbit.scatter(
        dispatch_x,
        dispatch_y,
        s=120,
        color=theme["cyan"],
        alpha=0.92,
        edgecolors=theme["ink"],
        linewidths=0.7,
    )
    for idx, (agent_x, agent_y) in enumerate(zip(dispatch_x, dispatch_y), start=1):
        ax_orbit.plot([0, agent_x], [0, agent_y], color=theme["line"], alpha=0.36, linewidth=1.0)
        ax_orbit.text(agent_x, agent_y + 0.11, f"A{idx}", color=theme["ink"], fontsize=7.5, ha="center")

    ax_orbit.text(-1.74, 1.56, "Dispatch lanes", color=theme["muted"], fontsize=9, ha="left")

    ax_wave.plot(band_x, dispatch_band, color=theme["amber"], linewidth=2.2, label="dispatch")
    ax_wave.plot(band_x, moa_band, color=theme["cyan"], linewidth=1.8, label="moa stream")
    ax_wave.plot(band_x, judge_band, color=theme["violet"], linewidth=1.7, label="judgment")
    ax_wave.axhline(0, color=theme["line"], linewidth=1)
    ax_wave.axvline(phase_value, color=theme["amber"], linewidth=2.0, alpha=0.9)
    ax_wave.set_xlim(0, 1)
    ax_wave.set_ylim(-0.2, 1.05)
    ax_wave.set_xticks([])
    ax_wave.set_yticks([])
    for spine in ax_wave.spines.values():
        spine.set_color(theme["line"])
    ax_wave.set_title("Streaming MoA snapshot", color=theme["ink"], loc="left", fontsize=12, pad=10)
    ax_wave.legend(frameon=False, labelcolor=theme["muted"], loc="upper right")

    ax_cards.axis("off")
    ax_cards.set_facecolor(theme["panel"])
    ax_cards.text(0.03, 0.94, "Hermes v0.18", color=theme["ink"], fontsize=14, fontweight="bold", va="top")
    ax_cards.text(0.03, 0.86, "A compact snapshot of the operating surface.", color=theme["muted"], fontsize=9, va="top")

    cards = [
        ("dispatch", f"{len(dispatch_x)} active agents"),
        ("streaming", "layered MoA wave"),
        ("observability", "trail + ring capture"),
        ("judgment", "phase-aligned threshold"),
    ]
    y = 0.70
    for label, value in cards:
        ax_cards.add_patch(plt.Rectangle((0.03, y - 0.06), 0.94, 0.10, fill=False, edgecolor=theme["line"], linewidth=1.0))
        ax_cards.text(0.06, y, label, color=theme["cyan"], fontsize=9.5, fontweight="bold", va="center")
        ax_cards.text(0.38, y, value, color=theme["ink"], fontsize=9.5, va="center")
        y -= 0.13

    ax_cards.text(
        0.03,
        0.16,
        f"phase = {phase_value:.3f}",
        color=theme["amber"],
        fontsize=11,
        fontweight="bold",
        va="center",
    )
    ax_cards.text(0.03, 0.08, "Move the slider to shift the whole composition.", color=theme["muted"], fontsize=8.5, va="center")

    plt.tight_layout(pad=1.0)
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Reading the poster

    - The left panel is the control hub.
    - The top-right panel shows the streaming signal layers.
    - The lower-right panel condenses the feature set into an infographic.

    This version is meant to be easier to scan and more suitable for sharing as a static export.
    """)
    return


if __name__ == "__main__":
    app.run()
