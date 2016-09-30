from Component import Ant

def main():
    craneCost = {'P11':15, 'P12':26, 'P13':37, 'P14':9,'P15':32,
             'P21': 8, 'P22': 9, 'P23': 27, 'P24':11, 'P25': 4, 'P26': 5,
             'P31': 8, 'P32': 51, 'P33': 27, 'P34': 13, 'P35': 29,
             'P41': 10, 'P42':22, 'P43':25}
    vehicleCost = {'P11': 8, 'P12': 10, 'P13': 12, 'P14': 8, 'P15': 12,
                 'P21': 8, 'P22': 8, 'P23': 12, 'P24': 10, 'P25': 8, 'P26': 8,
                 'P31': 8, 'P32': 10, 'P33': 12, 'P34': 10, 'P35': 12,
                 'P41': 10, 'P42': 10, 'P43': 12}
    globPheromone = {}
    distance = {}
    ants = []
    ants_number = 1
    iter_time = 1

    calPram(craneCost, distance, globPheromone)

    for i in range(ants_number):
        ants.append(Ant.Ant(craneCost=craneCost, vehicleCost=vehicleCost))

    for _ in range(iter_time):
        for ant in ants:
            ant.reStart()
            ant.randomStart()

        for i in range(len(craneCost)):
            for ant in ants:
                ant.calProb(globPheromone=globPheromone, distance=distance)
                if len(ant.nextJob) == 0:
                    break
                ant.turnNextJob()

        for __ in craneCost:
            for ___ in craneCost:
                if __ != __:
                    globPheromone[__ + ___] = (1 - 0.6) * globPheromone[__ + ___] + ant.updatePher(100, __ + ___)

    slo = ants[0]
    for ant in range(len(ants)):
        if slo.totalTime <= ants[ant].totalTime:
            slo = ants[ant]

    print slo.recoder,slo.totalTime

def calPram(cost, dist, pher):
    for a in cost:
        for b in cost:
            if a != b:
                # print a + b
                dist[a + b] = cost[a] + cost[b]
                pher[a + b] = 1

if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))