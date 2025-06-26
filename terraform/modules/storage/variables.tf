variable "resource_group_name" {
  type        = string
  description = "Name of the resource group"
}

variable "location" {
  type        = string
  description = "Azure location"
}

variable "storage_account_name" {
  type        = string
  description = "Globally unique storage account name"
}

variable "container_names" {
  type        = list(string)
  description = "List of blob container names to create inside the Storage Account"
}

variable "allowed_subnet_ids" {
  type    = list(string)
  default = []
}