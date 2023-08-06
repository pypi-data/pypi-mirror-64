#!/usr/bin/python3

answers = ["Y", "y", "Yes", "YES"]
method_get_track = "song.getData"
method_get_album = "song.getListByAlbum"
method_get_user = "deezer.getUserData"
method_get_lyric = "song.getLyrics"
api_link = "https://api.deezer.com/"
api_track = "{}track/%s".format(api_link)
api_album = "{}album/%s".format(api_link)
api_playlist = "{}playlist/%s".format(api_link)
api_search_trk = "{}search/track/?q=%s".format(api_link)
p_api_link = "https://www.deezer.com/ajax/gw-light.php"
s_server = "https://e-cdns-proxy-{}.dzcdn.net/mobile/1/{}"