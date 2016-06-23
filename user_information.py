# import MySQLdb

def getUserInformation(client, user_name):

    # a permalink to a user
    user_url = 'http://soundcloud.com/' + user_name
    # resolve track URL into track resource
    user = client.get('/resolve', url=user_url)
    
    return user

    
def insertDB(user):
    
    database = MySQLdb.connect (host="127.0.0.1", user = "root", passwd ="", db = "soundcloud")
    database.set_character_set('utf8') 
    cursor = database.cursor()
    
    query = "INSERT INTO T_USERINFO (USERID, USERNAME, FULL_NAME, CITY, COUNTRY) VALUES (%s, %s, %s, %s, %s)"
    
    USERID = user.id
    USERNAME = user.username
    FULL_NAME = user.full_name
    CITY = user.city
    COUNTRY = user.country
    
    values = (USERID, USERNAME, FULL_NAME, CITY, COUNTRY)
    cursor.execute(query, values)
    cursor.close()
    database.commit()
    database.close()

from py2neo import Graph

def add2Neo4J(user):
    
    graph = Graph()
    
    print user.username
    
    tx = graph.cypher.begin()
    tx.append("CREATE (u1:User {id:{A}, permalink:{B}, username:{C}, country:{D}, full_name:{E}, city:{F}, track_count:{G}, playlist_count:{H}, followers_count:{I}, followings_count:{J}, public_favorites_count:{K}})", 
              {"A":user.id, "B":user.permalink, "C":user.username, "D":user.country, "E":user.full_name, "F":user.city, 
               "G":user.track_count, "H":user.playlist_count, "I":user.followers_count, "J":user.followings_count, "K":user.public_favorites_count})
    tx.process()
    tx.commit()    
    
