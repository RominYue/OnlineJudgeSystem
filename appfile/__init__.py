#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from flask import Flask

app = Flask(__name__)

from appfile import views

