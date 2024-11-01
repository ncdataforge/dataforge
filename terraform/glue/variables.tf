# Variables for Glue implementation
locals {
  glue_src_path = "${path.root}/glue_etl/"
}

variable "project" {
  type = string
}

variable "glue_job_name" {
  type = string
}

variable "glue_job_bucket" {
  type = string
}

variable "glue_connection_name" {
  type = string
}

variable "dataset_bucket" {
  type = string
}

variable "redshift_jdbc_connection" {
  type = string
}

variable "redshift_admin_username" {
  type = string
}

variable "redshift_admin_password" {
  type = string
}