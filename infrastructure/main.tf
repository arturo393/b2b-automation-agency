# Enable Artifact Registry API
resource "google_project_service" "artifact_registry" {
  service = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

# Enable Cloud Run API
resource "google_project_service" "cloud_run" {
  service = "run.googleapis.com"
  disable_on_destroy = false
}

# Artifact Registry Repository to store Docker images
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "agency-repo"
  description   = "Docker repository for B2B Agency Agents"
  format        = "DOCKER"
  depends_on    = [google_project_service.artifact_registry]
}

# Cloud Run Job for "The Hunter"
resource "google_cloud_run_v2_job" "hunter_job" {
  name     = "hunter-agent-job"
  location = var.region

  template {
    template {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.repo.name}/${var.image_name}:latest"
        
        env {
          name  = "GOOGLE_CLOUD_PROJECT"
          value = var.project_id
        }
        
        env {
          name  = "GOOGLE_CLOUD_REGION"
          value = var.region
        }
        
        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }
      }
    }
  }
  
  depends_on = [google_project_service.cloud_run]
}

# (Optional) Cloud Scheduler to run it every morning at 8 AM
resource "google_cloud_scheduler_job" "daily_hunt" {
  name        = "daily-hunter-trigger"
  description = "Triggers the Hunter agent every day at 8 AM"
  schedule    = "0 8 * * *"
  region      = var.region

  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${google_cloud_run_v2_job.hunter_job.name}:run"
    
    oauth_token {
      service_account_email = google_service_account.scheduler_sa.email
    }
  }
}

# Service Account for Scheduler to invoke Cloud Run
resource "google_service_account" "scheduler_sa" {
  account_id   = "scheduler-sa"
  display_name = "Cloud Scheduler Service Account"
}

resource "google_project_iam_member" "scheduler_invoker" {
    project = var.project_id
    role    = "roles/run.invoker"
    member  = "serviceAccount:${google_service_account.scheduler_sa.email}"
}
