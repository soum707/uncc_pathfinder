from config import SURVEY_LLM_MODEL, GROQ_API_KEY
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langchain import hub

SURVEY = [
    {
        "question": "What is your intended or declared major?",
        "options": ["Data Science", "Sports Analytics"],
        "multi": False

    },
    {
        "question": "Which of these most motivates you to study data and computation?",
        "options": [
            "Producing insights and reports for decision-making. ",
            "Designing, training, and explaining predictive models. ",
            "Building robust systems that move and store data.",
            "Conducting research into methods or theories.",
            "Applying data methods to domain problems."
        ],
        "multi": True
    },
    {
        "question": "Which daily activity sounds most like work you would enjoy? (Select one)",
        "options": [
            "Preparing dashboards, communicating results to stakeholders, and iterative analysis.",
            "Writing and debugging production code for models or backend services.",
            "Designing ETL(Extracting, Transforming, and Loading data) pipelines, optimizing databases, and testing scalability. ",
            "Designing experiments, statistical analysis, and interpreting uncertainty. ",
            "Reading literature, forming hypotheses, and writing technical papers or policy briefs."
        ],
        "multi": False
    },
    {
        "question": "Which best describes your current comfort level? (Select one)",
        "options": [
            "Comfortable with statistics, hypothesis testing, and basic regression.",
            "Comfortable coding (Python/Java/C++) and building software.",
            "Comfortable with databases, SQL, and data modeling. ",
            "Comfortable with visualization tools and storytelling with data.",
            "New to these topics; eager to learn."
        ],
        "multi": True
    },
    
    {
        "question": "Which tools or technologies would you most like to learn? (Select up to 2)",
        "options": [
            "SQL, relational databases, data modeling. ",
            "Python, R and statistical/machine-learning libraries.",
            "Big data and distributed systems (Spark, cloud). ",
            "Visualization / dashboards (Tableau, D3, ggplot). ",
            "Formal methods / advanced math (probability, optimization).",
            "Product analytics and business tools (A/B, Mixpanel, Excel)."
        ],
        "multi": True
    },
    
    {
        "question": "How do you respond to ill-defined problems?",
        "options": [
            "Prefer well-specified tasks with clear success metrics. ",
            "Comfortable defining the problem and iterating through experiments.",
            "Comfortable building prototypes and improving them until production-ready.",
            "Prefer open research questions and hypothesis-driven work."
        ],
        "multi": False
    },
    
    {
        "question": "When thinking about data science in society, which excites you most? (Select one)",
        "options": [
            "Making businesses more efficient and profitable.",
            "Improving health outcomes and saving lives.",
            "Tackling climate change and sustainability.",
            "Ensuring fairness, equity, and responsible AI.",
            "Advancing knowledge through science and discovery."
        ],
        "multi": True
    },
    
    {
        "question": "Which types of real-world problems most excite you to tackle with data?",
        "options": [
            "Predicting the stock market, reducing financial risk, or business growth.",
            "Understanding diseases, genes, or healthcare systems.",
            "Studying human behavior, psychology, or social systems.",
            "Building ethical, fair, and responsible AI systems.",
            "Developing next-gen technology (AI, robotics, computer vision)."
        ],
        "multi": True
    },
    {
        "question": "Where do you imagine applying your data skills? (Select one)",
        "options": [
            "Finance, banking, or corporate business.",
            "Hospitals, public health agencies, or biotech labs.",
            "Startups or tech companies building apps and tools.",
            "Universities or research centers.",
            "Government, NGOs, or policy think tanks"
        ],
        "multi": False
    }

]

def ask_survey():
    print("\n=== Student Academic Survey ===\n")
    answers = {}

    for i, item in enumerate(SURVEY, 1):
        print(f"Q{i}. {item['question']}")

        if item.get("free_text", False):
            ans = input("Your answer (optional, press Enter to skip): ").strip()
            answers[item['question']] = ans if ans else "No response"
            print()
            continue

        for j, opt in enumerate(item["options"], 1):
            print(f"   {j}. {opt}")

        if item.get("multi", False):
            choice = input("Enter your choices (comma-separated, e.g. 1,3): ").strip()
            indices = [int(x)-1 for x in choice.split(',') if x.strip().isdigit()]
            selected = [item["options"][idx] for idx in indices if 0 <= idx < len(item["options"])]
            answers[item['question']] = selected if selected else ["No response"]
        else:
            choice = input("Enter your choice (e.g. 1): ").strip()
            try:
                idx = int(choice) - 1
                answers[item['question']] = item["options"][idx]
            except (ValueError, IndexError):
                print("Invalid input, skipping.")
                answers[item['question']] = "No response"

        print()

    return answers



def summarize_responses(answers):
    llm = ChatGroq(
        model=SURVEY_LLM_MODEL,
        temperature=0.3,
        max_tokens=512,
        api_key=GROQ_API_KEY,
    )

    profile_text = "\n".join([
        f"{q}: {', '.join(a) if isinstance(a, list) else a}" 
        for q, a in answers.items()
    ])
    prompt = f"""
    You are an academic advisor summarizing a new student's academic preferences.
    Below are their survey responses. Extract key insights concisely:
    - Their academic focus
    - Preferred working style or motivation
    - Technical comfort
    - Domain interests
    - Career direction
    Include relevant [TAGS] mentioned (e.g., DS, ENG, RS, FIN).
    Return a 5–6 sentence paragraph profile.

    Survey Responses:
    {profile_text}
    """

    # Wrap the prompt in a HumanMessage for LangChain
    messages = [[HumanMessage(content=prompt)]]
    result = llm.generate(messages)

    # The text is inside result.generations[0][0].text
    summary = result.generations[0][0].text
    return summary
  

if __name__ == "__main__":
    answers = ask_survey()
    summary = summarize_responses(answers)
    print("\n--- Summary ---\n")
    print(summary)
