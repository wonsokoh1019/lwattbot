#!/bin/env bash

echo `python scripts/registerBot.py`
sleep 2
echo `python main.py --port=8080 --daemonize True`

