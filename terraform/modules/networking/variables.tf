variable "resource_group_name" {
  type        = string
  description = "Name of the resource group"
}

variable "location" {
  type        = string
  description = "Azure location"
}


variable "vnet_name" {
  type        = string
  description = "Name of VNET"
}

variable "snet1_name" {
  type        = string
  description = "Name of SNET1"
}

variable "snet2_name" {
  type        = string
  description = "Name of SNET2"
}