resource "azurerm_virtual_network" "vnet" {
  name     = "vnet-${var.vnet_name}"
  address_space = ["10.0.0.0/24"]
  resource_group_name = var.resource_group_name
  location = var.location

}

#  SUBNETS
resource "azurerm_subnet" "subnet1" {
  name                 = "snet-${var.snet1_name}" 
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.0.0/25"]
  service_endpoints = ["Microsoft.Storage"]
}

resource "azurerm_subnet" "subnet2" {
  name                 = "snet-${var.snet2_name}"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.0.128/25"]
}

# NSG
resource "azurerm_network_security_group" "nsg_snet1" {
  name                = "nsg-${var.snet1_name}"
  location            = var.location
  resource_group_name = var.resource_group_name

  security_rule {
    name                       = "AllowInput"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

#  ASOCIACIONES NSG <-> SUBNET

resource "azurerm_subnet_network_security_group_association" "snet1_assoc" {
  subnet_id                 = azurerm_subnet.subnet1.id
  network_security_group_id = azurerm_network_security_group.nsg_snet1.id
}

