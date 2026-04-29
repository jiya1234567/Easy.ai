# Deployment Script for Universal Lab to Google Cloud Run
# Project: thinking-avenue-475805-v1

$PROJECT_ID = "project-b189cc95-d807-4fa2-976"
$REGION = "us-central1"
$SERVICE_NAME = "universal"

Write-Host "--- Starting Deployment to Google Cloud Run ---" -ForegroundColor Cyan

# 1. Set the project
Write-Host "Setting project to $PROJECT_ID..."
gcloud.cmd config set project $PROJECT_ID

# 2. Enable necessary APIs
Write-Host "Ensuring necessary APIs are enabled..."
gcloud.cmd services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com

# 3. Build and push the image using Cloud Build
Write-Host "Building and pushing container image..."
gcloud.cmd builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# 4. Deploy to Cloud Run
Write-Host "Deploying to Cloud Run..."
$API_KEY = $env:GEMINI_API_KEY
if (-not $API_KEY) {
    $API_KEY = Read-Host "Please enter your GEMINI_API_KEY (or press enter to skip and set later in Console)"
}

if ($API_KEY) {
    gcloud.cmd run deploy $SERVICE_NAME `
        --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
        --platform managed `
        --region $REGION `
        --allow-unauthenticated `
        --memory 2Gi `
        --cpu 1 `
        --timeout 300 `
        --set-env-vars "GEMINI_API_KEY=$API_KEY"
} else {
    gcloud.cmd run deploy $SERVICE_NAME `
        --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
        --platform managed `
        --region $REGION `
        --allow-unauthenticated `
        --memory 2Gi `
        --cpu 1 `
        --timeout 300
}

Write-Host "--- Deployment Complete ---" -ForegroundColor Green
Write-Host "The URL above is your mobile-accessible link." -ForegroundColor Cyan
