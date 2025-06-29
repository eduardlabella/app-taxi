resource "azurerm_api_management" "apim" {
  name                = "apim-${var.apim_name}"
  location            = var.location
  resource_group_name = var.resource_group_name
  publisher_name      = "My Taxi company"
  #TODO
  publisher_email     = var.publisher_email

  sku_name = "Developer_1"
}
