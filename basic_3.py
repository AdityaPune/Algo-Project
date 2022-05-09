import sys
import time
import os,psutil


class algo():
	def generateStrings(self,filename):
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

	

	def matrixCompute(self,s1,s2,delta,alpha):
		def helperCharToInt(val):
			if val=="A":
				return 0
			elif val=="C":
				return 1
			elif val=="G":
				return 2
			else:
				return 3
		x=len(s1)
		y=len(s2)
		A=[[0 for _ in range(y+1)] for _ in range(x+1)]
		for i in range(1,x+1):
			A[i][0]=i*delta
		for j in range(1,y+1):
			A[0][j]=j*delta

		for i in range(1,x+1):
			for j in range(1,y+1):
				xi=helperCharToInt(s1[i-1])
				yj=helperCharToInt(s2[j-1])
				alphaval=alpha[xi][yj]
				A[i][j]=min(alphaval+A[i-1][j-1],delta+A[i-1][j],delta+A[i][j-1])
		return A,x,y

	def sequenceGeneration(self,Array,x,y,delta):
		i=x
		j=y
		new_s1=""
		new_s2=""
		while i>0 and j>0:
			if Array[i][j]==delta+Array[i][j-1]:
				j-=1
				new_s1="_"+new_s1
				new_s2=s2[j]+new_s2
				
			elif Array[i][j]==delta+Array[i-1][j]:
				j-=1
				new_s1="_"+new_s1
				new_s2=s2[j]+new_s2
				
			else:
				i-=1
				j-=1
				new_s1=s1[i]+new_s1
				new_s2=s2[j]+new_s2
		while i>0:
			i-=1
			new_s1=s1[i]+new_s1
			new_s2="_"+new_s2
		while j>0:
			j-=1
			new_s1="_"+new_s1
			new_s2=s2[j]+new_s2

		writeString1=new_s1[:50]+" "+new_s1[-50:]
		writeString2=new_s2[:50]+" "+new_s2[-50:]
		outputFile.write(str(Array[x][y]))
		outputFile.write("\n"+writeString1)
		outputFile.write("\n"+writeString2)
		
def process_memory():
	process = psutil.Process()
	memory_info = process.memory_info()
	memory_consumed = int(memory_info.rss/1024)
	return memory_consumed

if __name__=="__main__":	
	# Get file contents
	algo = algo()
	
	
	# file_path = os.path.join(parent_directory, 'SampleTestCases/input3.txt')
	file_path = sys.argv[-2]
	s1, s2 = algo.generateStrings(file_path)
	start_time = time.time()
	delta=30
	alpha=[[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]

	# Generating strings
	outputFile=open(sys.argv[-1],'w')

	# Matrix initialization
	Array,x,y=algo.matrixCompute(s1,s2,delta,alpha)


	# Minimum Value
	# print("\nAlignment Value = ",A[m][n])

	#Generating new sequences according to the path taken

	algo.sequenceGeneration(Array,x,y,delta)
	# outputFile.write("\n"+str(Array[x][y]))


	# print("\nTime:")
	outputFile.write("\n"+str(1000*(time.time() - start_time)))  # in seconds

	# print("\nMemory:")
	outputFile.write("\n"+str(process_memory()))  # in kilobytes

	outputFile.close()
