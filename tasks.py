import time
from crewai import Task
from agents import (
    create_research_agent,
    create_reader_agent,
    create_analysis_agent,
    create_summary_agent,
)


INTER_TASK_DELAY = 25  # seconds


def sleep_callback(output):
    """
    Called after each task completes.
    Sleeps to let Groq's token-per-minute window reset.
    """
    print(f"\n⏳ Waiting {INTER_TASK_DELAY}s before next agent (rate limit protection)...\n")
    time.sleep(INTER_TASK_DELAY)
    return output


def create_tasks(research_question: str):
    """
    Build and return all four chained tasks for a given research question.

    Args:
        research_question (str): The medical topic entered by the user.

    Returns:
        tuple: (tasks list, agents list)
    """

    # Instantiate all four agents
    research_agent = create_research_agent()
    reader_agent   = create_reader_agent()
    analysis_agent = create_analysis_agent()
    summary_agent  = create_summary_agent()

    # ── Task 1: Search ArXiv ──────────────────────────────────
    research_task = Task(
        description=(
            f"Search ArXiv for peer-reviewed papers on:\n\n'{research_question}'\n\n"
            f"Use the ArXiv search tool with 2 different queries to find "
            f"at least 4 relevant papers. For each paper record: title, "
            f"authors, publication date, URL, and abstract. "
            f"Keep your final answer concise — list the papers only."
        ),
        expected_output=(
            "A numbered list of 4 medical research papers, each with: "
            "title, authors, publication date, ArXiv URL, and abstract. "
            "No extra commentary."
        ),
        agent=research_agent,
        callback=sleep_callback,        # Wait after this task finishes
    )

    # ── Task 2: Extract key info ──────────────────────────────
    reading_task = Task(
        description=(
            f"Read the papers about '{research_question}' and extract "
            f"for each paper ONLY: study design, key findings, and "
            f"clinical implications. Be brief — 3-4 sentences per paper max."
        ),
        expected_output=(
            "A brief structured breakdown per paper with: "
            "Title, Study Design, Key Findings, Clinical Implications. "
            "Max 4 sentences per section."
        ),
        agent=reader_agent,
        context=[research_task],
        callback=sleep_callback,        # Wait after this task finishes
    )

    # ── Task 3: Compare findings ──────────────────────────────
    analysis_task = Task(
        description=(
            f"Compare the papers on '{research_question}'. "
            f"Write 2-3 sentences each on: "
            f"(1) consensus findings, (2) contradictions or gaps, "
            f"(3) overall evidence strength. Be concise."
        ),
        expected_output=(
            "A short comparative analysis with 3 sections: "
            "Consensus Findings, Contradictions & Gaps, Evidence Strength. "
            "2-3 sentences per section maximum."
        ),
        agent=analysis_agent,
        context=[reading_task],
        callback=sleep_callback,        # Wait after this task finishes
    )

    # ── Task 4: Write final report ────────────────────────────
    summary_task = Task(
        description=(
            f"Write a professional medical research report on:\n\n"
            f"'{research_question}'\n\n"
            f"Use this exact structure (keep each section concise):\n"
            f"1. EXECUTIVE SUMMARY\n"
            f"2. BACKGROUND\n"
            f"3. PAPERS REVIEWED\n"
            f"4. KEY FINDINGS PER PAPER\n"
            f"5. COMPARATIVE ANALYSIS\n"
            f"6. EVIDENCE STRENGTH\n"
            f"7. CLINICAL IMPLICATIONS\n"
            f"8. RESEARCH GAPS & FUTURE DIRECTIONS\n"
            f"9. CONCLUSION"
        ),
        expected_output=(
            "A complete medical research report with all 9 sections labelled. "
            "Written in clear professional prose for a clinical audience."
        ),
        agent=summary_agent,
        context=[research_task, reading_task, analysis_task],
    )

    agents = [research_agent, reader_agent, analysis_agent, summary_agent]
    tasks  = [research_task, reading_task, analysis_task, summary_task]

    return tasks, agents