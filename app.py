import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

# ---------- Sidebar ----------
with st.sidebar:
    st.title("🔎 Research Pipeline")
    st.markdown(
        "This app runs a 4-stage multi-agent pipeline:\n"
        "1. **Search Agent** – finds sources\n"
        "2. **Reader Agent** – scrapes the best one\n"
        "3. **Writer Chain** – drafts the report\n"
        "4. **Critic Chain** – reviews the report"
    )
    st.divider()
    topic = st.text_input("Research topic", placeholder="e.g. Impact of AI on renewable energy")
    run_btn = st.button("🚀 Run Pipeline", type="primary", use_container_width=True)
    st.divider()
    st.caption("Results from your last run stay visible until you run a new topic.")

# ---------- Session state ----------
if "result" not in st.session_state:
    st.session_state.result = None
if "topic" not in st.session_state:
    st.session_state.topic = ""

# ---------- Run pipeline ----------
if run_btn:
    if not topic or not topic.strip():
        st.warning("Please enter a research topic before running the pipeline.")
    else:
        steps = [
            "Step 1/4 — Search agent is finding sources...",
            "Step 2/4 — Reader agent is scraping content...",
            "Step 3/4 — Writer is drafting the report...",
            "Step 4/4 — Critic is reviewing the report...",
        ]
        with st.status(steps[0], expanded=True) as status:
            try:
                # NOTE: run_research_pipeline() runs all 4 steps internally as one
                # blocking call, so we can't show live per-step progress here unless
                # pipeline.py is refactored to accept a callback. See note below.
                result = run_research_pipeline(topic.strip())
                status.update(label="✅ Pipeline complete!", state="complete", expanded=False)
                st.session_state.result = result
                st.session_state.topic = topic.strip()
            except Exception as e:
                status.update(label="❌ Pipeline failed", state="error", expanded=True)
                st.error(f"Something went wrong: {e}")
                st.session_state.result = None

# ---------- Display results ----------
if st.session_state.result:
    result = st.session_state.result
    st.header(f"Results: {st.session_state.topic}")

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📚 Scraped Content"]
    )

    with tab_report:
        report_text = result.get("report", "")
        report_str = report_text if isinstance(report_text, str) else str(report_text)
        st.markdown(report_str)
        st.download_button(
            "⬇️ Download report (.md)",
            data=report_str,
            file_name=f"{st.session_state.topic.replace(' ', '_')}_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        feedback_text = result.get("feedback", "")
        feedback_str = feedback_text if isinstance(feedback_text, str) else str(feedback_text)
        st.markdown(feedback_str)

    with tab_search:
        st.text(result.get("search_results", "No search results found."))

    with tab_scraped:
        st.text(result.get("scraped_content", "No scraped content found."))

else:
    st.info("Enter a topic in the sidebar and click **Run Pipeline** to get started.")