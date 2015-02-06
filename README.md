# beets-plugin-importplaycount


imports playcount for each track from last.fm




To use this plugin you need the lastfm section in your config file:

config:

    lastfm:
        user: USERNAME
        api_key: 12345678901234567890


Realy nice is to create playlists with this data.

config:

    smartplaylist:
        auto: no
        relative_to: /home/decembersoul/MP3_beets
        playlist_dir: /home/decembersoul/MP3_beets/playlists
        
        playlists:
        - name: 'Top_All.m3u'
          query: 'lastfm_playcount:400.. lastfm_playcount-'
        - name: 'Top_Genre_$genre.m3u'
          query: 'lastfm_playcount:100.. lastfm_playcount-'
        - name: Top_Year_$year.m3u
          query: 'lastfm_playcount:1.. lastfm_playcount-'
        - name: Top_Artist_$artist.m3u
          query: 'lastfm_playcount:1.. lastfm_playcount-'


Call it like
	beet importplaycount

This could take very long. depends on how many tracks you have.


TODO:
add an option to refetch data. currently i don't ask for new data if a playcount not equal zero was found.
