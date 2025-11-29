# -----------------------
# AWS Provider
# -----------------------
variable "region" {
  description = "AWS region to deploy resources in"
  type        = string
  default     = "us-west-2"
}

# -----------------------
# VPC Configuration
# -----------------------
variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
  default     = "bedrock-poc-vpc"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "azs" {
  description = "Availability Zones for the VPC"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

variable "private_subnets" {
  description = "Private subnets CIDR blocks"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "public_subnets" {
  description = "Public subnets CIDR blocks"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

variable "enable_nat_gateway" {
  description = "Whether to enable NAT Gateway"
  type        = bool
  default     = true
}

variable "single_nat_gateway" {
  description = "Whether to use a single NAT Gateway"
  type        = bool
  default     = true
}

# -----------------------
# Aurora Serverless Configuration
# -----------------------
variable "db_cluster_identifier" {
  description = "Aurora Serverless cluster identifier"
  type        = string
  default     = "my-aurora-serverless"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "myapp"
}

variable "db_master_username" {
  description = "Master username for the database"
  type        = string
  default     = "dbadmin"
}

variable "db_max_capacity" {
  description = "Maximum Aurora Serverless capacity"
  type        = number
  default     = 1
}

variable "db_min_capacity" {
  description = "Minimum Aurora Serverless capacity"
  type        = number
  default     = 0.5
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the DB"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

# -----------------------
# S3 Bucket Configuration
# -----------------------
variable "s3_bucket_prefix" {
  description = "Prefix for S3 bucket name"
  type        = string
  default     = "bedrock-kb"
}

variable "s3_acl" {
  description = "S3 bucket ACL"
  type        = string
  default     = "private"
}

variable "s3_force_destroy" {
  description = "Whether to force destroy the bucket if not empty"
  type        = bool
  default     = true
}

# Tags applied to all resources
variable "tags" {
  description = "Tags applied to all resources"
  type        = map(string)
  default = {
    Terraform   = "true"
    Environment = "dev"
  }
}
