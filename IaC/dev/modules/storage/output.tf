output "function-storage-ac-name" {
  value = azurerm_storage_account.function-storage.name
}

output "function-storage-ac-access-key" {
  value = azurerm_storage_account.function-storage.primary_access_key
}