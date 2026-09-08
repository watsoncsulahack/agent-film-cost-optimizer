# 🎬 Cost Optimizer Agent
### Autonomous AI Video Production Cost Optimizer & Model Ranker

[![Google Cloud Run](https://img.shields.io/badge/Google_Cloud_Run-Live_App-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://agent-film-cost-optimizer-709949980336.us-central1.run.app)
[![Agentic Cinema](https://img.shields.io/badge/Hackathon-Agentic_Cinema_Parallel_Track-FF6B6B?style=for-the-badge)](https://agentic-cinema.devpost.com/rules)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![Google ADK](https://img.shields.io/badge/Google_ADK-1.18+-34A853?style=for-the-badge&logo=google&logoColor=white)](https://github.com/google/agent-development-kit)
[![Parallel Search API](https://img.shields.io/badge/Parallel_Search_API-Integrated-000000?style=for-the-badge&logo=search&logoColor=white)](https://parallel.ai)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge)](LICENSE)

---

> 🚀 **Live Hosted Application**: **[https://agent-film-cost-optimizer-709949980336.us-central1.run.app](https://agent-film-cost-optimizer-709949980336.us-central1.run.app)**  
> 🔗 **Sibling Repository (ClickHouse Track)**: **[agent-film-cost-optimizer-telemetry](https://github.com/watsoncsulahack/agent-film-cost-optimizer-telemetry)**  
> 🏆 **Built for**: *Agentic Cinema: The Blockbuster Hackathon* (Parallel Track)

---

## 💡 The Problem & The Solution

### The Challenge
AI video generation compute costs escalate exponentially during film production. Because video generation frequently requires **2x to 4x trial iterations (reruns)** to achieve desired cinematic consistency, filmmakers regularly burn through production budgets by routing basic shots (establishing scenes, macro textures, atmospheric b-roll) through expensive top-tier generative models ($0.15/sec) when lower-cost models ($0.04/sec) or live stock footage plates ($0.00) produce identical or superior results.

### The Solution: `CostOptimizerAgent`
`CostOptimizerAgent` is an autonomous production supervisor built on the **Google Agent Development Kit (ADK)** and powered by **Google Gemini** and **Parallel Search**. It parses desired scene prompts into technical dimensions (subject, camera trajectory, motion dynamics, physics simulation, character consistency), queries live market intelligence across major video generation providers, filters out incapable models, and calculates deterministic per-shot costs to deliver the **highest-quality, lowest-cost production strategy**.

---

## 🏛️ System Architecture

```
                                  🎬 DIRECTOR / FILMMAKER
                                             │
                                             ▼
                      ┌───────────────────────────────────────────┐
                      │   FastAPI Web App / Google ADK Studio     │
                      └──────────────────────┬────────────────────┘
                                             │
                                             ▼
                      ┌───────────────────────────────────────────┐
                      │    COST OPTIMIZER AGENT (Google ADK)      │
                      └──────────────────────┬────────────────────┘
                                             │
                        ┌────────────────────┴────────────────────┐
                        │                                         │
                        ▼                                         ▼
           ┌────────────────────────┐                ┌────────────────────────┐
           │   Shot Analysis Tool   │                │  Parallel Search Tool  │
           │  (Subject, Camera,     │                │  (Provider Intel &     │
           │   Physics, Dynamics)   │                │   Stock Plate Search)  │
           └────────────┬───────────┘                └────────────┬───────────┘
                        │                                         │
                        └────────────────────┬────────────────────┘
                                             │
                                             ▼
                      ┌───────────────────────────────────────────┐
                      │       Deterministic Cost Engine           │
                      │  • Normalizes Rates ($/sec)               │
                      │  • Applies Rerun Multipliers              │
                      │  • Eliminates Incompatible Models         │
                      └──────────────────────┬────────────────────┘
                                             │
                                             ▼
                      ┌───────────────────────────────────────────┐
                      │       Google Gemini LLM Reasoning         │
                      │  • Scene Technical Deconstruction         │
                      │  • Concrete Tradeoff Analysis             │
                      │  • Production Execution Strategy          │
                      └──────────────────────┬────────────────────┘
                                             │
                                             ▼
                      ┌───────────────────────────────────────────┐
                      │     Interactive Studio Dashboard (UI)     │
                      │   • Top 3 Model Recommendations           │
                      │   • Ranked Pricing & Savings Matrix       │
                      │   • Google AP2 Agent Wallet & Pre-Funding │
                      │   • Phase 2 Video Generation Review Modal │
                      │   • 10s Cinematic Loading HUD & Player    │
                      └───────────────────────────────────────────┘
```

---

## 📊 Supported Video Models & Pricing Benchmark

The Cost Engine standardizes pricing across different billing paradigms into normalized rates:

| Model | Provider | Pricing Paradigm | Base Rate | Normalized Rate | Quality Score | Primary Strengths |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Runway Gen-3 Alpha** | Runway | Credit-based ($0.05/sec) | $0.25 / 5s | $0.0500/sec | 88/100 | Camera control, photorealism |
| **Runway Gen-3 Turbo** | Runway | High-speed ($0.025/sec) | $0.125 / 5s | $0.0250/sec | 82/100 | High velocity, cost-efficient |
| **Luma Dream Machine** | Luma AI | Generation credit ($0.064/sec)| $0.32 / 5s | $0.0640/sec | 86/100 | Physical interaction, fluid motion |
| **Kling v1.5** | Kuaishou | Subscription/API ($0.07/sec) | $0.35 / 5s | $0.0700/sec | 85/100 | Cinematic lighting, motion scale |
| **Haiper v2** | Haiper | Flat per-generation ($0.04/sec)| $0.20 / 5s | $0.0400/sec | 78/100 | Stylized aesthetics, b-roll |
| **Pika 2.0** | Pika Labs| Credit-based ($0.055/sec) | $0.275 / 5s | $0.0550/sec | 80/100 | Special visual effects, objects |
| **Sora (Estimated)** | OpenAI | High-compute enterprise | $0.150 / 5s | $0.1500/sec | 95/100 | Complex physics, multi-shot scenes |

---

## 🛠️ Quickstart & Local Setup

### 1. Clone & Install
```bash
git clone https://github.com/watsoncsulahack/agent-film-cost-optimizer.git
cd agent-film-cost-optimizer
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and configure your API keys:
```bash
cp .env.example .env
```

### 3. Launch Studio
```bash
./run.sh
```
Navigate to [http://localhost:8000](http://localhost:8000).

---

## 📄 License
Licensed under the [Apache License 2.0](LICENSE).
