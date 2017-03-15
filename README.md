# CM_1 - FOMO

## INTRODUCTION AND SPECIFICATIONS
FOMO  is a fun web application that helps coders alleviate their fear of missing out while they’re coding. This application takes the information on a user’s coding activity on Github and queries the music events that they’ve missed based on their commit times via Tumblr API. Once the events are queried, a list of music events are displayed, which the user can click on to see more information.  When an event is clicked, the users are given information about albums, track, artists and playlists regarding the music event, which is drawn using the Spotify’s API. Now the users can still code away without missing out on any concerts that are taking place!
Link to website https://jersyandclaracm1.herokuapp.com/


# API’S and ENDPOINTS USED
GitHub
Commit times
User location 
User name
Tumblr 
Blog title 
Blog hash tags 
Blog information
Spotify
Albums
Tracks
Artists
Playlists

# TECHNICAL DETAILS
*Main Tools*
Flask 
Python
HTML/CSS/JavaScript

*Main Dependencies*
Flask_github
Pytumblr
Bootstrap
jQuery 
We modified the source codes of the first two packages so that they are compatible under python3.5. They are imported as separated .py file and they are not in the requirements.txt)  
