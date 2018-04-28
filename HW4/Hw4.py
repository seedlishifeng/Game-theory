

def value(m,n):
	if n == 0:
		return 1
	elif m == 0:
		return 1/(1+n)
	else: 
		return (1+n*(1-value(n-1,m))*value(n,m-1))/(1+(n+1)*value(n,m-1))

def result():
	for i in range(6):
		for j in range(6):
			print("m = " + str(i+1) +", n = " + str(j+1) + ", the value is " + str(round(value(i+1,j+1),4)))
	


if __name__ == '__main__':
    result()
