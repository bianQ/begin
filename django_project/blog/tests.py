from django.test import TestCase

# Create your tests here.
import re
import requests

from django.conf import settings
import os

d = os.environ.get('PASSWORD')
print(d)