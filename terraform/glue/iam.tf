# Assume role for Glue Job
data "aws_iam_policy_document" "glue_job_assume_role_policy" {
  statement {
    sid     = ""
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

# Policy document for S3 Glue Job bucket
data "aws_iam_policy_document" "glue_etl_policy" {
  statement {
    effect    = "Allow"
    resources = ["arn:aws:s3:::${var.glue_job_bucket}/*"]

    actions = ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"]
  }

  statement {
    effect    = "Allow"
    resources = ["arn:aws:s3:::${var.glue_job_bucket}/", "arn:aws:s3:::${var.dataset_bucket}/"]

    actions = ["s3:ListObject"]
  }
}

# IAM Policy attachment to S3 Glue Job bucket
resource "aws_iam_policy" "glue_etl_access_policy" {
  name        = "s3-glue-etl-policy-${var.glue_job_bucket}"
  description = "Allows for running glue jobs in the glue console and access my S3 bucket."
  policy      = data.aws_iam_policy_document.glue_etl_policy.json
  tags = {
    Application = var.project
  }
}

# IAM Role for Glue Job
resource "aws_iam_role" "glue_job_service_role" {
  name               = "aws_glue_job_runner"
  assume_role_policy = data.aws_iam_policy_document.glue_job_assume_role_policy.json
  tags = {
    Application = var.project
  }
}

# Attach IAM role to the S3 Glue Job bucket 
resource "aws_iam_role_policy_attachment" "glue_etl_permissions" {
  role       = aws_iam_role.glue_job_service_role.name
  policy_arn = aws_iam_policy.glue_etl_access_policy.arn
}

# Attach
resource "aws_iam_role_policy_attachment" "glue_redshift_connection" {
  role       = aws_iam_role.glue_job_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRedshiftFullAccess"
}

resource "aws_iam_role_policy_attachment" "glue_lake_attachment" {
  role       = aws_iam_role.glue_job_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLakeFormationDataAdmin"
}