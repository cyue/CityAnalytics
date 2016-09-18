import json
import urllib
import tweepy
from textblob import TextBlob
from tweepy import AppAuthHandler
from tweepy.cursor import Cursor
from datetime import date
from imdb import IMDb
import settings
import couchdb
import logging

# save up to 6 people's name for people field, i.e. director, writer, cast
def process_people_list(people_list):
	people = []
	for person in people_list:
		people.append(str(person))
	return ', '.join(people[0:6]).decode('utf8')

# process result retrieved from IMDB's database
def process_movie(result):
	movie = {}
	movie['title'] = result['title']
	movie['long title'] = result['long imdb title']
	movie['rating'] = result['rating']
	movie['genres'] = ', '.join(result['genres']).decode('utf8')
	movie['languages'] = ', '.join(result['languages'])
	movie['runtimes'] = result['runtimes'][0]
	movie['year'] = result['year']
	movie['outline'] = result['plot outline']
	movie['writer'] = process_people_list(result['writer'])
	movie['director'] = process_people_list(result['director'])
	movie['cast'] = process_people_list(result['cast'])
	movie['cover url'] = result['full-size cover url']
	return movie

# harvest movie info from IMDb database and save
def movie_from_imdb(server):
	try:
		db = server.create(settings.movie_database)
	except couchdb.http.PreconditionFailed as e:
		db = server[settings.movie_database]

	ia = IMDb()
	for name in settings.movies.keys():
		# find imdb id for a given movie title
		movie_list = ia.search_movie(name)
		first_match = movie_list[0]
		movie_id = first_match.movieID

		if movie_id not in db:
			result = ia.get_movie(movie_id)
			movie = process_movie(result)
			db[movie_id] = movie
	return db

'''
search a particular movie using Twitter Search API
add additional sentiment info and movie info to each tweet returned
save each tweet in couchdb with twitter id as id
'''
def search(db, movie_db, api, title, today):
	try:
		query = settings.movies[title]
		geo = settings.geocode
		for status in Cursor(api.search, geocode=geo, q=query, until=str(today), lang = 'en', count=100).items():
			if status.id_str not in db:
				tweet = status._json
				movie_id = settings.imdb[title]
				tweet['movie_info'] = {'title': title, 'id': movie_id, 'rating': movie_db[movie_id]['rating'], 'year': movie_db[movie_id]['year']}
				text = TextBlob(tweet['text'])
				tweet['sentiment'] = {"polarity": text.polarity, "subjectivity": text.subjectivity}
				db[tweet['id_str']] = tweet
	except tweepy.TweepError as e:
		logging.error("ERROR: " + str(e))

# do map-reduce to count movies number of each imdb rating value
def rate_movie(db):
	doc = {}
	map_fun = '''function(doc) {
		emit(doc.rating, 1);
	}'''

 	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# do map-reduce to count tweets number of each imdb rating value
def rate_heat(db):
	doc = {}
	map_fun = '''function(doc) {
		emit(doc.movie_info.rating, 1);
	}'''

 	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# do map-reduce to count sentiment value of each imdb rating value
def rate_sentiment(db):
	doc = {}
	map_fun = '''function(doc) {
		emit(doc.movie_info.rating, doc.sentiment.polarity);
	}'''

 	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# for a given range of imdb rating, precess results and calculated the related tweets number per movie and sentiment value
def process_rating(start, end, total_movie, total_tweets, sentiment, db):
	rating = {}
	name = str(start) + '-' + str(end)
	rating['range'] = {'start': start, 'end': end}
	for rate in total_movie.keys():
		if rate >= start and rate < end:
			rating['total_movie'] = rating.get('total_movie', 0) + total_movie[rate]
			rating['total_tweets'] = rating.get('total_tweets', 0) + total_tweets[rate]
			rating['sentiment'] = rating.get('sentiment', 0.0) + sentiment[rate]
	rating['tweets_per_movie'] = rating.get('total_tweets', 0) / float(rating['total_movie'])
	rating['sentiment'] = rating.get('sentiment', 0) / float(rating['total_tweets'])
	db[name] = rating

# data analysis based on imdb rating
def rate(server, tweet_db, movie_db):
	# build a new database for result
	try:
		db_rate = server.create('movie_rate')
	except couchdb.http.PreconditionFailed as e:
		del server['movie_rate']
		db_rate = server.create('movie_rate')

	total_movie = rate_movie(movie_db)
	total_tweets = rate_heat(tweet_db)
	sentiment = rate_sentiment(tweet_db)

	process_rating(5, 6, total_movie, total_tweets, sentiment, db_rate)
	process_rating(6, 7, total_movie, total_tweets, sentiment, db_rate)
	process_rating(7, 8, total_movie, total_tweets, sentiment, db_rate)
	process_rating(8, 9, total_movie, total_tweets, sentiment, db_rate)

# do map-reduce to count tweets number of each movie
def movie_heat(db, target_db):
	map_fun = '''function(doc) {
		emit(doc.movie_info.title, 1);
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		movie_id = settings.imdb[row.key]
		target_db[movie_id] = {'title': row.key, 'total_tweet': row.value}

# do map-reduce to count sentiment value of each movie
def movie_sentiment(db, target_db):
	map_fun = '''function(doc) {
			emit(doc.movie_info.title, doc.sentiment.polarity);
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		movie_id = settings.imdb[row.key]
		doc = target_db[movie_id]
		doc['sentiment'] = row.value / float(doc['total_tweet'])
		target_db[movie_id] = doc


# add additional descriprion to each result document
def add_description(target_db, source_db):
	for id in target_db:
		doc = target_db[id]
		movie_doc = source_db[id]
		description = {'image_url': movie_doc['cover url'], 'poster': movie_doc['cover url'].split('/')[-1], 'directer': movie_doc['director'], 'rating': movie_doc['rating'], 'title': movie_doc['long title'], 'cast': movie_doc['cast'], 'genres': movie_doc['genres'], 'runtimes': movie_doc['runtimes'], 'outline': movie_doc['outline']}
		doc['description'] = description
		target_db[id] = doc

# process title in case title is too long to display later
def process_title(db):
	for id in db:
		doc = db[id]
		title = doc['title']
		index = title.find(":")
		if index != -1:
			doc['title'] = title[0:index]
			db[id] = doc

# add poster image as a attachment to each result document
def add_attachment(db):
	for id in db:
		doc = db[id]
		url = doc['description']['image_url']
		image = doc['description']['poster']
		urllib.urlretrieve(url, image)
		f=open(image,'r')
		db.put_attachment(doc,f,filename=image)

# data analysis based on each movie
def movie(server, db, movie_db):
	# build a database for result
	try:
		db_movie = server.create('movie_chart')
	except couchdb.http.PreconditionFailed as e:
		del server['movie_chart']
		db_movie = server.create('movie_chart')

	movie_heat(db, db_movie)
	movie_sentiment(db, db_movie)
	add_description(db_movie, movie_db)
	process_title(db_movie)
	add_attachment(db_movie)

def main():
	fname = 'movie.log'
	logging.basicConfig(filename=fname, filemode='w', level=logging.DEBUG)

	couch = couchdb.Server(settings.database_address)
	movie_db = movie_from_imdb(couch)
	try:
		db = couch.create(settings.database)
	except couchdb.http.PreconditionFailed as e:
		db = couch[settings.database]

	# application-only authentication for Twitter REST api
	auth = AppAuthHandler(settings.consumer_key, settings.consumer_secret)
	# automatically wait for rate limits to replenish
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	# error handling for authentication
	if not api:
		print 'cannot authenticate'
		logging.error('cannot authenticate')
		return

	today = date.today()
	logging.info('start harvesting')
	for title in settings.movies.keys():
		print 'search: ' + title
		search(db, movie_db, api, title, today)
	logging.info('finish harvesting')
	
	# data analysis
	logging.info('start analysing')
	rate(couch, db, movie_db)
	movie(couch, db, movie_db)
	logging.info('finish analysing')

if __name__ == '__main__':
	main()

	