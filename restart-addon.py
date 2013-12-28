#!/usr/bin/python
# vim: ai tabstop=4 expandtab shiftwidth=4 softtabstop=4
# restart-addon - call RPC functions to, uh, restart the addon

import httplib

enable = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"script.service.mosquitto","enabled":true},"id":1}'
disable = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"script.service.mosquitto","enabled":false},"id":1}'

if __name__=="__main__":
    # FIXME - this really needs to read the address from somewhere sane
    h = httplib.HTTPConnection('172.24.33.71', port=8080)
    rc = h.request('GET', '/jsonrpc?request=' + disable)
    print h.getresponse().read()

    rc = h.request('GET', '/jsonrpc?request=' + enable)
    print h.getresponse().read()
