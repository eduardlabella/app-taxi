resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.name_rg}"
  location = var.location
}