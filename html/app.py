#!/usr/bin/python

''' Bottle app skeleton '''
import sys
import bottle
import couchdb
import json

PATH='.'
if len(sys.argv) > 1:
    PATH=sys.argv[1]
app = application = bottle.Bottle()
bottle.TEMPLATE_PATH.insert(0, PATH+'/views')

sys.path.append(PATH)

@app.route('/static/<filename:path>')
def static(filename):
    ''' serve static files '''
    return bottle.static_file(filename, root=PATH+'/static')


@app.route('/')
def show_index():
    ''' The front "index" page'''
    return bottle.template('front')


@app.route('/page/task1')
def show_page():
    ''' return a page that has been rendered using a template '''
    return bottle.template('task1')

@app.route('/page/task2')
def show_page():
    ''' return a page that has been rendered using a template '''
    return bottle.template('task2')

@app.route('/page/task3')
def show_page():
    ''' return a page that has been rendered using a template '''
    return bottle.template('task3')

@app.route('/page/task4')
def show_page():
    ''' return a page that has been rendered using a template '''
    return bottle.template('task4')

@app.route('/page/<page_name>')
def show():
    return bottle.template(page_name)

@app.route('/reference')
def show():
    return bottle.template('reference')

@app.route('/description')
def show():
    return bottle.template('description')


@app.route('/task1data1')
def task1data1():
    couch= couchdb.Server('http://115.146.89.121:5984/')

    db=couch['movie_chart']
    data=[]
    for id in db:
        #print db[id]
        data.append(db[id])

    return json.dumps(data)


@app.route("/task1data2")
def task1data2():
    couch= couchdb.Server('http://115.146.89.121:5984/')

    db=couch['movie_rate']
    data=[]
    for id in db:
        #print db[id]
        data.append(db[id])

    return json.dumps(data)


@app.route("/task2data")
def task2data():
    f = open('melbourne.json')
    for line in f:
        geo = json.loads(line)

    couch= couchdb.Server('http://115.146.89.121:5984/')

    db=couch['suburb_income_sentiment_update']
    postSent={}
    for id in db:
        adata=db[id]
        sent=float(adata['avg_sentiment_score'])
        suburb=adata['suburb']
        postSent[str(adata['postcode'])]=[]
        postSent[str(adata['postcode'])].append(suburb)
        if sent >0:
            red=sent*254
            red=hex(255-int(red))[-2:]
            postSent[str(adata['postcode'])].append('#'+red+'FF00')
        else:
            green=sent*(-254)
            green=hex(255-int(green))[-2:]
            postSent[str(adata['postcode'])].append('#'+'FF'+green+'00')
        #print 'red',red

        postSent[str(adata['postcode'])].append("{0:.2f}".format(sent))

    for afeature in geo['features']:
        postcode=str(afeature['properties']['postcode'])
        suburbColor=postSent.get(postcode,['',"#FFFFFF",'0'])
        color=suburbColor[1]
        suburb=suburbColor[0]
        sent=suburbColor[2]
        #opacity=postSent.get(postcode,0)

        afeature['properties']={
            "letter": "o",
            "color": color,
            "rank": "15",
            "ascii": "111",
            'suburb':suburb,
            'sent':sent
        }

    return json.dumps(geo)


@app.route("/task2data1")
def task2data1():
    couch= couchdb.Server('http://115.146.89.121:5984/')

    db=couch['suburb_income_sentiment_update']
    data=[]
    for id in db:
        #print db[id]
        data.append(db[id])

    data = sorted(data, key=lambda k: k['income'])

    return json.dumps(data)


@app.route("/task3data")
def task3data():
    couch= couchdb.Server('http://115.146.89.121:5984/')

    db=couch['topic_twitter_lang']
    postTopic={}
    postTwitter={}
    postLan={}
    postSuburb={}
    for id in db:
        adata=db[id]
        postTopic[str(adata['post'])]= adata['top_5_topic']
        postTwitter[str(adata['post'])]= adata['top_5_twitters']
        postSuburb[str(adata['post'])]= adata['suburb']
        postLan[str(adata['post'])]= adata['lang']

    f = open('melbourne.json')
    for line in f:
        geo = json.loads(line)
    for afeature in geo['features']:
        postcode=str(afeature['properties']['postcode'])
        suburb=postSuburb.get(postcode,'')
        topics=postTopic.get(postcode,0)
        twitters=postTwitter.get(postcode,0)
        lan=postLan.get(postcode,0)
        nlan=[]
        if lan!=0 and lan!=[]:
            for alan in lan:
                nlan.append({'name':alan[0],'y':alan[2]*100})

        nsuburb='<b>'+suburb+'</b>'

        ntopics=''
        if topics!=0 and topics!=[]:
            for topic in topics:
                ntopics+='<b>'+topic[0]+'</b>: '+str(topic[1])+'<br>'
        ntwitters=''
        if twitters!=0 and twitters!=[]:
            for atwitter in twitters:
                ntwitters+='<b>'+atwitter[0]+'</b>: '+str(atwitter[1])+'<br>'

        if topics==0 or topics==[]:
            color='white'
        else:
            color='blue'
        afeature['properties']={
            "letter": "o",
            "color": color,
            "rank": "15",
            "ascii": "111",
            'suburb':nsuburb,
            'topics':ntopics,
            'lan':nlan,
            'twitters':ntwitters
        }

    return json.dumps(geo)


@app.route("/task4data1")
def task4data1():
    import couchdb
    couch= couchdb.Server('http://115.146.89.121:5984/')

    db=couch['day_tweet_sent_stat']
    data=[]
    for id in db:
        #print db[id]
        data.append(db[id])

    data = sorted(data, key=lambda k: k['dayofweek'])
    return json.dumps(data)


@app.route("/task4data2")
def task4data2():
    import couchdb
    couch= couchdb.Server('http://115.146.89.121:5984/')

    db=couch['hour_tweet_sent_stat']
    data=[]
    for id in db:
        #print db[id]
        data.append(db[id])

    data = sorted(data, key=lambda k: k['hour'])
    return json.dumps(data)


@app.route("/task4data4")
def task4data4():
    import couchdb
    couch= couchdb.Server('http://115.146.89.121:5984/')

    db=couch['hour_user_sent_stat']
    data=[]
    for id in db:
        data.append(db[id])

    data = sorted(data, key=lambda k: k['hour'])
    return json.dumps(data)


@app.route("/task4data3")
def task4data3():
    import couchdb
    couch= couchdb.Server('http://115.146.89.121:5984/')

    db=couch['day_user_sent_stat']
    data=[]
    for id in db:
        data.append(db[id])

    data = sorted(data, key=lambda k: k['dayofweek'])
    return json.dumps(data)


class StripPathMiddleware(object):
    ''' get that slash out of the request '''
    
    def __init__(self, a):
        self.a = a
    
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)


if __name__ == '__main__':
    bottle.run(app=StripPathMiddleware(app),
                server='wsgiref',
                host='0.0.0.0',
                port=80)

