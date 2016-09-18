#!/bin/sh

cd ./task1
python all.py >> /var/log/task1.log 2>&1 

cd ../task2
python getSuburbSentiment.py /var/log/task2.log 2>&1

cd ../task3
python topic_language.py /var/log/task3.log 2>&1

cd ../task4
python task_run.py /var/log/task4.log 2>&1
