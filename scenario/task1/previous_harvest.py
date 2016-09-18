import re
from textblob import TextBlob
import couchdb
import settings
import logging

def couchdb_pager(db, view_name='_all_docs', startkey=None, startkey_docid=None, endkey=None, endkey_docid=None, bulk=5000):
	# Request one extra row to resume the listing there later.
	options = {'limit': bulk + 1}
	if startkey:
		options['startkey'] = startkey
		if startkey_docid:
			options['startkey_docid'] = startkey_docid
	if endkey:
		options['endkey'] = endkey
		if endkey_docid:
			options['endkey_docid'] = endkey_docid
	done = False
	while not done:
		view = db.view(view_name, **options)
		rows = []
		# If we got a short result (< limit + 1), we know we are done.
		if len(view) <= bulk:
			done = True
			rows = view.rows
		else:
			# Otherwise, continue at the new start position.
			rows = view.rows[:-1]
			last = view.rows[-1]
			options['startkey'] = last.key
			options['startkey_docid'] = last.id

		for row in rows:
			yield row.id

def search(source_db, target_db, movie_db):
	for id in couchdb_pager(source_db):
		if id not in target_db:
			doc = source_db[id]
			for title in settings.keywords.keys():
				if re.search(settings.keywords[title], doc['text'].lower()):
					movie_id = settings.imdb[title]
					doc['movie_info'] = {'title': title, 'id': movie_id, 'rating': movie_db[movie_id]['rating'], 'year': movie_db[movie_id]['year']}
					text = TextBlob(doc['text'])
					doc['sentiment'] = {'polarity': text.polarity, 'subjectivity': text.subjectivity}
					target_db[id] = doc
					break

def main():
	print 'begin'
	logging.info('start harvesting')
	couch = couchdb.Server(settings.database_address)
	target_db = couch[settings.database]
	movie_db = couch[settings.movie_database]
	source_server = couchdb.Server('http://115.146.89.191:5984/')
	source_db = source_server['melbourne_tweets']

	search(source_db, target_db, movie_db)
	print 'finished'
	logging.info('end harvesting')

if __name__ == '__main__':
	main()