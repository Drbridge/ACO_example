from random import choice
from Kit.WorkStation import WorkStation
from copy import deepcopy

class Ant(object):
    def __init__(self, craneCost, vehicleCost, alpha = 2.0, beta = 6.0):
        self.wholeJob = ['P11', 'P12', 'P13', 'P14', 'P15',
                        'P21','P22','P23','P24','P25','P26',
                        'P31','P32','P33','P34','P35',
                        'P41','P42','P43']
        self.currentJob = ''
        self.nextJob = []
        self.moveProb = {}
        self.totalTime = 0
        self.dist = {}
        self.pher = {}
        self.cranes = WorkStation(cost=craneCost)
        self.vehicles = WorkStation(cost=vehicleCost)
        self.alpha = alpha
        self.beta = beta
        self.recoder = []

    def randomStart(self):
        self.currentJob = choice(self.wholeJob)
        self.recoder.append(self.currentJob)
        self.wholeJob.remove(self.currentJob)
        self.nextJob = []

        for _ in self.wholeJob:
            if self.currentJob[1] == _[1]:
                self.nextJob.append(_)

        if len(self.nextJob) == 0:
            self.nextJob = deepcopy(self.wholeJob)

        self.cranes.startJob(self.currentJob)
        self.vehicles.startJob(self.currentJob, self.cranes.endTime)
        self.totalTime += self.vehicles.endTime

    def calProb(self, globPheromone, distance):
        sum = 0
        t = []
        n = []
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

        self.pher[tmp] = self.cranes.startTime
        self.cranes.startJob(self.currentJob)
        self.vehicles.startJob(self.currentJob, self.cranes.endTime)
        self.totalTime += self.vehicles.endTime
        self.pher[tmp] = self.vehicles.endTime - self.pher[tmp]
        self.dist[tmp] = self.vehicles.endTime - self.cranes.startTime

    def updatePher(self, Q, key):
        return Q / self.dist[key]

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