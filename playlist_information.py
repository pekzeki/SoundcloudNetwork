# import MySQLdb


def getPlaylistInformation(client, user_id, playlistCount):
    
    playlistList = list()
    playlist_url = '/users/' + str(user_id) + '/playlists'
    
    for i in range(0, playlistCount, 50):
        playlists = client.get(playlist_url, offset=i)
        playlistList.append(playlists)
    
    return playlistList
    
def insertDB(user_id, playListList):
    
    database = MySQLdb.connect (host="127.0.0.1", user = "root", passwd ="", db = "soundcloud")
    database.set_character_set('utf8') 
    cursor = database.cursor()
    
    for playlists in playListList:
    
        for playlist in playlists:
        
            query = "INSERT INTO T_PLAYLIST (USERID, PLAYLISTID, PLAYLISTNAME, CREATEDDATE) VALUES (%s, %s, %s, %s)"
            
            USERID = user_id
            PLAYLISTID = playlist.id
            PLAYLISTNAME = playlist.title
            CREATEDDATE = playlist.created_at
            
            values = (USERID, PLAYLISTID, PLAYLISTNAME, CREATEDDATE)
            cursor.execute(query, values)
        
        database.commit()
            
        for playlist in playlists:
              
            for track in playlist.tracks:
                
                query = "INSERT INTO T_PLAYLIST_DETAIL (PLAYLISTID, TRACKID) VALUES (%s, %s)"
                
                PLAYLISTID = playlist.id
                TRACKID = track['id']
                
                values = (PLAYLISTID, TRACKID)
                cursor.execute(query, values)
        
    cursor.close()
    database.commit()
    database.close()    
    
from py2neo import Graph
    
def add2Neo4J(user_id, playlistList):
        
    graph = Graph()
    
    for playlists in playlistList:
    
        for playlist in playlists:
            tx = graph.cypher.begin()
            tx.append("MATCH (u1:User) WHERE u1.id = {A} MERGE (p1:Playlist {id:{B}, title:{C}, created_at:{D}}) CREATE UNIQUE (u1)-[:CREATED_PLAYLIST]->(p1)", 
                  {"A":user_id, "B":playlist.id, "C":playlist.title, "D":playlist.created_at})
            tx.process()
            tx.commit()
            
            for track in playlist.tracks:
            
                tx = graph.cypher.begin()
                tx.append("MATCH (t1:Track), (p1:Playlist) WHERE t1.id = {A} AND p1.id = {B} CREATE UNIQUE (t1)-[:INOLVED_IN]->(p1)", 
                      {"A":track['id'], "B":playlist.id})
                tx.process()
                tx.commit()
    
