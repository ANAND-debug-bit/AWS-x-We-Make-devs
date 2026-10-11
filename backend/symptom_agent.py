import os
import json
import re
import urllib.request
from datetime import datetime, timedelta, timezone
import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB client (dynamically targets LocalStack if endpoint is set)
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.environ.get('DYNAMODB_ENDPOINT_URL') # e.g. http://localhost:4566 for LocalStack
)
TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME', 'aero_match_logs')

# Exact Pollutant and Symptom Knowledge Base
POLLUTANT_MAPPING = {
    "PM2.5": {
        "symptoms": ["shortness of breath", "chest tightness", "severe coughing", "asthma", "headache", "dizziness", "fatigue", "brain fog"],
        "action": "Turn on your HEPA air purifier immediately, close all windows, and avoid strenuous outdoor activity."
    },
    "PM10": {
        "symptoms": ["eye irritation", "redness", "watering", "sneezing", "runny nose", "hay fever", "skin rash", "itching"],
        "action": "Use lubricating eye drops, turn on a humidifier, wash your face/hands, and keep windows shut."
    },
    "NO2": {
        "symptoms": ["wheezing", "coughing", "sudden headache", "migraine"],
        "action": "Stay indoors away from heavy traffic corridors, turn on an air purifier with activated carbon, and avoid deep breathing."
    },
    "O3": {
        "symptoms": ["pain when taking a deep breath", "scratchy throat", "eye burning", "skin discomfort"],
        "action": "Remain indoors, avoid afternoon outdoor exposure when ozone peaks, and use throat lozenges or drink cool water."
    },
    "SO2": {
        "symptoms": ["airway constriction", "asthma attack", "chest pain"],
        "action": "Use your prescribed rescue inhaler if needed, stay indoors, close all windows, and run an air purifier."
    },
    "CO": {
        "symptoms": ["fatigue", "dizziness", "nausea", "chest pain"],
        "action": "Ventilate the space immediately if indoor source suspected, check CO detectors, and move to fresh air if symptoms persist."
    }
}

def fetch_open_meteo_aqi(lat: float, lon: float) -> dict:
    """Fetches real-time air quality data from the free Open-Meteo Air Quality API."""
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AeroMatch-MVP'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get("current", {})
    except Exception as e:
        print(f"Error fetching Open-Meteo data: {e}")
        return {}

def match_symptoms_to_culprit(user_text: str) -> list:
    """Maps user's natural language input to probable pollutants."""
    user_text_lower = user_text.lower()
    matched_culprits = []
    
    for pollutant, info in POLLUTANT_MAPPING.items():
        score = sum(1 for symptom in info["symptoms"] if symptom in user_text_lower)
        if score > 0:
            matched_culprits.append({
                "pollutant": pollutant,
                "score": score,
                "action": info["action"]
            })
            
    # Sort by relevance score
    matched_culprits.sort(key=lambda x: x["score"], reverse=True)
    return matched_culprits

def log_diagnosis_to_dynamodb(user_input: str, diagnosis: dict):
    """Logs the interaction to DynamoDB for audit and telemetry."""
    try:
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                'id': str(os.urandom(8).hex()),
                'user_input': user_input,
                'diagnosis': json.dumps(diagnosis),
                'timestamp': str(os.getenv('TIMESTAMP', 'now'))
            }
        )
    except Exception as e:
        print(f"Failed to log to DynamoDB: {e}")

def audit_counts(user_id: str, tags: list, days: int = 30) -> dict:
    """Count how often each symptom tag was logged for this user in the last `days` days."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    items = dynamodb.Table(TABLE_NAME).query(
        IndexName="user_ts", KeyConditionExpression=Key("user_id").eq(user_id) & Key("ts").gte(cutoff)
    ).get("Items", [])
    counts = {t: 0 for t in tags}
    for it in items:
        for t in (it.get("tags") or "").split(","):
            if t in counts:
                counts[t] += 1
    return counts


def audit_handler(event):
    """GET /audit?user_id=..&tags=a,b&culprit=PM2.5&log=1 -> prior counts, then logs this check."""
    q = event.get("queryStringParameters") or {}
    user_id = q.get("user_id", "")
    tags = [t for t in q.get("tags", "").split(",") if re.fullmatch(r"[a-z_]{1,20}", t)]
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", user_id):
        return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"}, "body": json.dumps({"error": "bad user_id"})}
    try:
        counts = audit_counts(user_id, tags)
        if q.get("log") == "1" and tags:
            dynamodb.Table(TABLE_NAME).put_item(Item={
                "id": os.urandom(8).hex(), "user_id": user_id, "ts": datetime.now(timezone.utc).isoformat(),
                "tags": ",".join(tags), "culprit": q.get("culprit", "")[:10]})
    except Exception as e:
        print(f"audit failure: {e}")
        return {"statusCode": 502, "headers": {"Access-Control-Allow-Origin": "*"}, "body": json.dumps({"error": "audit unavailable"})}
    return {"statusCode": 200, "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}, "body": json.dumps({"counts": counts})}


def lambda_handler(event, context):
    """AWS Lambda Entrypoint for Aero-Match backend service."""
    if str(event.get("path", "")).endswith("/audit"):
        return audit_handler(event)
    print(f"Received event: {json.dumps(event)}")
    
    # Parse query or body parameters
    body = {}
    if "body" in event:
        try:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
        except:
            body = {}
            
    params = event.get("queryStringParameters") or body or {}
    user_text = params.get("symptoms", "I have a headache and eye burning")
    lat = float(params.get("lat", 28.6139)) # Default: New Delhi
    lon = float(params.get("lon", 77.2090))
    
    # 1. Map user text to probable pollutant
    matched_culprits = match_symptoms_to_culprit(user_text)
    
    # 2. Fetch real-time live air quality data from Open-Meteo
    live_aqi = fetch_open_meteo_aqi(lat, lon)
    
    # 3. Cross-reference symptoms with live data levels
    primary_culprit = matched_culprits[0] if matched_culprits else {
        "pollutant": "PM2.5", 
        "action": "Keep windows closed and run an air purifier as a general precaution."
    }
    
    response_payload = {
        "status": "success",
        "user_complaint": user_text,
        "location": {"lat": lat, "lon": lon},
        "probable_culprit": primary_culprit["pollutant"],
        "recommended_action": primary_culprit["action"],
        "live_readings": live_aqi,
        "all_matched_pollutants": matched_culprits
    }
    
    # 4. Log to DynamoDB
    log_diagnosis_to_dynamodb(user_text, response_payload)
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response_payload)
    }
