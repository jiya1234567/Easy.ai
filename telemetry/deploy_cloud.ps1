# Deployment Script for OMEGA-CORE Telemetry Dashboard to Google Cloud Run
# Optimization: This script runs from the telemetry directory

$PROJECT_ID = "thinking-avenue-475805-v1"
$REGION = "us-central1"
$SERVICE_NAME = "telemetry-omega-dashboard"

Write-Host "--- Initiating Cloud Stress Test Deployment ---" -ForegroundColor Cyan

# 1. Set the project
Write-Host "Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# 2. Enable necessary APIs
Write-Host "Ensuring necessary Google Cloud APIs are enabled..."
gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com

# 3. Build and push the image using Cloud Build
Write-Host "Building and pushing container image from telemetry baseline..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME .

# 4. Deploy to Cloud Run
Write-Host "Deploying to Cloud Run for Stress Testing..."
$API_KEY = $env:GEMINI_API_KEY
if (-not $API_KEY) {
    # Check if we can pull it from .env
    if (Test-Path ".env") {
        $env_content = Get-Content ".env"
        foreach ($line in $env_content) {
            if ($line -match "GEMINI_API_KEY=(.*)") {
                $API_KEY = $matches[1]
                break
            }
        }
    }
}

if (-not $API_KEY) {
    $API_KEY = Read-Host "Please enter your GEMINI_API_KEY"
}

if ($API_KEY) {
    gcloud run deploy $SERVICE_NAME `
        --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
        --platform managed `
        --region $REGION `
        --allow-unauthenticated `
        --memory 2Gi `
        --cpu 1 `
        --timeout 300 `
        --set-env-vars "GEMINI_API_KEY=$API_KEY"
} else {
    gcloud run deploy $SERVICE_NAME `
        --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
        --platform managed `
        --region $REGION `
        --allow-unauthenticated `
        --memory 2Gi `
        --cpu 1 `
        --timeout 300
}

Write-Host "--- Cloud Stress Test Environment Ready ---" -ForegroundColor Green
Write-Host "Use the provided URL to access the dashboard and run Adversarial Stress Tests." -ForegroundColor Cyan
