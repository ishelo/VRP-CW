# -*- coding:utf-8 -*-
# @Author   : Helo
# @Email    : ishelo@aliyun.com
# @Language : Python3
# @Time     : 2019-07-20 21:08
# @Software : PyCharm

import csv
from operator import itemgetter

class Vrp():

    # -----------初始数据定义---------------------

    def __init__(self):
        self.mans = 7                                                   # 客户数量
        self.tons = 1895                                                # 车辆载重
        self.distanceLimit = 60                                         # 车辆一次行驶的最大距离
        self.distance = []                                              # 各个客户及配送中心距离
        self.q = [0, 628, 614, 507, 510, 581, 455, 547]                 # 8个客户分布需要的货物的需求量，第0位为配送中心自己
        self.savings = []                                               # 节约度
        self.Routes = []                                                # 路线
        self.Cost = 0                                                   # 总路程

    # -----------导入距离数据---------------------

    def datainput(self):
        with open("data2.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                line = [float(x) for x in line]
                self.distance.append(line)

    # -----------节约算法主程序---------------------

    def savingsAlgorithms(self):
        saving = 0
        for i in range(1, len(self.q)):
            self.Routes.append([i])

        for i in range(1, len(self.Routes) + 1):                                                 # 使用Sij = Ci0 + C0j - Cij计算节约度
            for j in range(1, len(self.Routes) + 1):
                if i == j:
                    pass
                else:
                    saving = (self.distance[i][0] + self.distance[0][j]) - self.distance[i][j]
                    self.savings.append([i, j, saving])                                          # 将结果以元组形式存放在列表中

        self.savings = sorted(self.savings, key=itemgetter(2), reverse=True)                     # 按照节约度从大到小进行排序
        for i in range(len(self.savings)):
            print(self.savings[i][0],'--',self.savings[i][1], "  ",self.savings[i][2])           # 打印节约度

        for i in range(len(self.savings)):
            startRoute = []
            endRoute = []
            routeDemand = 0
            for j in range(len(self.Routes)):
                if (self.savings[i][0] == self.Routes[j][-1]):
                    endRoute = self.Routes[j]
                elif (self.savings[i][1] == self.Routes[j][0]):
                    startRoute = self.Routes[j]

                if ((len(startRoute) != 0) and (len(endRoute) != 0)):
                    for k in range(len(startRoute)):
                        routeDemand += self.q[startRoute[k]]
                    for k in range(len(endRoute)):
                        routeDemand += self.q[endRoute[k]]
                    routeDistance = 0
                    routestore = [0]+endRoute+startRoute+[0]
                    for i in range(len(routestore)-1):
                        # print(routestore[i],routestore[i+1])
                        # print(self.distance[routestore[i]][routestore[i+1]])
                        routeDistance += self.distance[routestore[i]][routestore[i+1]]

                    #print(routestore,"== ==:",routeDistance)

                    if (routeDemand <= self.tons) and (routeDistance <= self.distanceLimit):     # 按照限制规则对​​路线进行更改
                        self.Routes.remove(startRoute)
                        self.Routes.remove(endRoute)
                        self.Routes.append(endRoute + startRoute)
                    break

        for i in range(len(self.Routes)):
            self.Routes[i].insert(0, 0)
            self.Routes[i].insert(len(self.Routes[i]), 0)

    # -----------输出最终结果---------------------

    def printRoutes(self):
        for i in self.Routes:
            costs = 0
            for j in range(len(i)-1):
                costs += self.distance[i[j]][i[j+1]]
            print("路线:  ",i,"  路程:  ",costs)

    def calcCosts(self):
        for i in range(len(self.Routes)):
            for j in range(len(self.Routes[i]) - 1):
                self.Cost += self.distance[self.Routes[i][j]][self.Routes[i][j + 1]]

        print("\nTotal Distance: ", round(self.Cost, 3))

    # -----------Master函数---------------------

    def start(self):                      # Master函数，调用所有其他函数
        print("== == == == == == == == == == == == == == == 导入数据 == == == == == == == = == == == == == == == =")
        self.datainput()
        print("== == == 距离表 == == ==")
        for i in self.distance:
            print(i)
        print("== == == 需求表 == == ==")
        print(self.q)
        print("== == == 限制条件 == == ==")
        print("车辆最大载重：",self.tons)
        print("车辆最长运输距离：", self.distanceLimit)
        print("== == == == == == == == == == == == == == == 节约度 == == == == == == == = == == == == == == == =")
        self.savingsAlgorithms()          # 函数调用计算节省量并生成路线
        print("== == == == == == == == == == == == == == == 结果 == == == == == == == = == == == == == == == =")
        self.printRoutes()
        self.calcCosts()
        self.datainput()