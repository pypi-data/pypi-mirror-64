# YTPO - Youtube playlist organizer
YouTube and YouTube music's playlist organization capabilities are severely lacking. Therefore, YTPO is a nifty app that allows you to organize your playlist via a host of methods.

## Options
### Folder mode
This mode retrieves all of your playlists, creates a folder for each playlist and fills each folder with filenames for each item in the playlist. Once the directory tree is generated, you can do the following - 
1. Copy/Move songs from one playlist folder to another
2. Delete songs from a playlist folder

The app will then remotely update your playlists to match the directory tree. The orders of songs within a playlist is preserved and new songs are added to the bottom of the playlist. 

### List mode
This mode retrieves all of your playlists, creates a text file for each playlist and fills each file with playlist items according to their position in the playlist. Once the files have been generated, you can -
1. Change the order of the items by changing their location in the file
1. Delete items by removing the corresponding line
1. Make copies of items by duplicating the lines
1. Add a new item from a different playlist by copying the corresponding line from the other playlist file and pasting it in the target playlist file.

## TODO
- Package the app as a python module
- Prune duplicate entries
- Append playlist to another playlist
- Shuffle playlist

