import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew, Process
from tasks import create_tasks

# Load environment variables from .env
load_dotenv()

# Validate Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
    print("\n[ERROR] GROQ_API_KEY is not set in your .env file.")
    print("  1. Open the .env file")
    print("  2. Replace 'your_groq_api_key_here' with your actual key")
    print("  3. Get a free key at https://console.groq.com\n")
    sys.exit(1)

os.environ["GROQ_API_KEY"] = GROQ_API_KEY


def get_research_question() -> str:
    print("\n" + "=" * 60)
    print("   Multi-Agent Medical Research Assistant")
    print("   Powered by CrewAI 1.x + Groq (llama3-8b-8192) + ArXiv")
    print("=" * 60)
    print("\nAgents: Research → Read → Analyse → Report\n")

    question = input("Enter your medical research question:\n> ").strip()

    if not question:
        question = "What are the latest findings on mRNA vaccines and long-term immune response?"
        print(f"\n[Demo question used]\n> {question}")

    return question


def save_report(report: str, question: str) -> str:
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c if c.isalnum() or c == " " else "_" for c in question[:40])
    safe_name = safe_name.strip().replace(" ", "_")
    filename  = f"reports/{safe_name}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"MEDICAL RESEARCH REPORT\n{'=' * 60}\n")
        f.write(f"Question  : {question}\n")
        f.write(f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'=' * 60}\n\n")
        f.write(str(report))

    return filename


def run():
    question = get_research_question()

    print(f"\n[INFO] Starting research: '{question}'")
    print("[INFO] This may take 1-3 minutes...\n")

    tasks, agents = create_tasks(question)

    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    print("=" * 60)
    print(" CREW STARTING — Sequential Agent Pipeline")
    print("=" * 60 + "\n")

    result = crew.kickoff()

    print("\n" + "=" * 60)
    print(" FINAL MEDICAL RESEARCH REPORT")
    print("=" * 60 + "\n")
    print(result)

    output_path = save_report(str(result), question)
    print(f"\n[INFO] Report saved to: {output_path}")
    print("[INFO] Done!\n")


if __name__ == "__main__":
    run()