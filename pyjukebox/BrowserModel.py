import json
import requests as req
import xml.sax

class SongHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.id = ""
        self.parent = ""
        self.title = ""
        self.album = ""
        self.artist = ""
        self.genre = ""
        self.status = ""
        self.currentIndex = ""
        self.playing = ""
   
    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "subsonic-response":
            self.status = attributes["status"]
        elif tag == 'jukeboxPlaylist':
            self.currentIndex = attributes["currentIndex"]
            self.playing = attributes['playing']
        else:
            self.id = attributes['id']
            self.parent = attributes['parent']
            self.title = attributes['title']
            self.album = attributes['album']
            self.artist = attributes['artist']
            self.genre = attributes['genre']

        
class Jukebox(object):
    def __init__(self, action = 'get'):
        self.action = action
        self.songs = ""

    def getALL(self):
        # send request to subsonic for songs
        # $this->SubADDR.'/rest/jukeboxControl.view'.'?u='.$this->SubUSER.'&t='.$this->SubPASS.'&s='.$this->SubSALT.'&v='.$this->SubVER.'&c='.$this->SubCLI.'&action='.$action.''
        r = req.get('https://subsonic.horwood.biz/rest/jukeboxControl?action=get&u=matt&t=78a7b8b38d0bb5bd1bf78999c4e4d769&s=8YI8D0qd&v=1.16.0&c=curl')
        # create an XMLReader
        parser = xml.sax.make_parser()
        # turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
          # override the default ContextHandler
        Handler = SongHandler()
        parser.setContentHandler( Handler )
   
        self.songs.append(parser.parse(r.text))
        return self.songs