"""
某在线游戏运营商对旗下的游戏后台数据做了快照，从中可以得到用户的登陆时间信息，希望据此快速得到历史最大的用户同时在线人数。

算法输入：每行英文逗号分隔的：一用户上线时间（简化为整数，不小于0）,下线时间（简化为整数，小于10000）；空行结束，如：

0,8
12,15
4,9
6,9
14,20
8,10
10,20

算法输出：最大同时在线人数，如：4
"""


class Statistics(object):

    def __init__(self):

        self.events = list()       # event (login, +1)  (logout, -1)
        self.logs = list()         # log (online, offline)
        self.max_nums = 0

    def input_data(self):
        print('Please input data of users!(start time, end time,e.g. 0,8.)')

        while True:
            line = input()
            if line == "":
                break
            login, logout = map(int, line.split(","))
            self.logs.append((login, logout))
            self.events.append((login, 1))
            self.events.append((logout + 1, -1))

    def calc_max_nums(self):

        self.events.sort()
        current_users = 0

        for event in self.events:
            current_users += event[1]
            self.max_nums = max(self.max_nums, current_users)

        return print(self.max_nums)


statistic = Statistics()
statistic.input_data()
statistic.calc_max_nums()