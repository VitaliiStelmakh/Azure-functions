locals {
  naming-location = lower(replace(var.location, " ", ""))
}

resource "random_string" "random_suffix" {
  length = 2
  lower = true
  numeric = true
}

resource "azurerm_storage_account" "main" {
  name                     = "sta1ocr1dev1${local.naming-location}1${random_string.random_suffix.result}"
  resource_group_name      = var.resource-group
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "dev"
  }
}

resource "azurerm_storage_account" "function-storage" {
  name                     = "sta1func1dev1${local.naming-location}1${random_string.random_suffix.result}"
  resource_group_name      = var.resource-group
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "dev"
    purpose     = "function"
  }
}

resource "azurerm_storage_container" "main" {
  name                  = "stc-ocr-dev-${local.naming-location}"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}


resource "azurerm_storage_share" "main" {
  name                 = "stsh-ocr-dev-${local.naming-location}"
  storage_account_name = azurerm_storage_account.main.name
  quota                = var.file-share-quota
}

