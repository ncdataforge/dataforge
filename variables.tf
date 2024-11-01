variable "project" {
  type    = string
  default = "bank-account-opening-fraud-detection"
}

variable "dataset_bucket" {
  type        = string
  description = "Principal S3 bucket for the dataset needed in the project"
}

variable "data_ingestion_bucket" {
  type        = string
  description = "Principal S3 bucket for data ingestion"
}

# Glue variables
variable "glue_job_name" {
  type        = string
  description = "Glue Job name"
}

variable "glue_job_bucket" {
  type        = string
  description = "Principal S3 bucket for glue job development"
}

variable "glue_connection_name" {
  type        = string
  description = "Glue connection for Redshift data warehouse"
}

variable "redshift_jdbc_connection" {
  type        = string
  description = "JDBC url for Redshift connection in Glue"
}

# Redshift variables
variable "redshift_namespace" {
  type        = string
  description = "Redshift namespace"
}

variable "redshift_workgroup" {
  type        = string
  description = "Redshift workgroup"
}

variable "redshift_database" {
  type        = string
  description = "Principal database in the data warehouse for the project"
}

variable "redshift_admin_username" {
  type        = string
  description = "Redshift admin username"
}

variable "redshift_admin_password" {
  type        = string
  description = "Redshift admin password"
}