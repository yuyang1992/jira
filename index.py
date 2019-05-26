import datetime
import json
import math
import time

import pandas as pd
import pytz
import requests
from dateutil.parser import parse
from jira import JIRA

managerGroup = "https://oapi.dingtalk.com/robot/send?access_token=37c465ab11ebcfd3ba9c7a9bf8c858e8a8b7e8d72dced86e9a4dca3f0cc1b429"

mobileDingDing = "https://oapi.dingtalk.com/robot/send?access_token=7043c60fd960191bea14995dc87ace78a0f606d9e8aebb44d35bf033bf827d4c"
dingdingTest = "https://oapi.dingtalk.com/robot/send?access_token=edd1d68e9440e0bf634f2a3d4d9ab860bbcc45b658a9ae39eaba696e9ddc5eb7"
onlineDingDing = "https://oapi.dingtalk.com/robot/send?access_token=99b79b6f4949bf156da40ee500cee9bc881c4f4616fe17338c1663dccfdc8fb6"
dayBugDingDing = "https://oapi.dingtalk.com/robot/send?access_token=ad91f27b12153eade172f3a92a4d563a308c13bf56ec3ad3e0904cfba10c3aa1"
userIssueInfo = [{"title": "已完成",
                  "type": 1,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11362?filter=11350",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status = Closed AND labels not in (不予解决, 暂不处理)"},
                 {"title": "未完成",
                  "type": 2,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11502?filter=11351",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理)"},
                 {"title": "房客楼",
                  "type": 3,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11362?filter=11350",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status = Closed AND labels not in (不予解决, 暂不处理)"},
                 {"title": "交易组",
                  "type": 4,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11362?filter=11350",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status = Closed AND labels not in (不予解决, 暂不处理)"},
                 {"title": "公共组",
                  "type": 5,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11362?filter=11350",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status = Closed AND labels not in (不予解决, 暂不处理)"},
                 {"title": "移动端",
                  "type": 6,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11362?filter=11350",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status = Closed AND labels not in (不予解决, 暂不处理)"}
                 ]

onlineBugInfo = [{"title": "已完成",
                  "type": 1,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11560?filter=11352",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status = Closed"},
                 {"title": "未完成",
                  "type": 2,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11502?filter=11351",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理)"},
                 {"title": "房客楼",
                  "type": 3,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11502?filter=11351",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理)"},
                 {"title": "交易组",
                  "type": 4,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11362?filter=11351",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理)"},
                 {"title": "公共组",
                  "type": 5,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11362?filter=11351",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理)"},
                 {"title": "移动端",
                  "type": 6,
                  "link": "https://jira.qiaofangyun.com/browse/SAAS2-11362?filter=11351",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理)"}
                 ]

userQuestionCount = [{
    "title": "线上问题统计",
    "data": onlineBugInfo
}, {"title": "客户需求统计", "data": userIssueInfo}]

waitFixBugInfo = [
    {"title": "房客楼",
     "type": 3,
     "link": "https://jira.qiaofangyun.com/secure/Dashboard.jspa?selectPageId=10207",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND (labels is EMPTY OR labels not in (移动端, IOS, iOS, Android, 延迟修复)) AND (fixVersion <= V20.1905.00 OR fixVersion is EMPTY) AND createdDate < startOfDay(-8h)"},
    {"title": "交易组",
     "type": 4,
     "link": "https://jira.qiaofangyun.com/secure/Dashboard.jspa?selectPageId=10207",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND (labels is EMPTY OR labels not in (移动端, IOS, iOS, Android, 延迟修复)) AND (fixVersion <= V20.1905.00 OR fixVersion is EMPTY) AND createdDate < startOfDay(-8h)"},
    {"title": "公共组",
     "type": 5,
     "link": "https://jira.qiaofangyun.com/secure/Dashboard.jspa?selectPageId=10207",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND (labels is EMPTY OR labels not in (移动端, IOS, iOS, Android, 延迟修复)) AND (fixVersion <= V20.1905.00 OR fixVersion is EMPTY) AND createdDate < startOfDay(-8h)"},
    {"title": "移动端",
     "type": 6,
     "link": "https://jira.qiaofangyun.com/secure/Dashboard.jspa?selectPageId=10207",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND labels in (移动端, IOS, iOS, Android) AND (fixVersion <= V20.1905.00 OR fixVersion is EMPTY) AND createdDate < startOfDay(-8h) AND labels not in (延迟修复)"}]
waitVerifyBugInfo = [
    {"title": "房客楼",
     "type": 3,
     "link": "https://jira.qiaofangyun.com/secure/Dashboard.jspa?selectPageId=10207",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h)"},
    {"title": "交易组",
     "type": 4,
     "link": "https://jira.qiaofangyun.com/secure/Dashboard.jspa?selectPageId=10207",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h)"},
    {"title": "公共组",
     "type": 5,
     "link": "https://jira.qiaofangyun.com/secure/Dashboard.jspa?selectPageId=10207",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h)"},
    {"title": "移动端",
     "type": 6,
     "link": "https://jira.qiaofangyun.com/secure/Dashboard.jspa?selectPageId=10207",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h)"}]
dayBugCount = [{
    "title": "昨日待修复bug统计",
    "data": waitFixBugInfo
}, {
    "title": "昨日待验证bug统计",
    "data": waitVerifyBugInfo
}]


def searchUserStory(jira, jql):
    issues = jira.search_issues(jql, maxResults=10000)
    for issue in issues.iterable:
        createTime = parse(issue.fields.created[0:19])
        completedTime = parse(utc_to_local(
            issue.fields.resolutiondate[0:19])) if issue.fields.resolutiondate != None else parse(
            datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S")))
        issue.fields.diff = (completedTime - createTime).days
        issue.fields.createTime = createTime
        issue.fields.completedTime = completedTime
    data = map(lambda issue: {
        "问题关键字": issue.key,
        "概要": issue.fields.summary,
        "经办人": issue.fields.assignee.displayName,
        "问题创建时间": issue.fields.createTime,
        "问题完成时间": issue.fields.createTime,
        "平均完成时间": issue.fields.diff,
        "备注": ""
    },
               issues.iterable)
    fieldsDF = pd.DataFrame(data,
                            columns=["问题关键字", "概要", "经办人", "问题创建时间", "问题完成时间", "平均完成时间", "备注"])
    return fieldsDF


def searchSubTask(jira, maxResults=None):
    jql = "project = SAAS2 AND issuetype in ( 子任务) AND Sprint = 215 AND assignee in (nan.xia, zhen.xu, huainan.qu, jingyan.wan, haitao.cao, li.zhang)"

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


def searchIterationSummary(jira):
    jql = "project = SAAS2 AND issuetype in (任务, 用户故事) AND Sprint = 215 AND assignee in (nan.xia, zhen.xu, huainan.qu, jingyan.wan, haitao.cao, li.zhang)"
    issues = jira.search_issues(jql)
    print(issues)

    for issue in issues.iterable:
        # print(dir(issue.fields))
        print(vars(issue))

    data = map(lambda issue: {"问题类型": issue.fields.issuetype.name,
                              "JiraID": issue.key,
                              "概要": issue.fields.summary,
                              "初始预估（d）": math.ceil(
                                  issue.fields.aggregatetimeoriginalestimate / 3600 / 8) if issue.fields.aggregatetimeoriginalestimate else 0,
                              "完成百分比": "100%" if issue.fields.status.id == '6' else "0%",
                              "经办人": issue.fields.assignee.displayName,
                              "备注": ""
                              },
               issues.iterable)
    fieldsDF = pd.DataFrame(data, columns=["问题类型", "JiraID", "概要", "初始预估（d）", "经办人", "完成百分比", "备注"])
    fieldsDF.to_excel('sprint06迭代总结.xlsx', sheet_name='Sheet1')
    print(fieldsDF)


def searchDayIssue(jira, data):
    issues = jira.search_issues(data["jql"], maxResults=500)

    data = map(lambda issue: {
        "问题关键字": issue.key,
        "经办人": issue.fields.assignee.displayName,
    },
               issues.iterable)
    fieldsDF = pd.DataFrame(data)
    groups = fieldsDF.groupby(["经办人"]).size().reset_index(name='bug数量').sort_values(by="bug数量",
                                                                                    ascending=False)

    print(groups)
    # groups.set_index(["经办人"], inplace=True)

    # groups.plot(kind='bar', title=title, style='ko--', rot=0,
    #             yticks=range(0, groups['bug数量'].max() + 1))
    # plt.savefig(fileName)
    # plt.show()
    # uploadPhoto(fileName, title)


def uploadPhoto(fileName, title):
    headers = {
        "qf-auth-token": "qianhouduanliandiaoy_saas2_99dcd576f--item--2--item--9999--item--111111"}

    files = {'file': open(fileName, 'rb')}

    response = requests.post("http://jedibackend.dev.qiaofangyun.com/systemUpload/uploadSingleFile",
                             files=files, headers=headers)
    photoUrl = "https:" + response.json()['data']["fileUrl"]
    print("上传成功", photoUrl)
    # data = {
    #     "msgtype": "markdown",
    #     "markdown": {"title": title,
    #                  "text": '# ![]({uploadResult})  \n\n\n\n #### [点击查看]({link})'.format(
    #                      uploadResult=uploadResult, link=link
    #                  )},
    #     "at": {
    #         "isAtAll": False
    #     }
    # }
    # dingdingMsg(photoUrl, "https://jira.qiaofangyun.com/secure/Dashboard.jspa?selectPageId=10207",
    #             title)


def dingdingMsg(dingdingRobot, data):
    headers = {'Content-Type': 'application/json'}
    dingdingPost = requests.post(dingdingRobot, data=json.dumps(data), headers=headers)
    print(dingdingPost.text)


def completedIssueCount(jira, data, callBack, dingdingRobot=dingdingTest):
    allOnLinedata = []
    title = data["title"]
    for onLineBean in data["data"]:
        df = searchUserStory(jira, onLineBean["jql"])
        accumulatePD = pd.DataFrame(df.mean(numeric_only="平均完成时间"))
        onLineBean["totalCount"] = df.shape[0]
        onLineBean["meanTime"] = int(accumulatePD.loc["平均完成时间", 0])
        onLineBean["timeTitle"] = "平均完成时间" if onLineBean["type"] == 1 else "平均等待时间"
        allOnLinedata.append(callBack(onLineBean))
    dingMsg = {
        "msgtype": "markdown",
        "markdown": {
            "title": "{title}\n\n".format(title=title),
            "text": "## {title}\n\n".format(title=title) + "\n\n".join(allOnLinedata)
        },
        "at": {
            "isAtAll": False
        }
    }

    dingdingMsg(dingdingRobot, dingMsg)


def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S'):
    local_tz = pytz.timezone('Asia/Shanghai')  # 定义本地时区
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)  # 讲世界时间的格式转化为datetime.datetime格式
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(
        local_tz)  # 想将datetime格式添加上世界时区，然后astimezone切换时区：世界时区==>本地时区
    formatTime = int(time.mktime(local_dt.timetuple()))
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(formatTime))


if __name__ == '__main__':
    host = "https://jira.qiaofangyun.com"
    options = {'server': host}
    print("开始登录...")
    jira = JIRA(options, basic_auth=('huainan.qu', 'Qiaofang123'))
    print("登录成功...")
    for data in userQuestionCount:
        completedIssueCount(jira, data,
                            lambda
                                onLineBean: '### {title}:  {totalCount} 个； {timeTitle}:{time} ；[点击查看]({link})'.format(
                                title=onLineBean["title"], totalCount=onLineBean["totalCount"],
                                time=onLineBean["meanTime"],
                                timeTitle=onLineBean["timeTitle"],
                                link=onLineBean["link"]
                            ), onlineDingDing)

    for data in dayBugCount:
        completedIssueCount(jira, data,
                            lambda onLineBean: '### {title}:  {totalCount} 个；[点击查看]({link})'.format(
                                title=onLineBean["title"], totalCount=onLineBean["totalCount"],
                                link=onLineBean["link"]
                            ), dayBugDingDing)

