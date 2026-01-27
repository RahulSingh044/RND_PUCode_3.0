

# 🧠 Host AI Recommendation Engine (Blockbuzz)

**Host AI Recommendation Engine** is an AI-powered backend service that converts **incident intelligence + live event context** into **actionable, execution-ready recommendations** for event hosts.

It does **not detect incidents**.
It does **not score events**.

It answers a different question:

> **“Given what has gone wrong before, and what this event looks like now — what should the host do to run a successful event?”**

---

## 🎯 Problem This Service Solves

Event platforms often know:

* which events failed
* which hosts are risky
* where problems happened

…but hosts still ask:

* *What should I actually do differently?*
* *How many volunteers do I need?*
* *How do I manage food and entry without chaos?*
* *What actions matter most for THIS event?*

This service bridges that gap by converting **intelligence into execution**.

---

## 🧠 What This Service Produces

For every event, the system generates:

* structured **before / during / after** recommendations
* volunteer planning (count + roles)
* food & crowd management guidance
* venue-aware, constraint-safe actions
* a **confidence score** (honest uncertainty)
* a **branded, downloadable PDF checklist** for hosts

---

## 🏗️ High-Level Architecture

```
Incident Intelligence Service (Repo-1)
   │
   │ (host_risks.json, venue_risks.json)
   ▼
Host AI Recommendation Engine (FastAPI)
   │
   ├── Historical signal extraction
   ├── Live event context analysis
   ├── Failure-mode prediction
   ├── Constraint-aware recommendations
   ├── Volunteer & food planning
   ├── Confidence estimation
   ├── Checklist generation
   ▼
JSON Response + Branded PDF Playbook
```

---

## 🔁 End-to-End Flow (Step-by-Step)

### 1️⃣ Backend Sends Event Context

Backend sends **only factual, current event information**.

Example:

```json
{
  "host_id": "host_45",
  "event_context": {
    "participant_count": 250,
    "event_type": "tech_talk",
    "venue_type": "indoor",
    "event_duration_minutes": 120,
    "ticketing_type": "free",
    "audience_type": "students",
    "food_provided": true
  }
}
```

> ❗ Backend does **not** send incident scores, NLP outputs, or advice.

---

### 2️⃣ Historical Intelligence Is Loaded (Read-Only)

The service directly reads:

```
incident-intelligence-service/storage/
├── host_risks.json
└── venue_risks.json
```

These files contain:

* rolling incident scores
* recurring issues
* long-term risk patterns

This repo **never mutates** that data.

---

### 3️⃣ Signal Extraction (Abstraction Layer)

Raw numbers are converted into **reasoning signals**:

* dominant issue (e.g. entry, crowd)
* issue complexity
* trend (improving / worsening / stable)
* history depth (shallow vs deep)

This prevents overfitting to raw scores.

---

### 4️⃣ Event Context Analysis

Live context is normalized into behavioral signals:

* participant load (low / medium / high)
* free vs paid event
* student vs professional audience
* indoor vs outdoor constraints
* food involvement
* duration risk

---

### 5️⃣ Failure-Mode Prediction (Core Intelligence)

Instead of reacting to issues, the system predicts **how this event might fail**:

Examples:

* entry congestion
* late-arrival rush
* volunteer overstretch
* post-event food chaos
* crowd pressure during sessions

This makes recommendations **predictive, not reactive**.

---

### 6️⃣ Recommendation Generation (Constraint-Aware)

Recommendations are generated from failure modes and then filtered by constraints:

* ❌ no infra changes for indoor venues
* ❌ no unrealistic advice
* ✅ volunteer-driven actions
* ✅ timing & communication strategies

Output is grouped into:

* **Before Event**
* **During Event**
* **After Event**

---

### 7️⃣ Operational Planning

The system also computes:

#### 🧑‍🤝‍🧑 Volunteer Plan

* recommended ratio (1 per 40 participants)
* total volunteers required
* role split (entry, seating, food, lead)

#### 🍽 Food Management Plan

* buffer timing
* serving strategy
* batch release guidance
* estimated food counters

---

### 8️⃣ Confidence Calculation

The confidence score reflects:

* strength of historical evidence
* consistency of past issues
* depth of data

> **Low confidence does NOT mean bad recommendations.
> It means limited historical certainty.**

This keeps the system honest.

---

### 9️⃣ Checklist & PDF Generation

All recommendations are converted into:

* checkbox-style checklist
* grouped operational sections
* branded **Blockbuzz PDF playbook**

The PDF is:

* printable
* shareable
* execution-focused (not explanatory)

---

## 📤 API Output (Simplified)

```json
{
  "host_id": "host_45",
  "confidence": 0.35,
  "operational_guidance": {
    "volunteer_plan": {...},
    "food_management_plan": {...}
  },
  "host_success_recommendations": {
    "before_event": [...],
    "during_event": [...],
    "after_event": [...]
  },
  "assets": {
    "checklist_pdf": {
      "download_url": "data/generated/checklists/host_45_....pdf"
    }
  }
}
```

---

## 📂 Folder Structure (Detailed)

```
app/
├── main.py
│   └── FastAPI entry point & health check
│
├── api/
│   └── recommend.py
│       └── Public recommendation endpoint
│
├── services/
│   ├── repo1_loader.py
│   │   └── Read-only access to incident intelligence
│   ├── signal_extractor.py
│   │   └── Converts raw risk data into reasoning signals
│   ├── context_analyzer.py
│   │   └── Normalizes live event context
│   ├── recommendation_engine.py
│   │   └── Core failure-mode reasoning engine
│   ├── volunteer_calculator.py
│   │   └── Volunteer count & role planning
│   ├── food_planner.py
│   │   └── Food buffer & counter planning
│   ├── constraint_filter.py
│   │   └── Prevents unrealistic recommendations
│   ├── checklist_builder.py
│   │   └── Converts recommendations to actionable tasks
│   └── confidence_calculator.py
│       └── Honest confidence estimation
│
├── pdf/
│   └── checklist_generator.py
│       └── Branded Blockbuzz PDF generation
│
├── schemas/
│   ├── request.py
│   ├── response.py
│   └── internal.py
│
├── utils/
│   ├── file_utils.py
│   └── time_utils.py
│
└── data/
    └── generated/
        └── checklists/
```

---

## 🧠 Design Principles (Why This Is Industry-Grade)

* Clear separation between **intelligence** and **execution**
* Read-only dependency on incident data (safe & decoupled)
* Failure-mode–driven reasoning (not rule spam)
* Constraint-aware recommendations (realistic advice)
* Honest confidence scoring (no false certainty)
* Execution-first outputs (checklists, not paragraphs)
* PDF as a first-class product artifact
* ML-ready architecture without ML dependency

---

## 🏁 One-Line Summary

> **This service turns incident intelligence and event context into realistic, constraint-aware operational playbooks that hosts can actually execute.**

