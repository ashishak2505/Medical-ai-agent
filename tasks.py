from crewai import Task
from agents import (
    create_research_agent,
    create_reader_agent,
    create_analysis_agent,
    create_summary_agent,
)


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

    # ── Task 1: Search ArXiv for papers ──────────────────────
    research_task = Task(
        description=(
            f"Search ArXiv for peer-reviewed papers on:\n\n'{research_question}'\n\n"
            f"Use the ArXiv search tool with 2-3 different queries to find "
            f"at least 4 relevant papers. For each paper record: title, "
            f"authors, publication date, URL, and full abstract."
        ),
        expected_output=(
            "A numbered list of at least 4 medical research papers, each with: "
            "title, authors, publication date, ArXiv URL, and abstract."
        ),
        agent=research_agent,
    )

    # ── Task 2: Extract key info from each paper ──────────────
    reading_task = Task(
        description=(
            f"Read the papers about '{research_question}' and extract "
            f"for each: study design, core hypothesis, methodology, "
            f"key findings, limitations, and clinical implications."
        ),
        expected_output=(
            "A structured breakdown per paper with sections: Title, Study Design, "
            "Hypothesis, Methodology, Key Findings, Limitations, Clinical Implications."
        ),
        agent=reader_agent,
        context=[research_task],
    )

    # ── Task 3: Compare findings across papers ────────────────
    analysis_task = Task(
        description=(
            f"Compare the papers on '{research_question}'. Cover: "
            f"(1) consensus findings, (2) contradictions, "
            f"(3) methodological differences, (4) evidence strength, "
            f"(5) research gaps, (6) most important finding overall."
        ),
        expected_output=(
            "A comparative analysis with sections: Consensus Findings, "
            "Contradictions, Methodological Comparison, Evidence Strength, "
            "Research Gaps, and Most Significant Finding."
        ),
        agent=analysis_agent,
        context=[reading_task],
    )

    # ── Task 4: Write the final report ───────────────────────
    summary_task = Task(
        description=(
            f"Write a complete professional medical research report on:\n\n"
            f"'{research_question}'\n\n"
            f"Use this exact structure:\n"
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
            "A complete professionally formatted medical research report "
            "with all 9 sections clearly labelled. Minimum 600 words. "
            "Written in clear professional prose suitable for a clinical audience."
        ),
        agent=summary_agent,
        context=[research_task, reading_task, analysis_task],
    )

    agents = [research_agent, reader_agent, analysis_agent, summary_agent]
    tasks  = [research_task, reading_task, analysis_task, summary_task]

    return tasks, agents