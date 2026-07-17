terraform {
  required_providers {
    hcloud = {
      source = "hetznercloud/hcloud"
      version = "1.35.2"
    }

    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  # https://www.terraform.io/language/settings/backends/s3
  backend "s3" {
    bucket = "h3nnn4n-terraform-state"
    key    = "neo-personal-website"
    region = "us-east-1"
  }
}

provider "hcloud" {
  token = var.hcloud_token
}

provider "aws" {
  region = "us-east-1"
}
