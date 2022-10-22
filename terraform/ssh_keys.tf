# https://registry.terraform.io/providers/hetznercloud/hcloud/latest/docs/resources/ssh_key
resource "hcloud_ssh_key" "laptop" {
  name       = "Laptop"
  public_key = file("ssh_keys/laptop_rsa.pub")
}

# https://registry.terraform.io/providers/hetznercloud/hcloud/latest/docs/resources/ssh_key
resource "hcloud_ssh_key" "desktop" {
  name       = "Desktop"
  public_key = file("ssh_keys/desktop_rsa.pub")
}
