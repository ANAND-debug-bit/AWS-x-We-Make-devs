# 🩺 Aero-Match: Symptom-to-Pollutant AI Diagnostic Tool

> **Hackathon:** Environmental Hacks (AWS Bharat Builds Tour) — **Air Track**  
> **Goal:** An intuitive, real-time diagnostic AI tool that maps physical human symptoms to hyper-local air pollutants using Open-Meteo, client-side intelligence, and interactive health agents.

---

## 🚀 How to Run Locally

To run Aero-Match instantly, simply download or clone this repository, and open **`frontend.html`** in any web browser:
```bash
open frontend.html
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
├── backend/
     └── symptom_agent.py          # Core AI Mapping Logic & Open-Meteo API integration
```
