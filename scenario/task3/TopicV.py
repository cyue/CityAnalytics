#!/user/bin/python

import sys
import couchdb
from uuid import uuid4
import warnings

class TopicV(object):

    def __init__(self, conn_str, db):
        try:
            self._conn = couchdb.Server(conn_str)
            self._db = self._conn[db]
        except couchdb.http.ResourceNotFound:
            sys.stderr.write('No specified database in couchdb\n')
        except Exception:
            sys.stderr.write('Connection timeout\n')

    def topic_user_lang(self,):
        pass


    def save(self, doc, dest_db):
        try:
            dest_db = self._conn[dest_db]
            dest_db.save(doc)
        except couchdb.http.ResourceNotFound:
            self._conn.create(dest_db)
            warnings.warn('DB not found, automatically created the database "%s"\n' % dest_db)
        except Exception:
            sys.stderr.write('Database "%s" create error: %s\n' % (dest_db, ex))


    def create(self, dbname):
        try:
            self._conn.create(dbname)
        except couchdb.http.PreconditionFailed:
            self._conn.delete(dbname)
            self._conn.create(dbname)
        except Exception:
            sys.stderr.write('Database "%s" create error: %s\n' % (dbname, ex))


    def drop(self, dbname):
        try:
            self._conn.delete(dbname)
        except couchdb.http.ResourceNotFound:
            sys.stderr.write('No specified database in couchdb\n')
        except Exception:
            sys.stderr.write('Database "%s" delete error: %s\n' % (dbname, ex))
            
        
        

