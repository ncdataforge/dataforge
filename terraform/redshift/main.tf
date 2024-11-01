# Redshift Serverless Namespace
resource "aws_redshiftserverless_namespace" "baofd_namespace" {
  namespace_name      = var.redshift_namespace
  db_name             = var.redshift_database
  admin_username      = var.redshift_admin_username
  admin_user_password = var.redshift_admin_password

  tags = {
    project = var.project
  }
}

# Redshift Serverless Workgroup
resource "aws_redshiftserverless_workgroup" "baofd_workgroup" {
  namespace_name      = aws_redshiftserverless_namespace.baofd_namespace.namespace_name
  workgroup_name      = var.redshift_workgroup
  publicly_accessible = true
}

# Redshift Serverless Usage Limit
resource "aws_redshiftserverless_usage_limit" "baofd_usage_limit" {
  resource_arn  = aws_redshiftserverless_workgroup.baofd_workgroup.arn
  usage_type    = "serverless-compute"
  breach_action = "log"
  amount        = 50
}