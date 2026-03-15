# =============================================================
# agents.py — Four collaborative AI agents
# Compatible with crewai 1.x
# =============================================================

import os
import time
from crewai import Agent, LLM
from tools import arxiv_search_tool


def build_llm() -> LLM:
    """
    Initialise the Groq LLM.
    Using llama-3.1-8b-instant — fast, lightweight model with
    higher rate limits than the 70b model on Groq's free tier.
    """
    return LLM(
        model="groq/llama-3.1-8b-instant",   # Higher TPM limit on free tier
        temperature=0.3,
        max_tokens=1024,                       # Keep responses concise to save tokens
        api_key=os.getenv("GROQ_API_KEY"),
    )


# Shared LLM instance used by all agents
llm = build_llm()


def create_research_agent() -> Agent:
    """Searches ArXiv for relevant medical research papers."""
    return Agent(
        role="Medical Research Specialist",
        goal=(
            "Search ArXiv for the most relevant peer-reviewed papers on the "
            "given medical topic. Find at least 4 papers with titles, authors, "
            "dates, and abstracts."
        ),
        backstory=(
            "You are a medical librarian with 20 years of experience sourcing "
            "scientific literature. You craft precise search queries and only "
            "return credible, peer-reviewed sources."
        ),
        tools=[arxiv_search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,                            
    )


def create_reader_agent() -> Agent:
    """Reads papers and extracts structured key information."""
    return Agent(
        role="Medical Literature Analyst",
        goal=(
            "Read each paper and extract: study design, core hypothesis, "
            "methodology, key findings, limitations, and clinical implications. "
            "Be concise and structured."
        ),
        backstory=(
            "You are a clinical research analyst with a PhD in biomedical "
            "sciences. You distil dense academic papers into clear insights "
            "and always note study design and methodological weaknesses."
        ),
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
    )


def create_analysis_agent() -> Agent:
    """Compares findings across papers, identifying consensus and gaps."""
    return Agent(
        role="Comparative Medical Research Analyst",
        goal=(
            "Compare papers and identify: consensus findings, contradictions, "
            "methodological differences, evidence strength, and research gaps. "
            "Be analytical and cite papers by title."
        ),
        backstory=(
            "You are a senior epidemiologist specialising in evidence synthesis. "
            "You spot patterns, understand heterogeneity, and assess evidence "
            "quality without overstating conclusions."
        ),
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
    )


def create_summary_agent() -> Agent:
    """Writes the final structured medical research report."""
    return Agent(
        role="Medical Research Report Writer",
        goal=(
            "Write a concise professional medical research report with all 9 "
            "sections: Executive Summary, Background, Papers Reviewed, Key "
            "Findings, Comparative Analysis, Evidence Strength, Clinical "
            "Implications, Research Gaps, and Conclusion."
        ),
        backstory=(
            "You are a medical science communicator who authors research briefs "
            "for clinicians and policymakers. You write clear, professional prose "
            "with practical evidence-based takeaways."
        ),
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
    )