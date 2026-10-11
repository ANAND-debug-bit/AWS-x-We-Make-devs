# 🩺 Aero-Match: Symptom-to-Pollutant AI Diagnostic Tool



## About the Project

* **The Problem:** Air pollution is a silent, pervasive crisis, and millions of people experience recurring physical symptoms such as dry or burning eyes, coughing, shortness of breath, sudden headaches, or wheezing without knowing which specific pollutant is triggering their discomfort. Existing air quality apps only display numbers like an AQI of 350 or a PM2.5 level, but they fail to connect those numbers to human health symptoms or offer any personalized guidance.
* **The Solution (Aero-Match):** Aero-Match is an intelligent, real-time diagnostic web tool that bridges the gap between environmental monitoring and personal health. Users type their physical symptoms in natural language and select any pre-existing medical conditions, such as Asthma/COPD or severe allergies, and the tool then does the following:
  1. It maps their symptoms to specific airborne pollutants (PM2.5, PM10, NO2, O3, SO2, and CO).
  2. It pulls live, hyper-local air quality readings through GPS or location lookup.
  3. It delivers actionable mitigation steps and safety recommendations through **Dr. Pal**, an interactive AI health assistant.
  4. It maintains consultation audit logs and calculates a safety trust score.
* **Target Audience:**
  * Urban residents living in high-AQI regions benefit from understanding what is actually affecting them.
  * Individuals with pre-existing respiratory or cardiovascular conditions, such as asthma, COPD, or chronic sinus issues, get personalized guidance.
  * Community health advocates and environmental researchers can study local exposure patterns.

---

## How AWS Is Used

* **AWS Open Source Stack:**
  * **AWS SAM (Serverless Application Model)** is used to define, build, and package the serverless architecture as Infrastructure as Code in `template.yaml`.
  * **LocalStack**, set up through `localstack_setup.sh`, simulates AWS services locally at `http://localhost:4566`, which allows rapid offline development, testing, and debugging of Lambda functions and DynamoDB tables without incurring cloud costs.
  * **Python AWS SDK (`boto3`)** is used for programmatic database operations, item persistence, and querying audit trails.

* **AWS Services:**
  * **AWS Lambda** (`backend/symptom_agent.py`) powers the core serverless backend by parsing natural language symptoms, mapping them to pollutant profiles, integrating with external meteorological APIs, and returning real-time diagnostic responses.
  * **Amazon DynamoDB** (`aero_match_logs`) serves as the scalable NoSQL data store for consultation logs, audit histories, repeat frequency tracking, and symptom tags, using on-demand billing (`PAY_PER_REQUEST`).
  * **Amazon API Gateway** exposes the RESTful HTTP endpoints `/diagnose` and `/audit`, routing client requests securely to the Lambda backend.

---

##  How to Run Locally

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

## Key Features

1. **Hyper-Local Air Telemetry**: Fetches real-time pollutant readings (PM2.5, PM10, NO2, Ozone, SO2, CO) from the free Open-Meteo Air Quality API using GPS coordinates or city/locality autocomplete.
2. **Pre-Existing Medical Conditions Checkboxes**: During registration, users can select pre-existing health conditions (*Asthma / COPD, Heart Disease / Hypertension, Severe Allergies, Chronic Sinusitis / Migraine*) to personalize diagnostics.
3. **Internal Issue Flagging & Audit Log**: Tracks consultation history against audit records. If identical symptoms recur or correlate with pre-existing conditions, the app flags probable internal health issues and suggests consulting a doctor.
4. **AI Trust Score Calculation**: Dynamically computes a safety trust score badge factoring in repeat frequency and medical history against clinical thresholds.
5. **Dr. Pal Doctor Agent**: An interactive penguin health companion (`🐧`) providing instant guidance and safety warnings.

---

## Project Directory Structure

```text
AWS-x-We-Make-devs/
├── frontend.html                  # Full-stack Interactive UI (Dr. Pal, Registration, GPS, Trust Score, Audit)
├── template.yaml                  # AWS SAM Template for Serverless Stack
├── localstack_setup.sh            # LocalStack local testing script
├── backend/
     └── symptom_agent.py          # Core AI Mapping Logic & AWS Lambda Handler
```
