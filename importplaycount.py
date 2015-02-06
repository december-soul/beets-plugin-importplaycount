# coding=utf-8
# Copyright 2014, Rafael Bodill http://github.com/rafi
#  vim: set ts=8 sw=4 tw=80 et :

import logging
import requests
import json
from beets.plugins import BeetsPlugin
from beets import ui
from beets import dbcore
from beets import config
from pprint import pprint
from beets.dbcore import types

log = logging.getLogger('beets')
api_url = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&mbid=%s&api_key=%s&format=json'
api_url2 = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&artist=%s&track=%s&api_key=%s&format=json'

class LastImportPlugin(BeetsPlugin):
    def __init__(self):
        super(LastImportPlugin, self).__init__()
        config['lastfm'].add({
            'user':     '',
            'api_key':  '',
        })
        self.item_types = {
            'lastfm_playcount':  types.INTEGER,
            'lastfm_listeners':  types.INTEGER,
        }

    def commands(self):
        cmd = ui.Subcommand('importplaycount',
                help='import global last.fm play-count')

        def func(lib, opts, args):
            import_lastfm(self,lib,args)

        cmd.func = func
        return [cmd]

def import_lastfm(self, lib, args):
    api_key = config['lastfm']['api_key']

    if not api_key:
        raise ui.UserError('You must specify an api_key for importplaycount')

    log.info('Fetching last.fm play count')

    for album in lib.albums():
	for track in album.items():
            count = int(track.get('lastfm_playcount', 0))
       	    listeners = int(track.get('lastfm_listeners', 0))
	    if count == 0:
		try:
			page = fetch_track(track.mb_trackid, api_key)
			if "track" not in page:
				log.error(u'not found by mbid, try search by name')
				page = fetch_track2(track.artist, track.title, api_key)
			
			if "track" in page:		
			    if "playcount" in page["track"]:
					try:
						new_count = int(page["track"]["playcount"].strip())
					except ValueError:
						new_count = 0
						log.info(u'error convert playcount {0}'.format(page["track"]["playcount"]))
					try:
						new_listeners = int(page["track"]["listeners"].strip())
					except ValueError:
						new_listeners = 0
						log.info(u'error convert listeners {0}'.format(page["track"]["listeners"]))

					log.info(u'{0.artist} - {0.title}: \r\t\t\t\t\t\t\t\t change playcount from {1} to {2} \r\t\t\t\t\t\t\t\t\t\t\t\t\t\t listeners from {3} to {4}'.format(track, count, new_count, listeners, new_listeners))
					track['lastfm_playcount'] = new_count
					track['lastfm_listeners'] = new_listeners
					track.store()
			    else:
				    log.error(u'skip {0.artist} - {0.title} Track not found on lastfm, error'.format(track))
				    pprint(page)
        		else:
				log.error(u'skip {0.artist} - {0.title} Track not found on lastfm'.format(track))
		except ValueError:
			log.error(u'error {0.artist} - {0.title} Track not found on lastfm'.format(track))

    log.info('importplaycount: ... done!')

def fetch_track(mbid, api_key):
    return requests.get(api_url % (mbid, api_key)).json()

def fetch_track2(artist, title, api_key):
    return requests.get(api_url2 % (artist, title, api_key)).json()

