# import MySQLdb

def getTrackInformation(client, user_id, trackCount):
    
    trackList = list()
    tracks_url = '/users/' + str(user_id) + '/tracks'
    
    for i in range(0, trackCount, 50):
        tracks = client.get(tracks_url, offset=i)
        trackList.append(tracks)
        
    return trackList
    
def insertDB(trackList):

    database = MySQLdb.connect(host="127.0.0.1", user = "root", passwd="", db = "soundcloud")
    database.set_character_set('utf8') 
    cursor = database.cursor()
    
    for tracks in trackList:
       
        for track in tracks:
            
            query = "INSERT INTO T_TRACKINFO (TRACKID, TRACKNAME, GENRE, TRACKTYPE, UPLOADEDBY, DURATION, RELEASE_YEAR, RELEASE_MONTH, RELEASE_DAY, COMMENTABLE, ISSHARED, STREAMABLE, DOWNLOADABLE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            TRACKID = track.id
            TRACKNAME = track.title
            GENRE = track.genre
            TRACKTYPE = track.track_type
            UPLOADEDBY = track.user_id
            DURATION = track.duration
            RELEASE_YEAR = track.release_year
            RELEASE_MONTH = track.release_month
            RELEASE_DAY = track.release_day
            COMMENTABLE = track.commentable
            ISSHARED = track.sharing
            STREAMABLE = track.streamable
            DOWNLOADABLE = track.downloadable
            
            values = (TRACKID, TRACKNAME, GENRE, TRACKTYPE, UPLOADEDBY, DURATION,
            RELEASE_YEAR, RELEASE_MONTH, RELEASE_DAY, COMMENTABLE, ISSHARED,
            STREAMABLE, DOWNLOADABLE)
            
            cursor.execute(query, values)
            
    cursor.close()
    database.commit()
    database.close() 

from py2neo import Graph

def add2Neo4J(trackList):
    
    graph = Graph()
    
    tx = graph.cypher.begin()
    
    for tracks in trackList:
        for track in tracks:
            tx.append("MATCH (u1:User) WHERE u1.id = {A} MERGE (t1:Track {id:{B}, title:{C} }) CREATE UNIQUE (u1)-[:OWNS]->(t1)", 
                      {"A":track.user_id, "B":track.id, "C":track.title})
            tx.process()
    
    tx.commit()
       
