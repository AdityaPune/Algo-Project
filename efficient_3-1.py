
import sys
import time
import os,psutil

def generateStrings(filename):
	with open(filename) as f:
		s1=""
		s2=""
		curr=""
		for line in f:
			temp=line.rstrip()
			if not temp.isdecimal():
				s1=curr
				curr=temp
			else:
				index=int(temp)+1
				curr=curr[:index]+curr+curr[index:]
	s2=curr
	return s1,s2

def displayMat(A):
	for i in range(len(A)):
		for j in range(len(A[0])):
			print(A[i][j]," ",end="")
		print()

def helperCharToInt(c):
	if c=="A":
		return 0
	elif c=="C":
		return 1
	elif c=="G":
		return 2
	else:
		return 3

def computeMat(A,s1,s2,alpha):
	for i in range(1,len(s1)+1):
		for j in range(1,len(s2)+1):
			xi=helperCharToInt(s1[i-1])
			yj=helperCharToInt(s2[j-1])
			alphaval=alpha[xi][yj]
			# print(s1[i-1],s2[j-1])
			A[i][j]=min(alphaval+A[i-1][j-1],delta+A[i-1][j],delta+A[i][j-1])
	return A

def computeMatSpaceEfficientPrefix(s1,s2,alpha,delta):
  m=len(s1)
  n=len(s2)
  A=[[0 for i in range(n+1)] for j in range(2)]
  for i in range(n+1):
    A[0][i]=i*delta
  for i in range(1,m+1):
    A[1][0] = A[0][0] + delta
    for j in range(1,n+1):
      xi=intFromChar(s1[i-1])
      yj=intFromChar(s2[j-1])
      alphaval=alpha[xi][yj]
      # print(s1[i-1],s2[j-1])
      A[1][j]=min(alphaval+A[0][j-1],delta+A[1][j-1],delta+A[0][j])
    for i in range(0, n+1):
      A[0][i] = A[1][i]
  return A[1]

def computeMatSpaceEfficientSuffix(s1,s2,alpha,delta):
  m=len(s1)
  n=len(s2)
  A=[[0 for i in range(n+1)] for j in range(2)]
  for i in range(n+1):
    A[0][i]=i*delta
  for i in range(1,m+1):
    A[1][0] = A[0][0] + delta
    for j in range(1,n+1):
      xi=intFromChar(s1[m-i])
      yj=intFromChar(s2[n-j])
      alphaval=alpha[xi][yj]
      # print(s1[i],s2[j])
      A[1][j]=min(alphaval+A[0][j-1],delta+A[1][j-1],delta+A[0][j])
    for i in range(0, n+1):
      A[0][i] = A[1][i]
  return A[1]

def spaceEfficientAlignment(s1,s2,alpha,delta):
  m=len(s1)
  n=len(s2)

  if m < 2 or n < 2:
    return normalAlignment(s1,s2,alpha,delta)
  else:
	  pref = computeMatSpaceEfficientPrefix(s1[:m//2],s2,alpha,delta)
	  suff = computeMatSpaceEfficientSuffix(s1[m//2:],s2,alpha,delta)

	  seperation = [pref[j] + suff[n-j] for j in range(n+1)]
	  cut = seperation.index(min(seperation))
	  # print(seperation,cut)
	  pref = []
	  suff = []
	  seperation = []

	  left = spaceEfficientAlignment(s1[:m//2],s2[:cut],alpha,delta)
	  right = spaceEfficientAlignment(s1[m//2:],s2[cut:],alpha,delta)
	  return [left[i] + right[i] for i in range(3)]


def normalAlignment(s1,s2,alpha,delta):
  A,m,n=matInitialization(s1,s2,delta)
  A=computeMat(A,s1,s2,alpha)
  # print("\nAlignment Value = ",A[m][n])
  # final_s1, final_s2 = backTracking(A,m,n,delta)
  # print("back ",final_s1,final_s2)
  i = m
  j = n
  final_s1=""
  final_s2=""
  while i>0 and j>0:
  	if A[i][j] == delta + A[i-1][j]:
  		i -= 1
  		final_s1 = s1[i] + final_s1
  		final_s2 = '_' + final_s2
  	elif A[i][j] == delta + A[i][j-1]:
  		j-=1
  		final_s1 = '_' + final_s1
  		final_s2 = s2[j] + final_s2
  	else:
  		i-=1
  		j-=1
  		final_s1 = s1[i] + final_s1
  		final_s2 = s2[j] + final_s2
  while i>0:
  	i-=1
  	final_s1 = s1[i] + final_s1
  	final_s2 = '_' + final_s2
  while j>0:
  	j-=1
  	final_s1 = '_' + final_s1
  	final_s2 = s2[j] + final_s2
  # print(final_s1,final_s2)
  return [final_s1,final_s2,A[m][n]]

def matInitialization(s1,s2,delta):
	m=len(s1)
	n=len(s2)
	A=[[0 for i in range(n+1)] for j in range(m+1)]
	for i in range(1,m+1):
		A[i][0]=i*delta
	for j in range(1,n+1):
		A[0][j]=j*delta
	return A,m,n

def backTracking(A,m,n,delta):
	i=m
	j=n
	final_s1=""
	final_s2=""
	while i>0 and j>0:
		if A[i][j]==delta+A[i-1][j]:
			i-=1
			final_s1=s1[i]+final_s1
			final_s2="-"+final_s2
			# print(s1[i],"-")
		elif A[i][j]==delta+A[i][j-1]:
			j-=1
			final_s1="-"+final_s1
			final_s2=s2[j]+final_s2
			# print("-",s2[j])
		else:
			i-=1
			j-=1
			final_s1=s1[i]+final_s1
			final_s2=s2[j]+final_s2
			# print(s1[i],s2[j])
	while i>0:
		i-=1
		final_s1=s1[i]+final_s1
		final_s2="-"+final_s2
		# print(s1[i],"-")
	while j>0:
		j-=1
		final_s1="-"+final_s1
		final_s2=s2[j]+final_s2
	return final_s1,final_s2

finalPath=[]
if __name__=="__main__":

	
	# Get file contents
	filename=sys.argv[-1]
	outputFile=open('output-eff1.txt','w')

	process = psutil.Process(os.getpid())
	start_time = time.time()

	# Generating strings
	s1,s2=generateStrings(filename)

	# Values of alpha, delta
	delta=30
	alpha=[[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]

	# normalAlignment(s1,s2,alpha,delta)

	# Matrix initialization
	# A,m,n=matInitialization(s1,s2,delta)
	# Initial values in A	
	# displayMat(A)

	# Computing minimum matching value
	# A=computeMat(A,s1,s2,alpha)
	# displayMat(A)
	# Minimum Value
	# print("\nAlignment Value = ",A[m][n])

	#Back tracking
	# backTracking(A,m,n,delta)
	# print("##################################")

	ans = spaceEfficientAlignment(s1,s2,alpha,delta)
	end_time = str(time.time() - start_time)
	memory = str(process.memory_info().rss/1024)
	
	
	# First 50 elements of A & B
	# print("\n"+ans[0][:50]+" "+ans[0][:-50])
	outputFile.write(ans[0][:50]+" "+ans[0][-50:])
 
	# Last 50 elements of A & B
	# print("\n"+ans[1][:50]+" "+ans[1][-50:])
	outputFile.write("\n"+ans[1][:50]+" "+ans[1][-50:])
 
	# print("\nAlignment Value:"+str(ans[2]))
	outputFile.write("\n"+str(ans[2]))  # in seconds

	# print("\nTime:"+end_time)
	outputFile.write("\n"+end_time)  # in seconds

	# print("\nMemory:"+memory)
	outputFile.write("\n"+memory)  # in kilobytes

	outputFile.close()