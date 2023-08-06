## README

1. `python`
2. `from crackle_api_helpers.api_wrapper import APIWrapper`
3. `wrapper = APIWrapper()`

## Example usage

 
####if using a framework: 
for Crackle
`config = host_api_ps4()` 

for Phoenix make sure to set up environment variables: `tenant_id` `platform_id` `data_id` `secret` and pass in config. 

####or if using shell:  
`from collections import namedtuple ` 
`apiconfig = namedtuple('apiconfig','host partner_id secret geo_code')  `
`config = apiconfig('http://ios-api-us.crackle.com', '<PARTNER_ID>', '<SECRET>', 'US')`

 ####then:
`a = APIWrapper(config)` 
`a.find_media_with_min_duration()`  

## Available API methods:

Auth:
- register_config()
- register_quick()
- login(email, password)
- logout(user_id)
- deactivate(user_id)
- activate_device(user_id, activation_code)
- deactivate_device(user_id)

Video:
- find_media()  
        Find any media item  
        returns: ('media_id', 'short_name', 'media_duration')

- find_media_without_adverts()  
        Find a media item without any adverts  
        returns: ('media_id', 'short_name', 'media_duration')

- find_media_with_preroll()  
        Find a media item with a preroll  
        returns: ('media_id', 'short_name')
 
- find_media_without_preroll()  
        Find a media item without a preroll  
        returns: ('media_id', 'short_name')

- find_media_with_two_midrolls()  
        Find a media item with at least two midrolls  
        returns: ('media_id', 'short_name', [midroll timestamps (seconds)])
        
- find_media_with_rating(rating)  
        Find a media item with the given rating  
        rating: 'Not Rated', 'PG' 'PG-13', 'TV-14', 'R'  
        returns: ('media_id', 'short_name', name)  
        
- find_media_with_min_duration(min_duration_mins)  
        Find a media item with the minimum duration  
        min_duration: minimum duration in minutes  
        returns: ('media_id', 'short_name')  

- find_media_with_subtitles()  
        Find a media item with subtitles   
        returns: ('media_id', 'short_name')

- find_watch_tray_item_with_long_synopsis(category)
        Find a media item with long synopsis
        category: 'Title', 'Description'
        returns: ('Media Info', 'Position')

User:

`from crackle_api_helpers.api_wrapper import UserHelpers`
`wrapper = UserHelpers()`

 then:
 Configure config as indicated above and

`u = UserHelpers(config)` 
`u.continue_watching_remove(user_id, media_id)`

### Available methods:
- remove_playback_history(user_id, media_id)
- continue_watching_remove(user_id, media_id)

Other:
- get_watchnow_tray_metadata()
        Get metatdata for all items in a Watch Now tray (slot)
        Platforms - iOS, Roku
        returns: list of dictionaries. one dictionary per item.

- get_genre_carousel_metadata(genre)
        Get metadata for all items in a Genre page (TV, Movies) Spotlight carousel
        Platforms - iOS
        genre: TV, Movies
        returns: list of dictionaries. one dictionary per item.

- def get_genre_all_metadata(genre):
        Get the metadata for all items on a TV or Movies page
        Platforms - iOS, Roku
        genre: TV, Movies
        returns: list of dictionaries. one dictionary per item.

- def get_series_with_min_episodes(self, min_episodes=1, auth=False):
        Get the metadata for all TV episodes that have at least
        min_episodes episodes
        returns: list of dictionaries. one dictionary per item

- get_show_genres_roku()
        Get a list of all known Show genres for Roku
        returns: list of dictionaries. one dictionary per item

- get_genre_metadata_roku
        Get the metadata based on genre and sub-genre i.e TV/Comedy
        Platforms = Roku
        genre = TV, Movies
        genre_type = Comedy, Drama, Action, and so on
        returns: list of dictionaries. one dictionary per item

- get_playlist_metadata_roku
        Gel the playlist metadata for a video
        platforms = Roku
        returns: list of dictionaries. one dictionary per item


## Unit tests
 - Command to run Crackle unit tests:

`python -m unittest crackle_api_helpers.tests.TestHelpers`

 - Command to run Phoenix unit tests:

`python -m unittest phoenix_api_helpers.tests.TestHelpers`


## Deploying package to pypi

1. Delete old dist files from dist/
2. python3 setup.py sdist bdist_wheel
3. twine upload dist/*

Note twine may need to be configured to point to production pypi
