# 🚀 Photo AI Service – Event-Based Face Matching System

## 📌 Overview

**Photo AI Service** is a production-grade AI microservice designed to **automatically identify users in event photos**.

It enables platforms (like **BlockBuzz**) to:

* Let users upload a selfie once
* Let hosts upload all event photos
* Automatically surface **“Your Photos”** to each user
* Do this **securely, asynchronously, and at scale**

This service is **backend-friendly**, **privacy-aware**, and **scales horizontally** using multiprocessing.

---

## 🎯 What This System Does (In Simple Terms)

> Given:
>
> * a list of **user selfie image URLs**
> * a list of **event photo URLs**

The system:

1. Generates face embeddings for each user
2. Detects faces in event photos
3. Matches users to photos using face similarity
4. Sends results back to backend automatically

No polling. No frontend coupling. No ML logic in backend.

---

## 🧠 High-Level Architecture

```
┌────────────┐
│   Backend  │
│ (Node/API) │
└─────┬──────┘
      │ 1. POST event payload
      ▼
┌─────────────────────┐
│   Photo AI Service  │
│   (FastAPI + ML)    │
└─────┬───────────────┘
      │ 2. Async processing
      │    + multiprocessing
      ▼
┌─────────────────────┐
│ Backend Callback API│
│  (store results)    │
└─────────────────────┘
```

---

## 🔑 Core Design Principles

* **Backend stays dumb** (no ML logic)
* **AI owns identity & matching**
* **All communication via URLs**
* **Async & fault-tolerant**
* **Event-scoped processing**
* **Privacy-first (no embeddings leave AI)**

---

## 📥 What Backend Sends to This Service

Backend sends **everything at once**.

### ✅ Input Payload (`POST /process-event`)

```json
{
  "event_id": "evt_123",
  "users": [
    {
      "user_id": "user_1",
      "image_url": "https://cdn.app.com/selfies/u1.jpg"
    }
  ],
  "photos": [
    {
      "photo_id": "photo_1",
      "url": "https://cdn.app.com/events/e1/p1.jpg"
    }
  ],
  "callback_url": "https://api.backend.com/internal/photo-results"
}
```

### 🔹 Input Rules

#### Users

* Backend sends **ALL attendee selfie URLs at once**
* One selfie per user
* Image should clearly contain the user’s face

#### Photos

* Backend sends **ALL event photos at once**
* URLs must be publicly accessible or signed
* Photos may contain:

  * multiple faces
  * no faces
  * irrelevant faces (handled safely)

#### Callback URL

* Backend provides a **single callback endpoint**
* AI service posts final results here
* Optional but strongly recommended

---

## ⚙️ What the AI Service Does Internally

### Step 1: User Identity Preparation

* Downloads each user selfie
* Detects face (expects 1, handles more)
* Generates **512-D ArcFace embedding**
* Stores embeddings **in memory only**

### Step 2: Event Photo Processing

* Photos are processed in **batches**
* Batches are distributed across **multiple CPU processes**
* Each process:

  * Loads models safely
  * Downloads images
  * Detects faces
  * Generates embeddings
  * Matches with user embeddings

### Step 3: Matching Logic

* Uses **cosine similarity**
* Default threshold: `0.65`
* Produces `(user_id, photo_id, confidence)` tuples

### Step 4: Result Delivery

* Aggregates all matches
* Sends results to backend via `callback_url`

---

## 📤 What Backend Receives (Output)

### ✅ Callback Payload

```json
{
  "results": [
    {
      "event_id": "evt_123",
      "photo_id": "photo_45",
      "user_id": "user_7",
      "confidence": 0.82
    }
  ]
}
```

### 🔹 Output Guarantees

* One record = one **user × photo** match
* Same event_id across payload
* Confidence score already computed
* No images, no embeddings, no ML artifacts

---

## 🧠 Backend Responsibilities (Important)

The backend is expected to:

1. **Store results**
2. **Apply product rules**
3. **Serve UI**

### ❌ Backend Should NOT

* Detect faces
* Generate embeddings
* Decide ML thresholds
* Poll the AI service

---

## 🧩 Product Logic (Backend Side)

The AI service intentionally returns **raw matches**.
Backend applies business logic such as:

### Option 1: One Photo → One User

* For each photo, keep the highest-confidence user

### Option 2: Confidence Bucketing (Recommended)

| Confidence | Meaning             |
| ---------- | ------------------- |
| > 0.85     | Definitely the user |
| 0.70–0.85  | Probably the user   |
| < 0.70     | Ignore              |

### Option 3: Deduplication

* Prevent same photo showing twice to same user

These rules **must live in backend**, not AI.

---

## 📂 Folder Structure (Detailed)

```
photo-ai-service/
│
├── app/
│   ├── api/
│   │   └── routes.py                # FastAPI endpoints
│   │
│   ├── schemas/
│   │   └── event_payload.py         # Input/output contracts
│   │
│   ├── pipelines/
│   │   ├── detect_faces.py          # Face detection (RetinaFace)
│   │   ├── generate_embed.py        # Face embedding (ArcFace)
│   │   ├── generate_user_embeddings.py
│   │   └── match_faces.py           # Cosine similarity matching
│   │
│   ├── workers/
│   │   └── photo_worker.py           # Multiprocessing-safe worker
│   │
│   ├── services/
│   │   ├── image_loader.py           # Download + decode images
│   │   └── callback.py               # Send results to backend
│   │
│   ├── utils/
│   │   ├── batching.py               # Batch helpers
│   │   └── similarity.py             # Cosine similarity
│   │
│   ├── config.py                     # Central configuration
│   └── main.py                       # FastAPI app entry
│
├── venv/                             # Python virtual environment
├── requirements.txt
└── README.md
```

---

## 🧪 Testing & Validation

### Health Check

```
GET /health
```

### Swagger UI

```
http://localhost:8000/docs
```

### Bulk Testing

* Backend can send:

  * 50 users
  * 300+ photos
* System processes safely using multiprocessing

---

## 🚀 Performance Characteristics

| Scenario             | Expected Behavior  |
| -------------------- | ------------------ |
| 1 user, 10 photos    | < 10 seconds       |
| 10 users, 100 photos | ~1–2 minutes       |
| 50 users, 300 photos | ~3–4 minutes (CPU) |

Scales with CPU cores.

---

## 🔐 Privacy & Security

* Face embeddings **never leave AI service**
* Backend never stores biometric vectors
* URLs can be signed / expiring
* Callback endpoint can be internal / protected

---

## ❗ Failure Handling

* Broken image URLs → skipped
* No faces → skipped
* One batch failure → event continues
* Service never crashes mid-event

---

## 🛠 Configuration (Key Knobs)

```python
FACE_DETECTION_THRESHOLD = 0.6
FACE_MATCH_THRESHOLD = 0.65
PHOTO_BATCH_SIZE = 8
MAX_WORKERS = CPU_COUNT - 1
```

---

## 📌 What This System Is NOT

* ❌ Real-time streaming
* ❌ Video processing
* ❌ Face verification / authentication
* ❌ Law-enforcement grade biometric system

It is an **event discovery & experience feature**, not surveillance.

---

## ✅ Final Summary

✔ Backend sends everything once
✔ AI processes asynchronously & in parallel
✔ Results auto-returned via callback
✔ Backend owns UX & rules
✔ Scales safely
✔ Production-ready

---

## ✨ Status

**System is complete, tested, and production-grade.**


