resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  network_rules {
    default_action = "Allow"
    #virtual_network_subnet_ids = var.allowed_subnet_ids
    #bypass = ["AzureServices","Logging","Metrics"]
  }
}

resource "azurerm_storage_container" "env_containers" {
  for_each = toset(var.container_names)

  name                  = each.value
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}
