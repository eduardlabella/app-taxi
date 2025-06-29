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

variable "storage_account_access_key" {
  type        = string
  description = "Key unique storage account name"
}

variable "asp_name" {
  type        = string
  description = "Name of ASP associate it to the func app"
}

variable "funcapp_name" {
  type        = string
  description = "Name of the function app"
}