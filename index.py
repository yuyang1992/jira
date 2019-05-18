import math

import pandas as pd
from jira import JIRA


def searchUserStory(jira, jql):
    issues = jira.search_issues(jql)
    fields = map(lambda issue: issue.fields, issues.iterable)

    for issue in issues.iterable:
        print(issue.fields.issuetype.name)
    data = map(lambda issue: {"问题类型": issue.fields.issuetype.name,
                              "问题关键字": issue.key,
                              "概要": issue.fields.summary,
                              "经办人": issue.fields.assignee.displayName,
                              "备注": ""
                              },
               issues.iterable)
    fieldsDF = pd.DataFrame(data, columns=["问题类型", "问题关键字", "概要", "经办人", "备注"])
    fieldsDF.describe()
    fieldsDF.to_excel('sprint07.xlsx', sheet_name='Sheet1')
    print(fieldsDF)


def searchSubTask(jira, jql, maxResults=None):
    issues = jira.search_issues(jql, maxResults=maxResults)
    fields = map(lambda issue: issue.fields, issues.iterable)
    # for field in  issues:
    #     print(field)
    data = map(lambda field: {"问题类型": field.issuetype.name,
                              "问题关键字": field,
                              "概要": field.summary,
                              "经办人": field.assignee.displayName,
                              "任务估时": field.aggregatetimeoriginalestimate
                              }, fields)

    fieldsDF = pd.DataFrame(data, columns={"问题类型", "问题关键字", "概要", "经办人", "任务估时"})

    groups = fieldsDF.groupby("经办人")
    subTaskTime = []
    for name, group in groups:
        time = pd.DataFrame(group.sum(axis=0, numeric_only="任务估时")).get_value(col=0,
                                                                              index="任务估时") / 3600
        workTime = 25 if ("屈淮南" == name) else 63
        percent = math.ceil(time / workTime * 100).__str__() + "%"
        subTaskTime.append({"经办人": name, "任务估时": time, "可用工时": workTime, "饱和度": percent})
    subTaskDF = pd.DataFrame(subTaskTime, columns=["经办人", "任务估时", "可用工时", "饱和度"])
    print(subTaskDF)
    subTaskDF.to_excel('sprint08.xlsx', sheet_name='Sheet1')

host = "https://jira.qiaofangyun.com"

options = {'server': host}

print("开始登录...")
jira = JIRA(options, basic_auth=('huainan.qu', 'Qiaofang123'))
print("登录成功...")
searchIssueJql = "project = SAAS2 AND issuetype in (任务, 用户故事) AND Sprint = 215 AND assignee in (nan.xia, zhen.xu, huainan.qu, jingyan.wan, haitao.cao, li.zhang)"
searchUserStory(jira, searchIssueJql)

searchSubTaskJql = "project = SAAS2 AND issuetype in ( 子任务) AND Sprint = 215 AND assignee in (nan.xia, zhen.xu, huainan.qu, jingyan.wan, haitao.cao, li.zhang)"

searchSubTask(jira, searchSubTaskJql, 100)
