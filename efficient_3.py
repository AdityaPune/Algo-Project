import sys
import time
import os,psutil

class algo():
    
    def initializeMatrix(self,string_1,string_2,delta):
    	k=len(string_1)
    	l=len(string_2)
    	mat=[[0 for i in range(l+1)] for j in range(k+1)]
    	for i in range(1,k+1):
    		mat[i][0]=i*delta
    	for j in range(1,l+1):
    		mat[0][j]=j*delta
    	return mat,k,l
    
    def calAlignmentNormal(self,string_1,string_2,alpha,delta):
      mat,k,l=self.initializeMatrix(string_1,string_2,delta)
      mat=self.calMatrix(mat,string_1,string_2,alpha)
      i = k
      j = l
      final_string_1=""
      final_string_2=""
      while i>0 and j>0:
      	if mat[i][j] == delta + mat[i][j-1]:
      		j-=1
      		final_string_1 = '_' + final_string_1
      		final_string_2 = string_2[j] + final_string_2
      	elif mat[i][j] == delta + mat[i-1][j]:
              i -= 1
              final_string_1 = string_1[i] + final_string_1
              final_string_2 = '_' + final_string_2
      	else:
      		i-=1
      		j-=1
      		final_string_1 = string_1[i] + final_string_1
      		final_string_2 = string_2[j] + final_string_2
      while i>0:
      	i-=1
      	final_string_1 = string_1[i] + final_string_1
      	final_string_2 = '_' + final_string_2
      while j>0:
      	j-=1
      	final_string_1 = '_' + final_string_1
      	final_string_2 = string_2[j] + final_string_2
      return [final_string_1,final_string_2,mat[k][l]]
    
    def calAlignment(self,string_1,string_2,alpha,delta):
      k=len(string_1)
      l=len(string_2)
      if k < 2 or l < 2:
        return self.calAlignmentNormal(string_1,string_2,alpha,delta)
      else:
    	  end = self.calMatrixStart(string_1[:k//2],string_2,alpha,delta)
    	  start = self.calMatrixEnd(string_1[k//2:],string_2,alpha,delta)
    	  diverge = [end[j] + start[l-j] for j in range(l+1)]
    	  divide = diverge.index(min(diverge))
    	  end = []
    	  start = []
    	  diverge = []
    
    	  align_left = self.calAlignment(string_1[:k//2],string_2[:divide],alpha,delta)
    	  align_right = self.calAlignment(string_1[k//2:],string_2[divide:],alpha,delta)
    	  return [align_left[i] + align_right[i] for i in range(3)]
    
    def calMatrixEnd(self,string_1,string_2,alpha,delta):
      k, l=len(string_1), len(string_2)
      mat=[[0 for i in range(l+1)] for j in range(2)]
      for i in range(l+1):
        mat[0][i]=i*delta
      for i in range(1,k+1):
        mat[1][0] = mat[0][0] + delta
        for j in range(1,l+1):
          e=self.mapChar(string_1[k-i])
          f=self.mapChar(string_2[l-j])
          mat[1][j]=min(alpha[e][f]+mat[0][j-1],delta+mat[1][j-1],delta+mat[0][j])
        for i in range(0, l+1):
          mat[0][i] = mat[1][i]
      return mat[1]
  
    def calMatrix(self,mat,string_1,string_2,alpha):
    	for i in range(1,len(string_1)+1):
    		for j in range(1,len(string_2)+1):
    			e=self.mapChar(string_1[i-1])
    			f=self.mapChar(string_2[j-1])
    			mat[i][j]=min(alpha[e][f]+mat[i-1][j-1],delta+mat[i-1][j],delta+mat[i][j-1])
    	return mat
    
    def calMatrixStart(self,string_1,string_2,alpha,delta):
      k, l =len(string_1),len(string_2)
      mat=[[0 for i in range(l+1)] for j in range(2)]
      for i in range(l+1):
        mat[0][i]=i*delta
      for i in range(1,k+1):
        mat[1][0] = mat[0][0] + delta
        for j in range(1,l+1):
          e=self.mapChar(string_1[i-1])
          f=self.mapChar(string_2[j-1])
          get_alpha=alpha[e][f]
          mat[1][j]=min(get_alpha+mat[0][j-1],delta+mat[1][j-1],delta+mat[0][j])
        for i in range(0, l+1):
          mat[0][i] = mat[1][i]
      return mat[1]
    
    def mapChar(self,char):
    	if char=="A": return 0
    	elif char=="C": return 1
    	elif char=="G": return 2
    	else:return 3

    def stringBuilt(self,filename):
    	with open(filename) as f:
    		string_1=""
    		string_2=""
    		curr=""
    		for line in f:
    			temp=line.rstrip()
    			if not temp.isdecimal():
    				string_1=curr
    				curr=temp
    			else:
    				index=int(temp)+1
    				curr=curr[:index]+curr+curr[index:]
    	string_2=curr
    	return string_1,string_2
    
    def process_memory(self):
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_consumed = int(memory_info.rss/1024)
        return memory_consumed

if __name__=="__main__":
	algo = algo()
	current_directory = os.path.dirname(__file__)
	parent_directory = os.path.split(current_directory)[0] # Repeat as needed	
	file_path = os.path.join(parent_directory, 'SampleTestCases/input3.txt')
	string_1, string_2 = algo.stringBuilt(file_path)
	process = psutil.Process(os.getpid())
	start_time = time.time()
	delta=30
	alpha=[[0,110,48,94],[110,0,118,48],[48,118,0,110],[94,48,110,0]]
	ans = algo.calAlignment(string_1,string_2,alpha,delta)
	outputFile=open('outputeff.txt','w')
	outputFile.write(str(ans[2])+
                    "\n"+ans[0][:50]+" "+ans[0][-50:]+
					"\n"+ans[1][:50]+" "+ans[1][-50:]+
					"\n"+str(time.time() - start_time)+
					"\n"+str(algo.process_memory()))
 
	outputFile.close()