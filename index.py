import datetime
import json
import math
import sys
import time

import pandas as pd
import pytz
import requests
from PyQt5.QtWidgets import QApplication, QVBoxLayout
from apscheduler.schedulers.blocking import BlockingScheduler
from dateutil.parser import parse
from jira import JIRA

from views.JiraKit import JiraKit
from views.LoginView import LoginView

groups = [{"name": "移动端", "members": []},
          {"name": "人事公共组", "members": []},
          {"name": "交易组", "members": []},
          {"name": "房客组", "members": []}]
managerGroup = "https://oapi.dingtalk.com/robot/send?access_token=37c465ab11ebcfd3ba9c7a9bf8c858e8a8b7e8d72dced86e9a4dca3f0cc1b429"

mobileDingDing = "https://oapi.dingtalk.com/robot/send?access_token=7043c60fd960191bea14995dc87ace78a0f606d9e8aebb44d35bf033bf827d4c"
dingdingTest = "https://oapi.dingtalk.com/robot/send?access_token=edd1d68e9440e0bf634f2a3d4d9ab860bbcc45b658a9ae39eaba696e9ddc5eb7"
onlineDingDing = "https://oapi.dingtalk.com/robot/send?access_token=99b79b6f4949bf156da40ee500cee9bc881c4f4616fe17338c1663dccfdc8fb6"
dayBugDingDing = "https://oapi.dingtalk.com/robot/send?access_token=ad91f27b12153eade172f3a92a4d563a308c13bf56ec3ad3e0904cfba10c3aa1"
userIssueInfo = [{"title": "已完成总数",
                  "type": 1,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11350",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status = Closed AND labels not in (不予解决, 暂不处理)"},

                 {"title": "未完成总数",
                  "type": 2,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11351 ",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理)"},

                 {"title": "房客楼未完成",
                  "type": 3,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11358",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理) AND component in (房源, 客源, 楼盘字典, 带看) AND (labels not in (移动端, iOS, IOS, Android) OR labels is EMPTY)"},

                 {"title": "交易组未完成",
                  "type": 4,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11357",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理) AND component in (交易) AND (labels not in (移动端, iOS, IOS, Android) OR labels is EMPTY)"},

                 {"title": "公共组未完成",
                  "type": 5,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11359",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理) AND component in (公共, 首页, 审批流, 消息和待办, 组织结构, 考勤, 报表, 主页) AND (labels not in (移动端, iOS, IOS, Android) OR labels is EMPTY)"},
                 {"title": "移动端未完成",
                  "type": 6,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11360",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理) AND (labels in (移动端, iOS, IOS, Android) OR component in (移动端))"}
                 ]

onlineBugInfo = [{"title": "已完成总数",
                  "type": 1,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11352",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status = Closed"},
                 {"title": "未完成总数",
                  "type": 2,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11353",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status != Closed"},

                 {"title": "房客楼未完成",
                  "type": 3,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11361",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status != Closed AND component in (房源, 客源, 楼盘字典, 带看) AND (labels not in (移动端, iOS, IOS, Android) OR labels is EMPTY)"},

                 {"title": "交易组未完成",
                  "type": 4,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11362",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status != Closed AND component in (交易) AND (labels not in (移动端, iOS, IOS, Android) OR labels is not EMPTY)"},

                 {"title": "公共组未完成",
                  "type": 5,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11363",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status != Closed AND component in (公共, 首页, 审批流, 消息和待办, 组织结构, 考勤, 报表, 主页) AND (labels not in (移动端, iOS, IOS, Android) OR labels is EMPTY)"},
                 {"title": "移动端未完成",
                  "type": 6,
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11364",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status != Closed AND (labels in (移动端, iOS, IOS, Android) or component in (移动端))"}
                 ]

userQuestionCount = [{
    "title": "线上问题统计",
    "data": onlineBugInfo
}, {"title": "客户需求统计", "data": userIssueInfo}]

waitFixBugInfo = [
    {"title": "房客楼",
     "type": 3,
     "link": "https://jira.qiaofangyun.com/issues/?filter=11366",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND (labels is EMPTY OR labels not in (移动端, IOS, iOS, Android, 延迟修复)) AND createdDate < startOfDay(-8h) AND component in (房源, 客源, 楼盘字典, 带看)"},

    {"title": "交易组",
     "type": 4,
     "link": "https://jira.qiaofangyun.com/issues/?filter=11367",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND (labels is EMPTY OR labels not in (移动端, IOS, iOS, Android, 延迟修复)) AND createdDate < startOfDay(-8h) AND component in (交易)"},

    {"title": "公共组",
     "type": 5,
     "link": "https://jira.qiaofangyun.com/issues/?filter=11368",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND (labels is EMPTY OR labels not in (移动端, IOS, iOS, Android, 延迟修复)) AND createdDate < startOfDay(-8h) AND component in (公共, 首页, 审批流, 消息和待办, 组织结构, 考勤, 报表, 主页)"},

    {"title": "移动端",
     "type": 6,
     "link": "https://jira.qiaofangyun.com/issues/?filter=11311",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND (labels in (移动端, IOS, iOS, Android) OR component in (移动端)) AND createdDate < startOfDay(-8h) AND labels not in (延迟修复)"}]
waitVerifyBugInfo = [
    {"title": "房客楼",
     "type": 3,
     "link": "https://jira.qiaofangyun.com/issues/?filter=11369",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h) AND (labels is EMPTY OR labels not in (移动端, IOS, iOS, Android)) AND component in (房源, 客源, 楼盘字典, 带看)"},

    {"title": "交易组",
     "type": 4,
     "link": "https://jira.qiaofangyun.com/issues/?filter=11370",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h) AND (labels is EMPTY OR labels not in (移动端, IOS, iOS, Android)) AND component in (交易)"},

    {"title": "公共组",
     "type": 5,
     "link": "https://jira.qiaofangyun.com/issues/?filter=11371",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h) AND (labels is EMPTY OR labels not in (移动端, IOS, iOS, Android)) AND component in (公共, 首页, 审批流, 消息和待办, 组织结构, 考勤, 主页, 报表)"},

    {"title": "移动端",
     "type": 6,
     "link": "https://jira.qiaofangyun.com/issues/?filter=11372",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h) AND (labels in (移动端, iOS, IOS, Android) OR component in (移动端))"}]
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
        createTime = utc_to_local(issue.fields.created[0:19])
        statusName = issue.fields.status.name
        status = issue.fields.status.id
        updateTime = utc_to_local(issue.fields.updated[0:19]) if status == '6' else None
        nowTime = datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        resolutionTime = utc_to_local(
            issue.fields.resolutiondate[0:19]) if issue.fields.resolutiondate is not None else None
        issue.fields.diff = round(
            (parse(updateTime if status == 6 else nowTime) - parse(
                createTime)).total_seconds() / 3600 / 24, 1)
        issue.fields.createTime = createTime
        issue.fields.statusName = statusName
        issue.fields.status = status
        issue.fields.resolutionTime = resolutionTime
        issue.fields.updateTime = updateTime
    data = map(lambda issue: {
        "问题关键字": issue.key,
        "概要": issue.fields.summary,
        "标签": issue.fields.labels,
        "预估时间": issue.fields.aggregatetimeoriginalestimate / 3600 / 8 if issue.fields.aggregatetimeoriginalestimate is not None else 0,
        "经办人": issue.fields.assignee.displayName,
        "问题创建时间": issue.fields.createTime,
        "问题解决时间": issue.fields.resolutionTime,
        "问题更新时间": issue.fields.updateTime,
        "状态": issue.fields.status,
        "状态名称": issue.fields.statusName,
        "平均完成时间": issue.fields.diff,
        "子任务": issue.fields.subtasks,
        "备注": ""
    },
               issues.iterable)
    fieldsDF = pd.DataFrame(data)
    return fieldsDF


def diffTime(endTime, startTime):
    return round((parse(endTime) - parse(startTime)).total_seconds() / 3600 / 24, 1)


def searchSubTask(jira, maxResults=None):
    jql = "project = SAAS2 AND issuetype in ( 子任务) AND Sprint = 232 AND assignee in (nan.xia, zhen.xu, huainan.qu, jingyan.wan,yuanxiang.xu,  haitao.cao, li.zhang)"

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
        workTime = 18 if ("屈淮南" == name) else 56
        percent = math.ceil(time / workTime * 100).__str__() + "%"
        subTaskTime.append({"经办人": name, "任务估时": time, "可用工时": workTime, "饱和度": percent})
    subTaskDF = pd.DataFrame(subTaskTime, columns=["经办人", "任务估时", "可用工时", "饱和度"])
    print(subTaskDF)
    subTaskDF.to_excel('sprint08.xlsx', sheet_name='Sheet1')


def createExcel(df, name='sprint08.xlsx', sheet_name="sheet1"):
    df.to_excel(name, sheet_name=sheet_name)


def searchIterationSummary(jira, jql):
    # jql = "project = SAAS2 AND issuetype in (任务, 子任务) AND Sprint = 232 AND assignee in (currentUser(), nan.xia, zhen.xu, huainan.qu, jingyan.wan, li.zhang)"
    issues = jira.search_issues(jql)

    for issue in issues.iterable:
        # print(dir(issue.fields))
        print(issue.fields.subtasks)

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


def countBugFixTime(dataFrame):
    data = []
    statusArray = dataFrame["状态"]
    for index in statusArray.index:
        time = diffTime(dataFrame["问题解决时间"][index], dataFrame["问题创建时间"][index]) if (
                statusArray[index] == "5") else 0
        data.append(time * 24)
    return pd.Series(data)


def countBugVerifyTime(dataFrame):
    data = []
    statusArray = dataFrame["状态"]
    for index in statusArray.index:
        time = diffTime(dataFrame["问题更新时间"][index], dataFrame["问题解决时间"][index]) if (
                statusArray[index] == "6") else 0
        data.append(time * 24)
    return pd.Series(data)


def searchDayIssue(name, jira, jql):
    fieldsDF = searchUserStory(jira, jql)
    newDF = fieldsDF.assign(
        Bug修复时间=lambda df: countBugFixTime(df)).assign(
        Bug验证时间=lambda df: countBugVerifyTime(df))
    print(fieldsDF.shape[0])
    unFixCount = newDF["状态"].map(lambda item: 1 if item == "1" else 0).sum()
    unVerifyCount = newDF["状态"].map(lambda item: 1 if item == "5" else 0).sum()

    groups = newDF.filter(items=['经办人', "Bug修复时间", "Bug验证时间"], axis=1).groupby("经办人",

                                                                               sort=True)
    bugCountDF = groups.mean().round(1).assign(Bug平均数量=lambda item: groups.size()).sort_values(
        by=["Bug平均数量"], ascending=False)
    bugSeries = bugCountDF.mean().round(1)

    return pd.DataFrame(bugSeries.to_dict(), index=[name]).assign(未修复bug数量=unFixCount).assign(
        未验证bug数量=unVerifyCount).assign(Bug总数=fieldsDF.shape[0])


def computeSubTime(jira, subTasks):
    time = 0
    for task in subTasks:
        issue = jira.issue(task.key)
        status = issue.fields.status.id
        if status == "6" or status == "5":
            time = time + issue.fields.aggregatetimeoriginalestimate

    return time


def storyCount(name, jira, jql):
    df = searchUserStory(jira, jql)
    storyCount = df.shape
    completedCount = df["状态"].map(lambda item: 1 if item == "6" else 0).sum()
    storyRollBack = df["标签"].map(lambda item: 1 if "需求移交打回" in item else 0).sum()
    developRollBack = df["标签"].map(lambda item: 1 if "提测打回" in item else 0).sum()
    serverRollBack = df["标签"].map(lambda item: 1 if "后端提测打回" in item else 0).sum()
    productRollBack = df["标签"].map(lambda item: 1 if "产品验收打回" in item else 0).sum()
    uiRollBack = df["标签"].map(lambda item: 1 if "视觉走查打回" in item else 0).sum()
    testSelf = df["标签"].map(lambda item: 1 if "狗食" in item else 0).sum()
    acutalCompletedTime = df["子任务"].map(lambda item: computeSubTime(jira, item)).sum() / 3600 / 8
    planTime = df["预估时间"].sum()
    data = [{"总计划完成个数": storyCount[0],
             "总计划实际完成个数": completedCount,
             "计划完成工作量": planTime,
             "实际完成工作量": acutalCompletedTime,
             "需求移交打回个数": storyRollBack,
             "提测打回": developRollBack,
             "后端提测打回": serverRollBack,
             "产品验收打回": productRollBack,
             "视觉走查打回": uiRollBack,
             "狗食": testSelf}]
    return pd.DataFrame(data, index=[name])


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

        onLineBean["meanTime"] = int(
            0 if accumulatePD.empty else accumulatePD.loc["平均完成时间", 0])
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


def searchCustomerNeed(jira):
    for data in userQuestionCount:
        completedIssueCount(jira, data,
                            lambda
                                onLineBean: '### {title}:  {totalCount} 个； {timeTitle}:{time}天 ；[点击查看]({link})'.format(
                                title=onLineBean["title"], totalCount=onLineBean["totalCount"],
                                time=onLineBean["meanTime"],
                                timeTitle=onLineBean["timeTitle"],
                                link=onLineBean["link"]
                            ), onlineDingDing)


def searchDayBug(jira):
    for data in dayBugCount:
        completedIssueCount(jira, data,
                            lambda onLineBean: '### {title}:  {totalCount} 个；[点击查看]({link})'.format(
                                title=onLineBean["title"], totalCount=onLineBean["totalCount"],
                                link=onLineBean["link"]
                            ), dayBugDingDing)


def timeTask(hour, minute):
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', hour=hour, minute=minute)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def job():
    # searchSubTask(jira, 1000)
    # createExcel(searchUserStory(jira,
    #                             "project = SAAS2 AND issuetype in (任务, 用户故事) AND Sprint = 232 AND assignee in (nan.xia, zhen.xu, huainan.qu, jingyan.wan, haitao.cao, li.zhang)"))
    # searchDayIssue()
    host = "https://jira.qiaofangyun.com"
    options = {'server': host}
    print("开始登录...")
    jira = JIRA(options, basic_auth=('huainan.qu', 'Qiaofang123'))
    print("登录成功...")
    searchCustomerNeed(jira)
    searchDayBug(jira)
    print("定时任务")


def mergeDF(bugDF, leftName, storyDF, rightName):
    createExcel(bugDF.merge(storyDF, right_index=True, left_index=True), "迭代总结统计.xlsx", "房客组")
    pass


def searchGroupInfo():
    # for group in groups:
    #     groupInfo = jira.group_members(group["name"])
    #     members = []
    #     for k in groupInfo:
    #         members.append(groupInfo[k]["fullname"])
    #     group["members"] = members

    timeTask(9, 22)

    # bugDF = searchDayIssue("sprint08", jira,
    #                        "project = SAAS2 AND issuetype in (Bug, 故障) and createdDate >= '2019/5/13' and createdDate <= '2019/5/24' and component in (房源, 客源, 带看, 楼盘字典) and (labels not in (移动端, IOS, iOS, Android) or labels is EMPTY)")
    #
    # print(bugDF)
    # storyCountDF = storyCount("sprint08", jira,
    #                           "project = SAAS2 AND issuetype in (用户故事, 任务) and createdDate >= '2019/5/13' and createdDate <= '2019/5/24' and component in (房源, 客源, 带看, 楼盘字典) and (labels not in (移动端, IOS, iOS, Android) or labels is EMPTY)")
    # print(storyCountDF)
    # print(mergeDF(bugDF, "sprint08", storyCountDF, "sprint08"))
    # print(groups)


if __name__ == '__main__':
    # searchGroupInfo()
    app = QApplication(sys.argv)

    # ui = JiraKit()
    # ui.show()
    login = JiraKit()

    sys.exit(app.exec_())
