locals {
  naming-location = lower(replace(var.location, " ", ""))
}

resource "azurerm_resource_group" "dev" {
  name     = "rg-ocr-dev-${local.naming-location}"
  location = var.location
}

module "storage" {
  source           = "./modules/storage"
  location         = var.location
  resource-group   = azurerm_resource_group.dev.name
  file-share-quota = 1
}

module "function" {
  source                = "./modules/function"
  location              = var.location
  resource-group        = azurerm_resource_group.dev.name
  storage-ac-name       = module.storage.function-storage-ac-name
  storage-ac-access_key = module.storage.function-storage-ac-access-key
}