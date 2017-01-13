import sys
import xbmcplugin
import xbmcgui
import streamlink

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'live TV')

npo_url = 'http://www.npo.nl/live/npo-1'
li = xbmcgui.ListItem('NPO1', iconImage='DefaultVideo.png')
urls = streamlink.streams(npo_url)
url = urls['best'].url
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)
