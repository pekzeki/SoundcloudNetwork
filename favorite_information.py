# import MySQLdb

def getPlaylistInformation(client, user_id, favoritesCount):

    favoritesList = list()
    favorite_url = '/users/' + str(user_id) + '/favorites'

    for i in range(0, favoritesCount, 50):
        favorites = client.get(favorite_url, offset=i)
        favoritesList.append(favorites)
    
    return favoritesList
    
def insertDB(user_id, favoritesList):

    database = MySQLdb.connect(host="127.0.0.1", user = "root", passwd="", db = "soundcloud")
    database.set_character_set('utf8') 
    cursor = database.cursor()
    
    for favorites in favoritesList:
    
        for favorite in favorites:
            
            query = "INSERT INTO T_FAVORITEINFO (TRACKID, FAVUSERID) VALUES (%s, %s)"
            
            TRACKID = favorite.id   
            FAVUSERID = favorite.user_id
            values = (TRACKID, FAVUSERID)
            cursor.execute(query, values)
            
            query = "INSERT INTO T_ACTIVITY (USERID, ACTIVITYTYPE, FAVORITEID) VALUES (%s, %s, %s)"
            
            USERID = user_id
            ACTIVITYTYPE = "12"
            FAVORITEID = cursor.lastrowid
            
            values = (USERID, ACTIVITYTYPE, FAVORITEID)
            cursor.execute(query, values)
        
    cursor.close()
    database.commit()
    database.close()
    
from py2neo import Graph
    
def add2Neo4J(user_id, favoritesList):
        
    graph = Graph()
        
    tx = graph.cypher.begin()
    for favorites in favoritesList:
        
        for favorite in favorites:
            tx.append("MATCH (u1:User), (t1:Track) WHERE u1.id = {A} AND t1.id = {B} CREATE UNIQUE (t1)-[:FAVORITED_BY]->(u1)", 
                      {"A":user_id, "B":favorite.id})
            tx.process()
        
    tx.commit()
