#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/chadbot/")
sys.path.insert(0,"/var/www/chadbot/chadbot")

from chadbot import app as application
application.secret_key = 'CHAD20bot!'