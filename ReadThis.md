## AI Video Generation Pipeline (LangGraph + Remotion)

This project is an autonomous multi-agent system orchestrated using LangGraph. It is designed to take a user's text prompt and a batch of event photos and dynamically generate a fully runnable React-based Remotion video script.

### 🚀 Key Architectural Features & Differentiators

* 
**Self-Healing Compiler Loop:** Before rendering, a Compiler & Fixer node tests the generated React script for syntax errors. If an error is caught, the agent fetches the exact Remotion API documentation needed via RAG, packages the error context, and loops back to rewrite its own code dynamically.


* 
**Multi-Model Cost/Quality Routing:** The graph optimizes production economics by routing simple narrative structuring to a fast, cost-effective model (Llama 3.1 8B), while reserving the heavy-duty code generation for a massive 70B model (Llama 3.3 70B).


* 
**Zero Free-Text Parsing:** Every single step of the pipeline uses strict Pydantic schemas to enforce structured JSON outputs, eliminating reliance on messy string parsing.


* 
**LLM-as-Judge Evaluation:** The testing suite includes a programmatic AI judge to evaluate the narrative coherence of the generated storyboards offline.



---

### ⚙️ Prerequisites

Before you begin, ensure you have the following installed:

* 
**Python 3.11+**: Required for full compatibility with Pydantic and LangGraph dependencies.


* 
**Node.js**: Required to compile and run the final Remotion video dependencies.



---

### 🛠️ Setup Instructions

**1. Clone and Configure the Python Environment**

* Create a virtual environment and install the required packages:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

```



*Note: The `requirements.txt` includes strictly pinned versions to guarantee stability*.



**2. Configure Environment Variables**

* Copy the `.env.example` file to create a new `.env` file.


* Ensure your `.env` contains your Groq API key:


```env
GROQ_API_KEY=gsk_your_api_key_here

```



**3. Provide Image Inputs**

* Because this is a local command-line application, drop your batch of event photos (8-12 images) into the designated `/images` or `/data` folder in the project root. The Vision LLM will automatically analyze these files.



---

### 💻 Running the Pipeline

To execute the autonomous agent loop, run the orchestrator script from your terminal:

```bash
python -m src.graph

```

* The application will prompt you in real-time to enter your text prompt (e.g., *"Create a fast-paced, highly energetic promotional video using these 10 photos."*).


* You will be able to watch the terminal output as the agents sequence the narrative, generate code, and actively debug their own syntax errors in real-time.



---

### 🧪 Offline Evaluation & Mock Testing

This repository includes a robust, production-grade test suite that can run without active API keys.
To run the evaluation suite:

```bash
pytest tests/ -v -s

```

* This triggers the mocked LLM calls and evaluates the `LLM-as-Judge` storyboard narrative testing.



---

### ⚠️ Known Limitations

* 
**Strict Output Formats:** Small LLMs occasionally hallucinate keys outside of the strict Pydantic schema constraints. The pipeline mitigates this through LangChain's `.with_structured_output()`, but edge-case prompt injections can still break the parser.


* 
**Rate Limiting:** Free-tier Groq API keys may occasionally hit Tokens-Per-Minute (TPM) limits during the self-healing retry loop if the error context is exceptionally large.
