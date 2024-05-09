locals {
  naming-location = lower(replace(var.location, " ", ""))
}

resource "azurerm_cognitive_account" "main" {
  name                = "docinteleg-ocr-${local.naming-location}"
  location            = var.location
  resource_group_name = var.resource-group
  kind                = "FormRecognizer"
  sku_name = "F0"
}