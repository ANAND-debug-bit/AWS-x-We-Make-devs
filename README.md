# 🩺 Aero-Match: Symptom-to-Pollutant AI Diagnostic Tool

> **Hackathon:** Environmental Hacks (AWS Bharat Builds Tour) — **Air Track**  
> **Goal:** Build an intuitive, real-time diagnostic AI tool that maps physical human symptoms to hyper-local air pollutants using Open-Meteo, AWS Lambda, DynamoDB, and Serverless architectures.

---

## 🚀 Run the Application Live

👉 **[Click Here to Open Aero-Match Live Preview & Web App](https://ANAND-debug-bit.github.io/AWS-x-We-Make-devs/preview.html)** *(or open `frontend.html` locally in any browser)*

---

## ✨ Key Features

1. **Hyper-Local Air Telemetry**: Fetches real-time pollutant readings (PM2.5, PM10, NO2, Ozone, SO2, CO) from the free Open-Meteo Air Quality API using GPS coordinates or city/locality autocomplete.
2. **Pre-Existing Medical Conditions Checkboxes**: During registration, users can select pre-existing health conditions (*Asthma / COPD, Heart Disease / Hypertension, Severe Allergies, Chronic Sinusitis / Migraine*) to personalize diagnostics.
3. **Internal Issue Flagging & DynamoDB Audit Log**: Tracks consultation history against audit records. If identical symptoms recur or correlate with pre-existing conditions, the app flags probable internal health issues.
4. **AI Trust Score Calculation**: Dynamically computes a safety trust score badge factoring in repeat frequency and medical history against clinical thresholds.
5. **Dr. Pal Doctor Agent**: An interactive penguin health companion providing instant guidance and safety warnings.

---

## 📂 Project Directory Structure

```text
AWS-x-We-Make-devs/
├── frontend.html                  # Full-stack Interactive UI (Dr. Pal, Registration, GPS, Trust Score, Audit)
├── template.yaml                  # AWS SAM CLI Template for Serverless Stack
├── localstack_setup.sh            # LocalStack local development & test script
├── backend/
     └── symptom_agent.py          # Core AI Mapping Logic, Open-Meteo API & Lambda Handler
```

---

## 🛠️ 1. BUILD IT (Local Development & Testing with LocalStack & SAM)

### Prerequisites
- Docker & Docker Compose
- AWS SAM CLI (`sam`)
- Python 3.11+

### Step-by-Step Local Setup

1. **Start LocalStack & Build the SAM Project:**
   ```bash
   ./localstack_setup.sh
   ```

2. **Run the API Locally:**
   ```bash
   sam local start-api
   ```

3. **Test the Diagnosis API:**
   Run the following `curl` command in a separate terminal tab:
   ```bash
   curl -G "http://127.0.0.1:3000/diagnose" \
     --data-urlencode "symptoms=My eyes are burning and I woke up with a headache" \
     --data-urlencode "lat=19.0596" \
     --data-urlencode "lon=72.8295"
   ```

---

## 🚢 2. SHIP IT (Deploying to AWS Cloud)

When ready to deploy your production MVP to AWS Lambda, API Gateway, and DynamoDB:

1. **Configure AWS Credentials:**
   ```bash
   aws configure
   ```

2. **Deploy via SAM CLI (Guided):**
   ```bash
   sam deploy --guided
   ```
   *(Follow the prompts: accept defaults like stack name `aero-match-prod`, region `us-east-1` or your preferred region, and confirm changes).*
