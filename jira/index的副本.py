import json

import requests
from jira import JIRA

host = "https://jira.qiaofangyun.com"
url = "/rest/api/2/auditing/record"

options = {'server': host}

print("开始请求...")
jira = JIRA(options, basic_auth=('huainan.qu', 'Qiaofang123'))
print("请求完成...")
issue = jira.issue('SAAS2-11100', fields='summary,comment')
summary = issue.fields.summary

headers = jira.session()._options['headers']
response = jira.session()._session.get(host+url)



print(response.__dict__)
