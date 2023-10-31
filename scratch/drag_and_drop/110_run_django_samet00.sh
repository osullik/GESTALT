#!/bin/bash

echo "activating environment..."
source ../../gestalt_env/bin/activate

echo "starting server..."
python manage.py runserver 0.0.0.0:8000
