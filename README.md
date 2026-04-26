# 🎯 SkillProbe — AI-Powered Skill Assessment & Personalised Learning Plan Agent

<div align="center">

![SkillProbe Banner](https://img.shields.io/badge/SkillProbe-AI%20Skill%20Assessment-6366F1?style=for-the-badge&logo=target&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)

**A resume tells you what someone claims to know. SkillProbe verifies what they actually know.**

[🚀 Live Demo](https://skillprobe-yug.streamlit.app/) • [📹 Demo Video](https://drive.google.com/drive/folders/1gLH3-8Pv6NugBE_M7-kOR-OSclcOR78z?usp=drive_link) • [📁 Source Code]((https://github.com/yug03/skillprobe.git))

</div>

---

## 📌 Table of Contents

- [What Is SkillProbe](#what-is-skillprobe)
- [The Problem It Solves](#the-problem-it-solves)
- [Live Demo](#live-demo)
- [Demo Video](#demo-video)
- [How It Works](#how-it-works)
- [Architecture Diagram](#architecture-diagram)
- [Scoring Logic](#scoring-logic--methodology)
- [Adjacent Skill Reasoning](#adjacent-skill-reasoning)
- [Tech Stack](#tech-stack)
- [Local Setup Instructions](#local-setup-instructions)
- [Sample Inputs](#sample-inputs)
- [Sample Outputs](#sample-outputs)
- [Project Structure](#project-structure)
- [Agent Design](#agent-design--why-this-is-a-real-agent)
- [Trade-offs & Decisions](#trade-offs--decisions)
- [Future Improvements](#future-improvements)

---

## What Is SkillProbe

SkillProbe is a **candidate-facing AI skill verification and learning plan agent**.

A candidate finds a job they want. They paste the Job Description and their Resume.
SkillProbe does not trust the resume. Instead, it **actively tests** each required
skill through an adaptive conversation, determines real proficiency levels, identifies
genuine gaps against the job requirements, and generates a **personalised, phased
learning plan** to make the candidate hire-ready.

This is not a chatbot. This is not a resume screener. This is not a course recommender.

It is an **adaptive skill verification engine** — the tool every serious job seeker
should use before applying.

---

## The Problem It Solves
Resume says: "Proficient in Docker, FastAPI, LangChain, RAG systems"

Reality:
Docker → Used it once to containerise a hello-world app
FastAPI → Has only used Flask, never FastAPI
LangChain → Followed a YouTube tutorial once
RAG systems → Knows the acronym, built nothing real

The hiring manager finds out in the technical interview.
The candidate wasted everyone's time.

text

SkillProbe closes this gap **before the interview**.

It gives the candidate:
- An honest picture of where they actually stand
- Evidence-based proficiency scores with explanations
- A realistic, personalised plan to close the gaps
- Estimated time to become genuinely hire-ready

---

## Live Demo

**Deployed URL:** [https://YOUR-APP-NAME.streamlit.app](https://YOUR-APP-NAME.streamlit.app)

To test immediately:
1. Open the URL above
2. Click **"Load Sample Inputs (Demo)"**
3. Click **"Analyze My Readiness →"**
4. Answer the assessment questions
5. View results and download your PDF report

> No account required. No data stored. Your inputs stay in your session only.

---

## Demo Video

**Video Link:** [https://YOUR-VIDEO-URL-HERE](https://YOUR-VIDEO-URL-HERE)

**What the video covers (3-4 minutes):**
- Uploading a real AI Automation Engineer JD and candidate resume
- Watching the system parse and map 12 required skills
- Live adaptive assessment — difficulty changing based on answers
- Results dashboard with radar chart and gap analysis
- Personalised learning plan with adjacent skill reasoning
- PDF report download

---

## How It Works
## How It Works

┌──────────────────────────────────────────────────────────────┐
│                        USER FLOW                             │
│                                                              │
│  STEP 1        STEP 2              STEP 3                    │
│ ┌─────────┐   ┌─────────┐   ┌──────────────────────────┐     │
│ │ Paste   │ → │ Parse   │ → │ Adaptive Conversational  │     │
│ │ JD +    │   │ & Map   │   │ Assessment               │     │
│ │ Resume  │   │         │   │                          │     │
│ └─────────┘   └─────────┘   └──────────┬───────────────┘     │
│                                        │                     │
│                          STEP 4        │        STEP 5       │
│                   ┌──────────────┐     │    ┌──────────────┐  │
│                   │ Results      │ ◀────┘    Personalised │  │
│                   │ Dashboard    │          │ Learning Plan│  │
│                   │ + Gap Score  │ ─────────▶              │ │
│                   └──────────────┘          └──────┬───────┘ │
│                                                    │         │
│                                                    ▼         │
│                                      📄 PDF Report Download  │
└──────────────────────────────────────────────────────────────┘

text

### Step 1 — Input
User pastes or uploads a Job Description and their Resume.
Supports PDF, DOCX, and TXT file formats or plain text paste.

### Step 2 — Parse and Map
A single LLM call extracts:
- Required skills from JD with importance levels (critical / important / nice-to-have)
- Claimed skills from resume with evidence-based proficiency estimates
- Skill overlap, missing skills, and extra skills
- Prioritised assessment queue (critical skills first, max 5 skills)

### Step 3 — Adaptive Assessment
The agent runs a **Computerised Adaptive Testing (CAT)** inspired assessment:
- One skill at a time, in priority order
- Starts at a difficulty level based on claimed proficiency
- Adapts difficulty up or down after every answer
- Stops when confidence threshold is reached or max questions hit
- Decides everything autonomously — what to ask, when to stop, when to move on

### Step 4 — Results Dashboard
- Overall job readiness score with hire-ready weeks estimate
- Radar chart: required vs claimed vs assessed proficiency
- Gap analysis chart per skill
- Claim accuracy analysis (where resume was accurate, overstated, or understated)
- Per-skill breakdown with evidence and observations

### Step 5 — Personalised Learning Plan
- 3 phases: Quick Wins, Core Gaps, Advanced
- Adjacent skill reasoning for every skill in the plan
- Milestones, hands-on projects, time estimates
- Real resource links via DuckDuckGo search (no hallucinated URLs)
- Downloadable PDF report

---

## Architecture Diagram
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  SKILLPROBE AGENT SYSTEM                                    │
└──────────────────────────────────────────────────────────────────────────────────────────────┘

  INPUT LAYER
  ┌───────────────────────────────┐              ┌───────────────────────────────┐
  │ Job Description               │              │ Resume                        │
  │ (text / file upload)          │              │ (text / file upload)          │
  └───────────────┬───────────────┘              └───────────────┬───────────────┘
                  └──────────────────────────┬───────────────────┘
                                             ▼
  ┌──────────────────────────────────────────────────────────────────────────────────────────┐
  │ PARSER AGENT                                                                             │
  │ ---------------------------------------------------------------------------------------- │
  │ Single LLM-driven parsing flow that extracts:                                            │
  │ • JD structure and required skills                                                       │
  │ • Resume profile and claimed skills                                                      │
  │ • Required vs claimed skill map                                                          │
  │ • Prioritised assessment queue                                                           │
  │                                                                                          │
  │ Outputs: jd_parsed, resume_parsed, skill_map, assessment_queue                           │
  └──────────────────────────────────────────────┬───────────────────────────────────────────┘
                                                 ▼

  ┌──────────────────────────────────────────────────────────────────────────────────────────┐
  │ ADAPTIVE ASSESSMENT ENGINE (CAT)                                                         │
  │ ---------------------------------------------------------------------------------------- │
  │ Core agentic loop that verifies skill proficiency one skill at a time.                   │
  │                                                                                          │
  │  Per-skill state: SkillState                                                             │
  │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
  │  │ • Claimed proficiency → starting difficulty                                        │  │
  │  │ • History of Q&A pairs with evaluation scores                                      │  │
  │  │ • Confidence tracking (consistency + evidence coverage)                            │  │
  │  │ • Difficulty ceiling used to cap final proficiency                                 │  │
  │  └────────────────────────────────────────────────────────────────────────────────────┘  │
  │                                                                                          │
  │  For each skill in queue:                                                                │
  │  ┌────────────────────────────────────────────────────────────────────────────────────┐  │
  │  │ 1. generate_question()  → adaptive question based on current difficulty            │  │
  │  │ 2. candidate answers                                                               │  │
  │  │ 3. evaluate()           → answer scored across quality dimensions                  │  │
  │  │ 4. record()             → update difficulty, confidence, and stop condition        │  │
  │  │ 5. If confidence < threshold and question count < max → ask next adaptive question │  │
  │  │ 6. Else stop skill assessment and compute final proficiency                        │  │
  │  └────────────────────────────────────────────────────────────────────────────────────┘  │
  │                                                                                          │
  │  Then move automatically to the next skill until queue completion.                       │
  └──────────────────────────────────────────────┬───────────────────────────────────────────┘
                                                 ▼

  ┌──────────────────────────────────────────────────────────────────────────────────────────┐
  │ GAP ANALYZER                                                                             │
  │ ---------------------------------------------------------------------------------------- │
  │ Computes evidence-based readiness and skill gaps.                                        │
  │                                                                                          │
  │ For each skill:                                                                          │
  │ • gap = required_proficiency - assessed_proficiency                                      │
  │ • claim_accuracy = claimed_proficiency - assessed_proficiency                            │
  │                                                                                          │
  │ Overall readiness:                                                                       │
  │ • readiness = 1 - weighted_average_gap                                                   │
  │ • weights: critical = 3, important = 2, nice_to_have = 1                                 │
  │                                                                                          │
  │ Outputs:                                                                                 │
  │ • readiness_score                                                                        │
  │ • hire_ready_weeks                                                                       │
  │ • strengths                                                                              │
  │ • critical_gaps                                                                          │
  │ • quick_wins                                                                             │
  └──────────────────────────────────────────────┬───────────────────────────────────────────┘
                                                 ▼

  ┌──────────────────────────────────────────────────────────────────────────────────────────┐
  │ LEARNING PLAN AGENT                                                                      │
  │ ---------------------------------------------------------------------------------------- │
  │ Builds a phased, personalised roadmap from verified gaps and adjacent strengths.         │
  │                                                                                          │
  │ Inputs:                                                                                  │
  │ • gap analysis                                                                           │
  │ • full candidate skill profile                                                           │
  │                                                                                          │
  │ Phases:                                                                                  │
  │ • Phase 1: Quick Wins                                                                    │
  │ • Phase 2: Core Gaps                                                                     │
  │ • Phase 3: Advanced Progression                                                          │
  │                                                                                          │
  │ Per skill plan includes:                                                                 │
  │ • Adjacent skill reasoning (leveraging what the candidate already knows)                 │
  │ • Estimated learning hours                                                               │
  │ • Milestones                                                                             │
  │ • Hands-on project                                                                       │
  │ • Real resource links via DuckDuckGo search                                              │
  └──────────────────────────────────────────────┬───────────────────────────────────────────┘
                                                 ▼

  OUTPUT LAYER
  ┌────────────────────────────────────┐                  ┌────────────────────────────────────┐
  │ Results UI                         │                  │ PDF Report                         │
  │ Streamlit + Plotly dashboard       │                  │ fpdf2-generated professional report│
  │ • Readiness                        │                  │ • Assessment summary               │
  │ • Skill breakdown                  │                  │ • Skill scores                     │
  │ • Gaps and strengths               │                  │ • Gap analysis                     │
  │ • Charts and plan                  │                  │ • Learning roadmap                 │
  └────────────────────────────────────┘                  └────────────────────────────────────┘


  SHARED INFRASTRUCTURE
  ┌────────────────────────────────────┐                  ┌────────────────────────────────────┐
  │ LLM CLIENT                         │                  │ SESSION STATE                      │
  │ • Primary: Gemini 2.0 Flash        │                  │ core/state.py                      │
  │ • Backup: Groq Llama 3.3 70B       │                  │ Single source of truth for:        │
  │ • Retry + fallback logic           │                  │ • current step                     │
  │                                    │                  │ • parsed docs                      │
  │                                    │                  │ • assessment engine                │
  │                                    │                  │ • conversation log                 │
  │                                    │                  │ • results and plan                 │
  └────────────────────────────────────┘                  └────────────────────────────────────┘

text

---

## Scoring Logic & Methodology

### Difficulty Levels

| Level | Label | What It Tests |
|-------|-------|---------------|
| 1 | Conceptual | Can the candidate define and explain the concept? |
| 2 | Practical | Can they implement it in real code or scenarios? |
| 3 | Scenario | Can they apply it to solve a novel problem? |
| 4 | Architecture | Can they reason about trade-offs and edge cases? |

### Starting Difficulty (Based on Resume Claim)
Claimed proficiency >= 70% → Start at Level 3
Claimed proficiency >= 40% → Start at Level 2
Claimed proficiency < 40% → Start at Level 1

text

This prevents wasting questions on basics for experienced candidates
and avoids overwhelming beginners.

### Adaptive Logic (After Every Answer)
Strong answer (score >= 0.80) → difficulty + 1 (probe ceiling)
Moderate answer (score >= 0.50) → difficulty stays (gather more signal)
Weak answer (score < 0.50) → difficulty - 1 (find floor)

text

### Stopping Logic
Minimum 2 questions always asked (cannot stop before this)
Stop early if confidence >= 75% after minimum questions
Always stop at 3 questions maximum (token efficiency)

text

### Confidence Calculation

```python
base_confidence  = min(questions_asked / max_questions, 0.70)
variance         = variance of answer scores
consistency      = max(0, 1 - variance * 4)
confidence       = base_confidence + consistency * 0.30
Consistent answers (all strong or all weak) → high confidence early.
Inconsistent answers (strong then weak) → needs more questions.

Final Proficiency per Skill
python
weighted_score     = Σ(answer_score × difficulty) / Σ(difficulty)
difficulty_ceiling = max_difficulty_reached / 4
final_proficiency  = min(weighted_score × difficulty_ceiling × 1.3, 1.0)
The difficulty ceiling is critical.
If a candidate only ever answered Level 1-2 questions successfully,
they cannot be rated as Advanced or Expert regardless of their scores.
They must demonstrate Level 3-4 depth to reach those ratings.

Answer Evaluation (5 Dimensions)
Each answer is scored by the LLM on:

Correctness — Is the information accurate?
Depth — Does it go beyond surface level?
Relevance — Does it address the question?
Completeness — Are key aspects covered?
Practical signal — Does it show real hands-on experience?
Score bands:

text
Strong:    0.80 - 1.00  (accurate, deep, shows experience)
Moderate:  0.50 - 0.79  (mostly correct, some gaps)
Weak:      0.10 - 0.49  (partial or surface only)
No answer: 0.00         (skipped or empty)
Overall Readiness Score
python
importance_weights  = {"critical": 3.0, "important": 2.0, "nice_to_have": 1.0}
weighted_gap        = Σ(skill_gap × importance_weight) / Σ(importance_weights)
readiness_score     = 1 - weighted_gap
Critical skills have 3x the impact on the readiness score.
A 30% gap in a critical skill hurts far more than a 30% gap in a nice-to-have.

Hire-Ready Estimate
text
Readiness >= 85%  →  1 week   (minor polish needed)
Readiness >= 70%  →  3 weeks  (moderate gaps)
Readiness >= 50%  →  6 weeks  (significant gaps)
Readiness >= 30%  →  10 weeks (major gaps)
Readiness <  30%  →  16 weeks (foundational work needed)
Claim Accuracy Labels
text
|claimed - assessed| <= 0.10  →  Accurate
claimed - assessed   >  0.20  →  Overstated
claimed - assessed   >  0.10  →  Slightly overstated
assessed - claimed   >  0.20  →  Stronger than claimed
assessed - claimed   >  0.10  →  Slightly understated
Adjacent Skill Reasoning
This is a core differentiator. The learning plan does not just say "learn Docker."

It says:

"Since you already know Flask and REST API design, FastAPI is a natural next step.
Your existing routing, request handling, and middleware knowledge transfers directly.
Estimated to take 40% less time than someone learning without that background —
approximately 12 hours vs 20 hours."

The system achieves this by passing the candidate's complete skill profile
to the learning plan agent with explicit instructions to identify which existing
skills serve as foundations for each gap skill, and to quantify the learning
acceleration this provides.

Example adjacent skill chains from sample output:

text
Flask + REST APIs → FastAPI           (1-2 weeks vs 3-4 weeks)
PostgreSQL + Pandas → Data Engineering (accelerated data pipeline work)
Docker basics → Kubernetes             (container concepts transfer)
OpenAI API → LangChain                (API patterns already known)
ChromaDB experience → Pinecone/Weaviate (vector DB concepts transfer)
Tech Stack
Component	Technology	Why
UI Framework	Streamlit	Fast to build, stable, sufficient for demo
Primary LLM	Gemini 2.0 Flash	Free tier, fast, strong reasoning
Backup LLM	Groq Llama 3.3 70B	Free tier, fast inference
Charts	Plotly	Interactive, dark-theme compatible
PDF Generation	fpdf2	Pure Python, no binary deps, works on cloud
PDF Parsing	pdfplumber	Reliable text extraction
DOCX Parsing	python-docx	Standard DOCX support
Resource Search	duckduckgo-search	Free, no API key, real links
Config	python-dotenv	Clean .env based config
Language	Python 3.11+	Modern type hints, performance
Deployment	Streamlit Cloud	Free tier, GitHub integration
Local Setup Instructions
Prerequisites
Python 3.11 or higher
A free Gemini API key → https://aistudio.google.com/app/apikey
A free Groq API key (optional backup) → https://console.groq.com
Step 1 — Clone the Repository
bash
git clone https://github.com/YOURUSERNAME/skillprobe.git
cd skillprobe
Step 2 — Create Virtual Environment
bash
# Mac / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
Step 3 — Install Dependencies
bash
pip install -r requirements.txt
Step 4 — Configure API Keys
Create a .env file in the root folder:

bash
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
LLM_PROVIDER=gemini
Never commit the .env file. It is in .gitignore.

Step 5 — Run the Application
bash
streamlit run app.py
The app opens at http://localhost:8501

Step 6 — Test with Sample Inputs
Open http://localhost:8501
Click "Load Sample Inputs (Demo)"
Click "Analyze My Readiness →"
Answer the assessment questions (or click Skip to move through quickly)
View results and download the PDF report
Sample Inputs
Sample Job Description (sample_inputs/sample_jd.txt)
text
AI Automation Engineer

We are building AI-powered automation systems and looking for an engineer 
who can design, build, and deploy intelligent pipelines.

Responsibilities:
- Design and build AI/ML pipelines and automation workflows
- Build and deploy REST APIs using Python (FastAPI preferred)
- Work with LLMs (GPT-4, Gemini, Claude) and prompt engineering
- Build RAG (Retrieval-Augmented Generation) systems
- Work with vector databases (Pinecone, ChromaDB, Weaviate)
- Containerise applications with Docker, deploy to AWS or GCP
- Set up CI/CD pipelines, monitoring, and observability

Requirements:
- 2+ years software engineering experience
- Strong Python skills
- FastAPI or Flask for API development
- Hands-on LLM API experience and prompt engineering
- Understanding of RAG architecture
- Docker and containerisation
- Cloud platforms: AWS or GCP
- SQL and database design
- Git, CI/CD workflows

Nice to Have:
- LangChain or LlamaIndex
- Kubernetes
- Terraform / Infrastructure as Code
Sample Resume (sample_inputs/sample_resume.txt)
text
Sarah Chen — Software Engineer | AI Enthusiast

SUMMARY
Software engineer with 3 years experience building backend systems.
Transitioning into AI engineering. Strong Python and REST API background.

EXPERIENCE
Software Engineer — DataFlow Inc (2021–Present)
- Built REST APIs using Flask (10K+ daily requests)
- Designed PostgreSQL schemas, optimised SQL queries
- Containerised apps using Docker for dev and staging
- Used AWS S3 and EC2 for deployments
- Integrated ML models built by data science team

PROJECTS
- AI Assistant: Built chatbot using OpenAI API + ChromaDB for RAG.
  Used LangChain for prompt chaining. Deployed on Streamlit Cloud.
- ETL Pipeline: Automated data pipeline processing 1M+ records/day.

SKILLS
Python, Flask, PostgreSQL, SQL, Docker, AWS (S3/EC2), Git,
REST APIs, Pandas, pytest, LangChain (basic), OpenAI API, 
ChromaDB (basic), Streamlit

EDUCATION
B.S. Computer Science — State University (2020)
Sample Outputs
Parsed Skill Map
text
Required Skills (from JD):
  Python          — critical   — required: 80%
  FastAPI         — critical   — required: 70%
  LLM/Prompt Eng  — critical   — required: 75%
  RAG Systems     — critical   — required: 70%
  Docker          — important  — required: 65%
  AWS/GCP         — important  — required: 60%
  SQL             — important  — required: 65%
  LangChain       — nice_to_have — required: 45%

Matched: 7 skills
Missing: 1 skill (Kubernetes)
Assessment Queue: [Python, FastAPI, LLM/Prompt Eng, RAG Systems, Docker]
Assessment Results (Sample)
text
┌─────────────────┬──────────┬─────────┬──────────┬──────┬───────────────────────┐
│ Skill           │ Required │ Claimed │ Assessed │ Gap  │ Claim Accuracy        │
├─────────────────┼──────────┼─────────┼──────────┼──────┼───────────────────────┤
│ Python          │ 80%      │ 72%     │ 70%      │ 10%  │ Accurate              │
│ FastAPI         │ 70%      │ 25%     │ 20%      │ 50%  │ Accurate              │
│ LLM/Prompt Eng  │ 75%      │ 45%     │ 58%      │ 17%  │ Stronger than claimed │
│ RAG Systems     │ 70%      │ 35%     │ 30%      │ 40%  │ Accurate              │
│ Docker          │ 65%      │ 52%     │ 48%      │ 17%  │ Slightly overstated   │
└─────────────────┴──────────┴─────────┴──────────┴──────┴───────────────────────┘

Overall Readiness Score: 61%
Hire-Ready Estimate:     6 weeks

Strengths:   Python
Critical Gaps: FastAPI, RAG Systems
Quick Wins:  Docker, LLM/Prompt Engineering

Overall Observation:
"Sarah demonstrates solid Python fundamentals and stronger-than-claimed 
LLM knowledge, suggesting real hands-on AI experience beyond what the 
resume conveys. The primary gaps are FastAPI (she knows Flask but not 
FastAPI specifically) and RAG architecture depth. Both are learnable 
quickly given her existing foundation."
Claim Accuracy Summary
text
3/5 skills accurately represented
1/5 skills overstated (Docker)
1/5 skills stronger than claimed (LLM/Prompt Engineering)
Learning Plan Sample (Phase 1)
text
PHASE 1: QUICK WINS — 2 weeks

Skill: FastAPI
  Current: Beginner (20%) → Target: Intermediate (65%)
  Estimated: 14 hours

  Why This Is Achievable:
  "Since you already know Flask and REST API design patterns, FastAPI is a
  direct adjacent skill. Your existing knowledge of routing, request handling,
  middleware, and Pydantic-like validation transfers directly. You are learning
  syntax and async patterns, not concepts from scratch. Estimated 40% faster
  to learn than someone without Flask background — 14 hours vs 25 hours."

  Why Now: Highest priority gap. Blocking for the role. Flask knowledge makes
  this a quick win rather than a large effort.

  Learning Approach:
  Start with FastAPI official tutorial (1 day). Then rewrite one Flask endpoint
  in FastAPI to compare patterns. Then build a full CRUD API with Pydantic
  models. Focus on async/await and dependency injection — the two key differences
  from Flask.

  Milestones:
  1. Complete FastAPI official tutorial and run first endpoint locally
  2. Rewrite your Flask ETL API endpoint in FastAPI
  3. Build a complete CRUD API with authentication using FastAPI + PostgreSQL

  Hands-On Project:
  "Build a FastAPI-powered REST API that wraps the OpenAI API with rate limiting,
  request logging, and Pydantic response models. Deploy with Docker.
  This directly demonstrates the core skill stack required by the role."

  Resources:
  - FastAPI Official Documentation — https://fastapi.tiangolo.com
  - FastAPI Full Course — freeCodeCamp YouTube
  - Real Python FastAPI Tutorial — https://realpython.com/fastapi-python-web-apis/
PDF Report
The PDF report includes:

Cover page with readiness score
Full skill breakdown table
Strengths / gaps / quick wins
Complete phased learning plan
All resources with clickable links
Motivation note
Project Structure
text
skillprobe/
│
├── app.py                        Main router — no business logic
├── config.py                     All constants and configuration
├── requirements.txt
├── .env.example                  Template for environment variables
├── .gitignore
│
├── .streamlit/
│   └── config.toml               Dark theme configuration
│
├── agents/                       All AI agent modules
│   ├── __init__.py
│   ├── parser_agent.py           JD + Resume parsing in single LLM call
│   ├── skill_mapper.py           Skill matching and gap detection
│   ├── assessment_engine.py      CAT state machine — core agent
│   ├── answer_evaluator.py       5-dimension answer scoring
│   ├── gap_analyzer.py           Results computation and analysis
│   ├── resource_finder.py        DuckDuckGo real resource search
│   └── learning_plan_agent.py    Phased plan with adjacent skill reasoning
│
├── models/
│   ├── __init__.py
│   └── llm_client.py             Unified LLM interface (Gemini + Groq)
│
├── core/
│   ├── __init__.py
│   └── state.py                  Centralised session state manager
│
├── ui/
│   ├── __init__.py
│   ├── styles.py                 All CSS and HTML helpers
│   ├── step_input.py             Step 1 — Input page
│   ├── step_parsing.py           Step 2 — Parsing and skill map
│   ├── step_assessment.py        Step 3 — Adaptive assessment
│   ├── step_results.py           Step 4 — Results dashboard
│   └── step_plan.py              Step 5 — Learning plan
│
├── utils/
│   ├── __init__.py
│   ├── file_parser.py            PDF, DOCX, TXT text extraction
│   ├── charts.py                 Plotly chart builders
│   └── pdf_generator.py          PDF report generation
│
└── sample_inputs/
    ├── sample_jd.txt             Sample AI Engineer job description
    └── sample_resume.txt         Sample candidate resume
Agent Design — Why This Is a Real Agent
SkillProbe is not a wrapper around a single LLM call. It is a multi-agent
system with a stateful assessment engine at its core.

Agent Properties Demonstrated
Property	How SkillProbe Demonstrates It
Autonomy	Decides when to stop assessing a skill. Decides when confidence is sufficient. Decides when to move to the next skill. No user instruction needed.
Adaptation	Changes question difficulty dynamically after every answer. Strong answer → harder question. Weak answer → easier question.
Observation	Evaluates every answer on 5 explicit dimensions with structured scoring and reasoning. Not a vibe check.
Planning	Assesses skills in priority order. Critical skills first. Builds assessment queue based on job requirements.
Judgment	Produces explainable per-skill proficiency scores with difficulty ceiling. The score has a mathematical basis and a textual explanation.
What Makes It Adaptive (Not Just Sequential)
A standard system would ask 5 questions per skill regardless of answers.
SkillProbe's assessment engine maintains state per skill and adjusts:

text
Scenario A — Strong candidate:
  Q1 (Level 2): Strong → Q2 (Level 3): Strong → Q3 (Level 4): Moderate
  Result: Max difficulty Level 4 reached. Assessed: Advanced.
  Stop: confidence high after 3 questions.

Scenario B — Weaker candidate:
  Q1 (Level 2): Weak → Q2 (Level 1): Moderate → Q3 (Level 1): Moderate
  Result: Max difficulty Level 2 reached. Assessed: Beginner-Intermediate.
  Stop: max questions reached.

Scenario C — Inflated resume claim:
  Resume claims: Expert (85%)
  Q1 starts at Level 3: Weak → Q2 drops to Level 2: Moderate → Q3 (Level 2): Moderate
  Result: Assessed at 42% vs claimed 85%. Gap: 43%. Claim: Overstated.
Trade-offs & Decisions
Decision	Alternative Considered	Why This Choice
Streamlit over React	React + FastAPI backend	Faster to build, stable, sufficient UX for hackathon
Single combined parse call	3 separate calls	Saves 2 LLM calls = 66% token reduction on parsing
Rule-based observations	LLM per skill observation	Saves 1 call per skill, still produces useful output
fpdf2 over WeasyPrint	WeasyPrint, ReportLab	fpdf2 has no binary deps, works on Streamlit Cloud
DuckDuckGo over curated DB	Hardcoded resources	Real, current links. No stale URLs. No hallucination.
3 questions max	5 questions	40% token reduction. Sufficient signal for most skills.
5 skills max	8 skills	Meaningful assessment without exhausting free tier limits
Session-only storage	Database	Privacy feature. Candidate data never stored server-side.
Confidence-based stopping	Fixed question count	More efficient. High-signal skills assessed faster.
Future Improvements
text
Short term (next sprint):
  [ ] Code execution sandbox for programming skill verification
  [ ] Better question deduplication across skills
  [ ] Smarter token usage with streaming responses
  [ ] More granular adjacent skill graph

Medium term:
  [ ] Persistent sessions with local SQLite storage
  [ ] Export to formatted PDF with charts included
  [ ] Candidate progress tracking across multiple assessments
  [ ] Benchmark proficiency against real job market data

Long term:
  [ ] Integration with real course platforms (Coursera, Udemy APIs)
  [ ] Community-contributed skill rubrics
  [ ] Recruiter mode — send assessment link to candidate
  [ ] Multi-language support
  [ ] Voice input option for assessment answers
Privacy and Data
text
What we store:    Nothing on any server.
Where data lives: Your browser session only.
When it clears:   When you close the tab or click Start Over.
What we collect:  Zero. No analytics. No telemetry beyond Streamlit defaults.
Candidates can be completely honest in their answers because the results
are shown only to them and downloaded only by them.

License
MIT License — Built for the Deccan AI Hackathon.

Built By
Built for the Deccan AI Hackathon — an adaptive skill verification agent
that tests real proficiency, not resume claims.

If this helps you get hire-ready faster, it worked.

🚀 Try SkillProbe

```
