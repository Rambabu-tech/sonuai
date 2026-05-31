#!/bin/bash

cd /Users/rambabu/job-ai-bot
source ~/anaconda3/bin/activate base
python -m mailbot.gmail_watcher >> cron.log 2>&1
