# 🔌 API Integration & Core Payload Reference: Sepsis Monitor AI (Part 1)

This document provides technical specifications, environment configuration requirements, payload schemas, and defensive fallback behavior for the external cloud interfaces utilized by the platform.

---

## ⚙️ 1. Required Infrastructure Environment Variables

The application isolates all infrastructure credentials and configuration values. The following variables must be declared inside the root `.env` file for local development or injected securely into the container runtime environment:

```env
GROQ_API_KEY="gsk_..."             # Groq Cloud API credential
TWILIO_ACCOUNT_SID="AC..."         # Twilio Account SID
TWILIO_AUTH_TOKEN="your_token"     # Twilio authentication token
TWILIO_CLINICAL_PHONE="+407XXXXXX" # Target mobile number for emergency SMS alerts
TWILIO_TWILIO_PHONE="+1XXXXXXXXXX" # Outbound system Twilio virtual phone number
DATABASE_URL="sqlite:///sepsis_v2.db" # Database connection URL
```

---

## 🧠 2. Groq Cloud LPU Inference API Engine & Security Gateway

The platform routes text-augmented generation requests to low-latency Groq Processing units to build the virtual medical board diagnostics framework, running behind a strict server-side protection gate.

### Hardware Mapping & LLM Profile
*   **Target Core Endpoint**: `https://groq.com`
*   **Active Processing Core**: `groq:llama-3.3-70b-versatile` (Enterprise grade production model)
*   **Strict Inference Hyperparameters**: `temperature=0.1`, `max_tokens=1024` (Enforces absolute clinical determinism and eliminates conversational drift).

### Synchronous Regex Firewall Interception
Before context transmission to the Groq SDK client layer, the runtime compiled prompt vector is routed through an explicit synchronous validation function (`sanitize_clinical_payload`). This filter checks for word boundaries (`\b(IGNORE|OVERRIDE|CLEAN|SYSTEM RESET|DAN)\b`). If an adversarial prompt injection payload is captured, it is stripped and replaced by safe tokens (`[BLOCKED_ADVERSARIAL_ATTEMPT]`), dropping the exploit block before consuming Groq API tokens.

### Ingestion Payload Schema (JSON Context Integration)
The system serializes active clinical data points, dynamic calculated mass metrics, and family-centered care variables into the following context package matching the `telemetry` schema:

```json
{
  "weight_kg": 2.50,
  "heart_rate": 135,
  "temperature": 36.8,
  "oxygen_saturation": 98.0,
  "blood_pressure": "67/39 mmHg",
  "crp_level": 5.0,
  "pct_level": 0.5,
  "kangaroo_care_active": "Active / In Bratele Mamei",
  "renal_status_active": "Normal Baseline / Functie Normala",
  "music_therapy_active": "Active / Meloterapie Pornita"
}
```

### Semantic Encapsulation Expectations
The model output is strictly bounded via prompt engineering to return a formatted response partitioned inside explicit semantic XML boundaries for downstream text parsing:
*   `<RAPORT>`: Deep diagnostic and physiological trend analytics.
*   `<MEDICATIE>`: Validated antibiotic dosage verifications (**Ampicillin + Gentamicin**).
*   `<FCC>`: Non-pharmacological incubator environmental evaluation.

# 🔌 API Integration & Core Payload Reference: Sepsis Monitor AI (Part 2)

---

## 📱 3. Twilio SMS Emergency Alert Gateway

When critical clinical triggers are hit (`system_is_stable = False` caused by high temperature, tachycardia, or critical inflammatory trends), the platform bypasses passive web rendering and initializes an outbound REST call to the Twilio communication infrastructure via the native background loop.

### Technical Access Infrastructure
*   **Target URI Endpoint**: `https://twilio.com{AccountSid}/Messages.json`
*   **Authentication Mechanism**: HTTP Basic Auth (Utilizing `TWILIO_ACCOUNT_SID` as username and `TWILIO_AUTH_TOKEN` as password).
*   **Transmission Channel**: Secure REST POST requests.

### Outbound Alert Payload Schema (SMS String Data)
The system assembles real-time physiological telemetry parameters and laboratory biomarkers directly into a high-visibility text message formatted for immediate clinical triage:

```text
📱 LIVE ALERT -> Automatic SMS transmission via Twilio Gateway to [NICU Chief of Department/Physician on Duty] activated.

Payload: CRITICAL SEPSIS RISK ALERT - HR: 172, Temp: 39.1. Check Dashboard immediately for empirical protocol administration.
```

---

## 🛡️ 4. Defensive API Disruption Handling & Fallback Controls

To prevent runtime application locking or freezing during high-acuity operations, the network communication layer incorporates a strict defensive fault-tolerance setup:

### 1. Silent Exception Trapping
All external web requests or client handshakes (such as Groq SDK completions or Twilio REST dispatches) are encapsulated within robust `try/except` blocks. Network delay or dropouts are handled gracefully using local fail-safe exception blocks, logging trace logs to system outputs without corrupting the active user session state.

### 2. Local Deterministic Recovery
If the external Groq cloud infrastructure suffers an outage, the platform immediately aborts the active REST pipeline and falls back onto local, hardcoded medical protocols:
*   **Hyperinflammatory Fallback**: Automatically renders pre-validated fallback error tags directly inside the Streamlit informational tabs (`AI Decision Support`) based on the active interface language configuration.
*   **Zero Interface Disruption**: Guarantees that the underlying SQLite relational logging, line chart rendering, in-memory PDF generation, and background `womb_heartbeat.mp3` audio streams continue running completely offline without freezing the clinical UI web viewport.
