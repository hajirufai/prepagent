#!/bin/bash
# Deploy PrepAgent to Google Cloud Run
# Uses Vertex AI (charged to project, uses $1000 credits)
# Uses MongoDB Atlas for data storage

set -e

PROJECT_ID="interview-buddy-457520"
REGION="us-central1"
SERVICE_NAME="prepagent"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

MONGODB_URI="mongodb+srv://prepagent:PrepAgent2026!Hackathon@prepagentcluster.z1ydauh.mongodb.net/?retryWrites=true&w=majority"

echo "=== Building Docker image ==="
gcloud builds submit --tag ${IMAGE} --project ${PROJECT_ID}

echo "=== Deploying to Cloud Run ==="
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE} \
  --platform managed \
  --region ${REGION} \
  --project ${PROJECT_ID} \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 3 \
  --set-env-vars "MONGODB_URI=${MONGODB_URI}" \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=${PROJECT_ID}" \
  --set-env-vars "GOOGLE_CLOUD_LOCATION=${REGION}" \
  --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=TRUE"

echo "=== Done ==="
URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --project ${PROJECT_ID} --format='value(status.url)')
echo "PrepAgent is live at: ${URL}"
