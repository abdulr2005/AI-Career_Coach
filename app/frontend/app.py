"""
AI Career Coach — Streamlit dashboard
=====================================

A production-style Streamlit front end for an AI career-analysis product.
It calls a FastAPI backend (POST /analyze) that returns a JSON payload and
renders the results as a clean SaaS dashboard.

Design rules followed:
- Streamlit-native components only (no raw HTML/CSS injection).
- Every dictionary access goes through .get()-based helpers — a missing or
  malformed key renders an empty state instead of raising KeyError.
- Network/backend failures are caught and shown as a clear error, never a
  crash.

Run with:  streamlit run app.py
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Career Coach",
    page_icon=":compass:",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_API_URL = "http://localhost:8000/analyze"
REQUEST_TIMEOUT = 60  # seconds

EXPECTED_KEYS = [
    "cv_skills",
    "job_skills",
    "matched_skills",
    "missing_skills",
    "match_score",
    "ats_score",
    "recommended_courses",
    "roadmap",
    "suggestions",
    "resume_feedback",
]


# ---------------------------------------------------------------------------
# Safe-access helpers — every read of the API response goes through these.
# ---------------------------------------------------------------------------

def safe_list(data: Optional[Dict[str, Any]], key: str) -> List[Any]:
    """Return data[key] as a list, or [] if missing/wrong type."""
    if not isinstance(data, dict):
        return []
    value = data.get(key, [])
    return value if isinstance(value, list) else []


def safe_number(data: Optional[Dict[str, Any]], key: str, default: float = 0.0) -> float:
    """Return data[key] as a float, or `default` if missing/unparsable."""
    if not isinstance(data, dict):
        return default
    value = data.get(key, default)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return max(0.0, min(100.0, number))


def safe_str(item: Any, key: str, default: str = "Unspecified") -> str:
    """Read a string field off a possibly-malformed dict item."""
    if not isinstance(item, dict):
        return default
    value = item.get(key, default)
    return str(value) if value not in (None, "") else default


def validate_response(data: Any) -> Dict[str, Any]:
    """
    Normalize an arbitrary API payload into a dict with all expected keys
    present, so the rest of the app never has to guard against a missing
    top-level key. Unknown shapes degrade to empty defaults rather than
    raising.
    """
    if not isinstance(data, dict):
        data = {}
    normalized: Dict[str, Any] = {}
    for key in ("cv_skills", "job_skills", "matched_skills", "missing_skills",
                "recommended_courses", "roadmap", "suggestions", "resume_feedback"):
        normalized[key] = safe_list(data, key)
    normalized["match_score"] = safe_number(data, "match_score")
    normalized["ats_score"] = safe_number(data, "ats_score")
    return normalized


def score_color(score: float) -> str:
    if score >= 75:
        return "green"
    if score >= 50:
        return "orange"
    return "red"


def supports_badge() -> bool:
    return hasattr(st, "badge")


def render_tag_grid(items: List[str], kind: str, columns_per_row: int = 4) -> None:
    """Render a list of skill strings as colored tags, wrapped in rows."""
    items = [str(i) for i in items if str(i).strip()]
    if not items:
        st.caption("Nothing to show here yet.")
        return

    use_badge = supports_badge()
    for start in range(0, len(items), columns_per_row):
        row_items = items[start:start + columns_per_row]
        cols = st.columns(columns_per_row)
        for col, label in zip(cols, row_items):
            with col:
                if use_badge:
                    if kind == "good":
                        st.badge(label, icon=":material/check_circle:", color="green")
                    else:
                        st.badge(label, icon=":material/error:", color="red")
                else:
                    if kind == "good":
                        st.success(label, icon="✅")
                    else:
                        st.error(label, icon="⚠️")


def render_progress(label: str, value: float) -> None:
    pct = int(round(max(0.0, min(100.0, value))))
    try:
        st.progress(pct / 100, text=f"{label}: {pct}%")
    except TypeError:
        # Older Streamlit versions don't support the `text` kwarg.
        st.caption(f"{label}: {pct}%")
        st.progress(pct / 100)


# ---------------------------------------------------------------------------
# Demo data — lets the UI be explored fully without a live backend.
# ---------------------------------------------------------------------------

def demo_response() -> Dict[str, Any]:
    return {
        "cv_skills": ["Python", "SQL", "Data Analysis", "Communication", "Excel"],
        "job_skills": ["Python", "SQL", "Machine Learning", "Communication",
                        "Cloud Computing", "Leadership"],
        "matched_skills": ["Python", "SQL", "Communication"],
        "missing_skills": ["Machine Learning", "Cloud Computing", "Leadership"],
        "match_score": 68,
        "ats_score": 81,
        "recommended_courses": [
            {"skill": "Machine Learning", "course": "Machine Learning Specialization",
             "provider": "Coursera"},
            {"skill": "Cloud Computing", "course": "AWS Cloud Practitioner Essentials",
             "provider": "AWS Training"},
            {"skill": "Leadership", "course": "Leading People and Teams",
             "provider": "University of Michigan"},
        ],
        "roadmap": [
            {"step": 1, "skill": "Machine Learning", "difficulty": "Intermediate",
             "duration": "4 weeks"},
            {"step": 2, "skill": "Cloud Computing", "difficulty": "Beginner",
             "duration": "2 weeks"},
            {"step": 3, "skill": "Leadership", "difficulty": "Advanced",
             "duration": "6 weeks"},
        ],
        "suggestions": [
            "Add measurable outcomes to your recent project descriptions.",
            "Highlight any cloud or ML exposure, even at a beginner level.",
            "Move your most relevant experience to the top of your resume.",
        ],
        "resume_feedback": [
            "Resume is well structured but lacks quantified achievements.",
            "Consider a concise summary section tailored to the target role.",
            "Some bullet points are too long — aim for one line each.",
        ],
    }


# ---------------------------------------------------------------------------
# Backend call
# ---------------------------------------------------------------------------

def call_backend(base_url: str, cv_file, job_description: str) -> Dict[str, Any]:
    """
    POST the CV file + job description to the FastAPI backend.
    Returns a dict: {"ok": bool, "data": dict|None, "error": str|None}
    """
    if not base_url:
        return {"ok": False, "data": None, "error": "No API URL configured."}

    files = {}
    if cv_file is not None:
        files["cv_file"] = (cv_file.name, cv_file.getvalue(), "application/pdf")

    try:
        response = requests.post(
            base_url,
            files=files if files else None,
            data={"job_description": job_description},
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.ConnectTimeout:
        return {"ok": False, "data": None, "error": "The request to the backend timed out while connecting."}
    except requests.exceptions.ConnectionError:
        return {"ok": False, "data": None,
                "error": f"Couldn't reach the backend at {base_url}. Is it running?"}
    except requests.exceptions.Timeout:
        return {"ok": False, "data": None, "error": "The backend took too long to respond."}
    except requests.exceptions.RequestException as exc:
        return {"ok": False, "data": None, "error": f"Request failed: {exc}"}

    if response.status_code != 200:
        return {
            "ok": False,
            "data": None,
            "error": f"Backend returned status {response.status_code}: {response.text[:300]}",
        }

    try:
        payload = response.json()
    except ValueError:
        return {"ok": False, "data": None, "error": "Backend response was not valid JSON."}

    return {"ok": True, "data": payload, "error": None}


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

st.session_state.setdefault("result", None)
st.session_state.setdefault("last_error", None)
st.session_state.setdefault("api_url", DEFAULT_API_URL)
st.session_state.setdefault("demo_mode", True)


# ---------------------------------------------------------------------------
# Sidebar — connection settings
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### :gear: Settings")
    st.session_state.demo_mode = st.toggle(
        "Use demo data",
        value=st.session_state.demo_mode,
        help="Preview the dashboard with sample results, without calling a backend.",
    )
    st.session_state.api_url = st.text_input(
        "Backend endpoint",
        value=st.session_state.api_url,
        disabled=st.session_state.demo_mode,
        help="Your FastAPI /analyze endpoint.",
    )
    st.divider()
    with st.expander("How this works"):
        st.write(
            "Upload a CV and paste a job description, then click **Analyze**. "
            "The request is sent to your FastAPI backend, which returns a JSON "
            "report. This dashboard renders that report and never assumes a "
            "field is present — missing data always shows as an empty state, "
            "not an error."
        )
    if st.session_state.result is not None:
        if st.button("Clear results", use_container_width=True):
            st.session_state.result = None
            st.session_state.last_error = None
            st.rerun()


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("AI Career Coach")
st.caption("Your intelligent career analysis dashboard")
st.divider()


# ---------------------------------------------------------------------------
# Upload section
# ---------------------------------------------------------------------------

with st.container(border=True):
    st.subheader("Analyze a role")
    col_upload, col_job = st.columns([1, 1])

    with col_upload:
        cv_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])

    with col_job:
        job_description = st.text_area(
            "Paste the job description",
            height=180,
            placeholder="Paste the full job posting here...",
        )

    analyze_clicked = st.button("Analyze", type="primary", use_container_width=False)

    if analyze_clicked:
        if not st.session_state.demo_mode and cv_file is None and not job_description.strip():
            st.warning("Upload a CV or paste a job description before analyzing.")
        else:
            with st.spinner("Analyzing your fit for this role..."):
                if st.session_state.demo_mode:
                    time.sleep(1.0)
                    st.session_state.result = validate_response(demo_response())
                    st.session_state.last_error = None
                else:
                    outcome = call_backend(
                        st.session_state.api_url, cv_file, job_description
                    )
                    if outcome["ok"]:
                        st.session_state.result = validate_response(outcome["data"])
                        st.session_state.last_error = None
                    else:
                        st.session_state.result = None
                        st.session_state.last_error = outcome["error"]

st.write("")

# ---------------------------------------------------------------------------
# Error state
# ---------------------------------------------------------------------------

if st.session_state.last_error:
    st.error(f"Analysis failed: {st.session_state.last_error}")
    st.caption("Check that your backend is running and reachable, then try again.")

# ---------------------------------------------------------------------------
# Empty state
# ---------------------------------------------------------------------------

if st.session_state.result is None:
    if not st.session_state.last_error:
        st.info(
            "No analysis yet. Upload a CV and a job description, then click "
            "**Analyze** to see your match score, skill gaps, and roadmap here."
        )
    st.stop()

result = st.session_state.result

match_score = result["match_score"]
ats_score = result["ats_score"]
matched_skills = result["matched_skills"]
missing_skills = result["missing_skills"]
recommended_courses = result["recommended_courses"]
roadmap = result["roadmap"]
suggestions = result["suggestions"]
resume_feedback = result["resume_feedback"]
cv_skills = result["cv_skills"]
job_skills = result["job_skills"]


# ---------------------------------------------------------------------------
# Metrics row
# ---------------------------------------------------------------------------

st.subheader("Overview")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Match score", f"{match_score:.0f}%")
    render_progress("Match", match_score)

with m2:
    st.metric("ATS score", f"{ats_score:.0f}%")
    render_progress("ATS", ats_score)

with m3:
    st.metric("Matched skills", len(matched_skills))

with m4:
    st.metric("Missing skills", len(missing_skills))

st.write("")

# ---------------------------------------------------------------------------
# Skills section
# ---------------------------------------------------------------------------

st.subheader("Skills")
skill_col_left, skill_col_right = st.columns(2)

with skill_col_left:
    st.markdown("**Matched skills**")
    render_tag_grid(matched_skills, kind="good")

with skill_col_right:
    st.markdown("**Missing skills**")
    render_tag_grid(missing_skills, kind="bad")

with st.expander("View all extracted skills"):
    ce, je = st.columns(2)
    with ce:
        st.markdown("**From your CV**")
        if cv_skills:
            for skill in cv_skills:
                st.write(f"- {skill}")
        else:
            st.caption("No skills extracted from the CV.")
    with je:
        st.markdown("**From the job description**")
        if job_skills:
            for skill in job_skills:
                st.write(f"- {skill}")
        else:
            st.caption("No skills extracted from the job description.")

st.write("")

# ---------------------------------------------------------------------------
# Insights section
# ---------------------------------------------------------------------------

st.subheader("Insights")
tab_courses, tab_roadmap, tab_feedback, tab_suggestions = st.tabs(
    ["Recommended courses", "Career roadmap", "Resume feedback", "Suggestions"]
)

with tab_courses:
    if not recommended_courses:
        st.caption("No course recommendations available yet.")
    else:
        cols = st.columns(3)
        for idx, course in enumerate(recommended_courses):
            skill = safe_str(course, "skill")
            title = safe_str(course, "course", default="Untitled course")
            provider = safe_str(course, "provider", default="Unknown provider")
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"**{title}**")
                    st.caption(provider)
                    st.write(f"Builds: {skill}")

with tab_roadmap:
    if not roadmap:
        st.caption("No roadmap available yet.")
    else:
        ordered = sorted(
            roadmap,
            key=lambda item: item.get("step", 0) if isinstance(item, dict) else 0,
        )
        for position, item in enumerate(ordered, start=1):
            step_number = item.get("step", position) if isinstance(item, dict) else position
            skill = safe_str(item, "skill")
            difficulty = safe_str(item, "difficulty", default="Unspecified")
            duration = safe_str(item, "duration", default="Unspecified")
            with st.container(border=True):
                left, right = st.columns([3, 2])
                with left:
                    st.markdown(f"**Step {step_number}: {skill}**")
                with right:
                    if supports_badge():
                        color = DIFFICULTY_COLOR = {
                            "beginner": "green", "intermediate": "orange", "advanced": "red",
                        }.get(difficulty.lower(), "blue")
                        st.badge(difficulty, color=color)
                    else:
                        st.caption(f"Difficulty: {difficulty}")
                st.caption(f"Estimated duration: {duration}")

with tab_feedback:
    if not resume_feedback:
        st.caption("No resume feedback available yet.")
    else:
        for point in resume_feedback:
            st.write(f"- {point}")

with tab_suggestions:
    if not suggestions:
        st.caption("No suggestions available yet.")
    else:
        for point in suggestions:
            st.write(f"- {point}")