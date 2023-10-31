#!/bin/bash

echo "activating environment..."
source ../../../gestalt_env/bin/activate

echo "starting tmux session..."
tmux new-session -d -s gestalt python manage.py runserver 0.0.0.0:8000
