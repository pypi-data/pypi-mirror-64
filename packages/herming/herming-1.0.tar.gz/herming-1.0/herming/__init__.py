import random
class ch01():
	def __init__(self,):
		self._len_=10
		self._nb_len=5
		self._pn_=[]
		for i in range(self._nb_len):
			self._pn_.append({"0":1,"1":1,"2":1,"3":1,"4":1,"5":1,"6":1,"7":1,"8":1,"9":1})
		
		self._data_=["00000"]*self._len_
	def start(self,):
		for i in range(len(self._data_)):
			ans=""
			for j in range(self._nb_len):
				nbs=random.randint(0,sum(self._pn_[j].values()))
				for n in range(10):
					nbs-=self._pn_[j]["%s"%n]
					if nbs<=0:
						ans+="%s"%n
						break
			self._data_[i]=ans
		return self._data_
	def cheak(self,nb):
		for i in nb:
			nb_data=self._data_[int(i)]
			for j,k in enumerate(nb_data):
				self._pn_[j][k]+=1
	def get_data(self,):
		sn=""
		for i in self._pn_:
			#print(i)
			sn+="%s"%(list (i.keys()) [list (i.values()).index (max(i.values()))])
		return sn