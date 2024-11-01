# Redshift
output "redshift_output" {
  description = "Redshift output from module"
  value       = module.redshift_data_warehouse
}