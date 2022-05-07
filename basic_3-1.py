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

def helperCharToInt(val):
	if val=="A":
		return 0
	elif val=="C":
		return 1
	elif val=="G":
		return 2
	else:
		return 3

def matCompute(s1,s2,delta,alpha):
	m=len(s1)
	n=len(s2)
	A=[[0 for _ in range(n+1)] for _ in range(m+1)]
	for i in range(1,m+1):
		A[i][0]=i*delta
	for j in range(1,n+1):
		A[0][j]=j*delta

	for i in range(1,m+1):
		for j in range(1,n+1):
			xi=helperCharToInt(s1[i-1])
			yj=helperCharToInt(s2[j-1])
			alphaval=alpha[xi][yj]
			A[i][j]=min(alphaval+A[i-1][j-1],delta+A[i-1][j],delta+A[i][j-1])
	return A,m,n

def sequenceGeneration(A,m,n,delta):
	i=m
	j=n
	final_s1=""
	final_s2=""
	while i>0 and j>0:
		if A[i][j]==delta+A[i-1][j]:
			i-=1
			final_s1=s1[i]+final_s1
			final_s2="_"+final_s2
			# print(s1[i],"-")
		elif A[i][j]==delta+A[i][j-1]:
			j-=1
			final_s1="_"+final_s1
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
		final_s2="_"+final_s2
		# print(s1[i],"-")
	while j>0:
		j-=1
		final_s1="_"+final_s1
		final_s2=s2[j]+final_s2
		# print("-",s2[j])

	# print("\nActual Alignment: ")
	# print(final_s1)
	# print(final_s2)

	# print("\nFirst 50 elements and the last 50 elements:")
	# print(final_s1[:50]," ",final_s2[:50])
	# print(final_s1[-50:]," ", final_s2[-50:])
	temp1=final_s1[:50]+" "+final_s1[-50:]
	temp2=final_s2[:50]+" "+final_s2[-50:]
	outputFile.write(temp1)
	outputFile.write("\n"+temp2)

if __name__=="__main__":	
	# Get file contents
	filename=sys.argv[-1]
	outputFile=open('output.txt','w')

	process = psutil.Process(os.getpid())
	start_time = time.time()
	# Generating strings
	s1,s2=generateStrings(filename)

	# Values of alpha, delta
	delta=30
	alpha=[[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]

	# Matrix initialization
	A,m,n=matCompute(s1,s2,delta,alpha)

	# Displaying some stats
	# displayMat(A)
	# Minimum Value
	# print("\nAlignment Value = ",A[m][n])

	#Generating new sequences according to the path taken
	sequenceGeneration(A,m,n,delta)

	outputFile.write("\n"+str(A[m][n]))

	# print("\nTime:")
	outputFile.write("\n"+str(time.time() - start_time))  # in seconds

	# print("\nMemory:")
	outputFile.write("\n"+str(process.memory_info().rss/1024))  # in kilobytes

	outputFile.close()
