#!/bin/sh
env ESHU_CONFIG=site_settings.py gunicorn -b unix:/tmp/eshu.sock -k sanic.worker.GunicornWorker eshu:app
