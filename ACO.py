from Component import Ant

def main():
    # 起吊设备与小车的耗时时间表
    craneCost = {'P11':15, 'P12':26, 'P13':37, 'P14':9,'P15':32,
             'P21': 8, 'P22': 9, 'P23': 27, 'P24':11, 'P25': 4, 'P26': 5,
             'P31': 8, 'P32': 51, 'P33': 27, 'P34': 13, 'P35': 29,
             'P41': 10, 'P42':22, 'P43':25}
    vehicleCost = {'P11': 8, 'P12': 10, 'P13': 12, 'P14': 8, 'P15': 12,
                 'P21': 8, 'P22': 8, 'P23': 12, 'P24': 10, 'P25': 8, 'P26': 8,
                 'P31': 8, 'P32': 10, 'P33': 12, 'P34': 10, 'P35': 12,
                 'P41': 10, 'P42': 10, 'P43': 12}
    globPheromone = {}      # 全局信息素
    distance = {}           # 各设备之间移动耗时，起吊+小车 的总耗时
    ants = []               # 蚂蚁集
    ants_number = 1         # 蚂蚁数
    iter_time = 1           # 迭代次数

    calPram(craneCost, distance, globPheromone)

    for i in range(ants_number):
        ants.append(Ant.Ant(craneCost=craneCost, vehicleCost=vehicleCost))

    for _ in range(iter_time):
        for ant in ants:
            ant.reStart()       # 重设蚂蚁的状态
            ant.randomStart()   # 便蚂蚁随机选择起始位置

        for i in range(len(craneCost)):
            for ant in ants:
                # 计算下一个各个货物的选择概率
                ant.calProb(globPheromone=globPheromone, distance=distance)
                if len(ant.nextJob) == 0:
                    break
                # 选择下一个货物
                ant.turnNextJob()

        for __ in craneCost:
            for ___ in craneCost:
                if __ != __:
                    # 更新全局信息素
                    globPheromone[__ + ___] = (1 - 0.6) * globPheromone[__ + ___] + ant.updatePher(100, __ + ___)

    slo = ants[0]
    # 选择较优解输出
    for ant in range(len(ants)):
        if slo.totalTime <= ants[ant].totalTime:
            slo = ants[ant]

    print slo.recoder,slo.totalTime

# 计算全局信息素与各设备之前移动耗时
def calPram(cost, dist, pher):
    'cost: 起吊设备与小车的耗时时间表'
    'dist: 各设备之间的移动耗时表'
    'pher: 全局信息素'
    for a in cost:
        for b in cost:
            if a != b:
                # print a + b
                dist[a + b] = cost[a] + cost[b]
                pher[a + b] = 1

if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))