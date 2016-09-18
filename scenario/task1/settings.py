consumer_key = '9WTN0KUl3pd38jlQ4bT1F8VBq'
consumer_secret = '6r6GjNZzpsE4tTc1SgmAA8CXLe5GZWkBFV2Ck06kKhCK0q4scL'

database_address = 'http://115.146.89.121:5984/'
database = 'melb_movie_twitter'
source_database = 'melbourne_tweets'
movie_database = 'movie'

geocode = '-37.814396,144.963616,40km'

# key: title of movie, vlaue: imdb id
imdb = {'The Big Short': '1596363', 'Deadpool': '1431045', 'Captain America: Civil War': '3498820', 'The Revenant': '1663202', 'Eddie the Eagle': '1083452', 'Ant-Man': '0478970', 'Mad Max: Fury Road': '1392190', 'Zootopia': '2948356', 'The Martian': '3659388', 'Avengers: Age of Ultron': '2395427', 'Batman v Superman: Dawn of Justice': '2975590', 'The Jungle Book': '3040964', 'The Hunger Games: Mockingjay - Part 2': '1951266', 'Jurassic World': '0369610', "The Huntsman: Winter's War": '2381991', 'Star Wars: Episode VII - The Force Awakens': '2488496', 'Midnight Special': '2649554', 'Point Break': '2058673'}
# key: title of movie, value: search content for Twitter Search API
movies = {'Deadpool': 'Deadpool', 'Zootopia': 'Zootopia', 'Batman v Superman: Dawn of Justice': 'Batman v Superman OR Dawn of Justice', "The Huntsman: Winter's War": "Huntsman OR Winter's War", 'The Jungle Book': 'Jungle Book', 'Eddie the Eagle': 'Eddie the Eagle', 'Captain America: Civil War': 'Captain America OR Civil War', 'The Big Short': 'The Big Short', 'Midnight Special': 'Midnight Special', 'The Revenant': 'The Revenant', 'The Martian': 'The Martian', 'Star Wars: Episode VII - The Force Awakens': 'Star Wars VII OR Force Awakens', 'Avengers: Age of Ultron': 'Avengers OR Age of Ultron', 'Jurassic World': 'Jurassic World', 'Point Break': 'Point Break', 'Ant-Man': 'Ant-Man', 'The Hunger Games: Mockingjay - Part 2': 'Hunger Games OR Mockingjay', 'Mad Max: Fury Road': 'Mad Max OR Fury Road'}
# key: title of movie, value: regular expression of search content for given text of a tweet
keywords = {'Deadpool': 'deadpool', 'Zootopia': 'zootopia', 'Batman v Superman: Dawn of Justice': '(batman\s?v\s?superman)|(dawn\s?of\s?justice)', "The Huntsman: Winter's War": "(huntsman)|(winter's war)", 'The Jungle Book': '(jungle\s?book)', 'Eddie the Eagle': '(eddie\s?the\s?eagle)|(eddieeaglemovie)', 'Captain America: Civil War': '(captain\s?america)|(civil\s?war)', 'The Big Short': '(the\s?big\s?short)', 'Midnight Special': '(midnight\s?special)', 'The Revenant': '(the\s?revenant)|(@revenantmovie)', 'The Martian': '(the\s?martian)|(@martianmovie)', 'Star Wars: Episode VII - The Force Awakens': '(star\s?wars)|(force\s?awakens)', 'Avengers: Age of Ultron': '(avengers)|(age\s?of\s?ultron)', 'Jurassic World': '(jurassic\s?world)|(@jurassicpark)', 'Point Break': '(point\s?break)', 'Ant-Man': '(ant[- ]?man)', 'The Hunger Games: Mockingjay - Part 2': '(hunger\s?games)|(mockingjay)', 'Mad Max: Fury Road': '(mad\s?max)|(fury\s?road)'}