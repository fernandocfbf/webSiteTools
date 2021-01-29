# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 19:58:37 2020

@author: Fernando
"""
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json as js
import time
import sys
import os

print("DATA: ", sys.argv[1])
data_blank = sys.argv[1].strip()  # remove todos os espaços em branco
print("DATA BLANK: ", data_blank)
