# 🧠 Incident Intelligence Service

**Incident Intelligence Service** is an AI-powered backend service that analyzes event feedback and operational signals to detect, score, and track incidents related to **events, hosts, and venues**.

It converts **raw event data + user comments** into:
- incident risk scores
- severity levels
- explainable causes
- long-term host & venue risk profiles

The system is designed to be:
- **stateless in logic**
- **persistent via JSON**
- **ML-ready** for future upgrades

---

## 🎯 Problem This Service Solves

Event platforms often face:
- hidden safety issues
- overcrowding and poor logistics
- unreliable hosts or venues
- reactive incident handling

This service provides:
- **early detection** of risks
- **objective scoring** (not gut feeling)
- **explainable intelligence**
- **continuous learning from history**

---

## 🏗️ High-Level Architecture
```
Node Backend
   │
   │ (event data + comments)
   ▼
Incident Intelligence Service (FastAPI)
   │
   ├── NLP analysis (sentiment, aspects, severity)
   ├── Feedback aggregation
   ├── Behavioral signal derivation
   ├── Incident scoring
   ├── Risk profile updates
   ▼
JSON Storage (host & venue risk memory)
```


- Backend sends facts.
- This service produces intelligence.

---

## 🔁 End-to-End Flow (Step-by-Step)

### 1️⃣ Backend Sends Event Payload

The backend sends **raw, factual data only** to the Incident Intelligence Service.

**Included data:**
- `comments`
- `timing`
- `attendance`
- `refunds`
- `hostId`
- `venueId`

> ❗ No AI, NLP, or scoring logic is performed in the backend.  
> The backend acts purely as a **data provider**.

---

### 2️⃣ NLP Analysis (Per Comment)

Each comment is processed independently through the NLP pipeline:

- text cleaning
- sentiment analysis
- aspect detection (crowd, security, entry, etc.)
- severity detection
- incident hint detection

**Output per comment:**

```json
{
  "sentiment": -0.62,
  "aspects": ["crowd", "entry"],
  "severity": "high",
  "incidentHint": true,
  "signalStrength": 0.83
}

```

---

### 3️⃣ Feedback Aggregation

All comment-level outputs are aggregated to produce **stable, event-level signals**:

- average sentiment  
- negative feedback rate  
- high-severity ratio  
- incident hint rate  
- feedback confidence (based on comment volume)

This design ensures that **one angry comment does not over-penalize an entire event**.

---

### 4️⃣ Derived Behavioral Signals

From structured event data, the system derives behavioral indicators:

- schedule delay (planned vs actual start)  
- early exit rate (registered vs checked-in)  
- refund rate  

All derived signals are normalized to a **0–1 scale** for consistent scoring.

---

### 5️⃣ Incident Scoring

A weighted scoring model combines all signals to compute:

- `incidentScore` ∈ `[0, 1]`  
- `incidentLevel`: `low` / `medium` / `high`  
- `confidence`  
- score breakdown (for explainability)

**Example:**

```json
{
  "incidentScore": 0.469,
  "incidentLevel": "medium",
  "confidence": 0.85,
  "scoreBreakdown": {
    "incidentHint": 0.21,
    "negativeFeedback": 0.13,
    "earlyExit": 0.04
  }
}
```

### 6️⃣ Learning via Risk Profiles (Memory)

The system **learns over time** by continuously updating long-term risk profiles.

#### 🧑 Host Risk Profile
- rolling average incident score  
- decay-based memory (recent events matter more)  
- common recurring issues  
- stable risk level classification  

#### 🏟️ Venue Risk Profile
- slower decay (structural issues change slowly)  
- crowd and entry bottleneck patterns  
- infrastructure reliability trends  

This approach enables **learning without model training**, making it safe and reliable for production use.

---

## 🧠 How the System Learns (No ML Required)

Learning is achieved through deterministic, explainable mechanisms:

### ✅ Rolling Averages

Each new event updates historical risk using a decay-aware rolling average:

```
new_avg = (old_avg * count * decay + new_score) / (count * decay + 1)

```


### ✅ Decay

Decay controls how quickly past events lose influence:

- **Hosts**: recover faster (behavioral improvements are quicker)  
- **Venues**: recover slower (structural changes take time)  



### ✅ Issue Frequency Tracking

- Repeated issues are counted over time  
- Frequently recurring issues increase confidence in identifying root causes  

---

### 📥 API Input (Main Contract)

#### POST /api/incident/analyze-event


```json
{
  "eventId": "evt_101",
  "hostId": "host_12",
  "venueId": "venue_9",
  "comments": [
    "Extremely overcrowded and unsafe",
    "Long queues at entry gate"
  ],
  "timing": {
    "scheduledStart": "18:00",
    "actualStart": "18:20",
    "actualEnd": "21:30"
  },
  "attendance": {
    "registeredCount": 500,
    "checkedInCount": 420
  },
  "refunds": {
    "refundCount": 18,
    "refundRate": 0.036
  },
  "venue": {
    "venueCapacity": 600,
    "venueType": "open"
  }
}
```


#### 📤 API Output (Main Contract)


```json
{
  "eventId": "evt_101",
  "incident": {
    "incidentScore": 0.469,
    "incidentLevel": "medium",
    "confidence": 0.85
  },
  "incidentIssues": ["crowd", "entry"],
  "hostRisk": {
    "avgIncidentScore": 0.44,
    "riskLevel": "medium",
    "commonIssues": ["crowd"]
  },
  "venueRisk": {
    "avgIncidentScore": 0.51,
    "riskLevel": "medium",
    "commonIssues": ["entry", "crowd"]
  }
}

```

---

## 📂 Folder Structure (Detailed)

```
app/
├── main.py
│   └── FastAPI entry point, health check, router registration
│
├── api/
│   └── routes.py
│       └── Public API endpoints
│
├── schemas/
│   └── event_payload.py
│       └── Single public input contract (validated boundary)
│
├── nlp/
│   ├── pipeline.py
│   │   └── Orchestrates NLP per feedback
│   ├── sentiment.py
│   │   └── VADER-based sentiment analysis
│   ├── aspects.py
│   │   └── Aspect detection (crowd, security, etc.)
│   ├── severity.py
│   │   └── Severity classification (low / medium / high)
│
├── incident/
│   ├── analyzer.py
│   │   └── End-to-end event analysis orchestration
│   ├── aggregator.py
│   │   └── Stable aggregation of feedback signals
│   ├── scorer.py
│   │   └── Incident scoring + explainability
│   ├── derived_signals.py
│   │   └── Timing, attendance, refund feature extraction
│
├── risk_profiles/
│   ├── base.py
│   │   └── Rolling average + risk classification
│   ├── host.py
│   │   └── Host risk memory & learning
│   ├── venue.py
│   │   └── Venue risk memory & learning
│
├── utils/
│   ├── text_cleaner.py
│   │   └── Meaning-preserving text normalization
│   ├── json_store.py
│       └── Thread-safe, atomic JSON persistence

```

---

## 🗄️ Storage Strategy

The service uses a **simple but robust JSON-based persistence layer** for maintaining long-term memory.

- JSON-based persistence (`host_risks.json`, `venue_risks.json`)
- Atomic writes to prevent file corruption during crashes
- Thread-safe reads and writes to support concurrent requests
- Clean abstraction that can be easily replaced with a database later  
  (e.g., Redis, PostgreSQL) without changing business logic

This approach is ideal for an MVP while remaining production-safe.

---

## 🚀 Why This Design Is Industry-Grade

This system follows proven backend and AI engineering principles:

- Clear separation of concerns between NLP, scoring, and persistence
- Stateless business logic with externalized memory
- Defensive programming to handle bad or incomplete data safely
- Explainability at every stage of the pipeline
- ML-ready architecture without immediate ML dependency
- Easy integration with a Node.js backend
- Safe, scalable MVP architecture that can grow incrementally

---
---
---

I’ll explain **exactly how the backend should send data**, step-by-step, in **simple, production terms**, with **Node.js examples**.

---

# 🧠 How the Backend Should Send Data (FINAL, CLEAR GUIDE)

## 🔑 Core Rule (Lock This)

> **Backend sends ONE consolidated payload per event.
> Not per comment. Not per user. Not per action.**

---

## ✅ 1️⃣ Backend Responsibility (What Backend Does)

Backend is responsible for:

* storing comments
* storing attendance
* storing refunds
* storing timing
* knowing when an event is “done”

Backend is **NOT responsible** for:

* NLP
* sentiment
* severity
* scoring
* learning

---

## 🧩 2️⃣ When Backend Sends Data

### Recommended (Best Practice)

⏰ **Nightly batch at 3:00 AM**

Backend:

* fetches all events marked `COMPLETED`
* loops over them
* sends one API request per event

---

## 📦 3️⃣ Payload Format (Exactly What to Send)

Backend must send **this exact structure** (no extras, no missing fields):

```json
{
  "eventId": "evt_101",
  "hostId": "host_12",
  "venueId": "venue_9",
  "comments": [
    "Extremely overcrowded and unsafe",
    "Long queues at entry gate",
    "Security was weak"
  ],
  "timing": {
    "scheduledStart": "18:00",
    "actualStart": "18:20",
    "actualEnd": "21:30"
  },
  "attendance": {
    "registeredCount": 500,
    "checkedInCount": 420
  },
  "refunds": {
    "refundCount": 18,
    "refundRate": 0.036
  },
  "venue": {
    "venueCapacity": 600,
    "venueType": "open"
  }
}
```

🚫 Backend must NOT send:

* sentiment
* severity
* incidentScore
* partial fields

---

## 🔁 4️⃣ Batch Sending Logic (Node.js Example)

### Nightly Cron Job (Node.js)

```js
import axios from "axios";

async function sendEventsToIncidentService(events) {
  for (const event of events) {
    try {
      await axios.post(
        "http://incident-service/api/incident/analyze-event",
        event,
        { timeout: 10000 }
      );
    } catch (err) {
      console.error(
        `Incident analysis failed for event ${event.eventId}`,
        err.message
      );
    }
  }
}
```

### Where `events` come from:

```js
const events = await db.events.find({
  status: "COMPLETED",
  incidentProcessed: false
});
```

---

## 🔒 5️⃣ Idempotency & Safety Rules (VERY IMPORTANT)

### Rule 1: Process each event once

Backend should mark:

```json
"incidentProcessed": true
```

after a successful call.

---

### Rule 2: Retry safely

If a request fails:

* retry next night
* same payload is safe
* learning remains stable

---

### Rule 3: Timeouts & isolation

* One event failure must not stop batch
* Always wrap in try/catch

---

## 📥 6️⃣ What Backend Receives (And Stores)

Backend receives:

```json
{
  "incident": {
    "incidentScore": 0.13,
    "incidentLevel": "low",
    "confidence": 0.95
  },
  "incidentIssues": ["crowd", "security"],
  "hostRisk": {...},
  "venueRisk": {...}
}
```

Backend should store:

* `incidentScore`
* `incidentLevel`
* `incidentIssues`
* timestamps

---

## 🧠 7️⃣ How Backend USES This Data

Backend can now:

* show admin dashboards
* rank risky events
* trigger human review
* feed Repo-2 recommendations
* generate PDFs
* learn patterns

Backend **does not modify** this intelligence.

---

## ❌ 8️⃣ What Backend Must NOT Do

❌ Call per comment
❌ Call per click
❌ Run NLP
❌ Guess risk
❌ Aggregate manually

---

## 🏁 FINAL ONE-LINE SUMMARY

> **Backend sends one clean, factual payload per completed event (ideally in a nightly batch).
> The Incident Intelligence Service thinks, scores, learns, and remembers.**


