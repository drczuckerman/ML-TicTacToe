@echo off
set OLD_PYTHONPATH=%PYTHONPATH%
set PYTHONPATH=src;web
python web\web_server.py
set PYTHONPATH=%OLD_PYTHONPATH%
set OLD_PYTHONPATH=
