'''
Created on Dec 22, 2014

@author: szirkdas
'''
import comment_information as COMMENT
import favorite_information as FAV
import playlist_information as PLAYLIST
import following_information as FOLLOW
import user_information as USER
import track_information as TRACK

import soundcloud
from py2neo import authenticate, Graph
import configparser

settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('input/settings.ini')

host = settings.get('Neo4J', 'host')
username = settings.get('Neo4J', 'username')
password = settings.get('Neo4J', 'password')
client_id = settings.get('Soundcloud', 'client_id')
client_secret = settings.get('Soundcloud', 'client_secret')

# set up authentication parameters
# authenticate("localhost:7474", "neo4j", "adm")
authenticate(host, username, password)

# create client object with app credentials
client = soundcloud.Client(client_id=client_id,
                           client_secret=client_secret)

inputFile = open("input/permalink_username.txt", "r")
userIds = []
followingCounts = []
favoritedCounts = []


# Clear everything inside the neo4j
graph = Graph()
tx = graph.cypher.begin()
tx.append("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")
tx.process()
tx.commit()

for userName in inputFile:

    #---------------USERS--------------------
    user = USER.getUserInformation(client, userName)
    USER.add2Neo4J(user)
    
    userIds.append(user.id)
    followingCounts.append(user.followings_count)
    favoritedCounts.append(user.public_favorites_count)
    
    #---------------TRACKS--------------------
    trackList = TRACK.getTrackInformation(client, user.id, user.track_count)
    TRACK.add2Neo4J(trackList)
    
inputFile.close()

    
for i in range(0, len(userIds)):
    
    #---------------COMMENTS ON TRACKS--------------------
    comments = COMMENT.getCommentInformation(client, userIds[i])
    COMMENT.add2Neo4J(userIds[i], comments)
    
    #---------------FAVORITE TRACKS--------------------
    favoritesList = FAV.getPlaylistInformation(client, userIds[i], user.public_favorites_count)
    FAV.add2Neo4J(userIds[i], favoritesList)
    
    #---------------PLAYLISTS--------------------
    playlistList = PLAYLIST.getPlaylistInformation(client, userIds[i], user.playlist_count)
    PLAYLIST.add2Neo4J(userIds[i], playlistList)
    
    #---------------FOLLOWINGS--------------------
    followingsList = FOLLOW.getFollowingInformation(client, userIds[i], user.followings_count)
    FOLLOW.add2Neo4J(userIds[i], followingsList)
    
    
