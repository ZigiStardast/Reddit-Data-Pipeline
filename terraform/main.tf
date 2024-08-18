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
  region = var.aws_region
  shared_config_files      = [var.aws_config]
  shared_credentials_files = [var.aws_credentials]
  profile                  = var.aws_profile
}

# Create AWS S3 Bucket
resource "aws_s3_bucket" "reddit_bucket" {
  bucket = var.s3_bucket
  force_destroy = true
}

# Create Redshift Cluster
resource "aws_redshift_cluster" "reddit_redshift" {
  cluster_identifier = var.redshift_identifier
  database_name      = var.database_name
  master_username    = var.db_username
  master_password    = var.db_password
  node_type          = "dc2.large"
  cluster_type       = "single-node"
  iam_roles = [ aws_iam_role.redshift_role.arn ]
  skip_final_snapshot = true # ako zelimo da obrisemo redshift sa terraform destroy
  publicly_accessible = true
  vpc_security_group_ids = [aws_security_group.sg_redshift.id]
}

# Create IAM Role for Read Only S3 Bucket
resource "aws_iam_role" "redshift_role" {
  name = "RedShiftLoadRole"
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"]
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      },
    ]
  })
}


# Create Security Group - to allow all incoming and outgoing traffic
 resource "aws_security_group" "sg_redshift" {
  name        = "sg_redshift"
  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}