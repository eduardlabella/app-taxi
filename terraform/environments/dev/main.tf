module "resource_group" {
  source   = "../../modules/resource_group"
  name_rg  = var.resource_group_name
  location = var.location
}

module "networking" {
  source              = "../../modules/networking"
  resource_group_name = module.resource_group.name
  location            = var.location
  vnet_name           = var.vnet_name
  snet1_name          = var.snet1_name
  snet2_name          = var.snet2_name

}

module "storage" {
  source               = "../../modules/storage"
  resource_group_name  = module.resource_group.name
  location             = module.resource_group.location
  storage_account_name = var.storage_account_name
  container_names      = var.environment_container_names
  allowed_subnet_ids   = []
}



module "function_app" {
  source                     = "../../modules/function_app"
  resource_group_name        = module.resource_group.name
  location                   = module.resource_group.location
  storage_account_name       = var.storage_account_name
  storage_account_access_key = module.storage.storage_account_access_key
  funcapp_name               = var.funcapp_name
  asp_name                   = var.asp_name

}


module "apim" {
  source              = "../../modules/apim"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  apim_name           = var.apim_name

}
