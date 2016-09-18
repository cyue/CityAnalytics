#!/usr/bin/evn python

from TaskV import TaskV
import sys
import couchdb
from uuid import uuid4
from textblob import TextBlob
import re
import numpy as np

DEBUG=True
remove_pattern = re.compile(r'@\S+|http://\S+|https://\S+|#\w+')

class Task(TaskV):
    
    def __init__(self, src_conn, dst_conn, db):
        TaskV.__init__(self, src_conn, dst_conn, db)
        self._uds = self._dest['user_day_sent']
        self._uhs = self._dest['user_hour_sent']
        #self._prepare()


    def _get_sent(self,text):
        tweet = re.sub(remove_pattern, '', text).strip()
        blob = TextBlob(tweet)
        # 0 for negative, 1 for neutral, 2 for positive
        polarity = int(np.sign(blob.sentiment.polarity)) 
        return polarity
 
    
    def _prepare(self,):
        ''' creat temp database that contribute
            user related statistics '''

        # create day_of_week - user documents
        # TZO is timezoneoffset of Melbourne
        map_fun = '''function(doc) {
            var date = new Date(doc.created_at);
            TZO = -600;
            date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
            var day = date.getDay();
            emit([doc.user.id, day], doc.text);
        }'''

        # map function generate rows ordered by key, i.e [user_id,day]
        user_id = 0
        day = 9 # some invalid number
        doc = None
        rs = self._db.query(map_fun)
        db_name = 'user_day_sent'
        self.create(db_name)
        for row in rs.rows:
            # new key occur, save the previous key doc
            if row.key[0] != user_id or row.key[1] != day:
                if doc:
                    self.save(doc, db_name)
                # start all with the new user and day
                user_id = row.key[0]
                day= row.key[1]
                sent = self._get_sent(row.value)
                doc = {'_id': uuid4().hex,
                        'user_id': user_id,
                        'dayofweek': day,
                        'sent_score': sent}
            # old key, aggregate
            else:
                sent = self._get_sent(row.value)
                doc['sent_score'] += sent
        # insert the last doc
        self.save(doc, db_name)

        # create hour - user sent documents
        map_fun = '''function(doc) {
            var date = new Date(doc.created_at);
            TZO = -600;
            date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
            var hour = date.getHours();

            emit([doc.user.id, hour], doc.text);
        }'''

      # map function generate rows ordered by key, i.e [user_id,hour]
        user_id = 0
        hour = 99 # some invalid number
        doc = None
        rs = self._db.query(map_fun)
        db_name = 'user_hour_sent'
        self.create(db_name)
        for row in rs.rows:
            # new key occur, save the previous key doc
            if row.key[0] != user_id or row.key[1] != hour:
                if doc:
                    self.save(doc, db_name)
                # start all with the new user and day
                user_id = row.key[0]
                hour = row.key[1]
                sent = self._get_sent(row.value)
                doc = {'_id': uuid4().hex,
                        'user_id': user_id,
                        'hour': hour,
                        'sent_score': sent}
            # old key, aggregate
            else:
                sent = self._get_sent(row.value)
                doc['sent_score'] += sent
        # insert the last doc
        self.save(doc, db_name)


    def day_user_sent_stat(self,):
        ''' Calculate the statistics (user count wrt sentiment) based on day of week 
        '''
        map_fun = '''function(doc) {
            if (doc.sent_score > 0) {
                /* emit the emergence of a positive user wrt a day in a week*/
                emit([doc.dayofweek, "positive"], 1)
            }
            if (doc.sent_score == 0) {
                /* emit the emergence of a positive user wrt a day in a week*/
                emit([doc.dayofweek, "neutral"], 1)
            }
            if (doc.sent_score < 0) {
                /* emit the emergence of a positive user wrt a day in a week*/
                emit([doc.dayofweek, "negative"], 1)
            }
        }'''

        reduce_fun = '''function(keys, values) {
            return sum(values);
        }'''

        rs = self._uds.query(map_fun, reduce_fun, group_level=2)
        day_sent = {}
        for row in rs.rows:
            if row.key[0] not in day_sent:
                day_sent.setdefault(row.key[0], {row.key[1]: row.value})
            else:
                day_sent[row.key[0]].setdefault(row.key[1], row.value)

        db_name = 'day_user_sent_stat'
        self.create(db_name)
        for key in day_sent:
            doc = {'_id': uuid4().hex, 'dayofweek': key}
            doc.update(day_sent[key])
            self.save(doc, db_name)


    def hour_user_sent_stat(self, ):
        ''' Calculate the statistics (user count wrt sentiment) based on day of week 
        '''
        map_fun = '''function(doc) {
            if (doc.sent_score > 0) {
                /* emit the emergence of a positive user wrt hour in a day*/
                emit([doc.hour, "positive"], 1)
            }
            if (doc.sent_score == 0) {
                /* emit the emergence of a positive user wrt hour in a day*/
                emit([doc.hour, "neutral"], 1)
            }
            if (doc.sent_score < 0) {
                /* emit the emergence of a positive user wrt hour in a day*/
                emit([doc.hour, "negative"], 1)
            }
        }'''

        reduce_fun = '''function(keys, values) {
            return sum(values);
        }'''

        rs = self._uhs.query(map_fun, reduce_fun, group_level=2)
        hour_sent = {}
        for row in rs.rows:
            if row.key[0] not in hour_sent:
                hour_sent.setdefault(row.key[0], {row.key[1]: row.value})
            else:
                hour_sent[row.key[0]].setdefault(row.key[1], row.value)

        db_name = 'hour_user_sent_stat'
        self.create(db_name)
        for key in hour_sent:
            doc = {'_id': uuid4().hex, 'hour': key}
            doc.update(hour_sent[key])
            self.save(doc, db_name)


    def day_tweet_sent_stat(self, ):
        map_fun = '''function(doc) {
            var date = new Date(doc.created_at);
            TZO = -600;
            date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
            var day = date.getDay();
        
            emit(day, doc.text);
        }'''

        rs = self._db.query(map_fun)
        day = -1 # some invalid value
        doc = None
        db_name = 'day_tweet_sent_stat'
        self.create(db_name)
        for row in rs.rows:
            if row.key != day:
                if doc:
                    self.save(doc, db_name)
                day = row.key
                sent = self._get_sent(row.value)
                doc = {'_id': uuid4().hex, 'dayofweek': day, 
                        'positive': 0, 'neutral': 0, 'negative': 0}
                if sent < 0:
                    doc['negative'] += 1
                if sent > 0:
                    doc['positive'] += 1
                else:
                    doc['neutral'] += 1
            else:
                sent = self._get_sent(row.value)
                if sent < 0:
                    doc['negative'] += 1
                if sent > 0:
                    doc['positive'] += 1
                else:
                    doc['neutral'] += 1
        # insert the last one to couchdb
        self.save(doc, db_name)
                

    def hour_tweet_sent_stat(self, ):
        map_fun = '''function(doc) {
            var date = new Date(doc.created_at);
            TZO = -600;
            date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
            var hour = date.getHours();
        
            emit(hour, doc.text);
        }'''

        rs = self._db.query(map_fun)
        hour = -1 # some invalid value
        doc = None
        db_name = 'hour_tweet_sent_stat'
        self.create(db_name)
        for row in rs.rows:
            if row.key != hour:
                if doc:
                    self.save(doc, db_name)
                hour = row.key
                sent = self._get_sent(row.value)
                doc = {'_id': uuid4().hex, 'hour': hour, 
                        'positive': 0, 'neutral': 0, 'negative': 0}
                if sent < 0:
                    doc['negative'] += 1
                if sent > 0:
                    doc['positive'] += 1
                else:
                    doc['neutral'] += 1
            else:
                sent = self._get_sent(row.value)
                if sent < 0:
                    doc['negative'] += 1
                if sent > 0:
                    doc['positive'] += 1
                else:
                    doc['neutral'] += 1
        # insert the last one to couchdb
        self.save(doc, db_name)
 
            

if __name__ == '__main__':
    obj = Task('http://115.146.89.191:5984/', 'http://115.146.89.121:5984/', 'melbourne_tweets')
    obj.day_user_sent_stat()
    obj.hour_user_sent_stat()
    obj.day_tweet_sent_stat()
    obj.hour_tweet_sent_stat()

