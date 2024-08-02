HOW_IT_WORKS_TEXT = """
**Spotted Apple** downloads all playlists on your Spotify Account and dumps the contents into a 
Google Sheet, with each sheet representing a playlist. You can select, review, edit, and delete the playlists you 
would like transferred to Apple Music (**Note:** Spotify and Apple  Music tracks are not always aligned, 
and sometimes need to be interpolated. Additions to playlists are best administered  via your Spotify 
account.) Once each playlist is configured as desired, simply click "Transfer Playlists" and Spotted Apple 
will load all playlists from the Google Sheet into your Apple Music account!

"""

# TODO: This might not be the flow > I think users just need to sign into Spotify
REQUEST_PERMISSION_TEXT = """
Before you can authorize Spotted Apple to access your Spotify account, you must be added as a 
user of the application. In order to request access to Spotted Apple, please enter your email below:
"""

TEXT_BLOCKS = {
    'how_it_works': HOW_IT_WORKS_TEXT,
    'request_permission': REQUEST_PERMISSION_TEXT,
}