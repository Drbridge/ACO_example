# ACO_example
a demo of ACO algorithm

本代码为ACO在港口调度问题上的示例应用，采用蚂周模型

# 文件说明
## Compoent: 核心组件
### Ant.py
            本模块完成模拟ACO中蚂蚁行为的功能
#
## Kit: 辅助工具
### WorkStation.py
            本模块完成计算起吊设备、小车的耗时功能
#
## ACO.py
            本模块完成对ACO的参数初始化、运行控制与结果显示
#
# 算法说明
## step 1, 初始化起吊设备与小车的耗时时间表，craneCost, ehicleCost
## step 2, 初始化蚂蚁
## step 3, 随机分布蚂蚁，使蚂蚁随机选择起始货物
## step 4, 对每只蚂蚁下一步可选的货物计算选择概率
## step 5, 选择概率最大的作为下一步的货物
## step 6, 重复执行step (4,5), 直到所以蚂蚁均完成全部货物的调度
## step 7, 更新全局信息素
## step 8, 重复执行step (3，4，5，6，7)， 直到最大迭代次数
## step 9, 输出较优结果