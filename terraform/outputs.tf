# Output hostname of Redshift
output "redshift_cluster_hostname" {
  description = "The hostname of the Redshift cluster"
  value = replace(
    try(aws_redshift_cluster.reddit_redshift.endpoint, ""),
    format(":%s", try(aws_redshift_cluster.reddit_redshift.port, "")),
    "",
  )
}

# Output port of Redshift
output "redshift_port" {
    description = "Port of Redshift cluster"
    value = aws_redshift_cluster.reddit_redshift.port
}

# Output Redshift password
output "redshift_password" {
    description = "Password of Redshift cluster"
    value = var.db_password
}

# Output Redshift username
output "redshift_username" {
    description = "Username of Redshift cluster"
    value = aws_redshift_cluster.reddit_redshift.master_username
}

# Output Role assigned to Redshift
output "redshift_role" {
    description = "Role assigned to Redshift"
    value = aws_iam_role.redshift_role.name
}

# Output Account ID of AWS
data "aws_caller_identity" "current" {}
output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

# Output Region set for AWS
output "aws_region" {
    description = "Region set for AWS"
    value = var.aws_region
}

output "s3_bucket_name" {
    description = "S3 Bucket name"
    value = var.s3_bucket
}
