# Deployment Script for Universal Lab to Google Cloud Run
# Project: asi-resh
# Service: streamlit-mistral-app

$PROJECT_ID = "asi-resh"
$REGION = "us-central1"
$SERVICE_NAME = "streamlit-mistral-app"

Write-Host "--- Starting Deployment to Google Cloud Run ---" -ForegroundColor Cyan

# 1. Set the project
Write-Host "Setting project to $PROJECT_ID..."
gcloud.cmd config set project $PROJECT_ID

# 2. Enable necessary APIs
Write-Host "Ensuring necessary APIs are enabled..."
gcloud.cmd services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com

# 3. Build and push the image using Cloud Build
Write-Host "Building and pushing container image..."
gcloud.cmd builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# 4. Deploy to Cloud Run
Write-Host "Deploying to Cloud Run..."

# We use --set-secrets for production-grade security as per the Mistral Guide Step 4.
# This assumes you have created a secret named MISTRAL_API_KEY in Secret Manager.
gcloud.cmd run deploy $SERVICE_NAME `
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --port 8501 `
    --memory 2Gi `
    --cpu 1 `
    --timeout 300 `
    --set-secrets="MISTRAL_API_KEY=MISTRAL_API_KEY:latest"

Write-Host "--- Deployment Complete ---" -ForegroundColor Green
Write-Host "The URL above is your mobile-accessible link." -ForegroundColor Cyan
