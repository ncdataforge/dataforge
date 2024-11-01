terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

# S3 buckets for dataset and source code
module "s3_data_ingestion" {
  source                = "./terraform/s3"
  project               = var.project
  glue_job_bucket       = var.glue_job_bucket
  dataset_bucket        = var.dataset_bucket
  data_ingestion_bucket = var.data_ingestion_bucket
}

# Glue ETL process
module "glue_etl" {
  source                   = "./terraform/glue"
  project                  = var.project
  glue_job_name            = var.glue_job_name
  glue_connection_name     = var.glue_connection_name
  glue_job_bucket          = var.glue_job_bucket
  dataset_bucket           = var.dataset_bucket
  redshift_jdbc_connection = var.redshift_jdbc_connection
  redshift_admin_username  = var.redshift_admin_username
  redshift_admin_password  = var.redshift_admin_password

  depends_on = [
    module.redshift_data_warehouse
  ]
}

# Redshift data warehouse
module "redshift_data_warehouse" {
  source                  = "./terraform/redshift"
  project                 = var.project
  redshift_namespace      = var.redshift_namespace
  redshift_workgroup      = var.redshift_workgroup
  redshift_database       = var.redshift_database
  redshift_admin_username = var.redshift_admin_username
  redshift_admin_password = var.redshift_admin_password
}