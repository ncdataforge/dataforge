output "redshift_jdbc_url" {
  description = "Redshift JDBC endpoint for data warehouse access"
  value       = aws_redshiftserverless_workgroup.baofd_workgroup.endpoint
}

output "redshift_iam" {
  description = "Redshift IAM Roles that are used in the data warehouse"
  value       = aws_redshiftserverless_namespace.baofd_namespace.iam_roles
}