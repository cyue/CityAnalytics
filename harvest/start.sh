#!/bin/sh

python Tweepy_Stream.py >> /var/log/tweepy_stream.log 2>&1 &

