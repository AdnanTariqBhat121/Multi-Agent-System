import streamlit as st
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ─────────────────────────────────────────────────────────────────────────────
# Page config  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Global ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0B0F1C; color: #E2E8F0; }

#MainMenu, footer { visibility: hidden; }

.block-container {
    padding: 2.5rem 3.5rem 3rem;
    max-width: 1300px;
}

/* ── Header ── */
.ri-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #3B82F6;
    margin-bottom: 0.3rem;
}
.ri-heading {
    font-size: 2.1rem;
    font-weight: 700;
    color: #F1F5F9;
    margin: 0 0 0.3rem;
    line-height: 1.15;
}
.ri-sub {
    font-size: 0.88rem;
    color: #475569;
    margin-bottom: 0;
}
.ri-divider {
    border: none;
    border-top: 1px solid #1C2541;
    margin: 1.4rem 0 2rem;
}

/* ── Stage grid ── */
.stage-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.9rem;
    margin: 0 0 1.8rem;
}
.stage-card {
    background: #111827;
    border: 1px solid #1C2541;
    border-radius: 10px;
    padding: 1rem 1rem 0.9rem 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.stage-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 10px 0 0 10px;
    background: #1C2541;
    transition: background 0.25s;
}
.stage-card.s-active  { border-color: #2D3F60; }
.stage-card.s-active::before  { background: #F59E0B; }
.stage-card.s-done    { border-color: #1A3A30; }
.stage-card.s-done::before    { background: #10B981; }

.stage-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    color: #334155;
    margin-bottom: 0.35rem;
}
.stage-name {
    font-size: 0.84rem;
    font-weight: 600;
    color: #94A3B8;
    margin-bottom: 0.18rem;
}
.stage-card.s-active .stage-name { color: #FCD34D; }
.stage-card.s-done   .stage-name { color: #34D399; }

.stage-desc {
    font-size: 0.73rem;
    color: #334155;
    line-height: 1.45;
}
.stage-icon {
    position: absolute;
    top: 0.8rem; right: 0.9rem;
    font-size: 0.9rem;
}
@keyframes spin { to { transform: rotate(360deg); } }
.spinning { display: inline-block; animation: spin 1s linear infinite; }

/* ── Input area ── */
.stTextInput > div > div > input {
    background: #111827 !important;
    border: 1px solid #1C2541 !important;
    color: #E2E8F0 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1rem !important;
    caret-color: #3B82F6;
}
.stTextInput > div > div > input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.14) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: #334155 !important; }
.stTextInput > label { display: none !important; }

/* ── Run button ── */
.stButton > button {
    background: #3B82F6 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.64rem 1.4rem !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    transition: background 0.15s, transform 0.1s !important;
}
.stButton > button:hover  { background: #2563EB !important; }
.stButton > button:active { transform: scale(0.98) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1C2541 !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.65rem 1.3rem !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
    color: #3B82F6 !important;
    border-bottom-color: #3B82F6 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #111827 !important;
    border: 1px solid #1C2541 !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    padding: 1.6rem 1.8rem !important;
    margin-top: 0 !important;
}

/* ── Report markdown ── */
.stMarkdown p, .stMarkdown li {
    color: #CBD5E1 !important;
    line-height: 1.75 !important;
    font-size: 0.93rem !important;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #F1F5F9 !important;
    font-weight: 600 !important;
}
.stMarkdown h2 { border-bottom: 1px solid #1C2541; padding-bottom: 0.4rem; }
.stMarkdown code {
    background: #0B0F1C !important;
    color: #93C5FD !important;
    border: 1px solid #1C2541 !important;
    border-radius: 4px !important;
    padding: 0.15rem 0.4rem !important;
    font-size: 0.85em !important;
}
.stMarkdown blockquote {
    border-left: 3px solid #3B82F6 !important;
    padding-left: 1rem !important;
    color: #64748B !important;
}
.stMarkdown strong { color: #E2E8F0 !important; }

/* ── Raw text panes ── */
.stText {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.76rem !important;
    color: #475569 !important;
    background: #0B0F1C !important;
    border: 1px solid #1C2541 !important;
    border-radius: 8px !important;
    padding: 1.1rem !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
    line-height: 1.6 !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid #1C2541 !important;
    color: #475569 !important;
    font-size: 0.8rem !important;
    border-radius: 6px !important;
    padding: 0.38rem 0.9rem !important;
    transition: border-color 0.15s, color 0.15s !important;
}
.stDownloadButton > button:hover {
    border-color: #3B82F6 !important;
    color: #3B82F6 !important;
}

/* ── Success / warning / error ── */
div[data-testid="stAlert"] {
    background: #111827 !important;
    border-radius: 8px !important;
}

/* ── Spinner ── */
div[data-testid="stSpinner"] svg { stroke: #3B82F6 !important; }

/* ── Results heading ── */
.results-label {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 0.4rem 0 0.9rem;
}
.results-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3B82F6;
    background: rgba(59,130,246,.1);
    border: 1px solid rgba(59,130,246,.2);
    border-radius: 4px;
    padding: 0.18rem 0.55rem;
}
.results-topic {
    font-size: 0.95rem;
    font-weight: 600;
    color: #94A3B8;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Helper: extract string from LangChain output (AIMessage or plain str)
# ─────────────────────────────────────────────────────────────────────────────
def to_str(val) -> str:
    if val is None:
        return ""
    if isinstance(val, str):
        return val
    if hasattr(val, "content"):          # AIMessage
        return str(val.content)
    return str(val)

# ─────────────────────────────────────────────────────────────────────────────
# Pipeline stage definitions
# ─────────────────────────────────────────────────────────────────────────────
STAGES = [
    ("01", "Search Agent",  "Finding sources across the web"),
    ("02", "Reader Agent",  "Scraping the most relevant URL"),
    ("03", "Writer Chain",  "Drafting the research report"),
    ("04", "Critic Chain",  "Reviewing & scoring the report"),
]

def stages_html(active: int = -1, done: int = 0) -> str:
    """
    active  — index of the stage currently running (-1 = none)
    done    — how many stages have fully completed (from the left)
    """
    cards = []
    for i, (num, name, desc) in enumerate(STAGES):
        if i < done:
            cls  = "s-done"
            icon = '<span style="color:#10B981;">✓</span>'
        elif i == active:
            cls  = "s-active"
            icon = '<span class="spinning" style="color:#F59E0B;">⟳</span>'
        else:
            cls  = ""
            icon = '<span style="color:#1E293B;">·</span>'

        cards.append(f"""
        <div class="stage-card {cls}">
            <div class="stage-icon">{icon}</div>
            <div class="stage-num">{num}</div>
            <div class="stage-name">{name}</div>
            <div class="stage-desc">{desc}</div>
        </div>""")

    return f'<div class="stage-grid">{"".join(cards)}</div>'

# ─────────────────────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────────────────────
for key, default in [("result", None), ("run_topic", "")]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ri-eyebrow">Multi-Agent System</div>
<h1 class="ri-heading">Research Intelligence</h1>
<p class="ri-sub">Four specialized agents work in sequence — Search · Scrape · Write · Review</p>
<hr class="ri-divider">
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Input row
# ─────────────────────────────────────────────────────────────────────────────
col_inp, col_btn = st.columns([6, 1])
with col_inp:
    topic = st.text_input(
        "topic",
        placeholder="Enter a research topic  —  e.g. Impact of AI on drug discovery",
        label_visibility="collapsed",
    )
with col_btn:
    run = st.button("▶  Run", type="primary")

# Placeholder for live stage cards
stage_slot = st.empty()

# ─────────────────────────────────────────────────────────────────────────────
# Default idle stage view
# ─────────────────────────────────────────────────────────────────────────────
if not run:
    stage_slot.markdown(stages_html(), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Pipeline execution
# ─────────────────────────────────────────────────────────────────────────────
if run:
    if not topic or not topic.strip():
        st.warning("Please enter a research topic before running.")
        stage_slot.markdown(stages_html(), unsafe_allow_html=True)
    else:
        topic = topic.strip()
        state = {}

        try:
            # ── Step 1: Search ────────────────────────────────────────────────
            stage_slot.markdown(stages_html(active=0, done=0), unsafe_allow_html=True)
            with st.spinner("Search agent is finding sources…"):
                search_agent = build_search_agent()
                search_result = search_agent.invoke({
                    "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
                })
            state["search_results"] = to_str(search_result["messages"][-1].content)

            # ── Step 2: Reader ───────────────────────────────────────────────
            stage_slot.markdown(stages_html(active=1, done=1), unsafe_allow_html=True)
            with st.spinner("Reader agent is scraping the best source…"):
                reader_agent = build_reader_agent()
                reader_result = reader_agent.invoke({
                    "messages": [("user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}"
                    )]
                })
            state["scraped_content"] = to_str(reader_result["messages"][-1].content)

            # ── Step 3: Writer ───────────────────────────────────────────────
            stage_slot.markdown(stages_html(active=2, done=2), unsafe_allow_html=True)
            with st.spinner("Writer is drafting the report…"):
                research_combined = (
                    f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                    f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
                )
                raw_report = writer_chain.invoke({"topic": topic, "research": research_combined})
            state["report"] = to_str(raw_report)

            # ── Step 4: Critic ───────────────────────────────────────────────
            stage_slot.markdown(stages_html(active=3, done=3), unsafe_allow_html=True)
            with st.spinner("Critic is reviewing the report…"):
                raw_feedback = critic_chain.invoke({"report": state["report"]})
            state["feedback"] = to_str(raw_feedback)

            # ── Done ─────────────────────────────────────────────────────────
            stage_slot.markdown(stages_html(done=4), unsafe_allow_html=True)
            st.success("Pipeline complete — scroll down to read the report.")

            st.session_state.result    = state
            st.session_state.run_topic = topic

        except Exception as exc:
            stage_slot.markdown(stages_html(), unsafe_allow_html=True)
            st.error(f"**Pipeline error:** {exc}")

# ─────────────────────────────────────────────────────────────────────────────
# Results
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.result:
    result      = st.session_state.result
    run_topic   = st.session_state.run_topic

    st.markdown(f"""
    <div class="results-label">
        <span class="results-pill">Results</span>
        <span class="results-topic">{run_topic}</span>
    </div>
    """, unsafe_allow_html=True)

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs([
        "📄  Final Report",
        "🧐  Critic Feedback",
        "🔍  Search Results",
        "📚  Scraped Content",
    ])

    with tab_report:
        report_str = result.get("report", "") or ""
        st.markdown(report_str)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            "⬇  Download report (.md)",
            data=report_str,
            file_name=f"{run_topic.replace(' ', '_')}_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        feedback_str = result.get("feedback", "") or ""
        st.markdown(feedback_str)

    with tab_search:
        st.text(result.get("search_results", "No search results."))

    with tab_scraped:
        st.text(result.get("scraped_content", "No scraped content."))

elif not run:
    st.markdown(
        '<p style="color:#334155;font-size:0.85rem;text-align:center;margin-top:1rem;">'
        'Enter a topic above and click <strong style="color:#3B82F6;">▶ Run</strong> to start the pipeline.</p>',
        unsafe_allow_html=True
    )