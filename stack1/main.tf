provider "aws" {
  region = var.region
}

# -----------------------
# VPC Module
# -----------------------
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name             = var.vpc_name
  cidr             = var.vpc_cidr
  azs              = var.azs
  private_subnets  = var.private_subnets
  public_subnets   = var.public_subnets

  enable_nat_gateway = var.enable_nat_gateway
  single_nat_gateway = var.single_nat_gateway

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = var.tags
}

# -----------------------
# Aurora Serverless Module
# -----------------------
module "aurora_serverless" {
  source = "../modules/database"

  cluster_identifier = var.db_cluster_identifier
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.private_subnets

  database_name      = var.db_name
  master_username    = var.db_master_username
  max_capacity       = var.db_max_capacity
  min_capacity       = var.db_min_capacity
  # Omit engine_version to auto-select latest valid in region
  allowed_cidr_blocks = var.allowed_cidr_blocks
}

# -----------------------
# S3 Bucket Module
# -----------------------
data "aws_caller_identity" "current" {}

resource "random_id" "suffix" {
  byte_length = 4
}

locals {
  bucket_name = "${var.s3_bucket_prefix}-${data.aws_caller_identity.current.account_id}-${random_id.suffix.hex}"
}

module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 3.0"

  bucket = local.bucket_name
  acl    = var.s3_acl
  force_destroy = var.s3_force_destroy

  control_object_ownership = true
  object_ownership         = "BucketOwnerPreferred"

  versioning = {
    enabled = true
  }

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm = "AES256"
      }
    }
  }

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true

  tags = var.tags
}
