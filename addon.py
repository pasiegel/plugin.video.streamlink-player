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
# Let kodi show the streams as a list of files
xbmcplugin.setContent(pluginhandle, 'video')

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
        li.setInfo('video', infoLabels={'Title':streamname,'mediatype':'video'})
        xbmcplugin.addDirectoryItem(handle=pluginhandle, url=play_url(streamurl), listitem=li)
    xbmcplugin.endOfDirectory(pluginhandle)
    
def play_stream(stream_url):
    """
    Resolve and play a stream at the provided url.
    :param stream_url: str
    :return: None
    """
    
    try:
        urls = streamlink.streams(stream_url)
    except streamlink.exceptions.NoPluginError:
        xbmcgui.Dialog().notification('Unable to play stream', 'no plugin for stream at {}'.format(stream_url), xbmcgui.NOTIFICATION_ERROR, 5000)
        return
        
    best = urls['best']
    if type(best).__name__ == 'RTMPStream':
        #RTMPstream for some reason does not support .url, so we have to build it ourself       
        url = str(best.params['rtmp']) #start with rtmp://url
        for key,value in best.params.iteritems():
            if key != 'rtmp':
                url += ' ' + str(key) + "=" + str(value) #add ' key=value' for all other params to url
    else:
        #all other streams simply work
        url = best.url
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem=xbmcgui.ListItem(path=url))    
    
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
            list()
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of streams
        list()

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    router(sys.argv[2])