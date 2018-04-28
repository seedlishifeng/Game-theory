from numpy import *
import numpy as np
import pulp
from scipy.linalg import solve


def saddlePoint(arr):
	minOfRow = [] 
	for each in arr:
		minOfRow.append(each[0,:].min())
	for i in range(arr.shape[1]):
		if arr[:,i].max() in minOfRow:
			return (arr[:,i].max(),minOfRow.index(arr[:,i].max()), i)
	return False

def twoBytwo(arr):
	a = arr[0,0]
	b = arr[0,1]
	d = arr[1,0]
	c = arr[1,1]
	p = (c-d)/(a-b+c-d)
	q = (c-b)/(a-b+c-d)
	V = (c*a -b*d)/(a-b+c-d)
	return [round(V,2),round(p,2),round(q,2)]

def twoByN(arr):
	temp = mat([[0],[0]])
	rest = []
	model = pulp.LpProblem("twoByN", pulp.LpMaximize)
	p = pulp.LpVariable('p', lowBound=0, upBound=1)
	V = pulp.LpVariable('V')
	model += V, "Value"
	for i in range(arr.shape[1]):
		model += arr[0,i]*p + arr[1,i]*(1-p)>=V
	model.solve()
	V = round(pulp.value(model.objective),2)
	for i in range(arr.shape[1]):   #check which column is useful
		if round(arr[0,i]*p.varValue + arr[1,i]*(1-p.varValue),2) == V:
			temp = np.hstack((temp,arr[:,i]))
			rest.append(i)
	temp = np.delete(temp,0,axis=1)
	result = twoBytwo(temp)
	return result,rest


def indifference(arr):
	a = np.ones(arr.shape[0])
	b = np.ones(arr.shape[1])
	r = np.zeros(arr.shape[0])
	d = np.ones(1)
	r = np.hstack((r,d))
	a = -1*a
	left = np.column_stack((arr,a))
	c = np.zeros(1)
	b = np.hstack((b,c))
	left = np.row_stack((left,b))
	if left.shape[0] != left.shape[1]:
		return False
	result1 = solve(left,r)
	for each  in result1[0:-1]:
		if each <= 0:
			return False
	else:
		arr = arr.transpose()
		a = np.ones(arr.shape[0])
		b = np.ones(arr.shape[1])
		r = np.zeros(arr.shape[0])
		d = np.ones(1)
		r = np.hstack((r,d))
		a = -1*a
		left = np.column_stack((arr,a))
		c = np.zeros(1)
		b = np.hstack((b,c))
		left = np.row_stack((left,b))
		result2 = solve(left,r)
		for each  in result2[0:-1]:
			if each <= 0:
				return False
	return [result1[0:-1],result2[0:-1],result1[-1]]

def isInvariant(arr):
	temp = arr[::-1]
	rows = arr.shape[0]
	for i in range(int(rows/2)):
		for j in range(arr.shape[1]):
			if arr[i,j] != arr[rows-1-i,arr.shape[1]-1-j]:
				return False
	return True



def nByN(arr):
	one = np.ones(arr.shape[0])
	inverse = np.linalg.inv(arr)
	p = one*inverse / (one*inverse*one.reshape((arr.shape[0],1)))
	for i in range(p.shape[1]):
		if p[0,i] < 0:
			return False
	q = inverse*one.reshape((arr.shape[0],1)) / (one*inverse*one.reshape((arr.shape[0],1)))
	for i in range(q.shape[1]):
		if q[0,i] < 0:
			return False
	q = q.reshape(arr.shape[0])
	V = 1/(one*inverse*one.reshape((arr.shape[0],1)))
	return [p,q,V]

def mgc(arr):
	x = []
	y = []
	p = []
	q = []
	arr = np.array(arr)
	minValue = arr.min()
	if minValue < 0:
		arr = arr - minValue
	for i in range(arr.shape[0]):  #label x
		x.append('x' + str(i+1))
		p.append(0)
	for i in range(arr.shape[1]):  # label y
		y.append('y' + str(i+1))
		q.append(0)
	a = np.ones(arr.shape[0])
	b = -1 * np.ones(arr.shape[1])
	d = np.zeros(1)
	bottom = np.hstack((b,d))
	left = np.column_stack((arr,a))
	c = np.zeros(1)
	b = np.hstack((b,c))
	left = np.row_stack((left,b))   # new version
	#print(left)
	p_pivot = 0
	q_pivot = 0
	while left[left.shape[0]-1,:].min() < 0:
		tr = 1
		temp = left[left.shape[0]-1,:].min()
		for i in range(left.shape[1] - 1):
			if left[left.shape[0]-1,i] == temp:
				q_pivot = i
				break               #choose leftmost min negative value from border.
			else:
				continue
		for i in range(left.shape[0]-1):
			if left[i,q_pivot] <= 0:
				continue
			elif tr > left[i,left.shape[1]-1]/left[i,q_pivot]:
				tr = left[i,left.shape[1]-1]/left[i,q_pivot]
				p_pivot = i
			else:
				continue
		for i in range(left.shape[0]):  
			if i != p_pivot:
				for j in range(left.shape[1]):
					if j != q_pivot:
						left[i,j] = left[i,j] - left[p_pivot,j]*left[i,q_pivot]/left[p_pivot,q_pivot]
					else:
						continue
			else:
				continue
		for j in range(left.shape[1]):
			if j != q_pivot:
				left[p_pivot,j] = left[p_pivot,j]/left[p_pivot,q_pivot]
			else:
				continue
		for i in range(left.shape[0]):
			if i != p_pivot:
				left[i,q_pivot] = left[i,q_pivot]/(-left[p_pivot,q_pivot])
			else:
				continue
		left[p_pivot,q_pivot] = 1/left[p_pivot,q_pivot]
		tmp = x[p_pivot]
		x[p_pivot] = y[q_pivot]
		y[q_pivot] = tmp
		print(left)
		print(p_pivot,q_pivot)
	V = round(1/left[left.shape[0]-1,left.shape[1]-1] + minValue,2)
	
	for i in range(len(x)):
		if x[i][0] == 'y':
			q[int(x[i][1])-1] = left[i,left.shape[1]-1]
		else:
			continue
	for i in range(len(y)):
		if y[i][0] == 'x':
			p[int(y[i][1])-1] = left[left.shape[0]-1,i]
		else:
			continue
	#print(y,p)
	p = normalize(p)
	q = normalize(q)
	return [p,q,V]

def normalize(list):
	sum = 0
	for each in list:
		sum = sum + each
	for i in range(len(list)):
		list[i] = round(list[i]/sum,2)
	return list
	 







