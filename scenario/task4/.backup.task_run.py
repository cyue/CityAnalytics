#!/usr/bin/evn python

from TaskV import TaskV
import sys
import couchdb
from uuid import uuid4
from textblob import TextBlob
import re
import numpy as np

DEBUG=True

class Task(TaskV):
    
    def __init__(self, src_conn, dst_conn, db):
        TaskV.__init__(self, src_conn, dst_conn, db)
        self._day_dbstr= 'user_dayofweek_count'
        self._hour_dbstr= 'user_hour_count'
        self._prepare()
    
    def _prepare(self,):
        ''' creat temp database that contribute
            user related statistics '''

        # create day_of_week - user count documents
        # TZO is timezoneoffset of Melbourne
        map_fun = '''function(doc) {
            var date = new Date(doc.created_at);
            TZO = -600;
            date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
            var day = date.getDay();
            emit(doc.user.id, day);
        }'''

        user_day_count = {}
        day_user_rs = self._db.query(map_fun)
        for row in day_user_rs.rows:
            if row.key in user_day_count:
                user_day_count[row.key][row.value] += 1
            else:
                val = [0 for i in range(7)]
                val[row.value] = 1
                user_day_count.setdefault(row.key, val)

        self.create(self._day_dbstr)
        for user in user_day_count:
            doc = {'_id': uuid4().hex,
                    'userid': user,
                    'sun': user_day_count[user][0],
                    'mon': user_day_count[user][1],
                    'tue': user_day_count[user][2],
                    'wed': user_day_count[user][3],
                    'thu': user_day_count[user][4],
                    'fri': user_day_count[user][5],
                    'sat': user_day_count[user][6]}
            self.save(doc, self._day_dbstr)

        # create hour - user count documents
        map_fun = '''function(doc) {
            var date = new Date(doc.created_at);
            TZO = -600;
            date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
            var hour = date.getHours();

            emit(doc.user.id, hour);
        }'''

        user_hour_count = {}
        hour_user_rs = self._db.query(map_fun)
        for row in hour_user_rs.rows:
            if row.key in user_hour_count:
                user_hour_count[row.key][row.value] += 1
            else:
                val = [0 for i in range(24)]
                val[row.value] = 1
                user_hour_count.setdefault(row.key, val)

        self.create(self._hour_dbstr)
        for user in user_hour_count:
            doc = {'_id': uuid4().hex,
                    'userid': user}
            for idx in range(len(user_hour_count[user])):
                doc.setdefault(idx, user_hour_count[user][idx])
            self.save(doc, self._hour_dbstr)


    def day_tweet_stat(self,):
        ''' calculate the count of tweet per weekday '''

        map_fun = '''function(doc) {
            var date = new Date(doc.created_at);
            TZO = -600;
            date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
            var day = date.getDay();

            emit(day, 1);
        }'''

        reduce_fun = '''function(keys, values) {
            return sum(values);
        }'''

        day_tweet_rs = self._db.query(map_fun, reduce_fun, group_level=1)

        self.create('task5_dayofweek_tweet_stat')
        for row in day_tweet_rs.rows:
            doc = {'_id': uuid4().hex}
            doc.setdefault('dayofweek', row.key)
            doc.setdefault('count', row.value)
            self.save(doc, 'task5_dayofweek_tweet_stat')

   
    def hour_tweet_stat(self, ):
        map_fun = '''function(doc) {
            var date = new Date(doc.created_at);
            TZO = -600;
            date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
            var hour = date.getHours();

            emit(hour, 1);
        }'''

        reduce_fun = '''function(keys, values) {
            return sum(values);
        }'''

        hour_tweet_rs = self._db.query(map_fun, reduce_fun, group_level=1)

        self.create('task5_hour_tweet_stat')
        for row in hour_tweet_rs.rows:
            doc = {'_id':uuid4().hex} 
            doc.setdefault('hour', row.key)
            doc.setdefault('count', row.value)
            self.save(doc, 'task5_hour_tweet_stat')


    def day_user_stat(self, ):
        # mapreduce day-user count
        map_fun = '''function(doc) {
            if(doc.sun > 0) {
                emit(0, 1);
            }
            if(doc.mon > 0) {  
                emit(1, 1);
            }
            if(doc.tue > 0) {
                emit(2, 1);
            }
            if(doc.wed> 0) {
                emit(3, 1);
            }
            if(doc.thu> 0) {
                emit(4, 1);
            }
            if(doc.fri> 0) {
                emit(5, 1);
            }
            if(doc.sat > 0) {
                emit(6, 1);
            }
        }'''

        reduce_fun='''function(keys, values) {
            return sum(values);
        }'''
         
        db = self._dest[self._day_dbstr]
        day_user_rs = db.query(map_fun, reduce_fun, group_level=1)

        # create database
        self.create('task5_dayofweek_user_stat')
        for row in day_user_rs.rows:
            doc = {'_id': uuid4().hex}
            doc.setdefault('dayofweek', row.key)
            doc.setdefault('count', row.value)
            self.save(doc, 'task5_dayofweek_user_stat')


    def hour_user_stat(self, ):
        # mapreduce hour-user count
        map_fun = '''function(doc) {
            for (i=0; i<24; i++) {
                if(doc[i] > 0) {
                    emit(i, 1);
                }
            }
        }'''
        
        reduce_fun = '''function(keys, values) {
            return sum(values);
        }'''
        
        db = self._dest[self._hour_dbstr]
        hour_user_rs = db.query(map_fun, reduce_fun, group_level=1)

        # create database
        self.create('task5_hour_user_stat')
        for row in hour_user_rs.rows:           
            doc = {'_id': uuid4().hex}
            doc.setdefault('hour', row.key)
            doc.setdefault('count', row.value)
            self.save(doc, 'task5_hour_user_stat')
             

    def day_hour_sent_stat(self, ):
        map_fun = '''function(doc) {
            var date = new Date(doc.created_at);
            TZO = -600;
            date = new Date(date.getTime() + (60000*(date.getTimezoneOffset()-TZO)));
            var day = date.getDay();
            var hour = date.getHours();
        
            emit([day, hour], doc.text);
        }'''

        tweets = self._db.query(map_fun)

        # sentiment analysis
        remove_pattern = re.compile(r'@\S+|http://\S+|https://\S+|#\w+')
        day_sent, hour_sent = {}, {}
        for row in tweets.rows:
            tweet = re.sub(remove_pattern, '', row.value).strip()
            blob = TextBlob(tweet)
            # 0 for negative, 1 for neutral, 2 for positive
            polarity = int(np.sign(blob.sentiment.polarity)) + 1
            # day of week - sent tweet count
            if row.key[0] in day_sent:
                day_sent[row.key[0]][polarity] += 1
            else:
                val = [0 for i in range(3)]
                val[polarity] += 1
                day_sent.setdefault(row.key[0], val)

            # hour - sent tweet count
            if row.key[1] in hour_sent:            
                hour_sent[row.key[1]][polarity] += 1
            else:
                val = [0 for i in range(3)]
                val[polarity] += 1
                hour_sent.setdefault(row.key[1], val)
        
        self.create('task5_dayofweek_sent_stat')
        for day in day_sent:
            doc = {'_id': uuid4().hex}
            doc.setdefault('dayofweek', day) 
            doc.setdefault('negative', day_sent[day][0])
            doc.setdefault('neutral', day_sent[day][1])
            doc.setdefault('positive', day_sent[day][2])
            self.save(doc, 'task5_dayofweek_sent_stat')

        self.create('task5_hour_sent_stat')
        for hour in hour_sent:
            doc = {'_id': uuid4().hex}
            doc.setdefault('hour', hour)
            doc.setdefault('negative', hour_sent[hour][0])
            doc.setdefault('neutral', hour_sent[hour][1])
            doc.setdefault('positive', hour_sent[hour][2])
            self.save(doc, 'task5_hour_sent_stat')
 
            

if __name__ == '__main__':
    obj = Task('http://115.146.89.191:5984/', 'http://115.146.89.121:5984/', 'melbourne_tweets')
    #obj.day_tweet_stat()
    #obj.hour_tweet_stat()
    #obj.day_user_stat()
    #obj.hour_user_stat()
    obj.day_hour_sent_stat()


