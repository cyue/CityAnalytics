import re
import csv
import couchdb
import json

def suburb_avg_sentiment(source_db, suburb_income, target_db):
	map_fun = '''function(doc){
		emit([doc.suburb,doc.postal_code], doc.sentiment_score);
	}'''
	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	each_suburb_count = suburb_count(source_db)
	count = 1
	json_result = {}
	for row in source_db.query(map_fun, reduce_fun, group=True).rows:
		if row.key[0] in suburb_income and (row.key[0],row.key[1]) in each_suburb_count and row.value != 0 and each_suburb_count[(row.key[0],row.key[1])] > 16:
			print(str(row.value) + ', ' + str(each_suburb_count[(row.key[0],row.key[1])]))
			json_result['suburb'] = row.key[0]
			json_result['postcode'] = row.key[1]
			json_result['avg_sentiment_score'] = row.value/each_suburb_count[(row.key[0],row.key[1])]
			json_result['income'] = suburb_income[row.key[0]] 
			target_db[str(count)] = json_result
			print(json_result)
			count+=1

def suburb_count(source_db):
	map_fun = '''function(doc){
		emit([doc.suburb,doc.postal_code], 1);
	}'''
	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	each_suburb_count = {}
	for row in source_db.query(map_fun, reduce_fun, group=True).rows:
			each_suburb_count[row.key[0],row.key[1]] = row.value
	return each_suburb_count


couch = couchdb.Server('http://115.146.89.121:5984/')
try:
	source_database = couch.create('has_suburb_tweet')
except couchdb.http.PreconditionFailed as e:
	source_database = couch['has_suburb_tweet']

try:
	target_database = couch.create('suburb_income_sentiment_update')
except couchdb.http.PreconditionFailed as e:
	del couch['suburb_income_sentiment_update']
	target_database = couch.create('suburb_income_sentiment_update')

# get income data from suburb_income csv file
temp = []
suburb_income = {}
csvfile = file('suburb_income.csv', 'rb')
reader = csv.reader(csvfile)
for line in reader:
	if reader.line_num == 1:
		continue
	temp.append(line)
# print(temp)
for each in temp:
	suburb_income[each[0]] = int(each[1])
print(suburb_income)
suburb_avg_sentiment(source_database, suburb_income, target_database)
