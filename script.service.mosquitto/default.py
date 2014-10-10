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

connected = False


def stdmessage(sub='', txt='', img='DefaultIconInfo.png', delay=5000):
    if sub:
        xbmc.executebuiltin('Notification("%s","%s","%s","%s")' % (sub, txt, delay, img))
    else:
        xbmc.log("EE: [%s] - no header for notification specified" % (__scriptname__))


def on_message(mosq, obj, msg):
    try:
        u = json.loads(msg.payload)
    except:
        xbmc.log("EE: [%s] - could not parse JSON (%s)" % (__scriptname__, msg.payload))
        return

    # okay, looks like we have valid JSON
    try:
        stdmessage(**u)
    except:
        xbmc.log("EE: [%s] - error in JSON (%s)" % (__scriptname__, msg.payload))


def on_connect(mosq, obj, rc):
    global connected
    if rc == 0:
        xbmc.log("II: [%s] - connected to broker" % (__scriptname__))
        if conmsgs:
            xbmc.executebuiltin('Notification(xbmc-mqtt,Connected to MQTT broker,5000,DefaultIconInfo.png)')
        connected = True

        mqtt.subscribe(topic)


def on_disconnect(mosq, obj, msg):
    global connected
    xbmc.log("II: [%s] - disconnected from broker" % (__scriptname__))
    if conmsgs:
        xbmc.executebuiltin('Notification(xbmc-mqtt,Disconnected from MQTT broker,5000,DefaultIconWarning.png)')
    connected = False


if __name__ == "__main__":
    # get the basic settings

    # shorthand to make using the settings less verbose
    s = __addon__.getSetting

    host = s('hostname')
    port = int(s('port'))
    topic = s('topic')
    conmsgs = 'true' in s('conmsgs')

    # create a Mosquitto client, using the XBMC Device name as a label
    mqtt = mosquitto.Mosquitto(xbmc.getInfoLabel("System.FriendlyName") + "_" + xbmc.getInfoLabel("Network.IPAddress"))
    mqtt.username_pw_set(s('username'), s('password'))
    mqtt.on_message = on_message
    mqtt.on_connect = on_connect
    mqtt.on_disconnect = on_disconnect

    while True:
        if connected:
            try:
                mqtt.loop(timeout=1)
            except:
                xbmc.log("EE: [%s] - connection lost" % (__scriptname__))
                if conmsgs:
                    xbmc.executebuiltin('Notification(xbmc-mqtt,Connection lost,5000,DefaultIconError.png)')
                connected = False
        else:
            try:
                mqtt.connect(host, port, 60)
            except:
                xbmc.log("EE: [%s] - could not connect to MQTT broker (%s, %d)" % (__scriptname__, host, port))
                if conmsgs:
                    xbmc.executebuiltin('Notification(xbmc-mqtt,"Could not connect to MQTT broker %s:%s",5000,DefaultIconError.png)' % (host, port))
                xbmc.sleep(10000)
            else:
                connected = True

        if xbmc.abortRequested:
            xbmc.log("II: [%s] - abort requested" % (__scriptname__))
            break

    mqtt.disconnect()
