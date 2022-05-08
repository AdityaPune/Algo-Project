
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
    
    def helperCharToInt(self,c):
    	if c=="A": return 0
    	elif c=="C": return 1
    	elif c=="G": return 2
    	else:return 3
    
    def computeMat(self,A,s1,s2,alpha):
    	for i in range(1,len(s1)+1):
    		for j in range(1,len(s2)+1):
    			xi=self.helperCharToInt(s1[i-1])
    			yj=self.helperCharToInt(s2[j-1])
    			# print(s1[i-1],s2[j-1])
    			A[i][j]=min(alpha[xi][yj]+A[i-1][j-1],delta+A[i-1][j],delta+A[i][j-1])
    	return A
    
    def computeMatSpaceEfficientPrefix(self,s1,s2,alpha,delta):
      m, n =len(s1),len(s2)
      A=[[0 for i in range(n+1)] for j in range(2)]
      for i in range(n+1):
        A[0][i]=i*delta
      for i in range(1,m+1):
        A[1][0] = A[0][0] + delta
        for j in range(1,n+1):
          xi=self.helperCharToInt(s1[i-1])
          yj=self.helperCharToInt(s2[j-1])
          alphaval=alpha[xi][yj]
          # print(s1[i-1],s2[j-1])
          A[1][j]=min(alphaval+A[0][j-1],delta+A[1][j-1],delta+A[0][j])
        for i in range(0, n+1):
          A[0][i] = A[1][i]
      return A[1]
    
    def computeMatSpaceEfficientSuffix(self,s1,s2,alpha,delta):
      m, n=len(s1), len(s2)
      A=[[0 for i in range(n+1)] for j in range(2)]
      for i in range(n+1):
        A[0][i]=i*delta
      for i in range(1,m+1):
        A[1][0] = A[0][0] + delta
        for j in range(1,n+1):
          xi=self.helperCharToInt(s1[m-i])
          yj=self.helperCharToInt(s2[n-j])
          # print(s1[i],s2[j])
          A[1][j]=min(alpha[xi][yj]+A[0][j-1],delta+A[1][j-1],delta+A[0][j])
        for i in range(0, n+1):
          A[0][i] = A[1][i]
      return A[1]
    
    def spaceEfficientAlignment(self,s1,s2,alpha,delta):
      m=len(s1)
      n=len(s2)
      if m < 2 or n < 2:
        return self.normalAlignment(s1,s2,alpha,delta)
      else:
    	  pref = self.computeMatSpaceEfficientPrefix(s1[:m//2],s2,alpha,delta)
    	  suff = self.computeMatSpaceEfficientSuffix(s1[m//2:],s2,alpha,delta)
    # 	  print('pref suff', pref, suff)
    	  seperation = [pref[j] + suff[n-j] for j in range(n+1)]
    	  cut = seperation.index(min(seperation))
    	  pref = []
    	  suff = []
    	  seperation = []
    
    	  left = self.spaceEfficientAlignment(s1[:m//2],s2[:cut],alpha,delta)
    	  right = self.spaceEfficientAlignment(s1[m//2:],s2[cut:],alpha,delta)
    	  return [left[i] + right[i] for i in range(3)]
    
    
    def normalAlignment(self,s1,s2,alpha,delta):
      A,m,n=self.matInitialization(s1,s2,delta)
      A=self.computeMat(A,s1,s2,alpha)
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
    
    def matInitialization(self,s1,s2,delta):
    	m=len(s1)
    	n=len(s2)
    	A=[[0 for i in range(n+1)] for j in range(m+1)]
    	for i in range(1,m+1):
    		A[i][0]=i*delta
    	for j in range(1,n+1):
    		A[0][j]=j*delta
    	return A,m,n


if __name__=="__main__":

	algo = algo()
	# Get file contents # Generating strings
	current_directory = os.path.dirname(__file__)
	parent_directory = os.path.split(current_directory)[0] # Repeat as needed
	file_path = os.path.join(parent_directory, 'SampleTestCases/input1.txt')
	s1, s2 = algo.generateStrings(file_path)
	process = psutil.Process(os.getpid())
	start_time = time.time()
	delta=30
	alpha=[[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]
	ans = algo.spaceEfficientAlignment(s1,s2,alpha,delta)
	
	# First 50 elements of A & B
	print('check', ans)
# 	print("\n"+ans[0][:50]+" "+ans[0][:-50])
	outputFile=open('outputeff.txt','w')
	# Last 50 elements of A & B
# 	print("\n"+ans[1][:50]+" "+ans[1][-50:])
	outputFile.write(str(ans[2])+
                    "\n"+ans[0][:50]+" "+ans[0][-50:]+
					"\n"+ans[1][:50]+" "+ans[1][-50:]+
					"\n"+str(time.time() - start_time)+
					"\n"+str(process.memory_info().rss/1024))
 
	outputFile.close()