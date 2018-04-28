from numpy import *
import numpy as np
import pulp
from scipy.linalg import solve
import sys

def linear_program(arr):
    min=0
    for i in range(len(arr)):
        for j in range(len(arr[0])):
           if arr[i][j]<min:
               min=arr[i][j]
    if min<0:
        add_num=-min
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                arr[i][j]=arr[i][j]+add_num
    else:
        add_num=0
    table = [[0 for j in range(len(arr[0])+2)] for i in range(len(arr)+2)]

    for i in range(len(arr)+2):
        for j in range(len(arr[0])+2):
            if i==0:
                table[i][j]='y'+str(j)
            elif j==0:
                table[i][j]='x'+str(i)
            elif i==len(arr[0])+1 and j==len(arr)+1:
                table[i][j]=0
            elif i==len(arr)+1:
                table[i][j]=-1
            elif j==len(arr[0])+1:
                table[i][j]=1
            else:
                table[i][j]=arr[i-1][j-1]
    table[len(arr)+1][len(arr[0])+1]=0
    #print(table)
    while True:
        min_last_row=0
        pivot_y=-1
        for i in range(1,len(arr[0])+1):
            if table[len(arr)+1][i]<min_last_row:
                min_last_row=table[len(arr)+1][i]
                pivot_y=i
        if min_last_row>=0:
            break
        min_ratio=sys.maxsize
        pivot_x=-1
        #print("yy",pivot_y)
        for i in range(1,len(arr)+1):
            if table[i][pivot_y]<0:
                ratio=sys.maxsize
            elif table[i][pivot_y]==0:
                ratio=sys.maxsize
            else:
                ratio=table[i][len(arr[0])+1]/table[i][pivot_y]
            if ratio<min_ratio:
                min_ratio=ratio
                pivot_x=i
        next_table= [[0 for j in range(len(arr[0])+2)] for i in range(len(arr)+2)]
        pivot=table[pivot_x][pivot_y]
        #print(pivot)
        #print(pivot_x)
        for i in range(1,len(arr) + 2):
            for j in range(1,len(arr[0]) + 2):
                if i==pivot_x and j==pivot_y:
                    next_table[i][j]=1/pivot
                elif i==pivot_x and j!=pivot_y:
                    next_table[i][j]=table[i][j]/pivot
                elif j==pivot_y and i!=pivot_x:
                    next_table[i][j]=table[i][j]/(0-pivot)
                elif i!=pivot_x and j!=pivot_y:
                    if i==len(arr)+1 and j==len(arr[0])+1:
                        print(table[i][j],table[i][pivot_y],table[pivot_x][j],pivot)
                    next_table[i][j]=table[i][j]-(table[i][pivot_y]*table[pivot_x][j])/pivot
        for i in range(1,len(arr)+1):
            if i==pivot_x:
                next_table[i][0]=table[0][pivot_y]
            else:
                next_table[i][0]=table[i][0]
        for i in range(1,len(A[0])+1):
            if i==pivot_y:
                next_table[0][i]=table[pivot_x][0]
            else:
                next_table[0][i]=table[0][i]
        table=next_table
        #print(table)
    p=[]
    q=[]
    value=(1/table[len(arr)+1][len(arr[0])+1])-add_num
    temp1=0
    temp2=0
    y_list=[]
    x_list=[]

    for i in range(1,len(arr)+1):
        if table[i][0] == "y"+str(i):
            q[i]=table[i][len(A[0])+1]
            temp1=temp1+table[i][len(arr[0])+1]
    #print(q)

    temp1 = 1 / temp1

    for i in range(len(q)):
        q[i]=q[i]*temp1
    for i in range(1,len(arr[0])+1):
        if table[0][i] == "x"+str(i):
            p[i]=table[len(arr)+1][i]
            temp2=temp2+table[len(arr)+1][i]
    #print(p)

    temp2=1/temp2
    for i in range(len(p)):
        p[i]=p[i]*temp2
    return p,q,value


def saddlePoint(arr):
	minOfRow = []
	for each in arr:
		minOfRow.append(each[0, :].min())
	for i in range(arr.shape[1]):
		if arr[:, i].max() in minOfRow:
			return (arr[:, i].max(), minOfRow.index(arr[:, i].max()), i)
	return False


def TByT(arr):# two by two matrix
	a = arr[0, 0]
	b = arr[0, 1]
	d = arr[1, 0]
	c = arr[1, 1]
	p = (c - d) / (a - b + c - d)
	q = (c - b) / (a - b + c - d)
	V = (c * a - b * d) / (a - b + c - d)
	return [round(V, 2), round(p, 2), round(q, 2)]


def TByN(arr): # two by N matrix
	temp = mat([[0], [0]])
	rest = []
	model = pulp.LpProblem("twoByN", pulp.LpMaximize)
	p = pulp.LpVariable('p', lowBound=0, upBound=1)
	V = pulp.LpVariable('V')
	model += V, "Value"
	for i in range(arr.shape[1]):
		model += arr[0, i] * p + arr[1, i] * (1 - p) >= V
	model.solve()
	V = round(pulp.value(model.objective), 2)
	for i in range(arr.shape[1]):  # check which column is useful
		if round(arr[0, i] * p.varValue + arr[1, i] * (1 - p.varValue), 2) == V:
			temp = np.hstack((temp, arr[:, i]))
			rest.append(i)
	temp = np.delete(temp, 0, axis=1)
	result = TByT(temp)
	return result, rest


def indifference(arr):
	a = np.ones(arr.shape[0])
	b = np.ones(arr.shape[1])
	r = np.zeros(arr.shape[0])
	d = np.ones(1)
	r = np.hstack((r, d))
	a = -1 * a
	left = np.column_stack((arr, a))
	c = np.zeros(1)
	b = np.hstack((b, c))
	left = np.row_stack((left, b))
	if left.shape[0] != left.shape[1]:
		return False
	result1 = solve(left, r)
	for each in result1[0:-1]:
		if each <= 0:
			return False
	else:
		arr = arr.transpose()
		a = np.ones(arr.shape[0])
		b = np.ones(arr.shape[1])
		r = np.zeros(arr.shape[0])
		d = np.ones(1)
		r = np.hstack((r, d))
		a = -1 * a
		left = np.column_stack((arr, a))
		c = np.zeros(1)
		b = np.hstack((b, c))
		left = np.row_stack((left, b))
		result2 = solve(left, r)
		for each in result2[0:-1]:
			if each <= 0:
				return False
	return [result1[0:-1], result2[0:-1], result1[-1]]


def isInvariant(arr):
	temp = arr[::-1]
	rows = arr.shape[0]
	for i in range(int(rows / 2)):
		for j in range(arr.shape[1]):
			if arr[i, j] != arr[rows - 1 - i, arr.shape[1] - 1 - j]:
				return False
	return True


def NByN(arr): # n by n matrix
	one = np.ones(arr.shape[0])
	inverse = np.linalg.inv(arr)
	p = one * inverse / (one * inverse * one.reshape((arr.shape[0], 1)))
	for i in range(p.shape[1]):
		if p[0, i] < 0:
			return False
	q = inverse * one.reshape((arr.shape[0], 1)) / (one * inverse * one.reshape((arr.shape[0], 1)))
	for i in range(q.shape[1]):
		if q[0, i] < 0:
			return False
	q = q.reshape(arr.shape[0])
	V = 1 / (one * inverse * one.reshape((arr.shape[0], 1)))
	return [p, q, V]


def mgc(arr):
	x = []
	y = []
	p = []
	q = []
	arr = np.array(arr)
	minValue = arr.min()
	if minValue < 0:
		arr = arr - minValue
	for i in range(arr.shape[0]):  # label x
		x.append('x' + str(i + 1))
		p.append(0)
	for i in range(arr.shape[1]):  # label y
		y.append('y' + str(i + 1))
		q.append(0)
	a = np.ones(arr.shape[0])
	b = -1 * np.ones(arr.shape[1])
	d = np.zeros(1)
	bottom = np.hstack((b, d))
	left = np.column_stack((arr, a))
	c = np.zeros(1)
	b = np.hstack((b, c))
	left = np.row_stack((left, b))  # new version
	# print(left)
	p_pivot = 0
	q_pivot = 0
	while left[left.shape[0] - 1, :].min() < 0:
		tr = 1
		temp = left[left.shape[0] - 1, :].min()
		for i in range(left.shape[1] - 1):
			if left[left.shape[0] - 1, i] == temp:
				q_pivot = i
				break  # choose leftmost min negative value from border.
			else:
				continue
		for i in range(left.shape[0] - 1):
			if left[i, q_pivot] <= 0:
				continue
			elif tr > left[i, left.shape[1] - 1] / left[i, q_pivot]:
				tr = left[i, left.shape[1] - 1] / left[i, q_pivot]
				p_pivot = i
			else:
				continue
		for i in range(left.shape[0]):
			if i != p_pivot:
				for j in range(left.shape[1]):
					if j != q_pivot:
						left[i, j] = left[i, j] - left[p_pivot, j] * left[i, q_pivot] / left[p_pivot, q_pivot]
					else:
						continue
			else:
				continue
		for j in range(left.shape[1]):
			if j != q_pivot:
				left[p_pivot, j] = left[p_pivot, j] / left[p_pivot, q_pivot]
			else:
				continue
		for i in range(left.shape[0]):
			if i != p_pivot:
				left[i, q_pivot] = left[i, q_pivot] / (-left[p_pivot, q_pivot])
			else:
				continue
		left[p_pivot, q_pivot] = 1 / left[p_pivot, q_pivot]
		tmp = x[p_pivot]
		x[p_pivot] = y[q_pivot]
		y[q_pivot] = tmp
		print(left)
		print(p_pivot, q_pivot)
	V = round(1 / left[left.shape[0] - 1, left.shape[1] - 1] + minValue, 2)

	for i in range(len(x)):
		if x[i][0] == 'y':
			q[int(x[i][1]) - 1] = left[i, left.shape[1] - 1]
		else:
			continue
	for i in range(len(y)):
		if y[i][0] == 'x':
			p[int(y[i][1]) - 1] = left[left.shape[0] - 1, i]
		else:
			continue
	# print(y,p)
	p = normalize(p)
	q = normalize(q)
	return [p, q, V]


def normalize(list):
	sum = 0
	for each in list:
		sum = sum + each
	for i in range(len(list)):
		list[i] = round(list[i] / sum, 2)
	return list

'''
a1 = mat([[4,1,-3],[3,2,5],[0,1,6]]); #saddle point
a1 = mat([[2,3,1,5],[4,1,6,0]])      #two by n
a1 = a1.transpose()                  #m by two
a1 = mat([[0,1,-2],[1,-2,3],[-2,3,-4]])   # indifference
a1 = mat([[4,2,1,0],[1,3,0,-1],[-2,2,2,-2],[-1,0,3,1],[0,1,2,4]])  #invariant
a1 = mat([[1,2,-1],[2,-1,4],[-1,4,-3]])   #n by n
a1 = mat([[2,-1,6],[0,1,-1],[-2,2,1]])   #most general case
a1 = mat([[1,2,3,4,5],[3,4,5,6,7]])
a1 = mat([[1,-2,3,4],[0,1,-2,3],[0,0,1,-2],[0,0,0,1]])
a1 = mat([[0,2,1],[-2,0,-4],[-1,4,0]])
a1 = mat([[10,0,7,0],[0,6,4,0],[0,0,3,3]])
'''


f = open('testResult.txt','w')
time= 0
while (time < 100):
	time = time + 1

	a1 = np.random.randint(-1000,1000,size=[random.randint(1,100),random.randint(1,100)])  
	a1 = mat(a1)
	f.write(str(a1) + '\n')


	if (saddlePoint(a1) != False):
		result = saddlePoint(a1)
		f.write("There is a saddle point in the matrix: "+ '\n')
		f.write("A(" + str(result[1]+1) +',' + str(result[2]+1) +") = the value of game = V = " + str(result[0])+ '\n')
		f.write("And its strategy is pure strategy, p(x" + str(result[1]+1) +") = 1, and q(y" + str(result[2]+1) +") = 1." + '\n')
	elif a1.shape == (2,2):
		result = TByT(a1)
		f.write("Two by two: "+ '\n')
		f.write("The value of the game is " + str(result[0])+ '\n')
		f.write("The mixed strategy for player 1 is p = (" + str(result[1]) + ',' + str(1-result[1]) + ")."+ '\n')
		f.write("The mixed strategy for player 2 is q = (" + str(result[2]) + ',' + str(1-result[2]) + ")."+ '\n')
	elif a1.shape[0] == 2:
		result = TByN(a1)
		q = []
		for i in range(a1.shape[1]):
			q.append(0)
		q[result[1][0]] = result[0][2]
		q[result[1][1]] = round(1-result[0][2],2)
		f.write("Two dimensions: "+ '\n')
		f.write("The value of the game is " + str(result[0][0])+ '\n')
		f.write("The mixed strategy for player 1 is p = [" + str(result[0][1]) + ',' + str(round(1-result[0][1],2)) + "]."+ '\n')
		f.write("The mixed strategy for player 2 is q = " + str(q) + "."+ '\n')
	elif a1.shape[1] == 2:
		a1 = a1.transpose()
		result = TByN(a1)
		q = []
		for i in range(a1.shape[1]):
			q.append(0)
		q[result[1][0]] = result[0][2]
		q[result[1][1]] = round(1-result[0][2],2)
		f.write("The value of the game is " + str(result[0][0])+ '\n')
		f.write("The mixed strategy for player 1 is p = " + str(q) + "."+ '\n')
		f.write("The mixed strategy for player 2 is q = [" + str(result[0][1]) + ',' + str(round(1-result[0][1],2)) + "]."+ '\n')
	elif indifference(a1):
		result = indifference(a1)
		f.write("Indifference:"+ '\n')
		f.write("The value of the game is " + str(result[-1])+ '\n')
		f.write("The mixed strategy for player 1 is p = " + str(result[0]) + "."+ '\n')
		f.write("The mixed strategy for player 2 is q = " + str(result[1]) + "."+ '\n')
	elif isInvariant(a1):
		result = mgc(a1)
		f.write("Invariant:"+ '\n')
		f.write("The value of the game is " + str(result[-1])+ '\n')
		f.write("The mixed strategy for player 1 is p = " + str(result[0]) + "."+ '\n')
		f.write("The mixed strategy for player 2 is q = " + str(result[1]) + "."+ '\n')
	elif a1.shape[0] == a1.shape[1] and np.linalg.det(a1) != 0 and NByN(a1):
		result = NByN(a1)
		f.write("N by N:"+ '\n')
		f.write("The value of the game is " + str(result[-1])+ '\n')
		f.write("The mixed strategy for player 1 is p = " + str(result[0]) + "."+ '\n')
		f.write("The mixed strategy for player 2 is q = " + str(result[1]) + "."+ '\n')
	else:
		result = mgc(a1)
		f.write("The value of the game is " + str(result[-1])+ '\n')
		f.write("The mixed strategy for player 1 is p = " + str(result[0]) + "."+ '\n')
		f.write("The mixed strategy for player 2 is q = " + str(result[1]) + "."+ '\n')

