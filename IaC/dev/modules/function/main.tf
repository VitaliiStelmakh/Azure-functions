locals {
  naming-location = lower(replace(var.location, " ", ""))
}

resource "azurerm_service_plan" "example" {
  name                = "servpl-ocr-dev-${local.naming-location}"
  resource_group_name = var.resource-group
  location            = var.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "main" {
  name                = "func-ocr-dev-${local.naming-location}"
  resource_group_name = var.resource-group
  location            = var.location

  storage_account_name       = var.storage-ac-name
  storage_account_access_key = var.storage-ac-access_key
  service_plan_id            = azurerm_service_plan.example.id

  site_config {}
}