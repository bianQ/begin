from django.test import TestCase

# Create your tests here.
import re

r = '^[A-Za-z][A-Za-z0-9_.]*$'
d = 'sdf324234f='
s = re.findall(r,d)
if s == []:
    print(1)