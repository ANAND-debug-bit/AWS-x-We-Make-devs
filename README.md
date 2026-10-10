# Aero-Match: Symptom-to-Pollutant AI Diagnostic Tool

> **Hackathon:** Environmental Hacks (AWS Bharat Builds Tour) — **Air Track**  
> **Goal:** Build an intuitive, real-time diagnostic AI tool that maps physical human symptoms to hyper-local air pollutants using Open-Meteo, AWS Lambda, DynamoDB, and Amazon Bedrock/SageMaker.

---

## 📂 Project Directory Structure

To adhere to the hackathon's modularity rules and prevent `main.py` merge conflicts, all service components are structured modularly:

```text
AWS-x-We-Make-devs/
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
     --data-urlencode "lat=28.6139" \
     --data-urlencode "lon=77.2090"
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
   *Follow the prompts (accept defaults: stack name `aero-match-prod`, region `us-east-1` or your preferred region, confirm changes).*

---

## 🧠 3. Core AI Agent & Data Mapping Logic (`symptom_agent.py`)

The core script implements:
- **Natural Language Parsing:** Scans user statements against predefined medical symptom clusters (`PM2.5`, `PM10`, `NO2`, `O3`, `SO2`, `CO`).
- **Real-Time Data Integration:** Calls the free **Open-Meteo Air Quality API** to pull live regional pollutant levels.
- **Actionable Prescriptions:** Provides immediate, practical recommendations (e.g., turning on HEPA purifiers, closing windows, using lubricating eye drops).
- **Audit & Telemetry:** Logs all diagnostic interactions directly into **Amazon DynamoDB**.
