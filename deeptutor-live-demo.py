# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full", app_title="DeepTutor Live Demo")


@app.cell(hide_code=True)
def _():
    import json
    import os
    import textwrap
    import urllib.error
    import urllib.request

    import marimo as mo
    import numpy as np

    return json, mo, np, os, urllib


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # DeepTutor Live Demo

    A polished tutoring cockpit for mastery tracking, personalized question generation, and multi-channel delivery.

    This notebook is designed to sit behind the Edgelesslab.com demo surface and can switch to a live DeepTutor backend
    when the service endpoint is configured. Without that backend, it runs a deterministic demo model so the notebook stays usable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    # Edgeless design tokens
    teal = "#12b5a4"
    coral = "#ff6b6b"
    cyan = "#72d8ff"
    violet = "#9a9dff"
    amber = "#f7b955"
    amber_soft = "#ffd48a"
    green = "#7ce6bf"
    pink = "#ff8fb3"
    ink = "#f4ecde"
    muted = "#a8b2c5"
    bg = "#060a12"
    panel = "#0c1220"
    panel_soft = "#11192b"
    line = "#253147"
    mono = "'JetBrains Mono', 'SF Mono', 'Fira Code', 'Cascadia Code', monospace"

    theme = dict(
        teal=teal, coral=coral, cyan=cyan, violet=violet,
        amber=amber, amber_soft=amber_soft, green=green, pink=pink,
        ink=ink, muted=muted, bg=bg, panel=panel,
        panel_soft=panel_soft, line=line, mono=mono,
    )

    mo.md(
        f"""
        <div style="
          padding: 0.9rem 1rem;
          border: 1px solid {line};
          border-radius: 8px;
          background: {panel};
          color: {ink};
          font-family: {mono};
        ">
          <div style="font-size:0.72rem; letter-spacing:0.16em; text-transform:uppercase; color:{amber};">
            mastery trajectory + question generation + delivery
          </div>
          <div style="margin-top:0.4rem; display:grid; gap:0.25rem; color:{muted}; line-height:1.4; font-size:0.85rem;">
            <div><strong style="color:{ink};">Mastery trajectory:</strong> visualize growth across skills and time.</div>
            <div><strong style="color:{ink};">Personalized QG:</strong> generate targeted prompts from the weakest skill.</div>
            <div><strong style="color:{ink};">Multi-channel delivery:</strong> preview the same tutor packet for email, SMS, Discord, and dashboard.</div>
          </div>
        </div>
        """
    )
    return (theme,)


@app.cell(hide_code=True)
def _(mo):
    learner = mo.ui.dropdown(
        options=["Avery", "Jordan", "Mina", "Sam"],
        value="Avery",
        label="Learner",
        full_width=True,
    )
    subject = mo.ui.dropdown(
        options=["Algebra", "Biology", "Writing", "World History"],
        value="Algebra",
        label="Subject",
        full_width=True,
    )
    depth = mo.ui.slider(
        start=1,
        stop=5,
        step=1,
        value=3,
        label="Question depth",
        full_width=True,
    )
    week = mo.ui.slider(
        start=1,
        stop=12,
        step=1,
        value=6,
        label="Session week",
        full_width=True,
    )
    n_questions = mo.ui.slider(
        start=1,
        stop=5,
        step=1,
        value=3,
        label="Questions to generate",
        full_width=True,
    )
    email = mo.ui.checkbox(label="Email", value=True)
    sms = mo.ui.checkbox(label="SMS", value=True)
    discord = mo.ui.checkbox(label="Discord", value=True)
    dashboard = mo.ui.checkbox(label="Dashboard", value=True)
    mo.hstack([
        mo.vstack([learner, subject, depth], gap=1),
        mo.vstack([week, n_questions], gap=1),
        mo.vstack([email, sms, discord, dashboard], gap=0.6),
    ], gap=1)
    return (
        dashboard,
        depth,
        discord,
        email,
        learner,
        n_questions,
        sms,
        subject,
        week,
    )


@app.cell(hide_code=True)
def _(dashboard, discord, email, sms):
    profiles = {
        "Avery": {
            "tone": "irreverent, curiosity-first, and jargon-averse",
            "pace": 0.59,
            "goal": 'Richard Feynman | theoretical physics & science education | "What I cannot create, I do not understand."',
            "strengths": ["first-principles reasoning", "experimental verification"],
        },
        "Jordan": {
            "tone": "direct, decisive, and anti-bureaucratic",
            "pace": 0.63,
            "goal": 'Grace Hopper | computer science & programming | "It is better to beg forgiveness, than ask permission."',
            "strengths": ["compiler thinking", "plain-language communication"],
        },
        "Mina": {
            "tone": "austere, methodical, and evidence-led",
            "pace": 0.5,
            "goal": 'Marie Curie | radioactivity, chemistry, and medical physics | "I was taught that the way of progress was neither swift nor easy."',
            "strengths": ["experimental discipline", "methodical analysis"],
        },
        "Sam": {
            "tone": "humble, reflective, and growth-oriented",
            "pace": 0.54,
            "goal": 'Dirk Nowitzki | basketball & leadership | "Make mistakes and make bad decisions: you learn from them."',
            "strengths": ["growth mindset", "mental toughness"],
        },
    }

    subject_skills = {
        "Algebra": ["first-principles decomposition", "stepwise verification", "symbolic precision", "error checking"],
        "Biology": ["careful observation", "systems mapping", "hypothesis testing", "evidence tracking"],
        "Writing": ["clear explanation", "structured argument", "revision", "vivid analogy"],
        "World History": ["context", "causality", "comparison", "narrative synthesis"],
    }

    channel_flags = {
        "email": email.value,
        "sms": sms.value,
        "discord": discord.value,
        "dashboard": dashboard.value,
    }
    return channel_flags, profiles, subject_skills


@app.cell(hide_code=True)
def _(
    channel_flags,
    depth,
    learner,
    n_questions,
    np,
    profiles,
    subject,
    subject_skills,
    week,
):
    _profile = profiles[learner.value]
    _skills = subject_skills[subject.value]
    _weeks = np.arange(1, 13)
    skill_curves = {}
    _base_offsets = np.linspace(0.18, 0.42, len(_skills))
    _growth_rates = np.linspace(0.10, 0.22, len(_skills))

    for _idx, _skill in enumerate(_skills):
        _base = _base_offsets[_idx]
        _growth = _growth_rates[_idx] + (depth.value - 3) * 0.012
        _momentum = _profile["pace"] * 0.10
        _curve = _base + _growth * (1.0 - np.exp(-(_weeks / (2.2 + _idx * 0.5))))
        _curve += _momentum * np.sin((_weeks / 2.5) + _idx * 0.8)
        _curve = np.clip(_curve, 0.05, 0.98)
        skill_curves[_skill] = _curve

    current_index = week.value - 1
    current_snapshot = {skill: curve[current_index] for skill, curve in skill_curves.items()}
    sorted_skills = sorted(current_snapshot.items(), key=lambda item: item[1])
    weakest_skill, weakest_score = sorted_skills[0]
    strongest_skill, strongest_score = sorted_skills[-1]
    skills = _skills

    payload = {
        "learner": learner.value,
        "subject": subject.value,
        "tone": _profile["tone"],
        "goal": _profile["goal"],
        "strengths": _profile["strengths"],
        "weakest_skill": weakest_skill,
        "weakest_score": float(weakest_score),
        "strongest_skill": strongest_skill,
        "strongest_score": float(strongest_score),
        "week": week.value,
        "question_depth": depth.value,
        "questions": n_questions.value,
        "channels": [name for name, enabled in channel_flags.items() if enabled],
    }
    return payload, skill_curves, skills


@app.cell(hide_code=True)
def _(json, os, urllib):
    def _build_demo_response(request_payload):
        weak_skill = request_payload["weakest_skill"]
        strong_skill = request_payload["strongest_skill"]
        depth = request_payload["question_depth"]
        questions = []
        for idx in range(request_payload["questions"]):
            prompt = {
                1: f"Which part of {request_payload['subject']} is most important when {weak_skill} first appears?",
                2: f"Explain how a student could use {strong_skill} to support a weaker {weak_skill} answer.",
                3: f"Design a comparison question that makes the learner transfer {weak_skill} to a new scenario.",
                4: f"Ask a why/how question that forces the learner to justify the step that fixes {weak_skill}.",
                5: f"Create a multi-step challenge that combines {weak_skill} with a novel constraint.",
            }[depth]
            questions.append(f"{idx + 1}. {prompt}")

        channel_messages = {}
        for channel in request_payload["channels"]:
            if channel == "email":
                channel_messages[channel] = (
                    f"Subject: DeepTutor update for {request_payload['learner']}\n\n"
                    f"Mastery focus: {weak_skill} ({request_payload['weakest_score']:.0%}).\n"
                    f"Next questions:\n- " + "\n- ".join(questions)
                )
            elif channel == "sms":
                channel_messages[channel] = (
                    f"DeepTutor: {request_payload['learner']} needs {weak_skill} support. "
                    f"Ask: {questions[0]}".strip()
                )
            elif channel == "discord":
                channel_messages[channel] = (
                    f"**DeepTutor** | {request_payload['learner']} | {request_payload['subject']}\n"
                    f"Focus: {weak_skill} at {request_payload['weakest_score']:.0%}\n"
                    + "\n".join(f"- {q}" for q in questions)
                )
            elif channel == "dashboard":
                channel_messages[channel] = (
                    f"Dashboard card: {request_payload['learner']} trending up in {request_payload['subject']}, "
                    f"but {weak_skill} is still the next intervention."
                )
        return {
            "backend_mode": "demo",
            "summary": f"DeepTutor demo packet for {request_payload['learner']}",
            "questions": questions,
            "delivery": channel_messages,
            "trace": "Local deterministic tutor model",
        }

    def call_backend(request_payload):
        base_url = os.environ.get("DEEPTUTOR_API_URL", "").strip()
        if not base_url:
            return _build_demo_response(request_payload)

        api_key = os.environ.get("DEEPTUTOR_API_KEY", "").strip()
        body = json.dumps(request_payload).encode("utf-8")
        req = urllib.request.Request(
            base_url.rstrip("/"),
            data=body,
            headers={
                "Content-Type": "application/json",
                **({"Authorization": f"Bearer {api_key}"} if api_key else {}),
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            data.setdefault("backend_mode", "live")
            data.setdefault("trace", "Live DeepTutor backend")
            return data
        except Exception as exc:
            fallback = _build_demo_response(request_payload)
            fallback["backend_mode"] = "demo-fallback"
            fallback["trace"] = f"Backend unavailable: {exc.__class__.__name__}"
            return fallback

    return (call_backend,)


@app.cell(hide_code=True)
def _(call_backend, payload):
    tutor_packet = call_backend(payload)
    return (tutor_packet,)


@app.cell(hide_code=True)
def _(mo, payload, theme, tutor_packet):
    mastery_badge = f"{int(round(payload['weakest_score'] * 100))}%"
    strongest_badge = f"{int(round(payload['strongest_score'] * 100))}%"

    mo.hstack(
        [
            mo.md(
                f"""
                <div style="padding:0.75rem 0.9rem;border-radius:8px;background:{theme['panel']};border:1px solid {theme['line']};font-family:{theme['mono']};">
                  <div style="color:{theme['muted']};font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;">Mode</div>
                  <div style="margin-top:0.25rem;font-size:1rem;font-weight:700;color:{theme['ink']}">{tutor_packet.get('backend_mode', 'demo')}</div>
                  <div style="color:{theme['cyan']};margin-top:0.05rem;font-size:0.78rem;">{tutor_packet.get('trace', 'Deterministic tutor model')}</div>
                </div>
                """
            ),
            mo.md(
                f"""
                <div style="padding:0.75rem 0.9rem;border-radius:8px;background:{theme['panel']};border:1px solid {theme['line']};font-family:{theme['mono']};">
                  <div style="color:{theme['muted']};font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;">Weakest skill</div>
                  <div style="margin-top:0.25rem;font-size:1rem;font-weight:700;color:{theme['ink']}">{payload['weakest_skill']}</div>
                  <div style="color:{theme['amber']};margin-top:0.05rem;font-size:0.78rem;">{mastery_badge} mastery</div>
                </div>
                """
            ),
            mo.md(
                f"""
                <div style="padding:0.75rem 0.9rem;border-radius:8px;background:{theme['panel']};border:1px solid {theme['line']};font-family:{theme['mono']};">
                  <div style="color:{theme['muted']};font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;">Strongest skill</div>
                  <div style="margin-top:0.25rem;font-size:1rem;font-weight:700;color:{theme['ink']}">{payload['strongest_skill']}</div>
                  <div style="color:{theme['green']};margin-top:0.05rem;font-size:0.78rem;">{strongest_badge} mastery</div>
                </div>
                """
            ),
            mo.md(
                f"""
                <div style="padding:0.75rem 0.9rem;border-radius:8px;background:{theme['panel']};border:1px solid {theme['line']};font-family:{theme['mono']};">
                  <div style="color:{theme['muted']};font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;">Channels</div>
                  <div style="margin-top:0.25rem;font-size:1rem;font-weight:700;color:{theme['ink']}">{len(payload['channels'])} selected</div>
                  <div style="color:{theme['violet']};margin-top:0.05rem;font-size:0.78rem;">{', '.join(payload['channels']) if payload['channels'] else 'none'}</div>
                </div>
                """
            ),
        ],
        gap=0.7,
    )
    return


@app.cell(hide_code=True)
def _(mo, payload, skill_curves, skills, theme):
    week_index = payload["week"] - 1
    current_values = [skill_curves[skill][week_index] for skill in skills]
    palette = [theme["amber"], theme["cyan"], theme["violet"], theme["green"]]

    chart_width = 980
    chart_height = 340
    pad_x = 34
    pad_y = 24

    def _points(curve):
        span_x = chart_width - 2 * pad_x
        span_y = chart_height - 2 * pad_y
        return " ".join(
            f"{pad_x + (i / (len(curve) - 1)) * span_x:.1f},{chart_height - pad_y - value * span_y:.1f}"
            for i, value in enumerate(curve)
        )

    grid = "".join(
        f'<line x1="{pad_x}" y1="{y}" x2="{chart_width - pad_x}" y2="{y}" stroke="{theme["line"]}" stroke-width="1" opacity="0.8" />'
        for y in [48, 98, 148, 198, 248, 298]
    )
    trajectories = []
    for idx, skill in enumerate(skills):
        curve = skill_curves[skill]
        cursor_x = pad_x + ((payload["week"] - 1) / 11) * (chart_width - 2 * pad_x)
        cursor_y = chart_height - pad_y - curve[week_index] * (chart_height - 2 * pad_y)
        trajectories.append(
            f'<polyline fill="none" stroke="{palette[idx]}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" points="{_points(curve)}" />'
        )
        trajectories.append(
            f'<circle cx="{cursor_x:.1f}" cy="{cursor_y:.1f}" r="6.5" fill="{palette[idx]}" />'
        )

    bars = []
    for idx, (skill, value) in enumerate(zip(skills, current_values)):
        y = 18 + idx * 72
        bar_width = 330 * value
        bars.append(
            f"""
            <g transform="translate(0,{y})">
              <text x="0" y="16" fill="{theme['ink']}" font-size="13" font-weight="600">{skill}</text>
              <rect x="0" y="24" width="330" height="16" rx="8" fill="{theme['line']}" />
              <rect x="0" y="24" width="{bar_width:.1f}" height="16" rx="8" fill="{palette[idx]}" />
              <text x="{bar_width + 10:.1f}" y="36" fill="{theme['ink']}" font-size="12">{int(round(value * 100))}%</text>
            </g>
            """
        )

    mo.md(
        f"""
        <div style="display:grid;grid-template-columns:1.45fr 1fr;gap:1rem;align-items:start;">
          <div style="padding:1rem 1rem 0.85rem;border-radius:20px;background:{theme['panel']};border:1px solid {theme['line']};">
            <div style="display:flex;justify-content:space-between;gap:1rem;align-items:baseline;margin-bottom:0.8rem;">
              <div>
                <div style="color:{theme['muted']};font-size:0.76rem;text-transform:uppercase;letter-spacing:0.12em;">Mastery trajectory</div>
                <div style="color:{theme['ink']};font-size:1.15rem;font-weight:700;margin-top:0.18rem;">Week {payload['week']} progress for {payload['learner']}</div>
              </div>
              <div style="color:{theme['amber_soft']};font-size:0.86rem;">Focus: {payload['weakest_skill']}</div>
            </div>
            <svg viewBox="0 0 {chart_width} {chart_height}" width="100%" role="img" aria-label="Mastery trajectory chart" style="display:block;">
              <rect x="0" y="0" width="{chart_width}" height="{chart_height}" rx="18" fill="{theme['bg']}" opacity="0.4" />
              {grid}
              <line x1="{pad_x}" y1="300" x2="{chart_width - pad_x}" y2="300" stroke="{theme['line']}" stroke-width="1.2" />
              <line x1="{pad_x}" y1="30" x2="{pad_x}" y2="300" stroke="{theme['line']}" stroke-width="1.2" />
              {''.join(trajectories)}
              <line x1="{pad_x + ((payload['week'] - 1) / 11) * (chart_width - 2 * pad_x):.1f}" y1="30" x2="{pad_x + ((payload['week'] - 1) / 11) * (chart_width - 2 * pad_x):.1f}" y2="300" stroke="{theme['amber_soft']}" stroke-width="2.2" stroke-dasharray="7 6" />
              <text x="{pad_x}" y="330" fill="{theme['muted']}" font-size="12">Week 1</text>
              <text x="{chart_width - pad_x - 34}" y="330" fill="{theme['muted']}" font-size="12">Week 12</text>
            </svg>
          </div>
          <div style="padding:1rem 1rem 0.9rem;border-radius:20px;background:{theme['panel']};border:1px solid {theme['line']};">
            <div style="color:{theme['muted']};font-size:0.76rem;text-transform:uppercase;letter-spacing:0.12em;">Current snapshot</div>
            <div style="margin-top:0.25rem;color:{theme['ink']};font-size:1.1rem;font-weight:700;">Skill-by-skill intervention map</div>
            <div style="display:grid;gap:0.45rem;margin-top:1rem;">{''.join(bars)}</div>
          </div>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, payload, theme, tutor_packet):
    questions = tutor_packet.get("questions", [])
    if not questions:
        questions = ["No questions generated."]

    question_cards = []
    for question_idx, question in enumerate(questions[: payload["questions"]]):
        question_cards.append(
            mo.md(
                f"""
                <div style="padding:0.75rem 0.9rem;border-radius:8px;background:{theme['panel']};border:1px solid {theme['line']};margin-bottom:0.6rem;font-family:{theme['mono']};">
                  <div style="color:{theme['amber']};font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;">Question {question_idx + 1}</div>
                  <div style="margin-top:0.3rem;color:{theme['ink']};line-height:1.5;font-size:0.88rem;">{question}</div>
                </div>
                """
            )
        )

    mo.vstack(question_cards, gap=0.15)
    return


@app.cell(hide_code=True)
def _(mo, theme, tutor_packet):
    delivery = tutor_packet.get("delivery", {})

    def _channel_tab(channel_name, headline, tone):
        message = delivery.get(channel_name, "Channel not selected.")
        return mo.md(
            f"""
            <div style="padding:0.8rem 0.9rem;border-radius:8px;border:1px solid {theme['line']};background:{theme['panel']};font-family:{theme['mono']};">
              <div style="display:flex;justify-content:space-between;gap:1rem;align-items:baseline;">
                <div style="color:{theme['cyan']};font-weight:700;font-size:0.88rem;">{headline}</div>
                <div style="color:{theme['muted']};font-size:0.72rem;">{tone}</div>
              </div>
              <pre style="white-space:pre-wrap;word-break:break-word;margin-top:0.6rem;color:{theme['ink']};font-size:0.85rem;line-height:1.5;font-family:{theme['mono']};">{message}</pre>
            </div>
            """
        )

    tabs = {
        "Email": _channel_tab("email", "Email delivery", "long-form"),
        "SMS": _channel_tab("sms", "SMS delivery", "short-form"),
        "Discord": _channel_tab("discord", "Discord delivery", "community"),
        "Dashboard": _channel_tab("dashboard", "Tutor dashboard", "operator view"),
    }
    mo.ui.tabs(tabs)
    return


@app.cell(hide_code=True)
def _(mo, payload, tutor_packet):
    mo.md(
        f"""
        ## Delivery contract

        - Learner: **{payload['learner']}**
        - Subject: **{payload['subject']}**
        - Focus skill: **{payload['weakest_skill']}**
        - Goal: {payload['goal']}
        - Backend mode: **{tutor_packet.get('backend_mode', 'demo')}**

        The backend hook lives in the notebook and will POST the current payload to `DEEPTUTOR_API_URL` when configured.
        In this demo build, the notebook falls back to deterministic generation so the experience remains stable on Edgelesslab.com.
        """
    )
    return


if __name__ == "__main__":
    app.run()
