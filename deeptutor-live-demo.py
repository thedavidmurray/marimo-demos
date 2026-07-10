# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full", app_title="DeepTutor Live Demo")


@app.cell(hide_code=True)
def _():
    import base64
    import io
    import json
    import os
    import textwrap
    import urllib.error
    import urllib.request

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import marimo as mo
    import numpy as np

    return io, json, mo, np, os, plt, urllib


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
    return ink, line, muted, theme


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
def _(ink, json, line, muted, os, urllib):
    import html as html_lib

    _bg = "#060a12"
    _panel = "#0c1220"
    _panel_soft = "#11192b"
    _ink = "#f4ecde"
    _muted = "#a8b2c5"
    _amber = "#f7b955"
    _cyan = "#72d8ff"
    _violet = "#9a9dff"
    _green = "#7ce6bf"
    _line = "#253147"
    _mono = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"

    def _escape(value):
        return html_lib.escape(str(value))

    def _mode_badge(backend_mode):
        return "⚡ LIVE" if backend_mode == "live" else "🧪 DEMO"

    def _question_rows(questions):
        return "".join(
            f"<li style='margin:0 0 0.45rem 1rem;color:{_ink};'>{_escape(question)}</li>"
            for question in questions
        )

    def _render_email_mockup(request_payload, questions, backend_mode, trace):
        subject_line = f"DeepTutor update for {request_payload['learner']}"
        bullet_list = _question_rows(questions)
        return f"""
        <div style="border:1px solid {_line};border-radius:8px;background:{_panel};color:{_ink};font-family:{_mono};overflow:hidden;">
          <div style="padding:0.75rem 0.9rem;border-bottom:1px solid {_line};background:{_panel_soft};display:flex;justify-content:space-between;align-items:center;gap:1rem;">
            <div>
              <div style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:{_muted};">Subject</div>
              <div style="margin-top:0.2rem;font-size:0.95rem;font-weight:700;">{_escape(subject_line)}</div>
            </div>
            <span style="display:inline-flex;align-items:center;padding:0.22rem 0.55rem;border-radius:999px;border:1px solid {_line};background:{_panel_soft};color:{_ink};font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;">{_mode_badge(backend_mode)}</span>
          </div>
          <div style="padding:0.95rem 1rem 1rem;line-height:1.55;font-size:0.88rem;">
            <div style="color:{_muted};font-size:0.72rem;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.65rem;">Email preview</div>
            <p style="margin:0 0 0.75rem 0;">Hi {_escape(request_payload['learner'])},</p>
            <p style="margin:0 0 0.75rem 0;">Your current focus is <strong style="color:{_amber};">{_escape(request_payload['weakest_skill'])}</strong> at {int(round(request_payload['weakest_score'] * 100))}% mastery. The next step is to push on the weakest edge with targeted practice.</p>
            <div style="margin:0.85rem 0 0.55rem 0;color:{_cyan};font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;">Next questions</div>
            <ol style="margin:0;padding-left:1rem;">{bullet_list}</ol>
            <div style="margin-top:0.95rem;padding-top:0.75rem;border-top:1px solid {_line};color:{_muted};font-size:0.75rem;">
              Tone: {_escape(request_payload['tone'])} | Trace: {_escape(trace)}
            </div>
          </div>
        </div>
        """

    def _render_sms_mockup(request_payload, questions, backend_mode, trace):
        sms_body = _escape(f"DeepTutor: {request_payload['learner']} needs {request_payload['weakest_skill']} support. Ask: {questions[0]}")
        return f"""
        <div style="max-width:360px;margin:0 auto;padding:0.9rem;border:1px solid {_line};border-radius:8px;background:{_panel};font-family:{_mono};color:{_ink};">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.65rem;color:{_muted};font-size:0.72rem;">
            <span>Messages</span>
            <span style="display:inline-flex;align-items:center;padding:0.22rem 0.55rem;border-radius:999px;border:1px solid {_line};background:{_panel_soft};color:{_ink};font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;">{_mode_badge(backend_mode)}</span>
          </div>
          <div style="background:{_panel_soft};border:1px solid {_line};border-radius:18px 18px 6px 18px;padding:0.8rem 0.9rem;line-height:1.5;font-size:0.88rem;">
            {sms_body}
          </div>
          <div style="text-align:right;color:{_muted};font-size:0.7rem;margin-top:0.45rem;">Today, 7:42 PM</div>
          <div style="margin-top:0.55rem;color:{_muted};font-size:0.72rem;">Trace: {_escape(trace)}</div>
        </div>
        """

    def _render_discord_mockup(request_payload, questions, backend_mode, trace):
        code_block = "\n".join(f"- {question}" for question in questions)
        return f"""
        <div style="border:1px solid {_line};border-radius:8px;background:{_panel};color:{_ink};font-family:{_mono};overflow:hidden;">
          <div style="padding:0.8rem 0.95rem;border-bottom:1px solid {_line};background:{_panel_soft};display:flex;justify-content:space-between;align-items:center;gap:1rem;">
            <div>
              <div style="font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:{_muted};">Discord embed</div>
              <div style="margin-top:0.2rem;font-size:0.95rem;font-weight:700;">DeepTutor | {_escape(request_payload['subject'])}</div>
            </div>
            <span style="display:inline-flex;align-items:center;padding:0.22rem 0.55rem;border-radius:999px;border:1px solid {_line};background:{_panel_soft};color:{_ink};font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;">{_mode_badge(backend_mode)}</span>
          </div>
          <div style="padding:0.9rem 1rem 1rem;">
            <div style="display:flex;justify-content:space-between;gap:1rem;align-items:baseline;">
              <div style="color:{_cyan};font-weight:700;">@DeepTutor Bot</div>
              <div style="color:{_muted};font-size:0.72rem;">assignment / tutor packet</div>
            </div>
            <div style="margin-top:0.65rem;padding-left:0.85rem;border-left:2px solid {_violet};color:{_ink};line-height:1.5;font-size:0.87rem;">
              Focus skill: <strong>{_escape(request_payload['weakest_skill'])}</strong> at {int(round(request_payload['weakest_score'] * 100))}% mastery
            </div>
            <pre style="margin:0.75rem 0 0 0;padding:0.75rem;border-radius:8px;background:{_bg};border:1px solid {_line};color:{_green};white-space:pre-wrap;word-break:break-word;font-size:0.8rem;line-height:1.45;">{_escape(code_block)}</pre>
            <div style="margin-top:0.75rem;color:{_muted};font-size:0.72rem;">Footer: reacts, thread replies, and mentions stay compact in the live channel.</div>
            <div style="margin-top:0.45rem;color:{_muted};font-size:0.72rem;">Trace: {_escape(trace)}</div>
          </div>
        </div>
        """

    def _render_dashboard_mockup(request_payload, questions, backend_mode, trace):
        rows = [
            ("Learner", request_payload["learner"]),
            ("Subject", request_payload["subject"]),
            ("Weakest skill", request_payload["weakest_skill"]),
            ("Mode", _mode_badge(backend_mode)),
        ]
        row_html = "".join(
            f"""
            <div style="display:grid;grid-template-columns:1fr auto;gap:1rem;padding:0.5rem 0;border-top:1px solid {line};">
              <div style="color:{muted};font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;">{label}</div>
              <div style="color:{ink};font-size:0.86rem;font-weight:700;text-align:right;">{_escape(value)}</div>
            </div>
            """
            for label, value in rows
        )
        return f"""
        <div style="border:1px solid {_line};border-radius:8px;background:{_panel};padding:0.85rem 0.95rem;font-family:{_mono};color:{_ink};">
          <div style="display:flex;justify-content:space-between;gap:1rem;align-items:baseline;">
            <div>
              <div style="color:{_muted};font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;">Dashboard card</div>
              <div style="margin-top:0.18rem;font-size:0.98rem;font-weight:700;">Tutor summary</div>
            </div>
            <span style="display:inline-flex;align-items:center;padding:0.22rem 0.55rem;border-radius:999px;border:1px solid {_line};background:{_panel_soft};color:{_ink};font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;">{_mode_badge(backend_mode)}</span>
          </div>
          <div style="margin-top:0.7rem;">{row_html}</div>
          <div style="margin-top:0.55rem;color:{_muted};font-size:0.72rem;">{_escape(request_payload['goal'])}</div>
          <div style="margin-top:0.35rem;color:{_muted};font-size:0.72rem;">Trace: {_escape(trace)}</div>
        </div>
        """

    def _demo_questions(request_payload):
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
        return questions

    def _build_demo_response(request_payload):
        questions = _demo_questions(request_payload)
        backend_mode = "demo"
        trace = "Local deterministic tutor model"
        channel_messages = {
            "email": _render_email_mockup(request_payload, questions, backend_mode, trace),
            "sms": _render_sms_mockup(request_payload, questions, backend_mode, trace),
            "discord": _render_discord_mockup(request_payload, questions, backend_mode, trace),
            "dashboard": _render_dashboard_mockup(request_payload, questions, backend_mode, trace),
        }
        print("[DeepTutor] backend mode: demo")
        return {
            "backend_mode": backend_mode,
            "summary": f"DeepTutor demo packet for {request_payload['learner']}",
            "questions": questions,
            "delivery": {channel: channel_messages[channel] for channel in request_payload["channels"] if channel in channel_messages},
            "trace": trace,
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
            with urllib.request.urlopen(req, timeout=6) as resp:
                status = int(getattr(resp, "status", 200))
                raw = resp.read().decode("utf-8")
            if not 200 <= status < 300:
                raise urllib.error.HTTPError(base_url, status, f"DeepTutor backend returned {status}", hdrs=None, fp=None)
            data = json.loads(raw)
            if not isinstance(data, dict):
                raise ValueError("DeepTutor backend response must be a JSON object")

            questions = data.get("questions")
            if not isinstance(questions, list) or not questions:
                questions = _demo_questions(request_payload)
            questions = [str(question) for question in questions]
            trace = data.get("trace", "Live DeepTutor backend")
            data["backend_mode"] = "live"
            data["trace"] = trace
            data["questions"] = questions
            data["delivery"] = {
                "email": _render_email_mockup(request_payload, questions, "live", trace),
                "sms": _render_sms_mockup(request_payload, questions, "live", trace),
                "discord": _render_discord_mockup(request_payload, questions, "live", trace),
                "dashboard": _render_dashboard_mockup(request_payload, questions, "live", trace),
            }
            print(f"[DeepTutor] backend mode: live ({status})")
            return data
        except urllib.error.HTTPError as exc:
            fallback = _build_demo_response(request_payload)
            fallback["backend_mode"] = "demo-fallback"
            fallback["trace"] = f"Backend HTTP {exc.code}"
            print(f"[DeepTutor] backend mode: demo-fallback (HTTP {exc.code})")
            return fallback
        except (json.JSONDecodeError, ValueError) as exc:
            fallback = _build_demo_response(request_payload)
            fallback["backend_mode"] = "demo-fallback"
            fallback["trace"] = f"Backend parse failure: {exc.__class__.__name__}"
            print("[DeepTutor] backend mode: demo-fallback (parse failure)")
            return fallback
        except Exception as exc:
            fallback = _build_demo_response(request_payload)
            fallback["backend_mode"] = "demo-fallback"
            fallback["trace"] = f"Backend unavailable: {exc.__class__.__name__}"
            print(f"[DeepTutor] backend mode: demo-fallback ({exc.__class__.__name__})")
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
    _mode_badge = "⚡ LIVE" if tutor_packet.get("backend_mode") == "live" else "🧪 DEMO"

    mo.hstack(
        [
            mo.md(
                f"""
                <div style="padding:0.75rem 0.9rem;border-radius:8px;background:{theme['panel']};border:1px solid {theme['line']};font-family:{theme['mono']};">
                  <div style="color:{theme['muted']};font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;">Mode</div>
                  <div style="margin-top:0.25rem;font-size:1rem;font-weight:700;color:{theme['ink']}">{_mode_badge}</div>
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
def _(io, mo, np, payload, plt, skill_curves, skills, theme):
    week_index = payload["week"] - 1
    current_values = [skill_curves[skill][week_index] for skill in skills]
    palette = [theme["amber"], theme["cyan"], theme["violet"], theme["green"]]

    weeks = np.arange(1, 13)

    # ---- matplotlib chart ----
    plt.rcParams.update({
        "font.family": "monospace",
        "font.size": 11,
        "axes.facecolor": theme["bg"],
        "figure.facecolor": "none",
        "axes.edgecolor": theme["line"],
        "axes.labelcolor": theme["muted"],
        "xtick.color": theme["muted"],
        "ytick.color": theme["muted"],
        "grid.color": theme["line"],
        "grid.alpha": 0.5,
        "legend.facecolor": theme["panel"],
        "legend.edgecolor": theme["line"],
        "legend.labelcolor": theme["ink"],
        "legend.fontsize": 10,
    })

    fig, ax = plt.subplots(figsize=(12, 3.2))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor(theme["bg"])

    for idx, skill in enumerate(skills):
        curve = skill_curves[skill]
        _ws = payload["weakest_skill"]
        lw = 3.5 if skill == _ws else 2.0
        alpha = 1.0 if skill == _ws else 0.65
        ax.plot(
            weeks, curve,
            color=palette[idx % len(palette)],
            linewidth=lw, alpha=alpha,
            label=skill,
            solid_capstyle="round",
        )

    ax.axvline(
        payload["week"],
        color=theme["amber"],
        linewidth=1.8,
        linestyle="--",
        alpha=0.8,
        zorder=5,
    )
    ax.annotate(
        f"week {payload['week']}",
        xy=(payload["week"], 0.92),
        fontsize=9,
        color=theme["amber"],
        ha="center",
        fontfamily="monospace",
    )

    _ws = payload["weakest_skill"]
    ax.scatter(
        [payload["week"]],
        [skill_curves[_ws][week_index]],
        color=palette[skills.index(_ws)],
        s=120, zorder=10,
        edgecolors=theme["bg"],
        linewidths=2,
    )

    ax.set_xlim(0.5, 12.5)
    ax.set_ylim(0.0, 1.02)
    ax.set_xticks(range(1, 13))
    ax.set_xlabel("Week", fontsize=10, fontfamily="monospace")
    ax.set_ylabel("Mastery", fontsize=10, fontfamily="monospace")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.legend(
        loc="upper left",
        framealpha=0.85,
        borderpad=0.4,
        handlelength=1.2,
    )
    for spine in ax.spines.values():
        spine.set_linewidth(0.5)

    buf = io.BytesIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0.08, transparent=True)
    plt.close(fig)
    chart_svg = buf.getvalue().decode("utf-8")

    # ---- snapshot bars ----
    bars = []
    for idx, (skill, value) in enumerate(zip(skills, current_values)):
        bars.append(
            f"""
            <div style="margin-bottom:0.6rem;">
              <div style="display:flex;justify-content:space-between;gap:1rem;font-size:0.8rem;margin-bottom:0.2rem;">
                <span style="color:{theme['ink']};font-family:{theme['mono']};font-weight:600;">
                  {"⚠ " if skill == payload["weakest_skill"] else ""}{skill}
                </span>
                <span style="color:{palette[idx]};font-family:{theme['mono']};">{int(round(value * 100))}%</span>
              </div>
              <div style="height:14px;background:{theme['line']};border-radius:4px;overflow:hidden;">
                <div style="width:{value * 100:.1f}%;height:100%;background:{palette[idx]};border-radius:4px;"></div>
              </div>
            </div>
            """
        )

    mo.Html(
        f"""
        <div style="display:grid;grid-template-columns:1.6fr 1fr;gap:0.9rem;align-items:start;">
          <div style="padding:0.8rem 0.9rem 0.65rem;border-radius:8px;background:{theme['panel']};border:1px solid {theme['line']};font-family:{theme['mono']};">
            <div style="display:flex;justify-content:space-between;gap:1rem;align-items:baseline;margin-bottom:0.6rem;">
              <div>
                <div style="color:{theme['muted']};font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;">Mastery trajectory</div>
                <div style="color:{theme['ink']};font-size:1rem;font-weight:700;margin-top:0.15rem;">Week {payload['week']} — {payload['learner']}</div>
              </div>
              <div style="color:{theme['amber']};font-size:0.78rem;white-space:nowrap;">focus: {payload['weakest_skill']}</div>
            </div>
            {chart_svg}
          </div>
          <div style="padding:0.8rem 0.9rem 0.9rem;border-radius:8px;background:{theme['panel']};border:1px solid {theme['line']};font-family:{theme['mono']};">
            <div style="color:{theme['muted']};font-size:0.7rem;text-transform:uppercase;letter-spacing:0.12em;">Current snapshot</div>
            <div style="margin-top:0.2rem;color:{theme['ink']};font-size:0.85rem;font-weight:600;">Skill-by-skill map</div>
            <div style="margin-top:0.7rem;">{"".join(bars)}</div>
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
    _mode_badge = "⚡ LIVE" if tutor_packet.get("backend_mode") == "live" else "🧪 DEMO"

    def _channel_tab(channel_name, headline, tone):
        message = delivery.get(channel_name, f"<div style='padding:0.9rem;color:{theme['muted']};'>Channel not selected.</div>")
        return mo.Html(
            f"""
            <div style="padding:0.8rem 0.9rem;border-radius:8px;border:1px solid {theme['line']};background:{theme['bg']};font-family:{theme['mono']};color:{theme['ink']};">
              <div style="display:flex;justify-content:space-between;gap:1rem;align-items:baseline;margin-bottom:0.65rem;">
                <div>
                  <div style="color:{theme['cyan']};font-weight:700;font-size:0.88rem;">{headline}</div>
                  <div style="color:{theme['muted']};font-size:0.72rem;margin-top:0.12rem;">{tone}</div>
                </div>
                <div style="display:inline-flex;align-items:center;padding:0.22rem 0.55rem;border-radius:999px;border:1px solid {theme['line']};background:{theme['panel_soft']};color:{theme['ink']};font-size:0.68rem;letter-spacing:0.08em;text-transform:uppercase;">{_mode_badge}</div>
              </div>
              {message}
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
