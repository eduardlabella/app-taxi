terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0" # Or "~> 4.0" if you're using features from v4+
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "1ef32c48-1b76-40d6-8d71-0dad09d6a8bb"
}
