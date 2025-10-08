#!/usr/bin/env bash
gunicorn -w 4 -k unicorn.workers.UnicornWorker src.app.main:app