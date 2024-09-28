import sys
import re
import os
import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
from xbmc import log as ulog

# For RPC
import json

moviepath=xbmcaddon.Addon().getSetting("moviepath")
showpath=xbmcaddon.Addon().getSetting("showpath")
# moviepath="special://userdata/library/Movies/"
# showpath="special://userdata/library/TV/"

def cleanstr(instr):
    instr=instr.replace("&","and")
    return re.sub('[^ .0-9a-zA-Z]+', '', instr).replace(" ", ".")

def recursSea(playpath):
    
    payload = {'jsonrpc': '2.0', 'method': "Files.GetDirectory", 'params': {"properties": ['showtitle','title', 'season', 'episode', 'file'],"directory": playpath, "media": "video"}, 'id': 1}
    
    info = json.loads(xbmc.executeJSONRPC(json.dumps(payload)))
    info = info["result"]

    if not info['files'][0]:
        return
    
    showtitle=cleanstr(info['files'][0]['showtitle'])
    
    for ep in info['files']:
        if ep['type']=="episode":
            exportep(showtitle,ep['season'],ep['episode'],ep['label'],ep['file'])
            
def listshow(playpath):
    
    payload = {'jsonrpc': '2.0', 'method': "Files.GetDirectory", 'params': {"properties": ['showtitle','title', 'season', 'episode', 'file'],"directory": playpath, "media": "video"}, 'id': 1}

    info = xbmc.executeJSONRPC(json.dumps(payload))
    ulog(json.dumps(info),level=1)
    
    info = json.loads(info)
    seacnt=0
    stitle=""
    for sea in info["result"]["files"]:
        if sea["filetype"]=="directory":
            stitle=sea["showtitle"]
            seacnt=seacnt+1
            recursSea(sea["file"])
            
    xbmcgui.Dialog().notification("Export", "{} exported {} seasons".format(stitle,seacnt))

def exportep(showtitle,season,ep,title,playpath):

        showfolder = showtitle.replace('.', ' ')
        showdest="{}{} ({})/Season {}".format(showpath,showfolder,infotag.getYear(),season)
        if not xbmcvfs.exists(showdest):
            xbmcvfs.mkdirs(showdest)
        
        strmfile="{}/{}.S{}E{}.{}.strm".format(showdest,showtitle,str(season).zfill(2),str(ep).zfill(2),cleanstr(title))
        f = xbmcvfs.File(strmfile, 'w')
        f.write(playpath)
        f.close()
        ulog("ExportTo: {} -> {}".format(strmfile,playpath),level=1)

if __name__ == '__main__':
    if len(sys.argv)>1:
        if sys.argv[1]=="update":
            xbmcgui.Dialog().notification("ExportTo", "Updating Library...")
            xbmc.executebuiltin("UpdateLibrary(video)")
    else:
        infotag=sys.listitem.getVideoInfoTag()
        mediatype=infotag.getMediaType() #types=video,set,musicvideo,movie,tvshow,season,episode
        playpath=sys.listitem.getPath()
        if mediatype=="movie":
            if not xbmcvfs.exists(moviepath):
                xbmcvfs.mkdirs(moviepath)
            title=infotag.getTitle()
            year=str(infotag.getYear())
            strmfile="{}{}.{}.strm".format(moviepath,cleanstr(title),year)
            f = xbmcvfs.File(strmfile, 'w')
            f.write(playpath)
            f.close()
            xbmcgui.Dialog().notification("ExportTo", "Exported {} ({})".format(title,year))
        if mediatype=="tvshow":
            listshow(playpath)
        if mediatype=="season":
            recursSea(playpath)
            xbmcgui.Dialog().notification("ExportTo", "{} Season {} Exported".format(infotag.getTVShowTitle(),infotag.getSeason()))
        if mediatype=="episode":
            showtitle=infotag.getTVShowTitle()
            season=infotag.getSeason()
            episode=infotag.getEpisode()
            exportep(cleanstr(showtitle),season,episode,infotag.getTitle(),playpath)
            xbmcgui.Dialog().notification("ExportTo", "Exported {} Season {} Episode {}".format(showtitle,season,episode))
