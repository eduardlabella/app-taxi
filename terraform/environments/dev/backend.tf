
terraform {
  backend "azurerm" {
    resource_group_name  = "infra"
    storage_account_name = "stplatformtaxi"
    container_name       = "infracontainer"
    key                  = "dev.tfstate"
  }
}