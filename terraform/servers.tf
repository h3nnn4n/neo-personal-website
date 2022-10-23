# https://registry.terraform.io/providers/hetznercloud/hcloud/latest/docs/resources/server
resource "hcloud_server" "webserver" {
  name        = "neo-personal-website"
  image       = "ubuntu-22.04"
  server_type = "cpx11"
  location    = "ash"

  ssh_keys = [
    hcloud_ssh_key.desktop.id,
    hcloud_ssh_key.laptop.id
  ]

  firewall_ids = [
    hcloud_firewall.ping_ssh.id,
    hcloud_firewall.http_https.id,
  ]

  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }
}
