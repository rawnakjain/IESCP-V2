#!/bin/bash

celery -A app.celery beat --max-interval 1 --loglevel=info