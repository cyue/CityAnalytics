#!/usr/bin/evn python
######################################################################
# NAME: llv                                                          #
# ID  : 701197                                                       #
######################################################################

from __future__ import division
import sys
import couchdb
from TopicV import TopicV
from uuid import uuid4
from collections import defaultdict

DEBUG=True

class Task(TopicV):
    
    def __init__(self, conn_str, db):
        TopicV.__init__(self, conn_str, db)

    def topic_user_lang(self, ):
        # map suburb-topic
        map_fun_topic = '''function(doc) {
            var topics = doc.text.toLowerCase().match(/#\S+/g);
            for (var i in topics){
                emit([doc.suburb, topics[i]], 1);
            }

        }'''

        map_fun_user = '''function(doc) {
            var users = doc.text.toLowerCase().match(/@[a-zA-Z0-9_]+/g);
            for (var i in users){
                emit([doc.suburb,users[i]], 1);
            }

        }'''

        map_fun_post = '''function(doc) {
            emit(doc.suburb, doc.postal_code);
        }'''
        
        reduce_fun = '''function(keys, values) {
            return sum(values);
        }'''

        map_fun_lang = '''function(doc) {
            emit([doc.suburb, doc.lang], 1);
        }'''        
        #db = self._conn[self._topics_dbstr]
        topics_rs = self._db.query(map_fun_topic, reduce_fun, group_level=2)
        twitters_rs = self._db.query(map_fun_user, reduce_fun, group_level=2)
        post_rs = self._db.query(map_fun_post)
        lang_rs = self._db.query(map_fun_lang, reduce_fun, group_level=2)

        self.create('topic_twitter_lang')
        # create database
        suburbs_topics = defaultdict(lambda:defaultdict(int))
        for i, row in enumerate(topics_rs.rows):
            suburbs_topics[row.key[0]][row.key[1]] = row.value

        suburbs_users = defaultdict(lambda: defaultdict(int))
        for i, row in enumerate(twitters_rs.rows):
            suburbs_users[row.key[0]][row.key[1]] = row.value

        suburbs_post = dict()
        for row in post_rs.rows:           
            suburbs_post.setdefault(row.key, row.value)

        suburbs_lang = defaultdict(lambda:defaultdict(int))
        for i, row in enumerate(lang_rs.rows):
            suburbs_lang[row.key[0]][row.key[1]] = row.value
        

        suburbs_info = defaultdict(list)
        for suburb in suburbs_post:
            #suburbs_info.setdefault(suburb, list())
            suburbs_info[suburb].append(suburbs_post[suburb])
            suburbs_info[suburb].append(suburbs_topics.get(suburb, {}))
            suburbs_info[suburb].append(suburbs_users.get(suburb, {}))
            suburbs_info[suburb].append(suburbs_lang.get(suburb, {}))

        for i, suburb in enumerate(suburbs_info):
           doc = {'_id': uuid4().hex}
           topics = suburbs_info[suburb][1]
           users = suburbs_info[suburb][2]
           lang = suburbs_info[suburb][3]
           top_5_topic = sorted(zip(topics.iterkeys(), topics.itervalues()), key=lambda x:x[1],reverse=True)[:5]
           top_5_user = sorted(zip(users.iterkeys(), users.itervalues()), key=lambda x:x[1],reverse=True)[:5]
           total = sum(lang.itervalues())
           top_lang = sorted(zip(lang.iterkeys(), lang.itervalues()), key=lambda x:x[1],reverse=True)
           top_lang = [(LANG, POP, POP/total) for LANG, POP in top_lang]
           doc["suburb"] = suburb
           doc["top_5_topic"] = top_5_topic
           doc["top_5_twitters"] = top_5_user
           doc["lang"] = top_lang
           doc["post"] = suburbs_info[suburb][0]
           #if i < 2:
               #print doc["top_5_user"]
           self.save(doc, 'topic_twitter_lang')

if __name__ == '__main__':
    obj = Task('http://115.146.89.121:5984/', 'has_suburb_tweet')
    #obj.create("topics_test")
    #obj._prepare()
    obj.topic_user_lang()


