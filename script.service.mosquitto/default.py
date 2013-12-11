# vim: ai tabstop=4 expandtab shiftwidth=4 softtabstop=4

import os,sys
import xbmc
import xbmcaddon
import mosquitto
import json

__scriptname__  = "MQTT-to-XBMC plugin"
__version__     = "0.1"
__author__      = "Gordon JC Pearce"
__scriptId__    = "script.service.mosquitto"
__addon__       = xbmcaddon.Addon()
__cwd__         = __addon__.getAddonInfo('path')
__resource__    = xbmc.translatePath(os.path.join(__cwd__, 'resources'))

# loading message
xbmc.log("##### [%s] - Version: %s" % (__scriptname__,__version__,),level=xbmc.LOGDEBUG )

def stdmessage(sub, txt, img='', delay=5000):
    xbmc.executebuiltin('Notification(%s,%s,%s,%s)' % (sub, txt, delay, img))

def on_message(mosq, obj, msg):
    try:
        u = json.loads(msg.payload)
    except:
        xbmc.log("EE: [%s] - could not parse JSON (%s)" % (__scriptname__, msg.payload))
    # okay, looks like we have valid JSON
    stdmessage(**u)

def on_connect(mosq, obj, rc):
    if rc == 0:
        xbmc.log("II: [%s] - connected to broker" % (__scriptname__))
        xbmc.executebuiltin('Notification(xbmc-mqtt,Connected to MQTT broker,5000)')

def on_disconnect(mosq, obj, msg):
    xbmc.log("II: [%s] - connected to broker" % (__scriptname__))
    xbmc.executebuiltin('Notification(xbmc-mqtt,Disconnected from MQTT broker,5000)')

if __name__ == "__main__":
    # get the basic settings
    host = __addon__.getSetting("hostname")
    port = int(__addon__.getSetting('port'))
    topic = __addon__.getSetting('topic')

    # create a Mosquitto client, using the XBMC Device name as a label
    mqtt = mosquitto.Mosquitto(xbmc.getInfoLabel("System.FriendlyName"))
    try:
        mqtt.connect(host, port, 60)
    except:
        xbmc.log("EE: [%s] - could not connect to MQTT broker (%s, %d)" % (__scriptname__, host, port))
        xbmc.executebuiltin('Notification(xbmc-mqtt,Could not connect to MQTT broker %s:%s,5000)' % (host, port))
        sys.exit(1)

    mqtt.subscribe(topic)
    mqtt.on_message = on_message
    mqtt.on_connect = on_connect
    mqtt.on_disconnect = on_disconnect

    while not xbmc.abortRequested:
        mqtt.loop(timeout=1)
    mqtt.disconnect()
