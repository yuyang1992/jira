from jira import JIRA

from config.jiraCfg import host


class JiraServices(object):

    def login(self, userName, userPW):
        options = {'server': host}
        print("开始登录...")
        return JIRA(options, basic_auth=(userName, userPW))
