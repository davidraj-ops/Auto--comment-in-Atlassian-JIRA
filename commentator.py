import sys
import re
import time
from jirasession import JiraSession
import urllib3
import requests
import jira
import jira.client
from jira.client import JIRA
import xlsxwriter
from pydoc import text
import requests
import subprocess
from docxtpl import DocxTemplate
from pathlib import Path
import pandas as pd
import openpyxl

# To Get rid of warnings
urllib3.disable_warnings()

# Get into JIRA link
options = {'server': 'WEBSITE', 'verify': False}
jira = JIRA(options, basic_auth=('username', 'password'))
issues_in_project = jira.issue("JIRA ID")

# Data needed
Jira_ID = issues_in_project.key
resolution = issues_in_project.fields.resolution
device_name = ''
appname = ''
liveASIN = ''
CIC_link = ''
app_version = ''
vendor = ''
build = ''
build_output = (subprocess.getoutput("adb shell getprop")).split()
DSN_output = str(subprocess.getoutput("adb devices"))

# Condition to extract the device DSN
sub1 = "attached"
sub2 = "	device"

idx1 = DSN_output.index(sub1)
idx2 = DSN_output.index(sub2)

DSN = ''

for idx in range(idx1 + len(sub1) + 1, idx2):
    DSN = DSN + DSN_output[idx]

# Condition to extract build
index_1 = [i for i, val in enumerate(build_output) if val == '[ro.build.id]:']
index_2 = [i for i, val in enumerate(build_output) if val == '[ro.build.lab126.build]:']
output = []
for i, j in zip(index_1, index_2):
    output.extend(build_output[i:j])
b1 = output[1]
b1 = b1.replace("[RS", "")
b2 = b1.replace("N]", "")
b3 = b2.replace(".", "_")
build = "Ship_" + b3 + "_User"

# Condition to extract device name
index_3 = [i for i, val in enumerate(build_output) if val == '[ro.build.product]:']
index_4 = [i for i, val in enumerate(build_output) if val == '[ro.build.system_root_image]:']
output1 = []
for i, j in zip(index_3, index_4):
    output1.extend(build_output[i:j])
d1 = output1[1]
d1 = d1.replace("[", "")
d2 = d1.replace("]", "")
device_name = d2.capitalize()

#Defining comment that has to be printed
reproducible_comment = "Issue is reproducable in" + " " + device_name + " " + build + "\n" \
                       + "Device:" + " " + device_name + "\n" \
                       + "DSN:" + " " + DSN + "\n" \
                       + "[App Details]" + "\n" \
                       + "App Name:" + " " + appname + "\n" \
                       + "Live ASIN:" + " " + liveASIN + "\n" \
                       + "CIC Link:" + " " + CIC_link + "\n" \
                       + "App Version:" + " " + app_version + "\n" \
                       + "Vendor:" + " " + vendor + "\n" \


# If condition for issue
if resolution == "Unresolved" and issues_in_project.key == Jira_ID:
    jira.add_comment(Jira_ID, 'new comment')
else:
    print("Can't add comment since issue is resolved/closed")


comment = jira.comment("THIRDPARTY-21130", "Issue is reproducible in latest build")
