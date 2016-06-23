# import MySQLdb

def getFollowingInformation(client, user_id, followingCount):

    followingsList = list()
    user_url = '/users/' + str(user_id) + '/followings'
    
    for i in range(0, followingCount, 50):
        followings = client.get(user_url, offset=i)
        followingsList.append(followings)
    
    return followingsList
    
def insertDB(user_id, followingsList):

    database = MySQLdb.connect(host="127.0.0.1", user = "root", passwd="", db = "soundcloud")
    database.set_character_set('utf8') 
    cursor = database.cursor()
    
    for followings in followingsList:
    
        for following in followings:
            
            query = "INSERT INTO T_FOLLOWINFO (FOLLOWUSER) VALUES (%s)"
            FOLLOWUSER = following.id
            values = (FOLLOWUSER)
            cursor.execute(query, (values,))
            
            query = "INSERT INTO T_ACTIVITY (USERID, ACTIVITYTYPE, FOLLOWID) VALUES (%s, %s, %s)"
            
            USERID = user_id
            ACTIVITYTYPE = "10"
            FOLLOWID = cursor.lastrowid
            
            values = (USERID, ACTIVITYTYPE, FOLLOWID)
            cursor.execute(query, values)
        
    cursor.close()
    database.commit()
    database.close()
    
from py2neo import Graph
    
def add2Neo4J(user_id, followingsList):
        
    graph = Graph()

    for followings in followingsList:
        for following in followings.collection:
            tx = graph.cypher.begin()
            tx.append("MATCH (u1:User),(u2:User) WHERE u1.id = {A} AND u2.id = {B} CREATE UNIQUE (u1)-[:FOLLOWS]->(u2)", 
                      {"A":user_id, "B":following.id})
            tx.process()
            tx.commit()
    