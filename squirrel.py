#!/usr/bin/python3
"""
Rabbits Module is created by Furkan Baytekin
My GitHub profile: https://github.com/Elagoht
"""
from typing import Iterable, overload
from pickle import dump, dumps, load, loads
from base64 import b64encode, b64decode
from abc import ABC
inf=float("inf")
pi=3.141592653589793
e=2.718281828459045
class StaticBase:
	"""All useful static methods for external iterables located here."""
	@staticmethod
	def readCsv(filePath:str,sep:str=",",ignoreHeaders=True,encoding:str="UTF-8"):
		with open(filePath,"r",encoding=encoding) as file:
			data=[]
			for row in file.readlines()[1:] if ignoreHeaders else file.readlines():
				rows=[]
				for cell in row.split(sep): rows.append(cell)
				data.append(rows)
		return data
	@staticmethod
	def exportCsv(data:Iterable[Iterable[int]],filePath:str,encoding:str="UTF-8"):
		with open(filePath,"w",encoding=encoding) as file:
			for row in data:
				for index,cell in enumerate(row): file.write(cell+("," if index<len(row)-1 else ""))
	@staticmethod
	def transposeIter(items):
		return ValueBase(*items).getColumns(*range(max([len(row) for row in items])))
class ValueBase:
	def __init__(self,*cells:Iterable,colNames=[]):
		self._cells=[]
		self._columns={}
		self._axisnames=[]
		self._axisbackup=[]
		for index in range(len(cells)):
			row=[]
			for i in cells[index]:
				row.append(self.__convert__(i))
			self._cells.append(row)
		if colNames!=[]:
			self.renameColumns(*colNames)
	def __repr__(self): return f"<ValueBase with {len(self)} row"+("s" if len(self)>1 else "")+">" if len(self)>0 else "<ValueBase with no content>"
	def __convert__(self,input): return input
	@property
	def columns(self):
		if len(self)>0:
			columns=[]
			for row in range(len(self.transpose(False).transpose(False)[0])):
				try: columns.append(self._axisnames[row])
				except: columns.append(f"Column {row}")
			self._columns=dict((j,i) for i,j in enumerate(columns))
			return list(self._columns.keys())
		else: return []
	def c(self,stringdex)->int:
		self.columns
		try: return self._columns[stringdex]
		except: raise KeyError("Stringdex must be a column name.")
	def range(self,start:str,stop:str):
		"""Stop index will be include."""
		self.columns
		try: return range(self.c(start),self.c(stop)+1)
		except: raise KeyError("Start and stop must be a column name.")
	def query(self,querystring="",exact:bool=False,columns:Iterable[int]=[]):
		result=[]
		qryCol=[]
		if columns!=[]:
			for row in self._cells:
				qrlRow=[]
				for column in columns: qrlRow.append(row[column])
				qryCol.append(qrlRow)
		else: qryCol=self._cells
		if exact:
			for index,cell in enumerate(qryCol):
				if querystring in cell:
					for item in cell:
						if querystring==item:
							result.append(self._cells[index])
							break
		else:
			for index,cell in enumerate(qryCol):
				for item in cell:
					if str(querystring).lower() in str(item).lower():
						result.append(self._cells[index])
						break
		final=type(self)(*result)
		final._axisnames=self._axisnames
		return final
	def queries(self,queries:Iterable,exacts:Iterable[bool]=[],columns:Iterable[Iterable[int]]=[]):
		if exacts==[]: exacts=[False for _ in queries]
		if columns==[]: columns=[[] for _ in queries]
		result=self
		for query,exact,column in zip(queries,exacts,columns): result=result.query(query,exact,column)
		return result
	def __getitem__(self,index):
		if len(self): return self._cells[index]
	def __setitem__(self,index,val):
		if len(self):
			try:
				result=[]
				for item in val:
					result.append(self.__convert__(item))
				self._cells[index]=result
			except: raise TypeError("Items parameter must be iterable")
		return self
	def __len__(self): return len(self._cells)
	def __bool__(self):
		"""Returns True if it contains any item, else returns False."""
		return bool(len(self))
	@property
	def data(self):
		"""
		Returns a list copy of data.
		"""
		return self._cells
	def indexof(self,items:list):
		for index,item in enumerate(self._cells):
			if item==items: return index
		return -1
	def __add__(self,items:Iterable):
		try:
			result=[]
			for item in items:
				try: result.append(self.__convert__(item))
				except: result.append(None)
			self._cells.append(result)
			self.columns
			return self
		except: raise TypeError("Items parameter must be iterable")
	def __sub__(self,item):
		check=self.indexof(item)
		if check>-1:
			if item!=None: del self._cells[check]
		return self
	def addMany(self,*items:Iterable):
		for item in items: self+=[self.__convert__(i) for i in item]
	def sort(self,byColumn:int=0,asc=True,inPlace=True):
		if inPlace: self._cells.sort(key=lambda x:str(x[byColumn]) if x[byColumn]!=None else -float("inf"),reverse=not asc)
		else: return sorted(self._cells,key=lambda x:str(x[byColumn]) if x[byColumn]!=None else -float("inf"),reverse=not asc)
	@property
	def __maxlen__(self):
		if len(self)>0:
			lens=[]
			for i in self._cells:
				lens.append(len(i))
			return max(lens)
		else: return 0
	def getColumns(self,*columns):
		if self.__maxlen__>max(columns):
			result=[]
			for cell in columns:
				row=[]
				for rows in self._cells:
					try: row.append(rows[cell])
					except: row.append(None)
				result.append(row)
			return type(self)(*result)
		else: return self
	def getColumn(self,column:int):
		if self.__maxlen__>column:
			result=[]
			for rows in self._cells:
				try: result.append(rows[column])
				except: result.append(None)
			return tuple(result)
		else: return []
	def addCsv(self,filePath:str,sep:str=",",ignoreHeaders=True,encoding:str="UTF-8"):
		try:
			with open(filePath,"r",encoding=encoding) as file:
				lines=file.readlines()
				for row in lines[1:] if ignoreHeaders else lines:
					rows=[]
					for cell in row.split(sep):
						try:
							try:
								float(cell)
								rows.append(float(cell))
							except:
								str(cell)
								rows.append(cell.strip())
						except: rows.append(None)
					self+=rows
				if ignoreHeaders: self._axisnames.extend(lines[0].replace("\n","").split(sep))
		except: raise FileNotFoundError
	def saveCsv(self,filePath:str,encoding:str="UTF-8"):
		with open(filePath,"w",encoding=encoding) as file:
			for row in self:
				for index,cell in enumerate(row):
					file.write(str(cell)+("," if index<len(row)-1 else "\n"))
	def renameColumns(self,*columnNames):
		self._axisnames=list(columnNames[:self.__maxlen__])
	def transpose(self,inPlace=True):
		if len(self)>0:
			lens=max([len(row) for row in self._cells])
			if inPlace:
				self._cells=[*self.getColumns(*range(lens))]
				self._axisbackup,self._axisnames=self._axisnames,self._axisbackup
			else:
				copy=type(self)(*self.getColumns(*range(lens)))
				copy._axisbackup,copy._axisnames=self._axisnames,self._axisbackup 
				return copy
		elif not inPlace: return self
	def fillNull(self):
		exec("self.transpose(True);"*2)
	def fillNone(self,fillWith,includeNulls=False):
		if includeNulls: self.fillNull()
		if self.__convert__(fillWith)!=None:
			self.replace(None,fillWith)
		else: raise TypeError(f"Please provide a value compatible with {self}")
	def replace(self,old,new,count=-1,mode=0):
		"""
		Replace a value with a new value.\n
		Count parameter determines how many changes will bi applied.
		If you leave it blank or write -1, changes will be apply for all matches.
		If count is bigger than instance number, it will replace all matches and stop.\n
		If mode is -1, replaces all values contains "old" variable.
		If it is 0, replaces all exact matches.
		If it is 1, replaces all value matches.
		"""
		nth=0
		if count==-1:
			count=self.__maxlen__*len(self)
		for rowind,row in enumerate(self._cells):
			for cellind,cell in enumerate(row):
				if mode==-1:
					if str(old) in str(cell):
						self[rowind][cellind]=self.__convert__(new)
						nth+=1
						if nth>=count: break
				if mode==0:
					if cell==old:
						self[rowind][cellind]=self.__convert__(new)
						nth+=1
						if nth>=count: break
				if mode==1:
					if str(cell)==str(old):
						self[rowind][cellind]=self.__convert__(new)
						nth+=1
						if nth>=count: break
			if nth>=count: break
	def count(self,val,onColumns=[])->int:
		if len(self)>0:
			if onColumns==[]: onColumns=self.allColumns
			data=self.getColumns(*onColumns)
			count=0
			for row in data:
				count+=row.count(val)
			return count
		else: return 0
	def mirror(self,inPlace=True):
		if len(self)>0:
			columns=list(range(self.__maxlen__))
			columns.reverse()
			transformed=self.getColumns(*columns)
			transformed.transpose(True)
			self._axisnames.reverse()
			if inPlace: self._cells=transformed
			else: return transformed
		elif not inPlace: return self
	def flip(self,inPlace=True):
		if len(self)>0:
			rows=list(range(len(self)))
			rows.reverse()
			transformed=[]
			for i in rows:
				transformed.append(self._cells[i])
			if inPlace: self._cells=transformed
			else: return type(self)(*transformed)
		elif not inPlace: return self
	def rotate(self,mode=1,inPlace=True):
		"""
		mode:\n
		-1 -> 90 degrees counterclockwise\n
		 0 -> 0 degree\n
		 1 -> 90 degrees clockwise\n
		 2 -> 180 degrees
		"""
		if len(self)>0:
			copy=type(self)(*self)
			if mode==1:
				copy.transpose(True)
				copy.mirror()
			if mode==-1:
				copy.mirror()
				copy.transpose(True)
			if mode==2:
				copy.mirror()
				copy.flip()
			if inPlace:
				self._cells=copy
				self._axisbackup,self._axisnames=self._axisnames,self._axisbackup
			else:
				copy._axisbackup,copy._axisnames=self._axisnames,self._axisbackup
				return copy
		elif not inPlace:
			return self
	def clone(self):
		if len(self):
			result=type(self)(*self)
			result._axisnames=self._axisnames
			result._axisbackup=self._axisbackup
			return result
		else: return type(self)()
	def truncate(self):
		self._cells=[]
		self._columns={}
		self._axisnames=[]
		self._axisbackup=[]
	def print(self,prefix:str=None,suffix:str=None):
		if prefix!=None: print(str(prefix),end="")
		print(self.__repr__()+"\nItems=[")
		print("*"+str(self.columns)+"*")
		if len(self)>0:
			for i in self: print("",i)
		if suffix!=None: print("] "+str(suffix))
		else: print("]")
	def head(self,count:int=5):
		print(self.__repr__()+f"\nFirst {count} items=[")
		print("*"+str(self.columns)+"*")
		if len(self)>0:
			for i in self[:count]: print("",i)
		print("]")
	def tail(self,count:int=5):
		print(self.__repr__()+f"\nLast {count} items=[")
		print("*"+str(self.columns)+"*")
		if len(self)>0:
			for i in self[-count:]: print("",i)
		print("]")
	def apply(self,function,columns:Iterable[int]=[]):
		"""Function must take the value and return a new acceptable value. If the value is unacceptable it will become None.\n
		### Example\n
		```python
		apply(lambda x:-inf if x<3 else x,[*db.allColumns])
		```\n
		it changes the values less than 3 on all columns, to -inf.\n
		if columns parameter is [], it applies to all columns.
		"""
		if len(self)>0:
			data=self.clone()
			data.fillNull()
			if columns==[]: columns=data.allColumns
			for row in range(len(data)):
				for col in columns:
					data[row][col]=self.__convert__(function(data[row][col])) if data[row][col]!=None else None
				self._cells=data._cells
	def applyMany(self,functions:Iterable,columns:Iterable[Iterable[int]]):
		for i in zip(functions,columns): self.apply(*i)
	@property
	def allColumns(self):
		return range(len(self.transpose(False).transpose(False)[0]))
	def removeDuplicates(self,startFromBottom=False,inPlace=True):
		if len(self)>0:
			data=self.clone()
			if startFromBottom: data.flip()
			result=[]
			for row in data:
				if not (row in result): result.append(row)
			result=type(self)(*result)
			if startFromBottom: result.flip()
			if inPlace: self._cells=result._cells
			else: return result
		elif not inPlace: return self
	def merge(self,With,protectDataType:bool=False,addDuplicates=False,inPlace:bool=True):
		data=self.clone()
		if protectDataType: data.__class__=ValueBase
		for row in With:
			if addDuplicates:data+=row
			elif len(data.queries([*row],[True for _ in row],[data.allColumns for _ in row]))==0: data+=row
		if inPlace: 
			if protectDataType: self.__class__=ValueBase
			self._cells=data._cells
		return data
	def split(self,From:int):
		"""### Example:\n
			```python
			db0, db1 = db.split(3)
			```"""
		return type(self)(*self[:From]),type(self)(*self[From:])
	def compare(self,With:float,operator:str,byColumn):
		"Operator must be <, <=, ==, !=, >= or >."
		if len(self)>0:
			if operator in ("<", "<=", "==", "!=", ">=", ">"):
				try: With=float(With)
				except: raise TypeError("With parameter must be able to convert float type.")
				result=[]
				for index,cell in enumerate(self.getColumn(byColumn)):
					exec(f"if cell {operator} With: result.append(self[index])")
				return type(self)(*result)
			raise ValueError("Operator must be <, <=, ==, !=, >= or >.")
		return self
	def compareMany(self,With:Iterable[float],operators:Iterable[str],byColumns:Iterable[int]):
		if len(self)>0:
			result=self.clone()
			for i in zip(With,operators,byColumns):
				result=result.compare(*i)
			return result
		return self

class __SubBase__(ValueBase):
	def addCsv(self,filePath:str,sep:str=",",ignoreHeaders=True,encoding:str="UTF-8"):
		with open(filePath,"r",encoding=encoding) as file:
			lines=file.readlines()
			for row in lines[1:] if ignoreHeaders else lines:
				rows=[]
				for cell in row.split(sep): rows.append(self.__convert__(cell))
				self+=rows
			if ignoreHeaders: self._axisnames.extend(lines[0].replace("\n","").split(sep))

class __NumBase__(__SubBase__):
	def sort(self,byColumn:int=0,asc=True,inPlace=True):
		if len(self)>0:
			if inPlace: self._cells=sorted(self._cells,key=lambda x:x[byColumn] if x[byColumn]!=None else -float("inf"),reverse=not asc)
			else: return sorted(self._cells,key=lambda x:x[byColumn] if x[byColumn]!=None else -float("inf"),reverse=not asc)
		return self
	def sortColumn(self,column):
		if len(self)>0:
			data=list(self.getColumn(column))
			while None in data:
				data.remove(None)
			return sorted(data)
		return self
	def median(self,column):
		if len(self)>0: return self.percentile(50,column)
		return None
	def modes(self,column):
		if len(self)>0:
			data=self.sortColumn(column)
			dic={}
			for item in data: dic[item]=data.count(item)
			max_=max(dic.values())
			result=[]
			for i,j in dic.items():
				if j==max_: result.append(float(i))
			return tuple(result)
		return None,
	def mean(self,column):
		if len(self)>0:
			data=self.sortColumn(column)
			return sum(data)/len(data)
		return None
	def min(self,column):
		if len(self)>0:
			data=self.sortColumn(column)
			return float(min(data))
		return None
	def max(self,column):
		if len(self)>0: return float(max(self.sortColumn(column)))
		return None
	def quartiles(self,column):
		"""Returns a tuple contains first and third quartiles."""
		if len(self)>0: return self.percentile(25,column),self.percentile(75,column)
		return None,None
	def percentile(self,percent,column):
		"""Percent parameter must be in range [0-100]."""
		if len(self)>0:
			if percent<0 or percent>100: raise ValueError("Percent parameter must be in range [0-100].")
			data=self.sortColumn(column)
			k=(len(data)-1)*percent/100
			f=int(k)
			c=int(k)+1 if k!=int(k) else int(k)
			if f==c: return data[int(k)]
			return data[int(c)]*(k-f)+data[int(f)]*(c-k)
		return None
	def decile(self,decim,column):
		"""Percent parameter must be in range [0-100]."""
		if len(self)>0:
			if decim<0 or decim>10: raise ValueError("Percent parameter must be in range [0-10].")
			return self.percentile(decim*10,column)
	def abs(self,columns:Iterable[int]=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:abs(x),columns)
	def oppositeSign(self,columns=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:-x,columns)
	def increase(self,amount=1,columns=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x+amount,columns)
	def decrease(self,amount=1,columns=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x-amount,columns)
	def multiply(self,amount=1,columns=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x*amount,columns)
	def divide(self,amount=1,columns=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x/amount,columns)
	def floorDivide(self,amount=1,columns=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x//amount,columns)
	def modulus(self,amount=1,columns=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x%amount,columns)
	def power(self,amount=1,columns=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:pow(x,amount),columns)
	def round(self,ndigits=1,columns=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:round(x,ndigits),columns)
	def sum(self,axis=0):
		"""Returns a tuple with all sums of specified axis."""
		data=self.clone()
		if axis in ["x",1]: pass
		elif axis in ["y",0]: data.transpose()
		else: raise ValueError("Axis must be 'x', 1 or 'y', 0")
		result=[]
		for i in data: result.append(sum(i))
		return tuple(result)
	def summary(self,column): return f"""*** Column {column} ***
Minimum\t\t: {self.min(column)}
1st Quarter\t: {self.quartiles(column)[0]}
Median\t\t: {self.median(column)}
2ns Quarter\t: {self.quartiles(column)[1]}
Maximum\t\t: {self.max(column)}
Mean \t\t: {self.mean(column)}"""
	def summaries(self,*columns):
		"""Leave blank for get all columns."""
		if columns==(): columns=self.allColumns
		result=""
		for column in columns:
			result+=f"""\n*** Column {column} ***
Minimum\t\t: {self.min(column)}
1st Quarter\t: {self.quartiles(column)[0]}
Median\t\t: {self.median(column)}
2ns Quarter\t: {self.quartiles(column)[1]}
Maximum\t\t: {self.max(column)}
Mean \t\t: {self.mean(column)}"""
		return result.replace("\n","",1)
class StrBase(__SubBase__):
	def __repr__(self): return f"<StrBase with {len(self)} row"+("s" if len(self)>1 else "")+">" if len(self)>0 else "<StrBase with no content>"
	def __convert__(self,input):
		try:return str(input).strip()
		except: return None
	def compare(self,With:float,operator:str,byColumn):
		"Operator must be <, <=, ==, !=, >= or >."
		if len(self)>0:
			if operator in ("<", "<=", "==", "!=", ">=", ">"):
				With=str(With)
				result=[]
				for index,cell in enumerate(self.getColumn(byColumn)):
					exec(f"if cell {operator} With: result.append(self[index])")
				return type(self)(*result)
			else: raise ValueError("Operator must be <, <=, ==, !=, >= or >.")
		else: return self
class FloatBase(__NumBase__):
	def __repr__(self): return f"<FloatBase with {len(self)} row"+("s" if len(self)>1 else "")+">" if len(self)>0 else "<FloatBase with no content>"
	def __convert__(self,input):
		try: return (((float(input) if input!="e" else e) if input!="-e" else -e) if input!="pi" else pi) if input!="-pi" else -pi
		except: return None
	def floor(self,columns=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:int(x),columns)
	def ceil(self,columns=[]):
		"""if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:int(x)+1 if x!=int(x) else x,columns)
	def format(self,ndigits:int,columns=[]):
		"""CAUTION! This method may cause data correction loss.\n
		if columns parameter is [], it applies to all columns."""
		self.apply(lambda x:format(x,f".{ndigits}f"),columns)
	def print(self,ndigits:int=2,prefix:str=None,suffix:str=None):
		if prefix!=None: print(str(prefix),end="")
		print(self.__repr__()+"\nItems=[")
		print("*"+str(self.columns)+"*")
		if ndigits<1: ndigits=2
		if len(self)>0:
			for i in self: 
				print(" [",end="")
				for k,l in enumerate([(self.__convert__(format(j,f".{ndigits}f")) if len(str(j).split(".")[1])>=ndigits else str(j).split(".")[0]+"."+str(j).split(".")[1].ljust(ndigits,"0")) if "." in str(j) else j for j in i]):
					print(str(l)+(", " if k<self.__maxlen__-1 else ""),end="")
				print("]")
		if suffix!=None: print("] "+str(suffix))
		else: print("]")
class IntBase(__NumBase__):
	def __repr__(self): return f"<IntBase with {len(self)} row"+("s" if len(self)>1 else "")+">" if len(self)>0 else "<IntBase with no content>"
	def __convert__(self,input):
		try: return (((((((((int(input) if input!=-inf else -inf) if input!=inf else inf) if input!="inf" else inf) if input!="-inf" else -inf) if input!="e" else 3) if input!="-e" else -3) if input!=e else 3) if input!=-e else -3) if input!="pi" else 3) if input!="-pi" else -3
		except: return None
def saveDB(obj,filename):
	"""This function can be use to store any type of object."""
	with open(filename+".sqr","wb") as outp: dump(obj,outp,5)
def loadDB(filename,type_=ValueBase):
	"""This function can be use to restore any type of object."""
	with open(filename+".sqr","rb") as inp: 
		obj=load(inp)
		if type_==ValueBase: return ValueBase(*obj)
		elif type_==StrBase: return StrBase(*obj)
		elif type_==IntBase: return IntBase(*obj)
		elif type_==FloatBase: return FloatBase(*obj)
		else: return obj
def saveSecure(obj,filename):
	"""This function can be use to store any type of object."""
	with open(filename+".sqs","w") as outp: outp.write(b64encode(dumps(obj,5)).decode())
def loadSecure(filename,type_=ValueBase):
	"""This function can be use to restore any type of object."""
	with open(filename+".sqs","r") as inp:
		obj=loads(b64decode(inp.read()))
		if type_==ValueBase: return ValueBase(*obj)
		elif type_==StrBase: return StrBase(*obj)
		elif type_==IntBase: return IntBase(*obj)
		elif type_==FloatBase: return FloatBase(*obj)
		else: return obj