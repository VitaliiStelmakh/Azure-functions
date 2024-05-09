terraform {
  required_version = ">= 1.3.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.94.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.6.1"
    }
  }

  #  backend "azurerm" {
  #    resource_group_name  = ""
  #    storage_account_name = ""
  #    container_name       = ""
  #    key                  = ""
  #  }
}

provider "azurerm" {
  features {}
}

