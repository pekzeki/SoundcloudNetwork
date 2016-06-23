# SoundcloudNetwork

It crawls the Soundcloud profiles of the given accounts and creates a graph database (neo4j) from the entities and the relations. 

Entities:
  - Tracks
  - Users
  - Playlists
  - Comments

Relations:
  - User OWNS Tracks
  - User HAS Playlists
  - User FOLLOW Users
  - User WRITES Comments
  - Comment FOR Tracks
  - Track FAVORITED_BY Users
  - Track ADDED to Playlists

![Alt Text](https://github.com/pekzeki/SoundcloudNetwork/blob/master/output/neo4j-snapshot.png)

### Version
1.0

### Tech

The project requires some open-source projects to work properly:

* [Python] - General purpose programming language. 2.7+
* [Neo4J] - Graph Database
* [py2neo] - Python toolkit for neo4j.

### Installation

Installation of required pyhton libraries.

```sh
$ pip install py2neo==2.0.8
$ pip install configparser
$ pip install soundcloud
```

### Run

Edit input/permalink_username.txt to indicate profiles you need to crawl.
Change input/settings.ini file to make your own configuration for neo4j. Take an api-key from Soundcloud and set the cliend_id/client_secret parameters to get an access for the Soundcloud API. 

```sh
$ pyhon soundcloud_neo4j.py
```

### Todos

 - Create a bigger network and recommend user/tracks via 'link prediction'. 
 - Add Code Comments

### License
MIT

----

**Free Software, Hell Yeah!**

[//]: # 
   [Python]: <https://www.python.org/>
   [py2neo]: <http://py2neo.org/>


