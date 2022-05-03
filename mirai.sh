#!/bin/bash
while true
do
  count=`ps -ef|grep "./bot -faststart"|grep -v "grep"|wc -l`
  echo $count
  if [ $count -eq 0 ]; then
    nohup ./bot -faststart > /dev/null 2>&1 &
  fi
  sleep 2
  count=`ps -ef|grep "python3 bot.py"|grep -v "grep"|wc -l`
  echo $count
  if [ $count -eq 0 ]; then
    nohup python3 bot.py > /dev/null 2>&1 &
  fi
  sleep 2
  count=`awk 'END {print}' logs/$(date "+%Y-%m-%d").log|grep "parse incoming packet error: return code unsuccessful: -10001"|wc -l`
  echo $count
  if [ $count -eq 1 ]; then
    pid=`ps -ef|grep "./bot -faststart"|grep -v "grep"|awk '{print $2}'`
    kill -9 $pid
  fi
  sleep 2
done