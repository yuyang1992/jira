from itertools import groupby
from operator import itemgetter

import pandas as pd
from jira import JIRA

developer = []


def searchUserStory(jira, jql):
    issues = jira.search_issues(jql)
    fields = map(lambda issue: issue.fields, issues.iterable)
    data = map(lambda field: {"问题类型": field.issuetype.name,
                              "问题关键字": field.project.key + "-" + field.issuetype.id,
                              "概要": field.summary,
                              "经办人": field.assignee.displayName,
                              "备注": ""
                              },
               fields)
    fieldsDF = pd.DataFrame(data, columns=["问题类型", "问题关键字", "概要", "经办人", "备注"])
    fieldsDF.to_excel('sprint07.xlsx', sheet_name='Sheet1')
    print(fieldsDF)


def searchSubTask(jira, jql):
    issues = jira.search_issues(jql)
    # print(issues.iterable.fields)
    fields = map(lambda issue: issue.fields, issues.iterable)
    # print(list(fields))
    # for i in issues.iterable:
    #     issue = jira.issue(i)
    #     fields = issue.fields
    #     print(fields.__dict__)
    # "status": field.status.name, "priority": field.priority.name
    data = map(lambda field: {"issueType": field.issuetype.name,
                              "issueId": field.project.key + "-" + field.issuetype.id,
                              "summary": field.summary,
                              "assignee": field.assignee.displayName
                              },
               fields)

    print(list(data))
    indexs = map(lambda field: {"assignee": field.assignee.displayName}, fields)
    fieldsDF = pd.Series(data, index=["问题类型", "问题关键字", "概要", "经办人	"])
    print(fieldsDF)
    # print("fields",list(fields))
    # tables = groupby(lst, key=itemgetter("name"))

    tables = groupby(list(fields), key=itemgetter("assignee"))

    # for k in tables:
    #     print("key值", k)
    #     # print("value值", np.sum(list(map(lambda item: item["totalTime"], v))))
    # print("tables", tables)
    # for i in issues.iterable:
    #     issue = jira.issue(i)
    #     fields = issue.fields
    #     if (fields.assignee not in developer):
    #         developer.append(fields.assignee)
    #
    #     print("issue", issue, fields.summary, fields.issuetype, fields.assignee, fields.status,
    #           fields.priority, fields.aggregatetimeoriginalestimate / 3600)


host = "https://jira.qiaofangyun.com"

options = {'server': host}

print("开始登录...")
jira = JIRA(options, basic_auth=('huainan.qu', 'Qiaofang123'))
print("登录成功...")
searchIssueJql = "project = SAAS2 AND issuetype in (任务, 用户故事) AND Sprint = 215 AND assignee in (nan.xia, zhen.xu, huainan.qu, jingyan.wan, haitao.cao, li.zhang)"
searchUserStory(jira, searchIssueJql)

searchSubTaskJql = "project = SAAS2 AND issuetype = 子任务 AND status in (Open, Reopened) AND Sprint = 215 AND assignee in (nan.xia, zhen.xu, huainan.qu, jingyan.wan, li.zhang, haitao.cao)"

# searchSubTask(jira, searchSubTaskJql)
for item in developer:
    print("developer", item)
