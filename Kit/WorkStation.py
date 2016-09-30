class WorkStation(object):
    # __costMatrix = {'P11':15, 'P12':26, 'P13':37, 'P14':9,'P15':32,
    #               'P21': 8, 'P22': 9, 'P23': 27, 'P24':11, 'P25': 4, 'P26': 5,
    #               'P31': 8, 'P32': 51, 'P33': 27, 'P34': 13, 'P35': 29,
    #               'P41': 10, 'P42':22, 'P43':25}

    def __init__(self, cost):
        self.startTime = 0
        self.endTime = 0
        self.costTime = 0
        self.costMatrix = cost

    # 重置工作站的状态为初态
    def init(self):
        self.startTime = 0
        self.endTime = 0
        self.costTime = 0

    # return current job cost time
    def __getCostTime(self, obj):
        try:
            _ = self.costMatrix[obj]
            return _
        except Exception, e:
            print '%s, %s' % ('can not get cost time', e)
            return 0

    # 开始工作，自动计算本次工作所用的时间，消耗时间为costTime，完成时间为endTime
    def startJob(self, obj, start = 0):
        'obj: 货物名'
        'start = 0: 开始工作时间，默认为0时刻'
        if start == 0:
            self.startTime = self.endTime
        else:
            self.startTime = start
        self.costTime = self.__getCostTime(obj)
        self.endTime = self.startTime + self.costTime
