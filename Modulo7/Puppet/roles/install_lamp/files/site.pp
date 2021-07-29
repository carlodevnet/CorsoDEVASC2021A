node default { }

node 'puppetclient' {
  include lamp
  include cisco_routers
}