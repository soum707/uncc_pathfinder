from config import DB_FAISS_PATH, RAG_LLM_MODEL, GROQ_API_KEY, TOP_K, OPENAI_API_KEY
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq   import ChatGroq
# from langchain.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
# from langchain.prompts import ChatPromptTemplate
from survey import summarize_responses, ask_survey
# from langchainhub import LangChainHub
from langchain_core.messages import HumanMessage, SystemMessage

ADVISOR_PROMPT = """You are an Academic Advisor AI helping incoming college students decide suitable coursework and career paths.

    You are provided with:
    1. The student’s summarized survey profile (interests, motivations, and comfort levels).
    2. Retrieved information from the university’s course catalog.

    Your goals are:
    - Identify all **core courses** that align with the student’s intended MAJOR only! Be specific with the course names and numbers.
    - Each core course should have a description focused on SPECIFIC purpose or skill outcome.
    - Suggest **elective courses** from college departments' minors or majors according to their interest tags or domain areas. Specify the name of the minor/ major if applicable.
    - Make sure electives complement their major, goals, interest and personality.
    - Describe 5 **career opportunities** that match their survey profile and skills.

    Follow this format exactly:

    ### Student Summary
    <Brief restatement of key preferences>

    ### Core Courses
    - Course Name (department)— Short description
    - Course Name (department) - ...
    - Course Name  (department)- ... 

    ### Recommended Electives
    - MINORS
    - Course Name (department) — Short description
    - Course Name (department) - ...
    - ANY SUGGESTED DOUBLE MAJOR - Description

    ### Potential Career Paths
    - Career Title — How this program prepares them

    Keep the tone supportive and specific for first-year or incoming undergraduates.
    Only rely on the retrieved catalog text and the survey summary.
    
    If the catalog text does not contain relevant information, say "The catalog does not provide sufficient information to make specific course recommendations."""

def run_rag(summary):

    # 1. Load vector DB
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

    # 2. Retrieve relevant documents
    # Determine the major from the summary
    if "Data Science" in summary:
        major = "Data Science"
    elif "Sports Analytics" in summary:
        major = "Sports Analytics"
    else:
        major = "Data Science"  # default fallback
    
    query = f"{major} major core courses, electives, minors, double majors, and career paths: {summary}"
    retriever = db.as_retriever(search_kwargs={"k": TOP_K})
    docs = retriever.invoke(query)
    catalog_text = "\n".join([d.page_content for d in docs])
    print("Retrieved catalog text:")
    print(catalog_text[:2000])  # Print first 2000 chars to see
    print("---")
    #docs = retriever.get_relevant_documents(summary)

    # 3. Initialize LLM

    llm = ChatGroq(model=RAG_LLM_MODEL, temperature=0.4, api_key=GROQ_API_KEY)
    # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=OPENAI_API_KEY)

    # 4. Wrap messages
    messages = [
        SystemMessage(content=ADVISOR_PROMPT),
        HumanMessage(content=f"### Student Summary\n{summary}\n\n### Retrieved Catalog\n{catalog_text}")
    ]
    # 5. Use invoke() on LLM
    try:
        print("Calling LLM...")
        response = llm.invoke(messages)
        print("LLM response received:")
        print(response.content)
    except Exception as e:
        print(f"Error in run_rag: {e}")
        import traceback
        traceback.print_exc()

    # chain = template | llm
    # response = chain.invoke({"summary": summary, "catalog_text": catalog_text})
    # print(response.content)

if __name__ == "__main__":
    answers = ask_survey()
    summary = summarize_responses(answers)
    run_rag(summary)
