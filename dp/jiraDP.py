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
        # self.jira = JIRA(options, basic_auth=(userName, userPW))
        self.jira = JIRA(options, basic_auth=("li.zhang", "Qiaofang123"))
        self.dingdingCount()
        print("登录成功...")
        # self.searchCustomerNeed()

        # self.searchCustomerNeed()
        # df = self.sprintSummary(
        #     'project = SAAS2 AND issuetype in (任务, 用户故事) AND Sprint = 232 AND assignee in (nan.xia, zhen.xu, huainan.qu, jingyan.wan, haitao.cao, li.zhang) ORDER BY Rank')
        # self.createExcel(df)

    def searchUserStory(self, jql):
        issues = self.jira.search_issues(jql, maxResults=10000)
        data = []
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
                (parse(updateTime if status == "6" else nowTime) - parse(
                    createTime)).total_seconds() / 3600 / 24, 1)
            issue.fields.createTime = createTime
            issue.fields.statusName = statusName
            issue.fields.status = status
            issue.fields.resolutionTime = resolutionTime
            issue.fields.updateTime = updateTime
            # 客户提需求日期
            customerNeedCreateDate = issue.fields.customfield_10700
            # 客户需求上线日期
            customerOnlineDate = issue.fields.customfield_10702
            # 客户需求预计上线日期
            customerOnlineDate = issue.fields.customfield_10701
            # print(vars(issue.fields))
            item = {
                "类型": issue.fields.issuetype.name,
                "问题关键字": issue.key,
                "概要": issue.fields.summary,
                "标签": issue.fields.labels,
                "预估时间": issue.fields.aggregatetimeoriginalestimate / 3600 / 8 if issue.fields.aggregatetimeoriginalestimate is not None else 0,
                "经办人": issue.fields.assignee.displayName if issue.fields.assignee is not None else None,
                "问题创建时间": issue.fields.createTime,
                "问题解决时间": issue.fields.resolutionTime,
                "问题更新时间": issue.fields.updateTime,
                "状态": issue.fields.status,
                "状态名称": issue.fields.statusName,
                "需求完成时间": issue.fields.diff,
                "客户需求预计上线日期": issue.fields.customfield_10701,
                "客户需求上线日期": issue.fields.customfield_10702,
                "客户提需求日期": issue.fields.customfield_10700,
                "子任务": issue.fields.subtasks,
                "备注": ""
            }
            data.append(item)

        fieldsDF = pd.DataFrame(data)
        self.createExcel(fieldsDF, "09.xlsx")
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

    def diffCustomerTime(self, item):
        nowTime = datetime.datetime.now().strftime(("%Y-%m-%d"))
        status = item["状态"]
        # 客户提需求日期
        customerNeedCreateDate = utc_to_local(
            item["客户提需求日期"][0:19], "%Y-%m-%d") if item["客户提需求日期"] else None
        # 客户需求上线日期
        customerOnlineDate = utc_to_local(
            item["客户需求上线日期"][0:19], "%Y-%m-%d") if item["客户需求上线日期"] else None
        # 客户需求预计上线日期
        customerxpectOnlineDate = utc_to_local(
            item["客户需求预计上线日期"][0:19], "%Y-%m-%d") if item["客户需求预计上线日期"] else None
        updateTime = item["问题更新时间"]
        endTime = customerOnlineDate if customerOnlineDate is not None else (
            customerxpectOnlineDate if customerxpectOnlineDate is not None else updateTime)
        return (parse(endTime if status == "6" else nowTime) - parse(
            customerNeedCreateDate)).total_seconds() / 3600 / 24

    def unCompletedStoryTime(self,item):
        nowTime = datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        status = item["状态"]
        updateTime = item["问题更新时间"]
        createTime = item["问题创建时间"]
        return round(
            (parse(updateTime if status == "6" else nowTime) - parse(
                createTime)).total_seconds() / 3600 / 24, 1)

    def completedIssueCount(self, data, callBack, dingdingRobot=dingdingTest):
        allOnLinedata = []
        print(data)
        title = data["title"]
        for onLineBean in data["data"]:
            df = self.searchUserStory(onLineBean["jql"])
            onLineBean["totalCount"] = df.shape[0]
            if onLineBean["type"].find("customer-story") > -1:
                customerCompletedDate = df.apply(lambda item: self.diffCustomerTime(item), axis=1)
                print(round(customerCompletedDate.sum()/customerCompletedDate.shape[0]))
                onLineBean["meanTime"] = int(
                    0 if customerCompletedDate.empty else round(customerCompletedDate.sum()/customerCompletedDate.shape[0]))

            else:
                customerUncompletedDate = df.apply(lambda item: self.unCompletedStoryTime(item), axis=1)
                onLineBean["meanTime"] = int(
                    0 if customerUncompletedDate.empty else round(customerUncompletedDate.sum()/customerUncompletedDate.shape[0]))

            onLineBean["timeTitle"] = "平均完成时间" if (onLineBean["type"] == "completed-customer-story"
                                                   or onLineBean[
                                                       "type"] == "completed-online-bug") else "平均等待时间"
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
        print(dingMsg)
        self.dingdingMsg(dingdingRobot, dingMsg)

    def dingdingMsg(self, dingdingRobot, data):
        headers = {'Content-Type': 'application/json'}
        dingdingPost = requests.post(dingdingTest, data=json.dumps(data), headers=headers)
        print(dingdingPost.text)
        pass

    def searchCustomerNeed(self):
        for data in userQuestionCount:
            self.completedIssueCount(data,
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
            self.completedIssueCount(data,
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

    def searchDayIssue(self, name, jql):
        fieldsDF = self.searchUserStory(jql)
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

    def computeSubTime(self, subTasks):
        time = 0
        for task in subTasks:
            issue = self.jira.issue(task.key)
            status = issue.fields.status.id
            if status == "6" or status == "5":
                time = time + issue.fields.aggregatetimeoriginalestimate if issue.fields.aggregatetimeoriginalestimate is not None else 0

        return time

    def storyCount(self, name, jql):
        df = self.searchUserStory(jql)
        storyCount = df.shape
        completedCount = df["状态"].map(lambda item: 1 if item == "6" else 0).sum()
        storyRollBack = df["标签"].map(lambda item: 1 if "需求移交打回" in item else 0).sum()
        developRollBack = df["标签"].map(lambda item: 1 if "提测打回" in item else 0).sum()
        serverRollBack = df["标签"].map(lambda item: 1 if "后端提测打回" in item else 0).sum()
        productRollBack = df["标签"].map(lambda item: 1 if "产品验收打回" in item else 0).sum()
        uiRollBack = df["标签"].map(lambda item: 1 if "视觉走查打回" in item else 0).sum()
        testSelf = df["标签"].map(lambda item: 1 if "狗食" in item else 0).sum()
        acutalCompletedTime = df["子任务"].map(
            lambda item: self.computeSubTime(item)).sum() / 3600 / 8
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

    def sprintSummary(self, jql):
        df = self.searchUserStory(jql)
        progress = df.apply(lambda item: str(
            round(self.computeSubTime(item["子任务"]) / 3600 / 8 / item["预估时间"] * 100)) + "%", axis=1)
        newDF = df.filter(
            items=['类型', '问题关键字', '概要', "预估时间"]).assign(完成百分比=lambda item: progress,
                                                        ).assign(未完成原因="")

        self.createExcel(newDF, name="sprint迭代总结.xlsx")
