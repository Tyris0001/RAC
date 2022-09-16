import requests
from termcolor import colored
import os 
import random
import json
import time 
import re
import threading
import string 
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup

# EDIT THESE AT YOU OWN DISCRETION 

THREAD_NAME_LIST = [
    "Alph",
    "Brav",
    "Char",
    "Delt",
    "Echo",
    "Foxt",
    "Golf",
    "Hote",
    "Indi",
    "Juli",
    "Kilo",
    "Lima",
    "Mike",
    "Nove",
    "Osca",
    "Papa",
    "Queb",
    "Rome",
    "Sier",
    "Tang",
    "Unif",
    "Vict",
    "Whis",
    "Xray",
    "Yank",
    "Zulu"
]
CAPTCHA_KEY = ""
BASE_NAME = "TyrisBot_"
PASSWORD = "peewee2583"
COOKIEFILE = open('cookies.txt', 'a')
USE_PROXY = True 
PROXY_FILE = open('proxies.txt')
USERAGENTS = [
    "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G980F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Wildfire U20 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19E241 Safari/602.1",
    "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
    "Mozilla/5.0 (iPhone13,2; U; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1",
    "Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254"
]

CAPTCHA_TYPES = {
    "COMMENT":"63E4117F-E727-42B4-6DAA-C8448E9B137F",
    "CLOTHING_UPLOAD":"63E4117F-E727-42B4-6DAA-C8448E9B137F",
    "FOLLOW_USER":"63E4117F-E727-42B4-6DAA-C8448E9B137F",
    "GENERIC_CHALLENGE":"63E4117F-E727-42B4-6DAA-C8448E9B137F",
    "GROUP_JOIN":"63E4117F-E727-42B4-6DAA-C8448E9B137F",
    "GROUP_WALL_POST":"63E4117F-E727-42B4-6DAA-C8448E9B137F",
    "SUPPORT_REQUEST":"63E4117F-E727-42B4-6DAA-C8448E9B137F",
    "SIGNUP":"A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F",
    "LOGIN":"476068BF-9607-4799-B53D-966BE98E2B81"
}

def genuser():
    return BASE_NAME + (str)(random.randint(10000,9999999))


def clear():
    os.system('cls')