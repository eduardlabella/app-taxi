resource "azurerm_service_plan" "service_plan" {
  name                = "asp-${var.asp_name}"
  resource_group_name = var.resource_group_name
  location            = "westeurope"
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "function_app" {
  name                = "func-${var.funcapp_name}"
  resource_group_name = var.resource_group_name
  location            = "westeurope"

  service_plan_id = azurerm_service_plan.service_plan.id

  storage_account_name       = var.storage_account_name
  storage_account_access_key = var.storage_account_access_key

    site_config {
    application_stack {
      python_version = "3.12"
    }
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"
  }

}
