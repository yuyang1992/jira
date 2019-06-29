host = "https://jira.qiaofangyun.com"

groups = [{"name": "移动端", "members": []},
          {"name": "人事公共组", "members": []},
          {"name": "交易组", "members": []},
          {"name": "房客组", "members": []}]

memberWorkTimes = [{
    "name": "屈淮南",
    "profession": "Android",
    "duration": 7,
    "day": 9,
    "percent": 0.3,
}, {
    "name": "张荔",
    "profession": "Android",
    "duration": 7,
    "day": 9,
    "percent": 1,

}, {
    "name": "吴昊",
    "profession": "IOS",
    "duration": 7,
    "day": 9,
    "percent": 1,

}, {
    "name": "万经言",
    "profession": "Android",
    "duration": 7,
    "day": 9,
    "percent": 1,

}, {
    "name": "徐臻",
    "profession": "IOS",
    "duration": 7,
    "day": 9,
    "percent": 1,

}, {
    "name": "曹海涛",
    "profession": "IOS",
    "duration": 7,
    "day": 9,
    "percent": 1,

}, {
    "name": "徐远翔",
    "profession": "测试",
    "duration": 7,
    "day": 9,
    "percent": 1,
}, {
    "name": "虞阳",
    "profession": "测试",
    "duration": 7,
    "day": 9,
    "percent": 1,
}]
managerGroup = "https://oapi.dingtalk.com/robot/send?access_token=37c465ab11ebcfd3ba9c7a9bf8c858e8a8b7e8d72dced86e9a4dca3f0cc1b429"

mobileDingDing = "https://oapi.dingtalk.com/robot/send?access_token=7043c60fd960191bea14995dc87ace78a0f606d9e8aebb44d35bf033bf827d4c"
dingdingTest = "https://oapi.dingtalk.com/robot/send?access_token=edd1d68e9440e0bf634f2a3d4d9ab860bbcc45b658a9ae39eaba696e9ddc5eb7"
onlineDingDing = "https://oapi.dingtalk.com/robot/send?access_token=99b79b6f4949bf156da40ee500cee9bc881c4f4616fe17338c1663dccfdc8fb6"
dayBugDingDing = "https://oapi.dingtalk.com/robot/send?access_token=ad91f27b12153eade172f3a92a4d563a308c13bf56ec3ad3e0904cfba10c3aa1"
userIssueInfo = [{"title": "已完成总数",
                  "type": "completed-customer-story",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11350",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status = Closed AND labels not in (不予解决, 暂不处理) AND resolution in (已解决, Done, 完成) AND priority in (P0, P1, P2)"},

                 {"title": "未完成总数",
                  "type": "uncompleted-customer-story",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11351 ",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理) AND priority in (P0, P1, P2)"},

                 {"title": "房客楼未完成",
                  "type": "house-uncompleted-customer-story",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11358",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理) AND (component in (房源, 客源, 楼盘字典, 带看, 采房, 营销) AND (labels not in (移动端, iOS, IOS, Android) OR labels is EMPTY) AND 所属团队 is EMPTY OR 所属团队 = 房客楼组) AND priority in (P0, P1, P2)"},

                 {"title": "交易组未完成",
                  "type": "transaction-uncompleted-customer-story",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11357",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理) AND (component in (交易, 新房) AND (labels not in (移动端, iOS, IOS, Android) OR labels is EMPTY) AND 所属团队 is EMPTY OR 所属团队 = 交易组) AND priority in (P0, P1, P2)"},

                 {"title": "公共组未完成",
                  "type": "common-uncompleted-customer-story",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11359",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理) AND (component in (公共, 首页, 审批流, 消息和待办, 组织结构, 考勤, 报表, 主页, 行程) AND (labels not in (移动端, iOS, IOS, Android) OR labels is EMPTY) AND 所属团队 is EMPTY OR 所属团队 = 人事公共组) AND priority in (P0, P1, P2)"},
                 {"title": "移动端未完成",
                  "type": "mobile-uncompleted-customer-story",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11360",
                  "jql": "project = SAAS2 AND issuetype = 用户故事 AND 客户提需求日期 is not EMPTY AND status != Closed AND labels not in (不予解决, 暂不处理) AND ((labels in (移动端, iOS, IOS, Android) OR component in (移动端)) AND 所属团队 is EMPTY OR 所属团队 = 移动端) AND priority in (P0, P1, P2)"}
                 ]

onlineBugInfo = [{"title": "已完成总数",
                  "type": "completed-online-bug",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11352",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status = Closed"},
                 {"title": "未完成总数",
                  "type": "uncompleted-online-bug",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11353",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status != Closed"},

                 {"title": "房客楼未完成",
                  "type": "house-uncompleted-online-bug",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11361",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status != Closed AND component in (房源, 客源, 楼盘字典, 带看) AND (labels not in (移动端, iOS, IOS, Android) OR labels is EMPTY)"},

                 {"title": "交易组未完成",
                  "type": "transaction-uncompleted-online-bug",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11362",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status != Closed AND component in (交易,新房) AND (labels not in (移动端, iOS, IOS, Android) OR labels is not EMPTY)"},

                 {"title": "公共组未完成",
                  "type": "common-uncompleted-online-bug",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11363",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status != Closed AND component in (公共, 首页, 审批流, 消息和待办, 组织结构, 考勤, 报表, 主页) AND (labels not in (移动端, iOS, IOS, Android) OR labels is EMPTY)"},
                 {"title": "移动端未完成",
                  "type": "mobile-uncompleted-online-bug",
                  "link": "https://jira.qiaofangyun.com/issues/?filter=11364",
                  "jql": "project = SAAS2 AND issuetype = 线上问题 AND status != Closed AND (labels in (移动端, iOS, IOS, Android) or component in (移动端))"}
                 ]

userQuestionCount = [
    {"title": "客户需求统计", "type": "userStory", "data": userIssueInfo},
    {"title": "线上问题统计", "type": "onlineBug", "data": onlineBugInfo}
]

waitFixBugInfo = [
    {"title": "房客楼",
     "type": "house-wait-fix-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11366",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND (labels is EMPTY OR labels not in (延迟修复)) AND createdDate < startOfDay(-8h) AND assignee in membersOf(房客组)"},

    {"title": "交易组",
     "type": "transaction-wait-fix-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11367",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND (labels is EMPTY OR labels not in (延迟修复)) AND createdDate < startOfDay(-8h) AND assignee in membersOf(交易组)"},

    {"title": "公共组",
     "type": "common-wait-fix-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11368",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND (labels is EMPTY OR labels not in (延迟修复)) AND createdDate < startOfDay(-8h) AND assignee in membersOf(人事公共组)"},

    {"title": "移动端",
     "type": "mobile-wait-fix-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11311",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND assignee in membersOf(移动端) AND createdDate < startOfDay(-8h) AND labels not in (延迟修复)"}]
waitVerifyBugInfo = [
    {"title": "房客楼",
     "type": "house-wait-fix-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11369",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h) AND assignee in membersOf(房客组)"},

    {"title": "交易组",
     "type": "transaction-wait-fix-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11370",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h) AND assignee in membersOf(交易组)"},

    {"title": "公共组",
     "type": "common-wait-fix-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11371",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h) AND assignee in membersOf(人事公共组)"},

    {"title": "移动端",
     "type": "mobile-wait-fix-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11372",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(-7h) AND assignee in membersOf(移动端)"}]

waitCloseBugInfo = [
    {"title": "房客楼",
     "type": "house-wait-close-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11373",
     "jql": "project in ('SaaS 2.0') AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened, 已解决) AND assignee in membersOf(房客组)"},

    {"title": "交易组",
     "type": "transaction-wait-close-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11374",
     "jql": "project in ('SaaS 2.0') AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened, 已解决) AND assignee in membersOf(交易组)"},

    {"title": "公共组",
     "type": "common-wait-close-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11375",
     "jql": "project in ('SaaS 2.0') AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened, 已解决) AND assignee in membersOf(人事公共组)"},

    {"title": "移动端",
     "type": "mobile-wait-close-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11376",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened, 已解决) AND assignee in membersOf(移动端)"}]

delayFixBugInfo = [
    {"title": "房客楼",
     "type": "house-delay-close-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11384",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND labels in (延迟修复) AND assignee in membersOf(房客组)"},

    {"title": "交易组",
     "type": "transaction-delay-close-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11386",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND labels in (延迟修复) AND assignee in membersOf(交易组)"},

    {"title": "公共组",
     "type": "common-delay-close-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11385",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND labels in (延迟修复) AND assignee in membersOf(人事公共组)"},
    {"title": "移动端",
     "type": "mobile-delay-close-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11313",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND assignee in membersOf(移动端) AND labels in (延迟修复)"}]

dayBugCount = [{
    "title": "昨日待修复bug统计",
    "type": "wait-fix-bug",
    "data": waitFixBugInfo
}, {
    "title": "昨日待验证bug统计",
    "type": "wait-verify-bug",
    "data": waitVerifyBugInfo
}, {
    "title": "未关闭Bug总数统计(包含今日待修复与待验证的Bug)",
    "type": "wait-close-bug",
    "data": waitCloseBugInfo
}, {
    "title": "延迟修复Bug总数统计",
    "type": "delay-fix-bug",
    "data": delayFixBugInfo
}]

mobileDayBugCount = [{
    "title": "待修复bug统计",
    "type": "wait-fix-bug",
    "data": waitFixBugInfo
}, {
    "title": "待验证bug统计",
    "type": "wait-verify-bug",
    "data": waitVerifyBugInfo
}]

mobileDingDingTask = [
    {"title": "移动端待修复Bug",
     "type": "mobile-wait-fix-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11470",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (Open, 'In Progress', Reopened) AND labels in (移动端, IOS, iOS, Android) AND createdDate < startOfDay(16h) AND labels not in (延迟修复)"},
    {"title": "移动端待验证Bug",
     "type": "mobile-wait-verify-bug",
     "link": "https://jira.qiaofangyun.com/issues/?filter=11471",
     "jql": "project = SAAS2 AND issuetype in (Bug, 故障) AND status in (已解决) AND resolved < startOfDay(17h) AND labels in (移动端, IOS, iOS, Android)"
     }
]

groupDingDingTask = [
    {
        "title": "移动端钉钉提醒",
        "type": "mobile",
        "dingDing": 'https://oapi.dingtalk.com/robot/send?access_token=d826402b34bb0b42db763df60360909b3fba65975ba88b81a725c401a9f5400b',
        "data": mobileDingDingTask
    }
]
