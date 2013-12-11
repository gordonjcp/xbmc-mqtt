XBMC-MQTT
=========

Copy script.service.mosquitto/ to ~/.xbmc/addons/

In the Addons menu, go to Services/Mosquitto and fill in the details
of your broker and desired topic to listen to.

Send a message with something like:

  $ mosquitto_pub -h myhost.net -t xbmc/messages -m '{"sub":"A subject line", "txt":"A message to display","img":"url://for/image","delay":"5000"}'

Bugs
passing unexpected values in the JSON string will crash the addon
the addon doesn't reconnect automatically (maybe it shouldn't)
there is very little error detection
input validation is pretty much nonexistent too



