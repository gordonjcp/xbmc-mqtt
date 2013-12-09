import xbmc

xbmc.executebuiltin('Notification(Message,Test message from mqtt plugin,5000)')

while (not xbmc.abortRequested):
	pass
