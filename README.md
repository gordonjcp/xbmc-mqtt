XBMC-MQTT
=========

Copy everything to ~/.xbmc/addons/script.service.mosquitto/

In the Addons menu, go to Services/Mosquitto and fill in the details
of your broker and desired topic to listen to.

Send a message with something like:

  $ mosquitto_pub -h myhost.net -t xbmc/messages -m '{"sub":"A subject line", "txt":"A message to display"}'


