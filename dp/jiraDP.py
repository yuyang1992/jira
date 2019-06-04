import datetime
import json

import pandas as pd
import requests
from dateutil.parser import parse
from jira import JIRA

from config.jiraCfg import host, userQuestionCount, onlineDingDing, dayBugDingDing, dayBugCount, \
    dingdingTest
from utlis.dateUtlis import utc_to_local


class JiraDP(object):
    # 定义类属性记录单例对象引用
    instance = None
    jira = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def login(self, userName, userPW):
        options = {'server': host}
        print("开始登录...")
        self.jira = JIRA(options, basic_auth=(userName, userPW))
        print("登录成功...")

    def searchUserStory(self, jira, jql):
        issues = jira.search_issues(jql, maxResults=10000)
        for issue in issues.iterable:
            createTime = utc_to_local(issue.fields.created[0:19])
            statusName = issue.fields.status.name
            status = issue.fields.status.id
            updateTime = utc_to_local(issue.fields.updated[0:19]) if status == '6' else None
            nowTime = datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
            resolutionTime = utc_to_local(
                issue.fields.resolutiondate[
                0:19]) if issue.fields.resolutiondate is not None else None
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

    def exportSummrayExcel(self, sprintName):
        bugDF = self.searchDayIssue(sprintName, self.jira,
                                    "project = SAAS2 AND issuetype in (Bug, 故障) and createdDate >= '2019/5/13' and createdDate <= '2019/5/24' and component in (房源, 客源, 带看, 楼盘字典) and (labels not in (移动端, IOS, iOS, Android) or labels is EMPTY)")

        storyCountDF = self.storyCount(sprintName, self.jira,
                                       "project = SAAS2 AND issuetype in (用户故事, 任务) and createdDate >= '2019/5/13' and createdDate <= '2019/5/24' and component in (房源, 客源, 带看, 楼盘字典) and (labels not in (移动端, IOS, iOS, Android) or labels is EMPTY)")
        self.mergeDF(bugDF, storyCountDF)

    def mergeDF(self, bugDF, storyDF):
        self.createExcel(bugDF.merge(storyDF, right_index=True, left_index=True), "迭代总结统计.xlsx",
                         "房客组")
        pass

    def createExcel(self, df, name='sprint08.xlsx', sheet_name="sheet1"):
        df.to_excel(name, sheet_name=sheet_name)

    def dingdingCount(self):
        self.searchCustomerNeed()
        self.searchDayBug()

    def completedIssueCount(self, jira, data, callBack, dingdingRobot=dingdingTest):
        allOnLinedata = []
        title = data["title"]
        for onLineBean in data["data"]:
            df = self.searchUserStory(jira, onLineBean["jql"])
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

        self.dingdingMsg(dingdingRobot, dingMsg)

    def dingdingMsg(self, dingdingRobot, data):
        headers = {'Content-Type': 'application/json'}
        dingdingPost = requests.post(dingdingRobot, data=json.dumps(data), headers=headers)
        print(dingdingPost.text)

    def completedIssueCount(self, jira, data, callBack, dingdingRobot=dingdingTest):
        allOnLinedata = []
        title = data["title"]
        for onLineBean in data["data"]:
            df = self.searchUserStory(jira, onLineBean["jql"])
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

        self.dingdingMsg(dingdingRobot, dingMsg)

    def searchCustomerNeed(self):
        for data in userQuestionCount:
            self.completedIssueCount(self.jira, data,
                                     lambda
                                         onLineBean: '### {title}:  {totalCount} 个； {timeTitle}:{time}天 ；[点击查看]({link})'.format(
                                         title=onLineBean["title"],
                                         totalCount=onLineBean["totalCount"],
                                         time=onLineBean["meanTime"],
                                         timeTitle=onLineBean["timeTitle"],
                                         link=onLineBean["link"]
                                     ), onlineDingDing)

    def searchDayBug(self):
        for data in dayBugCount:
            self.completedIssueCount(self.jira, data,
                                     lambda
                                         onLineBean: '### {title}:  {totalCount} 个；[点击查看]({link})'.format(
                                         title=onLineBean["title"],
                                         totalCount=onLineBean["totalCount"],
                                         link=onLineBean["link"]
                                     ), dayBugDingDing)

    def countBugFixTime(self, dataFrame):
        data = []
        statusArray = dataFrame["状态"]
        for index in statusArray.index:
            time = self.diffTime(dataFrame["问题解决时间"][index], dataFrame["问题创建时间"][index]) if (
                    statusArray[index] == "5") else 0
            data.append(time * 24)
        return pd.Series(data)

    def countBugVerifyTime(self, dataFrame):
        data = []
        statusArray = dataFrame["状态"]
        for index in statusArray.index:
            time = self.diffTime(dataFrame["问题更新时间"][index], dataFrame["问题解决时间"][index]) if (
                    statusArray[index] == "6") else 0
            data.append(time * 24)
        return pd.Series(data)

    def diffTime(self, endTime, startTime):
        return round((parse(endTime) - parse(startTime)).total_seconds() / 3600 / 24, 1)

    def searchDayIssue(self, name, jira, jql):
        fieldsDF = self.searchUserStory(jira, jql)
        newDF = fieldsDF.assign(
            Bug修复时间=lambda df: self.countBugFixTime(df)).assign(
            Bug验证时间=lambda df: self.countBugVerifyTime(df))
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

    def computeSubTime(self,jira, subTasks):
        time = 0
        for task in subTasks:
            issue = jira.issue(task.key)
            status = issue.fields.status.id
            if status == "6" or status == "5":
                time = time + issue.fields.aggregatetimeoriginalestimate

        return time

    def storyCount(self, name, jira, jql):
        df = self.searchUserStory(jira, jql)
        storyCount = df.shape
        completedCount = df["状态"].map(lambda item: 1 if item == "6" else 0).sum()
        storyRollBack = df["标签"].map(lambda item: 1 if "需求移交打回" in item else 0).sum()
        developRollBack = df["标签"].map(lambda item: 1 if "提测打回" in item else 0).sum()
        serverRollBack = df["标签"].map(lambda item: 1 if "后端提测打回" in item else 0).sum()
        productRollBack = df["标签"].map(lambda item: 1 if "产品验收打回" in item else 0).sum()
        uiRollBack = df["标签"].map(lambda item: 1 if "视觉走查打回" in item else 0).sum()
        testSelf = df["标签"].map(lambda item: 1 if "狗食" in item else 0).sum()
        acutalCompletedTime = df["子任务"].map(
            lambda item: self.computeSubTime(jira, item)).sum() / 3600 / 8
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
