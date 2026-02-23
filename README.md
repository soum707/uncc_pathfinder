Project: UNCC Pathfinder — Terminal RAG Workflow

Overview
- This project is a terminal-based RAG (retrieval-augmented generation) pipeline that helps create academic-advisor-style recommendations for incoming students. It retrieves course catalog text from a FAISS vectorstore built from PDFs, summarizes a student's survey responses, and generates course/elective/career suggestions via a Groq-backed LLM.
- There is no web UI yet — everything runs from the terminal.

Quick start (local)
- Activate your environment (Conda or venv). Example (Conda base shown when active):

  ```powershell
  conda activate my-env  # or .\venv\Scripts\Activate.ps1
  python -m pip install -r requirements2.txt
  ```

- Build the vectorstore (put syllabus PDFs under `data/` or change the loader path):

  ```powershell
  python build_vectorstore.py
  ```

- Run the RAG pipeline (terminal survey + generation):

  ```powershell
  python rag_pipeline.py
  ```

Configuration and secrets
- See `config.py` for constants: `DB_FAISS_PATH`, `SURVEY_LLM_MODEL`, `RAG_LLM_MODEL`, `TOP_K`.
- API keys: set `GROQ_API_KEY` and optionally `OPENAI_API_KEY` in a `.env` file (project uses `python-dotenv`).

Important files and roles
- `rag_pipeline.py`: main RAG flow. Key function: `run_rag(summary)`.
  - `ADVISOR_PROMPT`: the System-level prompt that controls recommendation format and behavior.
  - Uses `HuggingFaceEmbeddings`, FAISS for retrieval, and `ChatGroq` for generation.
- `survey.py`: terminal survey UI and summarization helpers.
  - `SURVEY`: list of survey questions and options.
  - `ask_survey()`: prompts the user and returns `answers` dict.
  - `summarize_responses(answers)`: calls the survey LLM to create a short profile.
- `build_vectorstore.py`: loads PDFs, chunks them, generates embeddings, and saves a FAISS index to `vectorstore/db_faiss`.
- `config.py`: environment-driven configuration and default model names.
- `requirements2.txt` / `requirements.txt`: dependency lists. Use `python -m pip install -r requirements2.txt`.

How the pipeline works (high level)
1. Survey: `ask_survey()` collects user responses in the terminal.
2. Summarize: `summarize_responses()` uses an LLM to produce a short student profile.
3. Retrieve: `run_rag()` loads FAISS (`vectorstore/db_faiss`) and retrieves top `k` chunks for the student's major/query.
4. Generate: the `ChatGroq` model is called with `ADVISOR_PROMPT` + retrieved catalog text + student summary to produce the final output.
5. Print: the response is printed to stdout.

Sample survey questions (from `survey.py`)
- What is your intended or declared major?
- Which of these most motivates you to study data and computation?
- Which daily activity sounds most like work you would enjoy?
- Which best describes your current comfort level?
- Which tools or technologies would you most like to learn?
- How do you respond to ill-defined problems?
- When thinking about data science in society, which excites you most?
- Which types of real-world problems most excite you to tackle with data?
- Where do you imagine applying your data skills?

Example output (format enforced by `ADVISOR_PROMPT`)
### Core Courses
- DTSC 1110 - Sports Analytics (School of Data Science) — Introduction to data science and analytics in the context of sports.
- DTSC 1301 - Data and Society A (School of Data Science) — Exploration of data science approaches to socially relevant challenges.
- DTSC 1302 - Data and Society B (School of Data Science) — Continuation of data science approaches to socially relevant challenges, focusing on ethical implications and data analysis.
- DTSC 2301 - Modeling and Society A (School of Data Science) — Application of statistical methods and query languages to explore data science approaches to social science disciplines.
- DTSC 2302 - Modeling and Society B (School of Data Science) — Further application of statistical methods and query languages, with a focus on ethical implications and data analysis.

### Recommended Electives
- **MINORS**: Consider a minor in Bioinformatics and Genomics, which could complement Data Science skills, especially in the context of healthcare.
- STAT 1220 - Elements of Statistics (Department of Statistics) — Introduction to statistical concepts and their practical applications, which is crucial for data science.
- STAT 2122 - Introduction to Probability and Statistics (Department of Statistics) — Further exploration of probability and statistics, essential for data modeling and analysis.

### Potential Career Paths
- **Data Scientist in Healthcare** — Applying data science techniques to improve health outcomes, using skills learned from the Data Science major and complemented by electives in bioinformatics and statistics.
- **Climate Data Analyst** — Working with data related to climate change, using skills in data analysis, machine learning, and statistical modeling to inform policy and decision-making.

Prompting notes & immediate improvements
- Make the `ADVISOR_PROMPT` more explicit: require numbered lists, ask the model to cite the source document ID or page for each course recommendation, and add a strict token or length limit to avoid long, unfocused outputs.
- Add a fallback behavior if retrieved catalog text is sparse (e.g., return "catalog lacks details" instead of hallucinating).
- Consider returning structured JSON in addition to human-readable text (easier to parse and test).
- Keep `TOP_K` conservative (5–10) during development to reduce noise.

Where to change behavior
- To tweak recommendations or format: edit `ADVISOR_PROMPT` in `rag_pipeline.py`.
- To change survey questions: edit the `SURVEY` list in `survey.py`.
- To use a different embedding model or chunking behavior: edit `build_vectorstore.py`.

Next steps for a new teammate
- Verify interpreter and env: `python --version`, `where python`, `python -m pip --version`.
- Install dependencies and test imports: `python -m pip install -r requirements2.txt` and `python -c "import langchain_groq; print('ok')"`.
- Build the vectorstore with your own PDFs (or use the one under `vectorstore/`) then run `python rag_pipeline.py`.
- If you want to iterate on prompts, edit `ADVISOR_PROMPT` and run short test cases.

Contact & context
- Created by the UNCC Pathfinder team. Ask the original author for dataset specifics if unsure which PDFs are canonical for a particular major.
