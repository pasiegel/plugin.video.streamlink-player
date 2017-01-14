import sys
import os.path
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import streamlink
import xml.etree.ElementTree as ET
from urlparse import parse_qsl
from urllib import urlencode

#constants
xml_path = os.path.join(xbmcaddon.Addon().getAddonInfo("path"),'resources', 'data','streams.xml')

# Get the plugin url in plugin:// notation.
pluginurl = sys.argv[0]
# Get the plugin handle as an integer number.
pluginhandle = int(sys.argv[1])

xbmcplugin.setContent(pluginhandle, 'tvshows')

npo_url = 'http://www.npo.nl/live/npo-1'

def play_url(url):
    query = {'action': 'play', 'url':url}
    return (pluginurl + '?' + urlencode(query))

def list():
    if not os.path.isfile(xml_path):
        message = 'streams.xml could not be found'
        xbmcgui.Dialog().notification('file not found', message, xbmcgui.NOTIFICATION_ERROR, 5000)
        return
        
    root = ET.parse(xml_path).getroot()
    for child in root:
        streamname = child.attrib['name']
        streamurl = child.text
        li = xbmcgui.ListItem(streamname, iconImage='DefaultVideo.png')
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=pluginhandle, url=play_url(streamurl), listitem=li)
    xbmcplugin.endOfDirectory(pluginhandle)
    
def play_stream(stream_url):
    """
    Play a stream at the provided url.
    :param url: str
    :return: None
    """
    # Create a playable item with a path to play.
    urls = streamlink.streams(stream_url)
    url = urls['best'].url
    play_item = xbmcgui.ListItem(path=url)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem=play_item)    
    
def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    :param paramstring:
    :return:
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring[1:]))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'play':
            # Play a video from a provided URL.
            play_stream(params['url'])
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of streams
        list()

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    router(sys.argv[2])