import sys
import xbmcplugin
import xbmcgui
import xbmc
import streamlink
from urlparse import parse_qsl
from urllib import urlencode

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
    listurl = play_url(npo_url)
    li = xbmcgui.ListItem('NPO1', iconImage='DefaultVideo.png')
    li.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=pluginhandle, url=listurl, listitem=li)
    
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