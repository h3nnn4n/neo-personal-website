# https://registry.terraform.io/providers/hashipubcorp/aws/latest/docs/resources/route53_zone
resource "aws_route53_zone" "renan_website" {
  name = "renan.website"

  lifecycle {
    prevent_destroy = true
  }
}

#https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route53_record
resource "aws_route53_record" "renan_website" {
  zone_id = aws_route53_zone.renan_website.zone_id
  name    = "renan.website"
  type    = "A"
  ttl     = 300
  records = [hcloud_server.webserver.ipv4_address]
}
