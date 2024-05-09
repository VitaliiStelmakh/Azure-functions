variable "location" {
  description = "location of resources"
  type        = string
}

variable "resource-group" {
  description = "name of resource group"
  type        = string
}

variable "storage-ac-name" {
  description = "name of designated function storage"
  type        = string

}

variable "storage-ac-access_key" {
  description = "access key to designated function storage"
  type        = string
}
