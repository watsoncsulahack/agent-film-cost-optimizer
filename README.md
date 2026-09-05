# CostOptimizerAgent - AI Video Production Cost Optimizer

`CostOptimizerAgent` is an autonomous AI video production cost optimizer built with **Google ADK** (Agent Development Kit) on **Gemini**. It implements the **9-step reasoning architecture** and **2 core tools** to evaluate shot requirements, query model intelligence via Parallel Search, eliminate unsuitable models, and calculate the lowest-cost viable alternative.

> 🚀 **Live Production App (Google Cloud Run)**: [https://agent-film-cost-optimizer-709949980336.us-central1.run.app](https://agent-film-cost-optimizer-709949980336.us-central1.run.app)
> 🌐 **Interactive Client (GitHub Pages)**: [https://watsoncsulahack.github.io/agent-film-cost-optimizer/](https://watsoncsulahack.github.io/agent-film-cost-optimizer/)

---

## 🏛️ Architecture Overview

```
                        USER
                          |
                          v
          Gemini Enterprise Agent Platform
                          |
                          v
                COST OPTIMIZER AGENT
                   built with ADK
                          |
                   Gemini reasoning
                          |
            +-------------+-------------+
            |                           |
            v                           v
   Shot Analysis Tool          Parallel Search API
                                        |
                                        v
                            Current Model Information
                            • Pricing
                            • Capabilities
                            • Limitations
                            • Availability
            |                           |
            +-------------+-------------+
                          |
                          v
                     Cost Engine
                          |
                          v
                    Recommendation & Tradeoffs
```

---

## 🧠 The 9-Step Reasoning Workflow

1. **Extract technical shot requirements** (via [`analyze_shot_requirements`](cost_optimizer_agent/shot_analysis_tool.py))
2. **Determine which capabilities are essential** (e.g. photorealism, camera control, physics simulation, character consistency)
3. **Search current video-generation providers using Parallel** (via [`search_video_models_and_pricing`](cost_optimizer_agent/parallel_search_tool.py))
4. **Normalize pricing and capabilities** (deterministic $/sec across per-second, credit-based, and fixed-gen pricing)
5. **Eliminate unsuitable models** (filters out models lacking essential capabilities or suffering from disqualifying limitations)
6. **Calculate estimated cost per viable result** (applies duration and prompt rerun multiplier)
7. **Rank the alternatives** (orders viable models from lowest cost to highest tier)
8. **Recommend the lowest-cost viable approach** (selects the winning cost-effective model)
9. **Explain the tradeoff** (details the tradeoffs between budget savings, latency, and provider limitations)

---

## 📁 Project Structure

```
ai-film/
├── cost_optimizer_agent/
│   ├── __init__.py       # Package exports (root_agent, cost_optimizer_agent, tool)
│   ├── agent.py          # Google ADK Agent definition with Gemini instructions
│   ├── config.py         # Configuration settings & environment loader
│   └── tools.py          # Parallel Search API tool implementation
├── main.py               # Interactive CLI & demonstration runner
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # Documentation
```

---

## 🚀 Quickstart

### 1. Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file from the template:
```bash
cp .env.example .env
```

Edit `.env` to supply your API keys:
```ini
GEMINI_API_KEY="your_gemini_api_key"
PARALLEL_API_KEY="your_parallel_api_key"   # https://parallel.ai
GEMINI_MODEL="gemini-2.5-flash"
```

> **Note**: If `PARALLEL_API_KEY` is not provided, the tool automatically operates in simulated discovery mode with sample stock asset data for development and testing.

---

## 💻 Usage

### Option 0: Live Browser App on GitHub Pages (Zero Install)

Open the hosted web app in your browser:
**👉 [https://watsoncsulahack.github.io/agent-film-cost-optimizer/](https://watsoncsulahack.github.io/agent-film-cost-optimizer/)**

To host it on your own fork:
1. Go to your repository **Settings** → **Pages**.
2. Under **Build and deployment** → **Branch**, select `main` and folder `/docs` (or `/ (root)`).
3. Click **Save** — your site will be live in seconds!

### Option A: Filmmaker Interactive Web Frontend (`web_app.py`)

Launch the web app for visual shot analysis and ranked model comparisons:

```bash
python web_app.py
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

- **Interactive Controls**: Adjust shot duration (1s–20s), rerun multiplier (1.0x–5.0x), and target FPS.
- **Ranked Model Comparison**: Automatically sorts all 7 supported video models by normalized cost ($/sec).
- **Parallel Search Discovery**: Live stock video b-roll and VFX background plate matches with direct asset links.
- **Strategic Recommendations**: Actionable guidance on direct stock integration vs. hybrid VFX vs. full generative AI.

### Option B: Run via ADK CLI

You can run the agent directly using the Google ADK CLI:

```bash
# Interactive CLI session
adk run cost_optimizer_agent

# Or launch the ADK Web UI
adk web .
```

### Option C: Run via Python Runner (`main.py`)

#### 1. Analyze a Custom Shot Description
```bash
python main.py --shot "Drone aerial shot flying through futuristic neon Tokyo skyscrapers in rain"
```

#### 2. Direct Tool Execution (Without LLM Runner)
```bash
python main.py --tool-only --shot "Slow motion waves crashing onto black sand beach in Iceland at dusk"
```

---

## 🎯 Supported Video Models & Pricing Benchmarks

The optimizer evaluates and ranks the following 7 AI video models:

| Model | Pricing Paradigm | Base Rate | Normalized ($/sec) |
| :--- | :--- | :--- | :--- |
| **Hailuo** | Fixed Generation / Credits | $0.24 / 6s clip | **$0.040 / sec** |
| **Runway (Gen-3 Turbo)** | Credit-based | 5 credits / sec ($0.01/cr) | **$0.050 / sec** |
| **MiniMax-H3** | Fixed Generation | $0.25 / 5s video | **$0.050 / sec** |
| **Seedance** | Fixed Generation | $0.30 / 5s shot | **$0.060 / sec** |
| **Kling** | Credit-based | 35 credits / 5s ($0.01/cr) | **$0.070 / sec** |
| **Luma (Dream Machine)** | Fixed Generation | $0.40 / 5s clip | **$0.080 / sec** |
| **Runway (Gen-3 Alpha)** | Credit-based | 10 credits / sec ($0.01/cr) | **$0.100 / sec** |
| **Veo (Standard)** | Per-second | $0.15 / sec | **$0.150 / sec** |


---

## 🛠️ Tool Definition: `parallel_search_video_footage`

```python
def parallel_search_video_footage(
    shot_description: str,
    search_objective: Optional[str] = None,
    search_queries: Optional[List[str]] = None,
    mode: str = "turbo",
    max_results: int = 5,
) -> Dict[str, Any]:
    """Queries the Parallel Search API to find stock video footage and visual assets."""
```

### Parameters:
- `shot_description` (*str*): The scene prompt or storyboard shot description.
- `search_objective` (*Optional[str]*): Natural language search objective sent to Parallel Search API.
- `search_queries` (*Optional[List[str]]*): 2-3 specific search query variations (automatically constructed if omitted).
- `mode` (*str*): Parallel Search mode (`turbo`, `basic`, or `advanced`). Defaults to `turbo`.
- `max_results` (*int*): Maximum number of footage candidates to return.

---

## 📊 Example Output

```markdown
🎬 Shot Classification & Feasibility:
- Type: Establishing Shot / Drone B-Roll
- Feasibility of Stock Replacement: High (95% match likelihood)

🔍 Discovered Footage Assets:
1. "4K Stock Footage: Aerial drone shot rising over Manhattan skyline"
   - Source: Pexels (CC0 / Royalty Free)
   - Resolution: 3840x2160 (4K UHD)
   - URL: https://www.pexels.com/search/videos/Drone+aerial+shot

💰 Cost Breakdown:
- Full AI Video Generation (5s shot + 2.2x reruns): ~$0.77 USD
- Stock Sourcing: $0.00 USD
- Net Savings: $0.77 USD per shot (100% compute savings)

🚀 Recommended Production Action:
- Direct Stock Integration: Insert 4K stock plate directly into the timeline.
```
