import numpy as np
import operator

MAX_FEATURE = 13  #参与分类特性个数

def file2matrix(filename):
    fr = open(filename)
    # 获得文件中的数据行的行数
    filelines = len(fr.readlines())

    returndata = np.zeros((filelines, MAX_FEATURE))  # prepare matrix to return
    classlabel = []  # prepare labels return
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        # 缺省用空格分割字符串
        listfromline = line.split()
        # 每列的属性数据
        returndata[index, :] = listfromline[0:13]
        # 每列的类别数据，就是 label 标签数据
        classlabel.append(int(listfromline[-1]))
        index += 1
    # 返回数据矩阵returnMat和对应的类别classLabel
    return returndata, classlabel


def autoNorm(dataSet):
    """
    归一化公式：
        Y = (X-Xmin)/(Xmax-Xmin)
        其中的 min 和 max 分别是数据集中的最小特征值和最大特征值。该函数可以自动将数字特征值转化为0到1的区间。
    """
    # 计算每种属性的最大值、最小值、范围
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    # 极差
    ranges = maxVals - minVals
    normDataSet = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]
    # 生成与最小值之差组成的矩阵
    normDataSet = dataSet - np.tile(minVals, (m, 1))
    # 将最小值之差除以范围组成矩阵
    normDataSet = normDataSet / np.tile(ranges, (m, 1))  # element wise divide
    return normDataSet, ranges, minVals


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    #距离度量 度量公式为欧氏距离
    diffMat = np.tile(inX, (dataSetSize,1))-dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    
    #将距离排序：从小到大
    sortedDistIndicies = distances.argsort()
    #选取前K个最短距离， 选取这K个中最多的分类类别
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1 
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def hdClassTest():
    # 设置测试数据的的一个比例（训练数据集比例=1-hoRatio）
    hoRatio = 0.5  # 测试范围,一部分测试一部分作为样本
    # 从文件中加载数据
    datingDataMat, datingLabels = file2matrix('hd_data.txt')  # load data setfrom file
    # 归一化数据
    normMat, ranges, minVals = autoNorm(datingDataMat)
    # m 表示数据的行数，即矩阵的第一维
    m = normMat.shape[0]
    # 设置测试的样本数量， numTestVecs:m表示训练样本的数量
    numTestVecs = int(m * hoRatio)
    print('numTestVecs={0}'.format(numTestVecs))
    errorCount = 0.0
    for i in range(numTestVecs):
        # 对数据测试
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print("the classifier came back with: {0}, the real answer is: {1}".format(classifierResult, datingLabels[i]))
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print("the total error rate is: {0}".format(errorCount/float(numTestVecs)))
    print("errorCount:{}".format(errorCount))



hdClassTest()


