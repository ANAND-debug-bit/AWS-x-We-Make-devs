# 🩺 Aero-Match: Symptom-to-Pollutant AI Diagnostic Tool

> **Hackathon:** Environmental Hacks (AWS Bharat Builds Tour) — **Air Track**  
> **Goal:** An intuitive, real-time diagnostic AI tool that maps physical human symptoms to hyper-local air pollutants using Open-Meteo, AWS serverless architecture, and interactive health agents.

---

## 📋 Hackathon Submission Questionnaire & Answers

### 1. What does your project do? 
**What problem does your project solve, and who is it for?**

* **The Problem:** Air pollution is a silent, pervasive crisis. Millions of people experience recurring physical symptoms (such as dry/burning eyes, coughing, shortness of breath, sudden headaches, or wheezing) without knowing which specific pollutant is triggering their discomfort. Existing air quality apps only display numbers (like AQI 350 or PM2.5 levels) but fail to connect those numbers directly to human health symptoms or provide personalized guidance.
* **The Solution (Aero-Match):** Aero-Match is an intelligent, real-time diagnostic web tool that bridges the gap between environmental monitoring and personal health. Users can type in their physical symptoms in natural language, select pre-existing medical conditions (such as Asthma/COPD or severe allergies), and instantly receive:
  1. A diagnosis mapping their symptoms to specific airborne pollutants (PM2.5, PM10, NO2, O3, SO2, CO).
  2. Live hyper-local air quality readings via GPS/location lookup.
  3. Actionable mitigation steps and safety recommendations delivered by **Dr. Pal**, an interactive AI health assistant.
  4. Consultation audit logs and safety trust score calculations.
* **Target Audience:** 
  * Urban residents living in high-AQI regions.
  * Individuals with pre-existing respiratory or cardiovascular conditions (Asthma, COPD, chronic sinus issues).
  * Community health advocates and environmental researchers seeking local exposure patterns.

---

### 2. How did you use AWS in your project? 
**Tell us what your project does and how you have used AWS in your project:**

* **AWS Open Source Stack:**
  * **AWS SAM (Serverless Application Model):** Utilized for defining, building, and packaging our serverless architecture as Infrastructure as Code (`template.yaml`).
  * **LocalStack:** Integrated via `localstack_setup.sh` to simulate AWS services locally (`http://localhost:4566`), enabling rapid offline development, testing, and debugging of Lambda functions and DynamoDB tables without incurring cloud costs during development.
  * **Python AWS SDK (`boto3`):** Utilized for programmatic database operations, item persistence, and querying audit trails.

* **AWS Services:**
  * **AWS Lambda (`backend/symptom_agent.py`):** Powers the core serverless backend. It handles natural language symptom parsing, maps symptoms to pollutant profiles, integrates with external meteorological APIs, and returns real-time diagnostic responses.
  * **Amazon DynamoDB (`aero_match_logs`):** Serves as our scalable NoSQL data store. It stores consultation logs, audit histories, repeat frequency tracking, and symptom tags with on-demand billing (`PAY_PER_REQUEST`).
  * **Amazon API Gateway:** Exposes RESTful HTTP endpoints (`/diagnose` and `/audit`) routing client requests securely to our AWS Lambda backend function.

---

## 🚀 How to Run Locally

To run Aero-Match instantly, simply download or clone this repository, and open **`frontend.html`** in any web browser:
```bash
open frontend.html
```

### Running with AWS SAM & LocalStack (Optional)
```bash
# 1. Start LocalStack and build SAM application
./localstack_setup.sh

# 2. Run local API server
sam local start-api --warm-containers EAGER --skip-pull-image
```

---

## ✨ Key Features

1. **Hyper-Local Air Telemetry**: Fetches real-time pollutant readings (PM2.5, PM10, NO2, Ozone, SO2, CO) from the free Open-Meteo Air Quality API using GPS coordinates or city/locality autocomplete.
2. **Pre-Existing Medical Conditions Checkboxes**: During registration, users can select pre-existing health conditions (*Asthma / COPD, Heart Disease / Hypertension, Severe Allergies, Chronic Sinusitis / Migraine*) to personalize diagnostics.
3. **Internal Issue Flagging & Audit Log**: Tracks consultation history against audit records. If identical symptoms recur or correlate with pre-existing conditions, the app flags probable internal health issues and suggests consulting a doctor.
4. **AI Trust Score Calculation**: Dynamically computes a safety trust score badge factoring in repeat frequency and medical history against clinical thresholds.
5. **Dr. Pal Doctor Agent**: An interactive penguin health companion (`🐧`) providing instant guidance and safety warnings.

---

## 📂 Project Directory Structure

```text
AWS-x-We-Make-devs/
├── frontend.html                  # Full-stack Interactive UI (Dr. Pal, Registration, GPS, Trust Score, Audit)
├── template.yaml                  # AWS SAM Template for Serverless Stack
├── localstack_setup.sh            # LocalStack local testing script
├── backend/
     └── symptom_agent.py          # Core AI Mapping Logic & AWS Lambda Handler
```
