from config import DB_FAISS_PATH, RAG_LLM_MODEL, GROQ_API_KEY, TOP_K
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from survey import summarize_responses, ask_survey
from langchain import hub
from langchain.schema import HumanMessage, SystemMessage

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

    ex: If the student in DATA SCIENCE major, core courses should be:
    

    DTSC 1301 - Data and Society A 
    DTSC 1302 - Data and Society B 
    DTSC 2301 - Modeling and Society A 
    DTSC 2302 - Modeling and Society B 
    DTSC 3601 - Predictive Analytics and Their Implications A 
    DTSC 3602 - Predictive Analytics and Their Implications B 

    Mathematics and Statistics Courses (15 credit hours)MATH 1120 - Calculus (3)
    or MATH 1241 - Calculus I (3)STAT 1220 - Elements of Statistics I (BUSN) (3)
    or STAT 1221 - Elements of Statistics I (3)
    or STAT 1222 - Introduction to Statistics (3)MATH 2164 - Matrices and Linear Algebra (3)STAT 2223 - Elements of Statistics II (3)STAT 3160 - Applied Multivariate Analysis (3)

    Computing Core Courses (16 credit hours)ITSC 1213 - Introduction to Computer Science II (4)ITSC 2175 - Logic and Algorithms (3)
    or MATH 1165 - Introduction to Discrete Structures (3)ITSC 2214 - Data Structures and Algorithms (4)ITCS 3162 - Introduction to Data Mining (3)ITSC 3160 - Database Design and Implementation (3)
    
    Capstone Courses (6 credit hours)DTSC 4301 - Data Science for Social Good A (3)DTSC 4302 - Data Science for Social Good B (3)

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
    retriever = db.as_retriever(search_kwargs={"k": TOP_K})
    docs = retriever.invoke(summary)
    catalog_text = "\n".join([d.page_content for d in docs])
    #docs = retriever.get_relevant_documents(summary)

    # 3. Initialize LLM

    llm = ChatGroq(model=RAG_LLM_MODEL, temperature=0.4, api_key=GROQ_API_KEY)

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
