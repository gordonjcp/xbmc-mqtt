# vim: ai tabstop=4 expandtab shiftwidth=4 softtabstop=4

import os
import xbmc
import xbmcaddon
import mosquitto

__scriptname__   = "MQTT-to-XBMC plugin"
__author__      = "Gordon JC Pearce"
__scriptId__    = "script.service.mosquitto"
__addon__       = xbmcaddon.Addon()
__cwd__         = __addon__.getAddonInfo('path')
__resource__    = xbmc.translatePath(os.path.join(__cwd__, 'resources'))

icon = __resource__+"/media/mqtt.png"

print "gjcp.net:@r"
print __addon__

while (not xbmc.abortRequested):
	pass
