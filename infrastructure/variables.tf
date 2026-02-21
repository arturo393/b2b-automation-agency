variable "project_id" {
  description = "The Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "The Google Cloud Region"
  type        = string
  default     = "us-central1"
}

variable "image_name" {
  description = "The Docker image name (e.g., hunter-agent)"
  type        = string
  default     = "hunter-agent"
}

variable "service_account_email" {
  description = "Service account email for Cloud Run Job"
  type        = string
  default     = ""
}
