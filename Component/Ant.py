from random import choice
from Kit.WorkStation import WorkStation
from copy import deepcopy

class Ant(object):
    def __init__(self, craneCost, vehicleCost, alpha = 2.0, beta = 6.0):
        # 全部货物表
        self.wholeJob = ['P11', 'P12', 'P13', 'P14', 'P15',
                        'P21','P22','P23','P24','P25','P26',
                        'P31','P32','P33','P34','P35',
                        'P41','P42','P43']
        self.currentJob = ''                                # 当前的移动的货物
        self.nextJob = []                                   # 下一个可以移动的货物集
        self.moveProb = {}                                  # 下一下可以移到的货物概率集
        self.totalTime = 0                                  # 当前总移动消耗时间值
        self.dist = {}                                      # 各个货物之间移动消耗的时间值
        self.pher = {}                                      # 该蚂蚁自己的留下的信息素
        self.cranes = WorkStation(cost=craneCost)           # 起吊设备
        self.vehicles = WorkStation(cost=vehicleCost)       # 小车设备
        self.alpha = alpha                                  # ACO算法中的常数值
        self.beta = beta                                    # ACO算法中的常数值
        self.recoder = []                                   # 货物运输序列的记录，最终的结果输出

    def randomStart(self):
        # 随机选择一个货物开始运输
        self.currentJob = choice(self.wholeJob)
        self.recoder.append(self.currentJob)
        self.wholeJob.remove(self.currentJob)
        self.nextJob = []

        for _ in self.wholeJob:
            if self.currentJob[1] == _[1]:
                self.nextJob.append(_)

        if len(self.nextJob) == 0:
            self.nextJob = deepcopy(self.wholeJob)
        
        # 设置吊车、小车开始工作，并得到本次运输时间
        self.cranes.startJob(self.currentJob)
        self.vehicles.startJob(self.currentJob, self.cranes.endTime)
        self.totalTime += self.vehicles.endTime

    # 计算下一个可选的货物的概率值
    def calProb(self, globPheromone, distance):
        'globPheromone: 全局信息值'
        'distance: 全局距离值'
        sum = 0     # 公式中的和值
        t = []      # 临时变量，记录全局信息素的alpha次方值
        n = []      # 临时变量，记录全局距离的beta次方值
        self.moveProb = {}
        for job in self.nextJob:
            # print self.nextJob,self.currentJob,self.wholeJob
            _t = globPheromone[self.currentJob+job] ** self.alpha
            t.append(_t)
            _n = distance[self.currentJob + job] ** self.beta
            n.append(_n)
            sum += _t * _n
        for i in range(len(self.nextJob)):
            self.moveProb[self.nextJob[i]] = (t[i] * n[i]) / sum
        # print self.moveProb,self.nextJob

    # 选择下一个货物并记录在recoder，同时计算消耗时间
    def turnNextJob(self):
        prob = 0.0
        for _ in self.moveProb:
            if prob <= self.moveProb[_]:
                prob = self.moveProb[_]
                job = _
        tmp = self.currentJob+job
        self.recoder.append(job)
        try:
            self.wholeJob.remove(job)
        except Exception,e:
            # print self.currentJob,e,self.wholeJob
            pass
        self.currentJob = job
        self.nextJob = []

        for _ in self.wholeJob:
            if self.currentJob[1] == _[1]:
                self.nextJob.append(_)

        if len(self.nextJob) == 0:
            self.nextJob = deepcopy(self.wholeJob)
        # print self.nextJob,self.currentJob,self.wholeJob

        # 更新自身的信息
        self.pher[tmp] = self.cranes.startTime
        self.cranes.startJob(self.currentJob)
        self.vehicles.startJob(self.currentJob, self.cranes.endTime)
        self.totalTime += self.vehicles.endTime
        self.pher[tmp] = self.vehicles.endTime - self.pher[tmp]
        self.dist[tmp] = self.vehicles.endTime - self.cranes.startTime
    
    # 辅助更新全局信息素
    def updatePher(self, Q, key):
        return Q / self.dist[key]

    # 重置蚂蚁的全部信息
    def reStart(self):
        self.wholeJob = ['P11', 'P12', 'P13', 'P14', 'P15',
                         'P21', 'P22', 'P23', 'P24', 'P25', 'P26',
                         'P31', 'P32', 'P33', 'P34', 'P35',
                         'P41', 'P42', 'P43']
        self.currentJob = ''
        self.nextJob = []
        self.moveProb = {}
        self.totalTime = 0
        self.cranes.init()
        self.vehicles.init()
        self.recoder = []
        self.pher = {}