# import MySQLdb

def getCommentInformation(client, user_id):

    comment_url = '/users/' + str(user_id) + '/comments'
    comments = client.get(comment_url)
    
    return comments
    
def insertDB(comments):

    database = MySQLdb.connect(host="127.0.0.1", user = "root", passwd="", db = "soundcloud")
    database.set_character_set('utf8') 
    cursor = database.cursor()
    
    for comment in comments:
        
        query = "INSERT INTO T_COMMENTINFO (COMMENTEDTRACKID, CREATED_AT, COMMENT) VALUES (%s, %s, %s)"
        
        COMMENTEDTRACKID = comment.track_id
        CREATED_AT = comment.created_at    
        COMMENT = comment.body
        values = (COMMENTEDTRACKID, CREATED_AT, COMMENT)
        cursor.execute(query, values)
        
        query = "INSERT INTO T_ACTIVITY (USERID, ACTIVITYTYPE, COMMENTID) VALUES (%s, %s, %s)"
        
        USERID = comment.user_id
        ACTIVITYTYPE = "11"
        COMMENTID = cursor.lastrowid
        
        values = (USERID, ACTIVITYTYPE, COMMENTID)
        cursor.execute(query, values)
        
    cursor.close()
    database.commit()
    database.close()
  
from py2neo import Graph
    
def add2Neo4J(user_id, comments):

    graph = Graph()
        
    for comment in comments:
        tx = graph.cypher.begin()
        tx.append("MATCH (u1:User) WHERE u1.id = {A} MERGE (c1:Comment {id:{B}, body:{C}, created_at:{D}}) CREATE UNIQUE (u1)-[:WROTE]->(c1)", 
                  {"A":user_id, "B":comment.id, "C":comment.body, "D":comment.created_at })
        tx.process()
        tx.commit()
        
        tx = graph.cypher.begin()
        tx.append("MATCH (t1:Track), (c1:Comment) WHERE t1.id = {A} AND c1.id = {B} CREATE UNIQUE (c1)-[:COMMENTED_FOR]->(t1)", 
                  {"A":comment.track_id, "B":comment.id})
        tx.process()
        tx.commit()
