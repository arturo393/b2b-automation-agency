#!/bin/bash
set -e

# Configuration
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
IMAGE_NAME="hunter-agent"
REPO_NAME="agency-repo"
IMAGE_TAG="latest"

echo "🚀 Starting Deployment for Project: $PROJECT_ID"

# 1. Enable Artifact Registry (if not enabled via Terraform yet, need it for push)
echo "📦 Enabling Artifact Registry API..."
gcloud services enable artifactregistry.googleapis.com

# 2. Check if Repo exists, create if not (Terraform manages this, but we need it for push before apply sometimes)
# Actually, let's run Terraform first to create the repo, then push, then update job?
# Chicken-egg problem. Terraform creates repo. We push. Terraform creates Job using image.
# So: Terraform Target Repo -> Push -> Terraform Full Apply.

echo "🏗️  Initializing Terraform..."
cd infrastructure
terraform init

echo "🧱 Creating Artifact Registry first..."
terraform apply -target=google_artifact_registry_repository.repo -var="project_id=$PROJECT_ID" -var="region=$REGION" -var="gemini_api_key=$GEMINI_API_KEY" -auto-approve

# 3. Build & Push Docker Image
echo "🐳 Building Docker Image..."
cd ..
# Configure Docker auth
gcloud auth configure-docker ${REGION}-docker.pkg.dev

IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${IMAGE_TAG}"
docker build -t $IMAGE_URI .
docker push $IMAGE_URI

# 4. Full Terraform Apply
echo "🌍 Deploying Cloud Run Job..."
cd infrastructure
terraform apply -var="project_id=$PROJECT_ID" -var="region=$REGION" -var="gemini_api_key=$GEMINI_API_KEY" -auto-approve

echo "✅ Deployment Complete!"
echo "🏃 Executing Job for Demo..."
gcloud run jobs execute hunter-agent-job --region=$REGION

echo ""
echo "🛑 Press ENTER to DESTROY infrastructure (Cost Saving Mode)..."
read

echo "💥 Destroying Infrastructure..."
terraform destroy -var="project_id=$PROJECT_ID" -var="region=$REGION" -var="gemini_api_key=$GEMINI_API_KEY" -auto-approve

echo "✨ Cleaned up successfully."
