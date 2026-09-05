# 🎬 Cost Optimizer Agent
### Autonomous AI Video Production Cost Optimizer & Model Ranker

[![Google Cloud Run](https://img.shields.io/badge/Google_Cloud_Run-Deployed-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://agent-film-cost-optimizer-709949980336.us-central1.run.app)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![Google ADK](https://img.shields.io/badge/Google_ADK-1.18+-34A853?style=for-the-badge&logo=google&logoColor=white)](https://github.com/google/adk)
[![Parallel Search API](https://img.shields.io/badge/Parallel_Search_API-Integrated-000000?style=for-the-badge&logo=search&logoColor=white)](https://parallel.ai)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Pytest-30_Passed-10B981?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

---

> 🚀 **Live Hosted Web Application**: **[https://agent-film-cost-optimizer-709949980336.us-central1.run.app](https://agent-film-cost-optimizer-709949980336.us-central1.run.app)**  
> 🏆 **Built for**: *Agentic Cinema: The Blockbuster Hackathon*

---

## 💡 The Problem & The Solution

### The Challenge
AI video generation compute costs escalate exponentially during film production. Because video generation frequently requires **2x to 4x trial iterations (reruns)** to achieve desired cinematic consistency, filmmakers regularly burn through production budgets by routing basic shots (establishing scenes, macro textures, atmospheric b-roll) through expensive top-tier generative models ($0.15/sec) when lower-cost models ($0.04/sec) or live stock footage plates ($0.00) produce identical or superior results.

### The Solution: `CostOptimizerAgent`
`CostOptimizerAgent` is an autonomous production supervisor built on the **Google Agent Development Kit (ADK)** and powered by **Google Gemini** and **Parallel Search**. It parses desired scene prompts into technical dimensions (subject, camera trajectory, motion dynamics, physics simulation, character consistency), queries live market intelligence across major video generation providers, filters out incapable models, and calculates deterministic per-shot costs to deliver the **highest-quality, lowest-cost production strategy**.

---

## 🏛️ System Architecture

```
                                  🎬 FILMMAKER
                                        │
                                        ▼
                  ┌───────────────────────────────────────────┐
                  │   FastAPI Web App / Google ADK Runner     │
                  └─────────────────────┬─────────────────────┘
                                        │
                                        ▼
                  ┌───────────────────────────────────────────┐
                  │       COST OPTIMIZER AGENT (Google ADK)   │
                  └─────────────────────┬─────────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
       ┌────────────────────────┐              ┌────────────────────────┐
       │   Shot Analysis Tool   │              │  Parallel Search Tool  │
       │  (Subject, Camera,     │              │  (Provider Intel &     │
       │   Physics, Dynamics)   │              │   Stock Plate Search)  │
       └────────────┬───────────┘              └────────────┬───────────┘
                    │                                       │
                    └───────────────────┬───────────────────┘
                                        │
                                        ▼
                  ┌───────────────────────────────────────────┐
                  │       Deterministic Cost Engine           │
                  │  • Normalizes Rates ($/sec)               │
                  │  • Applies Rerun Multipliers              │
                  │  • Eliminates Incompatible Models         │
                  └─────────────────────┬─────────────────────┘
                                        │
                                        ▼
                  ┌───────────────────────────────────────────┐
                  │       Google Gemini LLM Reasoning         │
                  │  • Scene Technical Deconstruction         │
                  │  • Concrete Tradeoff Analysis             │
                  │  • Production Execution Strategy          │
                  └─────────────────────┬─────────────────────┘
                                        │
                                        ▼
                  ┌───────────────────────────────────────────┐
                  │   Interactive Comparison Dashboard (UI)   │
                  │   • Top 3 Model Recommendations           │
                  │   • Ranked Pricing & Savings Matrix       │
                  │   • Disqualification Explanations         │
                  │   • Live Stock/B-Roll Replacement Cards   │
                  └───────────────────────────────────────────┘
```

---

## 🧠 The 9-Step Reasoning Workflow

1. **Extract Technical Shot Requirements**: Deconstructs prompts into subject type, camera movement, motion velocity, lighting style, and physics complexity.
2. **Determine Essential Capabilities**: Infers mandatory model capabilities (e.g. `camera_motion_control`, `complex_physics_simulation`, `character_anatomy_consistency`).
3. **Query Live Provider Intelligence via Parallel Search**: Queries active pricing, known limits, and capability updates across providers.
4. **Discover Stock Footage & VFX Plates via Parallel Search**: Identifies existing 4K b-roll and background plates to reduce compute requirements.
5. **Normalize Cross-Paradigm Pricing**: Translates per-second, credit-based, and fixed-generation rates into a unified `$ / second` standard.
6. **Eliminate Unsuitable Models**: Enforces strict capability matching, disqualifying models lacking necessary features.
7. **Calculate Total Estimated Budget**: Factors in target clip duration and iterative rerun multipliers (`Cost = Rate × Duration × Reruns`).
8. **Rank Viable Alternatives**: Orders viable options from lowest to highest cost.
9. **Synthesize Gemini Tradeoff Reasoning**: Generates expert cinematic advice detailing visual fidelity tradeoffs vs. cost savings.

---

## 📊 Supported Video Models & Pricing Benchmark

The Cost Engine standardizes pricing across different billing paradigms into normalized rates:

| Model | Provider | Pricing Paradigm | Base Rate | Normalized Rate | Quality Score | Primary Strengths |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hailuo** | MiniMax | Fixed Generation | $0.24 / 6s | **$0.040 / sec** | 8.7 / 10 | Realistic human faces, organic motion, budget efficiency |
| **Runway (Gen-3 Turbo)** | RunwayML | Credit-based | 5 cr/sec ($0.01/cr) | **$0.050 / sec** | 8.8 / 10 | Ultra-fast inference, strong camera motion presets |
| **MiniMax-H3** | MiniMax | Fixed Generation | $0.25 / 5s | **$0.050 / sec** | 8.8 / 10 | High prompt adherence, physical object interaction |
| **Seedance** | ByteDance | Fixed Generation | $0.30 / 5s | **$0.060 / sec** | 8.6 / 10 | Consistent character styling, smooth natural motion |
| **Kling / Kling-Pro** | Kuaishou | Credit-based | 35–70 cr / 5–10s | **$0.070 / sec** | 9.1 / 10 | Long 10s coherence, complex human anatomy |
| **Luma (Dream Machine)** | Luma AI | Fixed Generation | $0.40 / 5s | **$0.080 / sec** | 8.9 / 10 | Sweeping camera moves, massive environmental scale |
| **Veo-Fast** | Google / Vertex AI | Per-second | $0.08 / sec | **$0.080 / sec** | 8.7 / 10 | Cost-effective cinematic framing and rapid turnaround |
| **Runway (Gen-3 Alpha)** | RunwayML | Credit-based | 10 cr/sec ($0.01/cr) | **$0.100 / sec** | 9.3 / 10 | Hollywood dynamic range, complex cinematic lighting |
| **Veo (Standard)** | Google / Vertex AI | Per-second | $0.15 / sec | **$0.150 / sec** | 9.4 / 10 | Industry-leading physics, fluid simulation, visual fidelity |

---

## 📁 Repository Structure

```
ai-film/
├── cost_optimizer_agent/
│   ├── __init__.py               # Package exports (root_agent, ADK tools)
│   ├── agent.py                  # Google ADK Agent definition with Gemini instructions
│   ├── config.py                 # Configuration settings & environment loaders
│   ├── cost_engine.py            # 9-step deterministic cost & capability engine
│   ├── gemini_service.py         # Google Gemini LLM reasoning service
│   ├── models_pricing.py         # Model specifications & pricing registry
│   ├── parallel_search_tool.py   # Parallel Search API tool for provider intelligence
│   ├── pricing.py                # Pricing normalization formulas
│   ├── shot_analysis_tool.py     # Prompt requirement extraction tool
│   └── tools.py                  # Parallel Search stock video footage discovery tool
├── test_model_pricing.py         # Model pricing registry unit tests (16 tests)
├── test_pricing.py               # Unit conversion and normalization tests (10 tests)
├── test_workflow.py              # Full 9-step workflow & tool tests (4 tests)
├── Dockerfile                    # Container definition for Google Cloud Run
├── requirements.txt              # Production Python dependencies
├── run.sh                        # One-command local startup script
├── web_app.py                    # FastAPI web application with real-time UI
├── main.py                       # CLI runner & interactive ADK demonstration
├── .env.example                  # Environment variable configuration template
├── LICENSE                       # Open source license (Apache 2.0)
└── README.md                     # Documentation
```

---

## 🚀 Quickstart & Local Setup

### 1. Clone & Setup Environment

```bash
git clone https://github.com/watsoncsulahack/agent-film-cost-optimizer.git
cd agent-film-cost-optimizer

# Copy environment template
cp .env.example .env
```

### 2. Configure API Keys

Edit `.env` or set keys in your environment:
```ini
GEMINI_API_KEY="your_google_gemini_api_key"
PARALLEL_API_KEY="your_parallel_api_key"       # https://parallel.ai
GEMINI_MODEL="gemini-2.5-flash"
```

> **Note**: Both `GEMINI_API_KEY` and `PARALLEL_API_KEY` are strictly required. Keys can also be entered directly in the web UI's **API Settings** panel.

### 3. Launch the Web Application

```bash
# Option A: Using the startup script
chmod +x run.sh && ./run.sh

# Option B: Direct Python execution
pip install -r requirements.txt
python web_app.py
```

Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

## 💻 Alternative Execution Modes

### Option A: Interactive CLI Runner (`main.py`)
```bash
# Analyze a custom shot with Gemini LLM reasoning
python main.py --shot "Drone aerial shot flying through futuristic neon Tokyo skyscrapers in rain"

# Direct tool-only execution (bypasses LLM runner)
python main.py --tool-only --shot "Slow motion waves crashing onto black sand beach in Iceland at dusk"
```

### Option B: Google ADK CLI
```bash
# Interactive ADK session
adk run cost_optimizer_agent

# ADK Web GUI
adk web .
```

### Option C: Docker Container
```bash
docker build -t cost-optimizer-agent .
docker run -p 8000:8000 -e GEMINI_API_KEY="your_key" -e PARALLEL_API_KEY="your_key" cost-optimizer-agent
```

---

## 🧪 Testing & Verification

The test suite validates model pricing, normalization formulas, capability elimination matrices, and strict API key authentication:

```bash
pytest -v
```

```
============================== test session starts ==============================
test_model_pricing.py::test_model_registry_contains_all_models PASSED     [  3%]
test_model_pricing.py::test_hailuo_pricing_normalization PASSED           [  6%]
...
test_workflow.py::test_tool_1_shot_analysis PASSED                        [ 90%]
test_workflow.py::test_tool_2_parallel_search_missing_key_raises_error PASSED [ 93%]
test_workflow.py::test_gemini_service_missing_key_raises_error PASSED     [ 96%]
test_workflow.py::test_cost_engine_elimination_and_ranking PASSED         [100%]
============================== 30 passed in 6.85s ===============================
```

---

## 🛡️ License

This project is open-source under the [Apache 2.0 License](LICENSE).  
Built with ❤️ for **Agentic Cinema: The Blockbuster Hackathon**.
