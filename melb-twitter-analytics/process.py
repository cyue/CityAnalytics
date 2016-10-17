#!/usr/bin/env python
'''
    Author: Cong Yue
    Melbourne twitters' statistics via MPI on Spartan (HTC/HPC cluster)
'''
import re
from time import time
import numpy as np
import json
import random
import sys
from mpi4py import MPI

# term condidate list
term_list = ["good","nice","excellent","positive","fortunate","correct","superior","great",
             "bad","nasty","poor","negative","unfortunate","wrong","inferior","awful",
             "convert", "travel", "extract", "find", "go", "touch", "drink", "conquer",
             "dictonary", "hand", "rice", "water", "computer", "finger", "paper", "pillow"]

DICTIONARY_PATTERN = re.compile(r'"({"".+})"')
HASHTAG_PATTERN = re.compile(r'#\w+')
USER_PATTERN = re.compile(r'@\w+')

_start_time = None
_end_time = None

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()


def count_term_user_hashtag_occurrence(tweets, term):
    ''' return (count of term, user-count dictionary, tag-count dictionary)'''
    count, user_dic, tag_dic = 0, {}, {}
    for tweet in tweets:
        # build user-count dictionary
        users = re.findall(USER_PATTERN, tweet.lower())
        # if some users are mentioned in this tweet
        if users:
            for user in users:
                user_dic[user] = user_dic.get(user,0) + 1 
        # count term occurrence
        for word in tweet.strip().lower().split(' '):
            if word == term:
                count += 1
        # build tag-count dictionary
        tags = re.findall(HASHTAG_PATTERN, tweet.lower())
        # if there are tags in this tweet
        if tags:
            for tag in tags:
                tag_dic[tag] = tag_dic.get(tag, 0) + 1

    return count, user_dic, tag_dic
        


if __name__ == '__main__':
    tweets = []
    # randomly select search term from condidate list - term_list
    term = random.sample(term_list, 1)[0]
    # begin record the start execution time
    _start_time = time()

    twitter_file = '/data/projects/COMP90024/twitter.csv'
    if len(sys.argv) > 1:
        twitter_file = sys.argv[1]

    with open(twitter_file) as f:
        line_count = 0
        for line_no, line in enumerate(f):
            # if current line does not map to current rank
            if line_no % comm_size != comm_rank:
                continue
            try:
                m = re.search(DICTIONARY_PATTERN, line)
                if not m:
                    continue
                dic = m.group(1)
                dic = re.sub('""', '"', dic)
                data = json.loads(dic)
                tweets.append(data['text'])
            except Exception as ex:
                sys.stderr.write('Tweet extraction error: %s' % ex)
                sys.exit()

    term_count, userd, tagd = count_term_user_hashtag_occurrence(tweets, term)
    
    
    # balance workload to all machines
    machine = range(comm_size)
    try:
        # summing on term_count on all machines
        term_count_sum = comm.reduce(term_count, root=0, op=MPI.SUM)
        # gather all localized user-count dictionary to 2nd available machine
        userd_list = comm.gather(userd, root=machine[1%comm_size])
        # gather all localized hashtag-count dictionary to 3rd available machine
        tagd_list = comm.gather(tagd, root=machine[2%comm_size])
    except Exception as ex:
        sys.stderr.write('Reduce or Gather error: %s\n' % ex)
        sys.exit()

    # handle top 10 twitter task on 2nd machine(node or core)
    if comm_rank == machine[1%comm_size]:
        all_users = {}
        for userd in userd_list:
            for user in userd:
                all_users[user] = all_users.get(user, 0) + userd[user]
        # list of tuple-(user, user_count)
        top_users = []
        for user in all_users:
            # if in intial state 
            if len(top_users) < 10:
                top_users.append((user, all_users[user]))
                continue
            # if current user count more than the smallest one in top users
            # replace the smallest on that index        
            top_count_list = list(zip(*top_users))[1]
            min_count = min(top_count_list)
            min_count_idx = top_count_list.index(min_count)
            if all_users[user] > min_count:
                top_users[min_count_idx] = (user, all_users[user])
            
        sorted_top_users = sorted(top_users, key=lambda k: k[1], reverse=True)
        # return to root
        try:
            comm.send(sorted_top_users, dest=0, tag=1)
        except Exception as ex:
            sys.stderr.write('Worker[twitter] to root send error: %s\n' % ex)
            sys.exit()
    
    # handle top 10 hashtag task on 3rd machine(node or core)
    if comm_rank == machine[2%comm_size]:
        all_tags = {}
        for tagd in tagd_list:
            for tag in tagd:
                all_tags[tag] = all_tags.get(tag, 0) + tagd[tag]
        top_tags = []
        for tag in all_tags:
            # if in initial state
            if len(top_tags) < 10:
                top_tags.append((tag, all_tags[tag]))
                continue
            top_count_list = list(zip(*top_tags))[1]
            min_count = min(top_count_list)
            min_count_idx = top_count_list.index(min_count)
            if all_tags[tag] > min_count:
                top_tags[min_count_idx] = (tag, all_tags[tag])
            
        sorted_top_tags = sorted(top_tags, key=lambda k: k[1], reverse=True)
        # return to root
        try:
            comm.send(sorted_top_tags, dest=0, tag=2)
        except Exception as ex:
            sys.stderr.write('Worker[hashtag] to root send error: %s\n' % ex)
            sys.exit()
            
    # gather all and produce the result
    if comm_rank == 0:
        # gather all results
        try:
            top_users = comm.recv(source=machine[1%comm_size], tag=1)
            top_tags = comm.recv(source=machine[2%comm_size], tag=2)
        except Exception as ex:
            sys.stderr.write('Root recv error: %s\n' % ex)
            sys.exit()


        # all job finished, record end time
        _end_time = time()
        
        print ('---------------------------')
        print ('The total count of randomly selected term "%s" is: %s' % (term, term_count_sum))
        print ('---------------------------')
        print ('Top 10 twitters that mentioned and their counts are:')
        for user, count in top_users:
            print (user+': '+str(count))
        print ('---------------------------')
        print ('Top 10 hashtags that mentioned and their counts are:')
        for tag, count in top_tags:
            print (tag+': '+str(count)) 
        print ('---------------------------')
        print ('The time (seconds) cost is: %s' % (_end_time-_start_time))
        print ('---------------------------')
        

    
                
