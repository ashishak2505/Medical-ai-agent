import arxiv
from crewai.tools import tool


@tool("ArXiv Medical Research Search")
def arxiv_search_tool(query: str) -> str:
    """
    Searches ArXiv for peer-reviewed medical research papers.
    Input should be a specific medical research query string.
    Returns paper titles, authors, abstracts, and links.
    """
    try:
        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance,
        )

        results = []
        for i, paper in enumerate(search.results(), start=1):
            # Truncate abstract to keep context manageable
            abstract = paper.summary[:600].replace("\n", " ")
            if len(paper.summary) > 600:
                abstract += "..."

            paper_info = (
                f"--- Paper {i} ---\n"
                f"Title    : {paper.title}\n"
                f"Authors  : {', '.join(a.name for a in paper.authors[:4])}\n"
                f"Published: {paper.published.strftime('%Y-%m-%d')}\n"
                f"URL      : {paper.entry_id}\n"
                f"Abstract : {abstract}\n"
            )
            results.append(paper_info)

        if not results:
            return "No papers found. Try a broader search term."

        return f"Found {len(results)} papers on '{query}':\n\n" + "\n".join(results)

    except Exception as e:
        return f"Error searching ArXiv: {str(e)}. Please try a different query."