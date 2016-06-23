'''
Created on Dec 22, 2014

@author: szirkdas
'''

import user_information as USER
import track_information as TRACK
import playlist_information as PLAYLIST
import following_information as FOLLOW
import comment_information as COMMENT
import favorite_information as FAV

import soundcloud

# create client object with app credentials
client = soundcloud.Client(client_id="e7d87b6c5834935bd7b3122b55af9b9e",
                           client_secret="b3711657c70cf1e728608a4335db579b")

inputFile = open( "input/permalink_username.txt", "r" )
userIds = []
followingCounts = []
favoritedCounts = []

for userName in inputFile:

    #---------------USERS--------------------
    
    user = USER.getUserInformation(client, userName)
    USER.insertDB(user)
    
    userIds.append(user.id)
    followingCounts.append(user.followings_count)
    favoritedCounts.append(user.public_favorites_count)
    
    #---------------TRACKS--------------------
    
    trackList = TRACK.getTrackInformation(client, user.id, user.track_count)
    TRACK.insertDB(trackList)
    
    #---------------PLAYLISTS--------------------
    
    playlistList = PLAYLIST.getPlaylistInformation(client, user.id, user.playlist_count)
    PLAYLIST.insertDB(user.id, playlistList)
    
    #---------------FOLLOWINGS--------------------
    
    followingsList = FOLLOW.getFollowingInformation(client, user.id, user.followings_count)
    FOLLOW.insertDB(user.id, followingsList)
    
    #---------------COMMENTS ON TRACKS--------------------
    
    comments = COMMENT.getCommentInformation(client, user.id)
    COMMENT.insertDB(comments)
       
    #---------------FAVORITE TRACKS--------------------
    
    favoritesList = FAV.getPlaylistInformation(client, user.id, user.public_favorites_count)
    FAV.insertDB(user.id, favoritesList)
    
inputFile.close()
    
