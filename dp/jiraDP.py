from services.JiraServices import JiraServices


class JiraDP(object):
    def login(self,userName, userPW):
        return JiraServices.login(self,userName, userPW)
