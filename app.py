# =============================================================
# app.py — Streamlit UI for Multi-Agent Medical Research Assistant
# =============================================================
# Run with:  streamlit run app.py
# =============================================================

import os
import time
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Medical Research Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — dark theme + readable text ───────────────────
st.markdown("""
<style>
    /* ── Global dark background ── */
    .stApp, .stApp > div, section[data-testid="stSidebar"] {
        background-color: #0f1117 !important;
        color: #e8eaed !important;
    }

    /* ── All text elements ── */
    p, li, span, label, div, h1, h2, h3, h4, h5, h6,
    .stMarkdown, .stText {
        color: #e8eaed !important;
    }

    /* ── Header banner ── */
    .header-banner {
        background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }
    .header-banner h1 { font-size: 2rem; font-weight: 700; margin: 0; color: #ffffff !important; }
    .header-banner p  { font-size: 1rem; opacity: 0.9; margin: 0.4rem 0 0; color: #ffffff !important; }

    /* ── Stat cards ── */
    .stat-card {
        background: #1e2130;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #2d3147;
    }
    .stat-number { font-size: 1.8rem; font-weight: 700; color: #4da3ff !important; }
    .stat-label  { font-size: 0.78rem; color: #9aa0b4 !important; margin-top: 4px; }

    /* ── Disclaimer ── */
    .disclaimer {
        background: #2a2400;
        border: 1px solid #ffc107;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        font-size: 0.84rem;
        color: #ffd54f !important;
        margin-bottom: 1rem;
    }

    /* ── Agent cards in sidebar ── */
    .agent-card {
        background: #1e2130;
        border-radius: 10px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.6rem;
        border-left: 4px solid #2d3147;
    }
    .agent-card.done { border-left-color: #34a853; }
    .agent-name { font-weight: 600; font-size: 0.88rem; color: #e8eaed !important; }
    .agent-role { font-size: 0.75rem; color: #9aa0b4 !important; margin-top: 3px; }

    /* ── Report box ── */
    .report-box {
        background: #1e2130;
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid #2d3147;
        color: #e8eaed !important;
        line-height: 1.8;
        font-size: 0.96rem;
    }
    .report-box p, .report-box li, .report-box span {
        color: #d0d4e4 !important;
    }

    /* ── Section headers inside report ── */
    .report-section {
        background: #162032;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin: 1.2rem 0 0.5rem;
        font-weight: 700;
        color: #4da3ff !important;
        font-size: 1rem;
        border-left: 3px solid #1a73e8;
    }

    /* ── Input / Textarea ── */
    .stTextArea textarea, .stTextInput input {
        background: #1e2130 !important;
        color: #e8eaed !important;
        border: 1.5px solid #2d3147 !important;
        border-radius: 12px !important;
        font-size: 0.97rem !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #1a73e8 !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #1a73e8, #0d47a1) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
    }
    .stButton > button:hover { opacity: 0.88 !important; }
    .stButton > button:disabled {
        background: #2d3147 !important;
        color: #666 !important;
    }

    /* ── Download button ── */
    .stDownloadButton > button {
        background: #1e6e3e !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        width: 100% !important;
        font-weight: 600 !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #1e2130 !important;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #9aa0b4 !important;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #162032 !important;
        color: #4da3ff !important;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: transparent !important;
    }

    /* ── Progress bar ── */
    .stProgress > div > div {
        background: linear-gradient(90deg, #1a73e8, #34a853) !important;
    }

    /* ── Alerts / success / error ── */
    .stSuccess { background: #0d2b1a !important; color: #81c995 !important; border-color: #34a853 !important; }
    .stError   { background: #2b0d0d !important; color: #f28b82 !important; border-color: #ea4335 !important; }
    .stWarning { background: #2b2200 !important; color: #fdd663 !important; border-color: #fbc02d !important; }

    /* ── Sidebar divider ── */
    hr { border-color: #2d3147 !important; }

    /* ── Sample question buttons ── */
    .stButton > button[kind="secondary"] {
        background: #1e2130 !important;
        color: #9aa0b4 !important;
        border: 1px solid #2d3147 !important;
        font-size: 0.82rem !important;
        padding: 0.4rem 0.8rem !important;
    }

    /* ── Text area in Raw tab ── */
    .stTextArea [data-baseweb="textarea"] {
        background: #1e2130 !important;
    }

    /* ── Spinner text ── */
    .stSpinner p { color: #9aa0b4 !important; }

    /* ── Hide Streamlit branding ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0f1117; }
    ::-webkit-scrollbar-thumb { background: #2d3147; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────
def check_api_key() -> bool:
    key = os.getenv("GROQ_API_KEY", "")
    return bool(key) and key != "your_groq_api_key_here"


def run_crew(question: str) -> str:
    import re
    from tasks import create_tasks
    from crewai import Crew, Process

    tasks, agents = create_tasks(question)
    crew = Crew(agents=agents, tasks=tasks, process=Process.sequential, verbose=False)

    # Retry up to 3 times on rate limit errors
    for attempt in range(3):
        try:
            return str(crew.kickoff())
        except Exception as e:
            err = str(e)
            if "rate_limit_exceeded" in err or "RateLimitError" in err:
                match = re.search(r"try again in (\d+\.?\d*)s", err)
                wait  = float(match.group(1)) + 3 if match else 20
                st.warning(f"⏳ Rate limit hit — waiting {wait:.0f}s before retry (attempt {attempt+1}/3)...")
                time.sleep(wait)
                tasks, agents = create_tasks(question)
                crew = Crew(agents=agents, tasks=tasks, process=Process.sequential, verbose=False)
            else:
                raise
    raise Exception("Rate limit retries exhausted. Please wait a minute and try again.")


def save_report_file(report: str, question: str) -> str:
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() or c == " " else "_" for c in question[:40])
    safe = safe.strip().replace(" ", "_")
    path = f"reports/{safe}_{timestamp}.txt"
    content = (
        f"MEDICAL RESEARCH REPORT\n{'='*60}\n"
        f"Question  : {question}\n"
        f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{'='*60}\n\n{report}"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return content


# ── Session state defaults ────────────────────────────────────
for key, val in {
    "report": None, "question": "", "running": False,
    "elapsed": 0, "report_text": "", "error": None,
    "api_key_saved": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    # API key is loaded silently from .env — not shown in UI

    st.markdown("## 🤖 Agent Pipeline")
    for icon, name, role in [
        ("🔍", "Research Agent",  "Searches ArXiv for papers"),
        ("📖", "Reader Agent",    "Extracts key information"),
        ("🔬", "Analysis Agent",  "Compares findings"),
        ("📝", "Summary Agent",   "Writes final report"),
    ]:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-name">{icon} {name}</div>
            <div class="agent-role">{role}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Sample questions
    st.markdown("## 💡 Sample Questions")
    for s in [
        "Effects of mRNA vaccines on long-term immunity",
        "Machine learning in cancer diagnosis",
        "Antibiotic resistance in bacteria",
        "Deep learning for diabetic retinopathy",
        "COVID-19 and cardiovascular complications",
    ]:
        if st.button(s, key=f"s_{s[:15]}", use_container_width=True):
            st.session_state.question = s

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem;color:#555;text-align:center'>"
        "Powered by CrewAI · Groq · ArXiv</div>",
        unsafe_allow_html=True,
    )


# ── Main content ──────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <h1>🏥 Multi-Agent Medical Research Assistant</h1>
    <p>4 AI agents collaborate to search, read, analyse, and report on any medical topic</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    ⚠️ <strong>Disclaimer:</strong> For research and educational purposes only.
    Not a substitute for professional medical advice.
</div>
""", unsafe_allow_html=True)

# Stats
c1, c2, c3, c4 = st.columns(4)
for col, num, label in zip(
    [c1, c2, c3, c4],
    ["4", "5+", "9", "~2m"],
    ["AI Agents", "Papers Searched", "Report Sections", "Avg. Runtime"],
):
    col.markdown(
        f'<div class="stat-card"><div class="stat-number">{num}</div>'
        f'<div class="stat-label">{label}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Question input
st.markdown("### 🔎 Enter Your Medical Research Question")
question = st.text_area(
    "question",
    value=st.session_state.question,
    placeholder="e.g. What are the latest findings on mRNA vaccines and long-term immune response?",
    height=110,
    label_visibility="collapsed",
)

run_clicked = st.button(
    "🚀 Run Research Agents",
    disabled=not check_api_key() or not question.strip(),
    use_container_width=True,
)

# Warn if user entered multiple questions
if question.strip():
    lines = [l.strip() for l in question.strip().split("\n") if l.strip()]
    q_marks = question.count("?")
    if len(lines) > 1 or q_marks > 1:
        st.warning(
            "⚠️ Please enter **one question at a time** for best results. "
            "Multiple questions overload the agents and cause token limit errors."
        )

# ── Execute ───────────────────────────────────────────────────
# Block if multiple questions detected
lines   = [l.strip() for l in question.strip().split("\n") if l.strip()]
q_marks = question.count("?")
multi_q = len(lines) > 1 or q_marks > 1

if run_clicked and multi_q:
    st.error("❌ Please enter only **one question** at a time and click Run again.")

elif run_clicked and question.strip():
    st.session_state.report      = None
    st.session_state.error       = None
    st.session_state.report_text = ""
    st.session_state.question    = question.strip()

    st.markdown("---")
    st.markdown("### ⚙️ Agent Pipeline Running...")
    progress_bar = st.progress(0)
    status_text  = st.empty()
    timing_text  = st.empty()
    start_time   = time.time()

    try:
        with st.spinner("Running 4 agents sequentially — takes 3-4 minutes (includes rate limit delays)..."):
            for prog, msg in [
                (0.10, "🔍 Research Agent searching ArXiv..."),
                (0.35, "⏳ Waiting 25s before Reader Agent (rate limit protection)..."),
                (0.50, "📖 Reader Agent extracting information..."),
                (0.65, "⏳ Waiting 25s before Analysis Agent..."),
                (0.75, "🔬 Analysis Agent comparing findings..."),
                (0.88, "⏳ Waiting 25s before Summary Agent..."),
                (0.93, "📝 Summary Agent writing report..."),
            ]:
                progress_bar.progress(prog)
                status_text.markdown(f"**{msg}**")
                timing_text.markdown(f"⏱️ Elapsed: `{time.time()-start_time:.0f}s`")

            report = run_crew(question.strip())

        progress_bar.progress(1.0)
        elapsed = time.time() - start_time
        status_text.markdown("**✅ All agents completed!**")
        timing_text.markdown(f"⏱️ Total: `{elapsed:.0f}s`")

        report_content = save_report_file(report, question.strip())
        st.session_state.report      = report
        st.session_state.report_text = report_content
        st.session_state.elapsed     = elapsed

    except Exception as e:
        st.session_state.error = str(e)


# ── Error display ─────────────────────────────────────────────
if st.session_state.error:
    st.markdown("---")
    st.error(f"❌ **Error:** {st.session_state.error}")
    with st.expander("🛠️ Troubleshooting Tips"):
        st.markdown("""
        - ✅ Check your Groq API key is valid at [console.groq.com](https://console.groq.com)
        - ✅ Run `pip install litellm` if you see an LLM error
        - ✅ Check your internet connection (ArXiv needs internet)
        - ✅ Make sure all agents files are in the same folder
        """)


# ── Report display ────────────────────────────────────────────
if st.session_state.report:
    st.markdown("---")
    st.success(f"✅ Research completed in {st.session_state.elapsed:.0f} seconds!")

    tab1, tab2, tab3 = st.tabs(["📄 Formatted Report", "📋 Raw Text", "💾 Download"])

    with tab1:
        st.markdown("### 📋 Medical Research Report")
        report = st.session_state.report

        # Render each section with styled headers
        for section in report.split("\n\n"):
            s = section.strip()
            if not s:
                continue
            lines = s.split("\n")
            first = lines[0].strip()
            # Detect "1. SECTION TITLE" pattern
            if first and first[0].isdigit() and ". " in first[:6]:
                st.markdown(
                    f'<div class="report-section">🔹 {first}</div>',
                    unsafe_allow_html=True,
                )
                body = "\n".join(lines[1:]).strip()
                if body:
                    # Render markdown properly (bold, bullets etc.)
                    st.markdown(body)
            else:
                # Render markdown properly
                st.markdown(s)

    with tab2:
        st.text_area(
            "raw",
            value=st.session_state.report,
            height=500,
            label_visibility="collapsed",
        )

    with tab3:
        st.markdown(f"**Question:** {st.session_state.question}")
        st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        fname = (
            "".join(c if c.isalnum() or c == " " else "_"
                    for c in st.session_state.question[:30])
            .strip().replace(" ", "_")
        )
        st.download_button(
            label="⬇️ Download Report as .txt",
            data=st.session_state.report_text,
            file_name=f"medical_report_{fname}.txt",
            mime="text/plain",
            use_container_width=True,
        )