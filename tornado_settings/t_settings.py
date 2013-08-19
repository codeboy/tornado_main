# -*- coding: utf-8 -*-

import os

PORT = 80
TEMPLATE_PATH = 'templates'

DEBUG = False
# DEBUG = True

STATIC_PATH = os.path.join(os.path.dirname(__file__), '', '../static').replace('\\','/')