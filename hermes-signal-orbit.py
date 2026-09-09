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
app = marimo.App(width="full", app_title="Hermes Signal Orbit")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Hermes Signal Orbit

    A reactive Marimo demo with an auto-animated slider that drives a glowing control-plane visualization.

    The slider below cycles a signal phase through a stylized Hermes v0.18 scene:
    dispatch lanes, streaming MoA traces, judgment thresholds, and observability rings.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    theme = {
        "bg": "#070b14",
        "panel": "#0c1220",
        "panel_soft": "#11192b",
        "ink": "#f3ead9",
        "muted": "#a7b1c2",
        "amber": "#ffb74d",
        "amber_soft": "#ffcc80",
        "cyan": "#67d9ff",
        "violet": "#8d9bff",
        "green": "#7ff1b5",
        "red": "#ff7f8f",
        "line": "#243147",
    }

    mo.md(
        f"""
        <div style="
            padding: 1rem 1.1rem;
            border: 1px solid {theme['line']};
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(255,183,77,0.10), rgba(103,217,255,0.06) 40%, rgba(141,155,255,0.05));
            color: {theme['ink']};
        ">
          <div style="font-size:0.85rem; letter-spacing:0.14em; text-transform:uppercase; color:{theme['amber_soft']};">
            v0.18 feature map
          </div>
          <div style="margin-top:0.45rem; display:grid; gap:0.45rem;">
            <div><strong>Dispatch:</strong> orbiting agents route around the hub</div>
            <div><strong>Streaming MoA:</strong> layered signal bands animate in phase</div>
            <div><strong>Judgment:</strong> the center ring lights up on each sweep</div>
            <div><strong>Observability:</strong> the trail captures recent state changes</div>
          </div>
        </div>
        """
    )
    return theme


@app.cell(hide_code=True)
def _(mo):
    playback = mo.state({"running": True, "phase": 0.0, "speed": 0.025, "direction": 1})
    return playback


@app.cell(hide_code=True)
def _(mo):
    timer = mo.ui.refresh(options=["120ms", "250ms", "500ms"], default_interval="120ms")
    return timer


@app.cell(hide_code=True)
def _(playback, timer):
    _tick = timer.value
    _playback_state = playback.value
    if _playback_state["running"]:
        _next_phase = (
            _playback_state["phase"]
            + _playback_state["speed"] * _playback_state["direction"]
        )
        if _next_phase >= 1.0:
            _next_phase = 1.0
            playback.value = {
                **_playback_state,
                "phase": _next_phase,
                "direction": -1,
            }
        elif _next_phase <= 0.0:
            _next_phase = 0.0
            playback.value = {
                **_playback_state,
                "phase": _next_phase,
                "direction": 1,
            }
        else:
            playback.value = {**_playback_state, "phase": _next_phase}
    return


@app.cell(hide_code=True)
def _(mo, playback):
    _playback_state = playback.value
    play_pause_button = mo.ui.run_button(
        label="⏸ Pause" if _playback_state["running"] else "▶ Play"
    )
    speed_slider = mo.ui.slider(
        start=0.01,
        stop=0.08,
        step=0.005,
        value=_playback_state["speed"],
        label="Phase speed",
    )
    phase_slider = mo.ui.slider(
        start=0.0,
        stop=1.0,
        step=0.001,
        value=_playback_state["phase"],
        label="Signal phase",
    )

    layout = mo.hstack(
        [
            play_pause_button,
            mo.md(f"**Speed**\n\n{speed_slider}"),
            mo.md(f"**Phase**\n\n{phase_slider}"),
        ],
        gap=1,
    )
    layout
    return phase_slider, play_pause_button, speed_slider


@app.cell(hide_code=True)
def _(phase_slider, play_pause_button, playback, speed_slider):
    _playback_state = playback.value
    if play_pause_button.value:
        playback.value = {
            **_playback_state,
            "running": not _playback_state["running"],
        }
        _playback_state = playback.value

    if abs(speed_slider.value - _playback_state["speed"]) > 1e-9:
        playback.value = {**_playback_state, "speed": speed_slider.value}
        _playback_state = playback.value

    if abs(phase_slider.value - _playback_state["phase"]) > 0.001:
        playback.value = {
            **_playback_state,
            "phase": phase_slider.value,
            "running": False,
        }
    return


@app.cell(hide_code=True)
def _(mo, playback):
    _playback_state = playback.value
    phase_pct = int(round(_playback_state["phase"] * 100))
    direction = "forward" if _playback_state["direction"] > 0 else "reverse"

    mo.hstack(
        [
            mo.md(
                f"""
                <div style="padding:0.9rem 1rem; border-radius:14px; background:#0c1220; border:1px solid #243147;">
                  <div style="color:#a7b1c2; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.12em;">Playback</div>
                  <div style="font-size:1.8rem; font-weight:700; color:#f3ead9; margin-top:0.25rem;">{phase_pct}%</div>
                  <div style="color:#67d9ff; margin-top:0.15rem;">{direction} sweep</div>
                </div>
                """
            ),
            mo.md(
                """
                <div style="padding:0.9rem 1rem; border-radius:14px; background:#0c1220; border:1px solid #243147;">
                  <div style="color:#a7b1c2; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.12em;">Mood</div>
                  <div style="font-size:1.2rem; font-weight:700; color:#ffb74d; margin-top:0.25rem;">Signal dawn</div>
                  <div style="color:#a7b1c2; margin-top:0.15rem;">amber pulse over navy glass</div>
                </div>
                """
            ),
        ],
        gap=1,
    )
    return


@app.cell(hide_code=True)
def _(np, playback):
    _playback_state = playback.value
    orbit_phase = _playback_state["phase"]

    n = 240
    theta = np.linspace(0, 2 * np.pi, n)
    base_radius = 1.0
    wobble = 0.18 * np.sin(5 * theta + orbit_phase * 2 * np.pi)
    wave = base_radius + wobble + 0.05 * np.sin(13 * theta - orbit_phase * 6)
    orbit_x = wave * np.cos(theta)
    orbit_y = wave * np.sin(theta)

    agent_count = 8
    agent_angles = (
        np.linspace(0, 2 * np.pi, agent_count, endpoint=False)
        + orbit_phase * 2 * np.pi
    )
    agent_radius = 1.25 + 0.12 * np.sin(agent_angles * 2 - orbit_phase * 5)
    agents_x = agent_radius * np.cos(agent_angles)
    agents_y = agent_radius * np.sin(agent_angles)

    trail_len = 90
    trail_theta = np.linspace(
        orbit_phase * 2 * np.pi - 1.7, orbit_phase * 2 * np.pi, trail_len
    )
    trail_radius = 1.35 + 0.18 * np.sin(3.0 * trail_theta)
    trail_x = trail_radius * np.cos(trail_theta)
    trail_y = trail_radius * np.sin(trail_theta)

    layers = {
        "x": orbit_x,
        "y": orbit_y,
        "agents_x": agents_x,
        "agents_y": agents_y,
        "trail_x": trail_x,
        "trail_y": trail_y,
        "phase": orbit_phase,
    }
    return layers


@app.cell(hide_code=True)
def _(layers, np, plt, theme):
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(13.5, 9.2),
        gridspec_kw={"width_ratios": [1.3, 1.0], "height_ratios": [1.0, 0.92]},
    )
    fig.patch.set_facecolor(theme["bg"])

    for ax in axes.flat:
        ax.set_facecolor(theme["bg"])

    ax_main = axes[0, 0]
    ax_signal = axes[0, 1]
    ax_bands = axes[1, 0]
    ax_stats = axes[1, 1]

    ax_main.set_aspect("equal")
    ax_main.set_xlim(-1.9, 1.9)
    ax_main.set_ylim(-1.9, 1.9)
    ax_main.axis("off")

    # Outer observability ring
    ring = plt.Circle((0, 0), 1.45, fill=False, color=theme["cyan"], alpha=0.18, linewidth=2.2)
    ax_main.add_patch(ring)
    ax_main.add_patch(plt.Circle((0, 0), 1.0, fill=False, color=theme["amber"], alpha=0.16, linewidth=1.8))

    # Trail and signal orbit
    ax_main.plot(layers["trail_x"], layers["trail_y"], color=theme["violet"], alpha=0.32, linewidth=2.4)
    ax_main.plot(layers["x"], layers["y"], color=theme["amber"], alpha=0.85, linewidth=2.8)
    ax_main.fill(layers["x"], layers["y"], color=theme["amber"], alpha=0.08)

    # Hub
    ax_main.scatter([0], [0], s=900, color=theme["amber"], alpha=0.08, zorder=5)
    ax_main.scatter([0], [0], s=260, color=theme["amber_soft"], edgecolors=theme["ink"], linewidths=1.4, zorder=6)
    ax_main.text(0, 0.02, "HERMES", color=theme["bg"], fontsize=14, fontweight="bold", ha="center", va="center", zorder=7)
    ax_main.text(0, -0.22, "control plane", color=theme["bg"], fontsize=7.5, ha="center", va="center", zorder=7)

    # Agents
    ax_main.scatter(
        layers["agents_x"],
        layers["agents_y"],
        s=np.linspace(70, 160, len(layers["agents_x"])),
        c=[theme["cyan"]] * len(layers["agents_x"]),
        alpha=0.9,
        edgecolors=theme["ink"],
        linewidths=0.8,
        zorder=8,
    )
    for idx, (agent_x, agent_y) in enumerate(
        zip(layers["agents_x"], layers["agents_y"]), start=1
    ):
        ax_main.text(
            agent_x,
            agent_y + 0.11,
            f"A{idx}",
            color=theme["ink"],
            fontsize=7.5,
            ha="center",
            va="bottom",
            zorder=9,
        )

    # Dispatch lanes from hub to agents
    for lane_x, lane_y in zip(layers["agents_x"], layers["agents_y"]):
        ax_main.plot(
            [0, lane_x],
            [0, lane_y],
            color=theme["line"],
            alpha=0.28,
            linewidth=1.1,
        )

    ax_main.text(-1.82, 1.58, "Dispatch lanes", color=theme["muted"], fontsize=9, ha="left", va="top")

    # Signal bands
    t = np.linspace(0, 1, 420)
    plot_phase = layers["phase"]
    band1 = np.sin(2 * np.pi * (t * 1.0 + plot_phase))
    band2 = 0.55 * np.sin(2 * np.pi * (t * 2.0 - plot_phase * 0.9))
    band3 = 0.28 * np.sin(2 * np.pi * (t * 4.2 + plot_phase * 1.7))

    ax_signal.plot(t, band1, color=theme["amber"], linewidth=2.2, label="dispatch")
    ax_signal.plot(t, band2, color=theme["cyan"], linewidth=1.9, label="moa")
    ax_signal.plot(t, band3, color=theme["violet"], linewidth=1.6, label="telemetry")
    ax_signal.fill_between(t, band1, color=theme["amber"], alpha=0.07)
    ax_signal.axhline(0, color=theme["line"], linewidth=1)
    ax_signal.set_xlim(0, 1)
    ax_signal.set_ylim(-1.15, 1.15)
    ax_signal.set_xticks([])
    ax_signal.set_yticks([])
    for spine in ax_signal.spines.values():
        spine.set_color(theme["line"])
    ax_signal.set_title("Streaming MoA waveform", color=theme["ink"], loc="left", fontsize=12, pad=10)
    ax_signal.legend(frameon=False, labelcolor=theme["muted"], loc="upper right")

    # Judgment bands and progress arc
    ax_bands.set_xlim(0, 1)
    ax_bands.set_ylim(0, 1)
    ax_bands.axis("off")
    band_x = np.linspace(0, 1, 120)
    thresholds = 0.38 + 0.12 * np.sin(2 * np.pi * (band_x * 1.0 + plot_phase))
    confidence = 0.72 + 0.18 * np.cos(2 * np.pi * (band_x * 0.5 - plot_phase * 0.7))
    ax_bands.fill_between(
        band_x, 0.08, 0.08 + thresholds * 0.65, color=theme["violet"], alpha=0.12
    )
    ax_bands.plot(band_x, thresholds * 0.65 + 0.08, color=theme["violet"], linewidth=2.0)
    ax_bands.plot(band_x, confidence * 0.18 + 0.53, color=theme["green"], linewidth=1.8)
    ax_bands.axvline(plot_phase, color=theme["amber"], linewidth=2.2, alpha=0.95)
    ax_bands.text(0.0, 0.98, "Judgment threshold", color=theme["ink"], fontsize=12, va="top")
    ax_bands.text(0.0, 0.88, "phase-aligned scoring and recovery signal", color=theme["muted"], fontsize=9, va="top")
    ax_bands.text(0.02, 0.12, "low", color=theme["muted"], fontsize=8)
    ax_bands.text(0.90, 0.12, "high", color=theme["muted"], fontsize=8)

    # Stats panel
    ax_stats.set_facecolor(theme["panel"])
    ax_stats.axis("off")
    stats_lines = [
        ("feature", "streaming MoA"),
        ("dispatch", f"{len(layers['agents_x'])} active lanes"),
        ("observability", "ring + trail capture"),
        ("judgment", "phase-triggered thresholding"),
        ("scale", "elastic, event-driven"),
    ]
    ax_stats.text(0.03, 0.95, "Hermes v0.18 sketch", color=theme["ink"], fontsize=13, fontweight="bold", va="top")
    ax_stats.text(0.03, 0.88, "A compact visualization of the control surface.", color=theme["muted"], fontsize=9, va="top")

    y = 0.74
    for label, value in stats_lines:
        ax_stats.text(0.05, y, label, color=theme["cyan"], fontsize=9.5, fontweight="bold", va="center")
        ax_stats.text(0.37, y, value, color=theme["ink"], fontsize=9.5, va="center")
        y -= 0.12

    ax_stats.add_patch(plt.Rectangle((0.04, 0.06), 0.92, 0.13, fill=False, edgecolor=theme["line"], linewidth=1.1))
    ax_stats.text(
        0.06,
        0.125,
        f"signal phase = {plot_phase:.3f}",
        color=theme["amber_soft"],
        fontsize=10,
        fontweight="bold",
        va="center",
    )
    ax_stats.text(0.06, 0.08, "The slider drives the entire notebook reactively.", color=theme["muted"], fontsize=8.5, va="center")

    plt.tight_layout(pad=1.1)
    plt
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## How it works

    1. `mo.ui.refresh` advances a phase value on a fixed interval.
    2. `mo.state` stores the current playback position, speed, and direction.
    3. The slider mirrors the state, so manual scrubbing and autoplay stay in sync.
    4. The plot cell recomputes the orbit, signal bands, and stats from that single reactive source.

    The result is a notebook that feels animated without any custom event loop.
    """)
    return


if __name__ == "__main__":
    app.run()
