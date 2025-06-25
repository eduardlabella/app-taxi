variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "storage_account_name" {
  description = "Name of the storage account (must be globally unique)"
  type        = string
}


variable "environment_container_names" {
  type        = list(string)
  description = "Names of containers for each environment"
}

variable "funcapp_name" {
  description = "Name of the function app"
  type        = string
}

variable "asp_name" {
  description = "Name of the asp associated to funcapp"
  type        = string
}

variable "apim_name" {
  description = "Name of the apim"
  type        = string
}