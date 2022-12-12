#!/bin/env python
"""
Squirrel Module is created by Furkan Baytekin
My GitHub profile: https://github.com/Elagoht
"""
from typing import Iterable, Tuple
from pickle import dump, dumps, load, loads
from base64 import b64encode, b64decode
from re import search, A, I, S

inf=float("inf")
pi=3.141592653589793
e=2.718281828459045
class StaticBase:
	"""All useful static methods for external iterables located here."""
	@staticmethod
	def readCsv(filePath:str,sep:str=",",FirstLineIsColumnNames=True,encoding:str="UTF-8"):
		with open(filePath,"r",encoding=encoding) as file:
			data=[]
			for row in file.readlines()[1:] if FirstLineIsColumnNames else file.readlines():
				rows = list(row.replace("\n","").split(sep))
				data.append(rows)
		return data
	@staticmethod
	def exportCsv(data:Iterable[Iterable[int]],filePath:str,encoding:str="UTF-8"):
		with open(filePath,"w",encoding=encoding) as file:
			for row in data:
				for index,cell in enumerate(row): file.write(cell+("," if index<len(row)-1 else ""))
	@staticmethod
	def transposeIter(items):
		return ValueBase(*items).getColumns(*range(max(len(row) for row in items)))
class ValueBase:
	def __init__(self,*cells:Iterable,colNames=[]):
		self._cells=[]
		self._columns={}
		self._axisnames=[]
		self._axisbackup=[]
		for row in cells:
			rows = [self.__convert__(val) for val in row]
			self._cells.append(rows)
		if colNames!=[]: self.renameColumns(*colNames)
	def __repr__(self): return f"<ValueBase with {len(self)} row"+("s" if len(self)>1 else "")+">" if len(self) else "<ValueBase with no content>"
	def __convert__(self,input_): return input_
	@property
	def columns(self):
		"""Returns a list that contains all column names."""
		if not len(self):
			return []
		columns=[]
		for row in range(len(self.transpose(False).transpose(False)[0])):
			try: columns.append(self._axisnames[row])
			except: columns.append(f"Column {row}")
		self._columns = {j: i for i,j in enumerate(columns)}
		return list(self._columns.keys())
	def c(self,stringdex) -> int:
		"""All methods takes integer values to detect columns, this method allows you to get integer value of specified column name.

In example, for a database with column names ("name", "surname", "phone"), self.c("surname") will return 1.

Note that, stringdex is case sensitive."""
		self.columns
		try: return self._columns[stringdex]
		except: raise KeyError("Stringdex must be a column name.")
	def range(self,start:str,stop:str) -> range:
		"""Returns a range object that specify between given column names.

Stop index will be include."""
		self.columns
		try: return range(self.c(start),self.c(stop)+1)
		except: raise KeyError("Start and stop must be a column name.")
	def cloneFromColumns(self,*columns:Iterable[int],newColumnNames=[]):
		"""Returns a database as same type made with columns specified.

If newColumnNames equals [], use imported columns names. Do not use one column twice while not giving new column names."""
		result=type(self)(*(self.getColumn(i) for i in columns))
		result.transpose()
		if newColumnNames==[]:
			result.renameColumns(*[self.columns[i] for i in columns])
		else:
			result.renameColumns(*newColumnNames)
		return result
	def cloneFromColumnRange(self,start:int,stop:int):
		"""Returns a database as same type made with columns in range specified. Stop index will be include."""
		result=type(self)(*(self.getColumn(i) for i in range(start,stop+1)))
		result.transpose()
		result.renameColumns(*[self.columns[i] for i in range(start,stop+1)])
		return result
	def query(self,querystring="",exact:bool=False,caseSensitive:bool=False,columns:Iterable[int]=[]):
		"""Let you search something in database. Returns same type of database."""
		result=[]
		qryCol=[]
		if columns!=[]:
			for row in self._cells:
				qryRow = [row[column] for column in columns]
				qryCol.append(qryRow)
		else: qryCol=self._cells
		for index, cell in enumerate(qryCol):
			if exact:
				if querystring in cell:
					for item in cell:
						if caseSensitive:
							if querystring==item:
								result.append(self._cells[index])
								break
						elif str(querystring).lower()==str(item).lower():
							result.append(self._cells[index])
							break
			else:
				for item in cell:
					if caseSensitive:
						if str(querystring) in str(item):
							result.append(self._cells[index])
							break
					elif str(querystring).lower() in str(item).lower():
						result.append(self._cells[index])
						break
		final=type(self)(*result)
		final._axisnames=self._axisnames
		return final
	def queries(self,queries:Iterable,exacts:Iterable[bool]=[],caseSensitives:Iterable[bool]=[],columns:Iterable[Iterable[int]]=[]):
		"""Lets you do more than one query at the same time. Ut may be looks like a little confusing. The concept is very simple. Pass every argument in a list for every query sequence.

I.e:

```py
db.query("some",True,False,[]).query("thing",False,False,[1])
```

is same thing as

```py
db.queries(["some","thing"],[True,False],[False,False],[[],[1]])"""
		if exacts==[]: exacts=[False for _ in queries]
		if columns==[]: columns=[[] for _ in queries]
		result=self
		for query,exact,case,column in zip(queries,exacts,caseSensitives,columns): result=result.query(query,exact,case,column)
		return result
	def regexQuery(self,regex="",columns:Iterable[int]=[],flags:str=""):
		r"""Let you search something in database via regular expression. Returns same type of database. 

Only ASCII (A), IGNORECASE (I) and DOTALL (S) flags are allowed. You can add them via writing into a string such as "ais", "ASI" etc. 

I.e (email validation):

db.regexQuery(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",[db.c("E-mail")],"i")
    """
		result=[]
		qryCol=[]
		if columns!=[]:
			for row in self._cells:
				qryRow=[row[column] for column in columns]
				qryCol.append(qryRow)
		else: qryCol=self._cells
		_flags=0
		for flag in flags:
			flag=flag.upper()
			if flag=="A": _flags|=A
			if flag=="I": _flags|=I
			if flag=="S": _flags|=S
			if flag not in "AIS": raise ValueError("Flags must be one of them: A, I, S.")
		for index, cell in enumerate(qryCol):
			if flags != None:
				result.extend(self._cells[index] for item in cell if search(regex,str(item),_flags))
			else:
				result.extend(self._cells[index] for item in cell if search(regex,str(item)))
		final=type(self)(*result)
		final._axisnames=self._axisnames
		return final
	def election(self,querystring="",exact:bool=False,caseSensitive:bool=False,columns:Iterable[int]=[]):
		"""Same as query but only keeps results on itself. Others will be deleted."""
		self._cells=self.query(querystring,exact,caseSensitive,columns).data
	def elections(self,queries:Iterable,exacts:Iterable[bool]=[],caseSensitives:Iterable[bool]=[],columns:Iterable[Iterable[int]]=[]):
		"""Same as queries but only keeps results on itself. Others will be deleted."""
		self._cells=self.queries(queries,exacts,caseSensitives,columns).data
	def fetch(self,querystring="",exact:bool=False,caseSensitive:bool=False,columns:Iterable[int]=[]):
		"""Same as query but return a list object instead of database."""
		return self.query(querystring,exact,caseSensitive,columns).data
	def fetchOne(self,querystring="",exact:bool=False,caseSensitive:bool=False,columns:Iterable[int]=[]):
		"""Returns the first entry as a list on query results."""
		result=self.fetch(querystring,exact,caseSensitive,columns)
		return result[0] if len(result)>0 else []
	def fetchX(self,queries:Iterable,exacts:Iterable[bool]=[],caseSensitives:Iterable[bool]=[],columns:Iterable[Iterable[int]]=[]):
		"""Stands for queries equilavent to fetch method."""
		return self.queries(queries,exacts,caseSensitives,columns).data
	def fetchXOne(self,queries:Iterable,exacts:Iterable[bool]=[],caseSensitives:Iterable[bool]=[],columns:Iterable[Iterable[int]]=[]):
		"""Stands for queries equilavent to fetchOne method."""
		result=self.fetchX(queries,exacts,caseSensitives,columns)
		return result[0] if len(result)>0 else []
	def __getitem__(self,index):
		"""Returns specified row in database as list object."""
		if len(self): return self._cells[index]
	def __setitem__(self,index,val):
		if len(self):
			try:
				result=[self.__convert__(item) for item in val]
				self._cells[index]=result
			except: raise TypeError("Items parameter must be iterable")
		return self
	def __len__(self) -> int:
		"""Returns row count."""
		return len(self._cells)
	def __bool__(self) -> bool:
		"""Returns True if it contains any item, else returns False."""
		return bool(len(self))
	@property
	def data(self):
		"""Returns a list copy of data."""
		return self._cells
	def indexof(self,items:list):
		"""if a row matches with items argument, it returns the row number of first matched instance else returns -1."""
		return next((index for index, item in enumerate(self._cells) if item == items), -1)
	def __add__(self,items:Iterable):
		"""Allows you to add rows by + and +="""
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
		if check > -1 and item!=None:
			del self._cells[check]
		return self
	def add(self,*items:Iterable):
		"""Add row to database. Prefer this method instead of + and +="""
		self+=items
		return len(self)
	def addMany(self,*items:Iterable):
		"""Add more than one row in one method."""
		for item in items: self+=[self.__convert__(i) for i in item]
	def remove(self,row:int,col:int):
		"""Delete a single cell on database. Remaining cells on the same row will justify left. Do not use on data science unless necesserity."""
		self-=self[row][col]
		return len(self)
	def removeRow(self,row:int):
		"""Deletes row to database. Prefer this method instead of - and -="""
		data=self[row]
		self-=self[row]
		return data
	def edit(self,new,row:int,col:int):
		"""Replaces data in specified row and column with new data. Returns the old data."""
		data=self[row][col]
		self[row][col]=new
		return len(data)
	def editRow(self,newRow,row:int):
		"""Replaces data in specified row with new data. Returns the old data."""
		data=self[row]
		self[row]=newRow
		return data
	def sort(self,byColumn:int=0,asc:bool=True,inPlace:bool=True):
		"""Sort every row by specified column. This method converts every data to string and sorts by that case.

If you want to specify a key function instead of converting string, use sortByKey method.

If you want to sort numbers by bigger to lesser, use sortNums method."""
		if inPlace: self._cells.sort(key=lambda x:str(x[byColumn]) if x[byColumn]!=None else -float("inf"),reverse=not asc)
		else: return sorted(self._cells,key=lambda x:str(x[byColumn]) if x[byColumn]!=None else -float("inf"),reverse=not asc)
	def sortByKey(self,key=lambda x:x[0],asc:bool=True,inPlace:bool=True):
		"""This method lets you determine sorting key function to sort data. You must specify column number like this: x[n].

I.e:

```py
db.sortByKey(lambda x:x[0].title() if type(x[0])==str else x[0])
```"""
		self.columns
		if inPlace: self._cells.sort(key=key,reverse=not asc)
		else: return sorted(self._cells,key=key,reverse=not asc)
	def sortNums(self,byColumn:int=0,asc:bool=True,inPlace:bool=True):
		"""Sorts columns that only contains numerical data in bigger to lesser value."""
		self.columns
		if inPlace: self._cells.sort(key=lambda x:float(x[byColumn]),reverse=asc)
		else: return sorted(self._cells,key=lambda x:float(x[byColumn]),reverse=asc)
	@property
	def columnCount(self):
		"""Basically, retuns the column count."""
		if len(self):
			lens=[len(i) for i in self._cells]
			return max(lens)
		else: return 0
	def getColumns(self,*columns):
		"""Returns data in specified columns as lists in a list."""
		if self.columnCount<=max(columns):
			return self
		result=[]
		for cell in columns:
			row=[]
			for rows in self._cells:
				try: row.append(rows[cell])
				except: row.append(None)
			result.append(row)
		return type(self)(*result)
	def getColumn(self,column:int):
		"""Returns data in specified columns as a list."""
		if self.columnCount<=column:
			return []
		result=[]
		for rows in self._cells:
			try: result.append(rows[column])
			except: result.append(None)
		return tuple(result)
	def addCsv(self,filePath:str,FirstLineIsColumnNames=True,sep:str=",",encoding:str="UTF-8"):
		"""Adds data in a csv formatted file to database. This method can update column names."""
		try:
			with open(filePath,"r",encoding=encoding) as file:
				lines=file.readlines()
				for row in lines[1:] if FirstLineIsColumnNames else lines:
					rows=[]
					for cell in row.split(sep):
						try:
							try:
								if "+" not in cell:
									float(cell)
									if float(cell)==int(cell): rows.append(int(cell))
									else: rows.append(float(cell))
								else: rows.append(cell.strip())
							except:
								str(cell)
								rows.append(cell.strip())
						except:
							rows.append(None)
					self+=rows
				if FirstLineIsColumnNames: self._axisnames.extend(lines[0].replace("\n","").split(sep))
		except: raise FileNotFoundError
	def saveCsv(self,filePath:str,encoding:str="UTF-8",IncludeColumnNames=True):
		"""Saves the data to a file in csv format. You can decide whether the csv file should have column names."""
		with open(filePath,"w",encoding=encoding) as file:
			if IncludeColumnNames: file.write(",".join(self.columns)+"\n")
			for row in self:
				for index,cell in enumerate(row):
					file.write(str(cell)+("," if index<len(row)-1 else "\n"))
	def renameColumns(self,*columnNames):
		"""Changes column names. You can use this methods in different ways. I.e:

```py
db.renameColumns(*[i.title() for i in db.columns])
```

This will make your column names title formatted."""
		if len(columnNames)==len(set(columnNames)): self._axisnames=list(columnNames[:self.columnCount])
		else: raise ValueError("Column names must be unique")
	def transpose(self,inPlace=True):
		"""Changes rows as columns, columns as rows. Don't worry you won't lose column names, they will appear in next transpose or rotate. You may need to define new column names for transposed columns."""
		if len(self):
			lens = max(len(row) for row in self._cells)
			if inPlace:
				self._cells=[*self.getColumns(*range(lens))]
				self._axisbackup,self._axisnames=self._axisnames,self._axisbackup
			else:
				copy=type(self)(*self.getColumns(*range(lens)))
				copy._axisbackup,copy._axisnames=self._axisnames,self._axisbackup
				return copy
		elif not inPlace: return self
	def fillNull(self):
		"""Fills null data with None value."""
		exec("self.transpose(True);"*2)
	def fillNone(self,fillWith,includeNulls=False):
		"""Fills None values with specified value. you can choose what will happen to null values."""
		if includeNulls: self.fillNull()
		if self.__convert__(fillWith)!=None:
			self.replace(None,fillWith)
		else: raise TypeError(f"Please provide a value compatible with {type(self)}")
	def replace(self,old,new,count=-1,mode=0):
		"""
		Replaces a value with a new value.

		Count parameter determines how many changes will be applied.

		If you leave it blank or write -1, changes will be apply for all matches.

		If count is bigger than instance number, it will replace all matches and stop.

		If mode is -1, replaces all values contains "old" variable.

		If it is 0, replaces all exact matches.

		If it is 1, replaces all value matches."""
		nth=0
		if count==-1:
			count=self.columnCount*len(self)
		for rowind,row in enumerate(self._cells):
			for cellind,cell in enumerate(row):
				if mode==-1 and str(old) in str(cell):
					self[rowind][cellind]=self.__convert__(new)
					nth+=1
					if nth>=count: break
				if mode==0 and cell==old:
					self[rowind][cellind]=self.__convert__(new)
					nth+=1
					if nth>=count: break
				if mode==1 and str(cell) ==str(old):
					self[rowind][cellind]=self.__convert__(new)
					nth+=1
					if nth>=count: break
			if nth>=count: break
	def count(self,val,onColumns=[]) -> int:
		"""Count any value on specified columns. [] for include all columns."""
		if len(self):
			if onColumns==[]: onColumns=self.allColumns
			data=self.getColumns(*onColumns)
			return sum(row.count(val) for row in data)
		else: return 0
	def mirror(self,inPlace=True):
		"""Reverse data by Y axis. Use flip method for X axis."""
		if len(self):
			columns=list(range(self.columnCount))
			columns.reverse()
			transformed=self.getColumns(*columns)
			transformed.transpose(True)
			self._axisnames.reverse()
			if inPlace: self._cells=transformed
			else: return transformed
		elif not inPlace: return self
	def flip(self,inPlace=True):
		"""Reverse data by X axis. Use mirror method for Y axis."""
		if len(self):
			rows=list(range(len(self)))
			rows.reverse()
			transformed=[self._cells[i] for i in rows]
			if inPlace: self._cells=transformed
			else: return type(self)(*transformed)
		elif not inPlace: return self
	def rotate(self,mode=1,inPlace=True):
		"""Rotate database. You won't lose column names, they will appear in next rotate or transpose.

Mode:

* -1 -> 90 degrees counterclockwise
* 0 -> 0 degree
* 1 -> 90 degrees clockwise
* 2 -> 180 degrees"""
		if len(self):
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
		"""Make a copy of database."""
		if not len(self):
			return type(self)()
		result=type(self)(*self)
		result._axisnames=self._axisnames
		result._axisbackup=self._axisbackup
		return result
	def truncate(self):
		"""Empty database. No ways to undo!"""
		self._cells=[]
		self._columns={}
		self._axisnames=[]
		self._axisbackup=[]
	def print(self,prefix:str=None,suffix:str=None,align:bool=True,countingStarts:int=0):
		"""Prints all of the data in a pretty looking table.

Disabling alignment may be faster but uglier for big databases."""
		if prefix!=None:
			print(prefix, end="")
		if align:
			lencol=[max(len(max((str(i) if type(i)!=str else f'"{i}"' for i in self.getColumn(col)), key=len)), len(self.columns[col])) for col in range(self.columnCount)]

		lendigit=len(str(len(self)+countingStarts))
		print(self.__repr__()+"\nItems = [")
		if align:
			print(" * [ ".rjust(lendigit+4), end="")
			for data,lc,n in zip(self.columns,lencol,range(self.columnCount)):
				print(f"{data}".center(lc),end="" if n==self.columnCount-1 else " | ")
			print(" ]")
		else: print(" *".rjust(lendigit+1)+" [ "+", ".join(self.columns)+" ]")
		if len(self):
			if align:
				for n,row in enumerate(self):
					print(f" {n+countingStarts} [ ".rjust(lendigit+4),end="")
					for data,lc,nth in zip(row,lencol,range(self.columnCount)):print(f"{data}".ljust(lc) if type(data)!=str else f'"{data}"'.ljust(lc),end=" " if nth==self.columnCount-1 else " | ")
					print("]")
			else:
				for n,i in enumerate(self): print(f" {n}".rjust(lendigit+1),i)
		if suffix!=None:
			print(f"] {suffix}")
		else: print("]")
	def head(self,count:int=5,prefix:str="",suffix:str="",align:bool=True,countingStarts:int=0):
		"""Prints first n rows in a table."""
		if len(self): type(self)(*self[:count],colNames=self.columns).print(prefix,suffix,align,countingStarts)
		else: self.print()
	def tail(self,count:int=5,prefix:str="",suffix:str="",align:bool=True,countingStarts:int=0):
		"""Prints last n rows in a table."""
		if len(self): type(self)(*self[-count:],colNames=self.columns).print(prefix,suffix,align,countingStarts+len(self)-count)
	def section(self,start:int=0,end:int=0,prefix:str="",suffix:str="",align:bool=True,countingStarts:int=0):
		"""Prints rows between start and stop values in a table. End point includes."""
		if len(self): type(self)(*self[start:end+1],colNames=self.columns).print(prefix,suffix,align,countingStarts+start)
	def apply(self,function,columns:Iterable[int]=[]):
		"""Apply a function to specified columns.

Function must take the value and return a new acceptable value. If the value is unacceptable it will become None.

I.e:

```py
apply(lambda x:-inf if x<3 else x,[*db.allColumns])
```

It changes the values less than 3 on all columns, to -inf.

if columns parameter is [], it applies to all columns."""
		if len(self):
			data=self.clone()
			data.fillNull()
			if columns==[]: columns=data.allColumns
			for row in range(len(data)):
				for col in columns:
					data[row][col]=self.__convert__(function(data[row][col])) if data[row][col]!=None else None
				self._cells=data._cells
	def applyMany(self,functions:Iterable,columns:Iterable[Iterable[int]]):
		"""Applies more than one function to specified columns in one method. It may look a little bit confusing. But the concept is simple.

```py
db.apply(lambda x:x.title()).apply(lambda x:x**2,[2,3])
```

is the same as

```py
db.applyMany([(lambda x:x.title()),(lambda x:x**2)],[[],[2,3]])
"""
		for i in zip(functions,columns): self.apply(*i)
	@property
	def allColumns(self):
		"""Returns a range object that refers all columns as integer."""
		return range(len(self.transpose(False).transpose(False)[0]))
	def removeDuplicates(self,startFromBottom=False,inPlace=True):
		"""Removes duplicate entries. You can determine which entry will kept, first or last."""
		if len(self):
			data=self.clone()
			if startFromBottom: data.flip()
			result=[]
			for row in data:
				if row not in result: result.append(row)
			result=type(self)(*result)
			if startFromBottom: result.flip()
			if inPlace: self._cells=result._cells
			else: return result
		elif not inPlace: return self
	def merge(self,With,protectDataType:bool=False,addDuplicates=False,inPlace:bool=True):
		"""Merge two database in one. You can determine what will happen to duplicate entries."""
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
		"""Slice the database into two pieces. Returnsa tuple, so you can compherence it.

Example:

```python
db0, db1=db.split(3)
```"""
		first=type(self)(*self[:From])
		first._axisnames=self._axisnames
		first._axisbackup=self._axisbackup[:From]
		second=type(self)(*self[From:])
		second._axisnames=self._axisnames
		second._axisbackup=self._axisbackup[From:]
		return first,second
	def compare(self,With:float,operator:str,byColumn:int):
		"""Like query method, returns only matched rows.

Operator must be a string and one of <, <=, ==, !=, >= or >."""
		if len(self):
			if operator.strip() in {"<", "<=", "==", "!=", ">=", ">"}:
				try:
					With=float(With)
				except: raise TypeError("With parameter must be able to convert float type.")
				result=[]
				for _ in self.getColumn(byColumn):
					exec(f"if cell {operator} With: result.append(self[index])")
				final=type(self)(*result)
				final._axisnames=self._axisnames
				final._axisbackup=self._axisbackup
				return final

			raise ValueError("Operator must be <, <=, ==, !=, >= or >.")
		return self
	def compareMany(self,With:Iterable[float],operators:Iterable[str],byColumns:Iterable[int]):
		"""Like queries method, filters database many times.

I.e:

```py
db.compare(4.71,"<=",3).compare(5.36,"!=",2)
```

is same as

```py
db.compareMany([4.71,5.36],["<"=","!="],[3,2])
```"""
		if len(self):
			result=self.clone()
			for i in zip(With,operators,byColumns):
				result=result.compare(*i)
			return result
		return self
	def saveDB(self,filename:str):
		"""Save database to a file to load it later."""
		saveDB(self,filename)
	def saveSecure(self,filename:str):
		"""Save database encrypted to a file to load it later."""
		saveSecure(self,filename)
	def saveToString(self):
		"""Get a string value of database encrypted."""
		return saveToString(self)
	def changeType(self,type_):
		"""Change database type."""
		data=type_(*self)
		data._axisnames=self._axisnames
		data._axisbackup=self._axisbackup
		return data
	def swap(self,from_:Tuple[int,int],to_:Tuple[int,int]):
		"Swaps two instances' positons."
		frm=self[from_[0]][from_[1]]
		to=self[to_[0]][to_[1]]
		self[from_[0]][from_[1]],self[to_[0]][to_[1]]=self[to_[0]][to_[1]],self[from_[0]][from_[1]]
		return f"{frm} swapped with {to}."
	def swapRow(self,from_,to_):
		"Swaps two row's position"
		frm=self.indexof(self[from_])
		to=self.indexof(self[to_])
		self[from_],self[to_]=self[to_],self[from_]
		return f"Row #{frm} swapped with #{to}"
	def moveUp(self,row,col):
		"""Swaps specified item and the item upper, if row equals 0, swaps with last row."""
		self.swap((row,col), (len(self)-1 if row < 1 else row-1, col))
	def moveDown(self,row,col):
		"""Swaps specified item and the item down, if row equals length, swaps with first row."""
		self.swap((row,col),(0 if row+1>len(self)-1 else row+1,col))
	def moveLeft(self,row,col):
		"""Swaps specified item and the item left, if column equals 0, swaps with last column."""
		self.swap((row,col), (row, col-1 if col > 1 else self.columnCount-1))
	def moveRight(self,row,col):
		"""Swaps specified item and the item right, if row equals length, swaps with first column."""
		self.swap((row,col),(row,0 if col+1>self.columnCount-1 else col+1))
class __SubBase__(ValueBase):
	def addCsv(self,filePath:str,sep:str=",",FirstLineIsColumnNames=True,encoding:str="UTF-8"):
		"""add CSV formatted file as pure numerical data. if a value is not numerical, it will be added as None value."""
		with open(filePath,"r",encoding=encoding) as file:
			lines=file.readlines()
			for row in lines[1:] if FirstLineIsColumnNames else lines:
				rows = [self.__convert__(cell) for cell in row.split(sep)]
				self+=rows
			if FirstLineIsColumnNames: self._axisnames.extend(lines[0].replace("\n","").split(sep))

class __NumBase__(__SubBase__):
	def sort(self,byColumn:int=0,asc=True,inPlace=True):
		"""Sorts numbers in lesser to bigger. Use sortNums method to sort bigger to lesser."""
		if len(self):
			if inPlace: self._cells=sorted(self._cells,key=lambda x:x[byColumn] if x[byColumn]!=None else -float("inf"),reverse=not asc)
			else: return sorted(self._cells,key=lambda x:x[byColumn] if x[byColumn]!=None else -float("inf"),reverse=not asc)
		return self
	def sortColumn(self,column):
		"""Returns a list object created by sorted state of selected column."""
		if len(self):
			data=list(self.getColumn(column))
			while None in data: data.remove(None)
			return sorted(data)
		return self
	def median(self,column):
		"""Returns median value of specified column."""
		return self.percentile(50,column) if len(self) else None
	def modes(self,column) -> tuple:
		"""Returns mode values of specified column in a tuple or None in a tuple."""
		if not len(self):
			return None,
		data=self.sortColumn(column)
		dic = {item: data.count(item) for item in data}
		max_=max(dic.values())
		result = [float(i) for i, j in dic.items() if j==max_]
		return tuple(result)
	def mean(self,column):
		"""Returns mean value of specified column."""
		if len(self):
			data=self.sortColumn(column)
			return sum(data)/len(data)
		return None
	def min(self,column):
		"""Returns minimum value of specified column."""
		return float(min(self.sortColumn(column))) if len(self) else None
	def max(self,column):
		"""Returns maximum value of specified column."""
		return float(max(self.sortColumn(column))) if len(self) else None
	def quartiles(self,column):
		"""Returns a tuple contains first and third quartiles."""
		if len(self): return self.percentile(25,column),self.percentile(75,column)
		return None,None
	def percentile(self,percent,column):
		"""Returns percentile value of specified column.

Percent parameter must be in range [0-100]."""
		if not len(self):
			return None
		if percent<0 or percent>100: raise ValueError("Percent parameter must be in range [0-100].")
		data=self.sortColumn(column)
		k=(len(data)-1)*percent/100
		f=int(k)
		c=int(k)+1 if k!=int(k) else int(k)
		return data[int(k)] if f==c else data[int(c)]*(k-f) + data[f] * (c-k)
	def decile(self,decim,column):
		"""Returns decile value of specified column.

Decim parameter must be in range [0-10]."""
		if len(self):
			if decim<0 or decim>10: raise ValueError("Decim parameter must be in range [0-10].")
			return self.percentile(decim*10,column)
	def abs(self,columns:Iterable[int]=[]):
		"""Makes every value on specified column absolute value.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:abs(x),columns)
	def oppositeSign(self,columns=[]):
		"""Makes every value on specified column reversed sign.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:-x,columns)
	def increase(self,amount=1,columns=[]):
		"""Increases every value on specified columns by the specified amount.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x+amount,columns)
	def decrease(self,amount=1,columns=[]):
		"""Decreases every value on specified columns by the specified amount.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x-amount,columns)
	def multiply(self,amount=1,columns=[]):
		"""Multiplies every value on specified columns by the specified amount.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x*amount,columns)
	def divide(self,amount=1,columns=[]):
		"""Divides every value on specified columns by the specified amount.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x/amount,columns)
	def floorDivide(self,amount=1,columns=[]):
		"""Floor divides every value on specified columns by the specified amount.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x//amount,columns)
	def modulus(self,amount=1,columns=[]):
		"""Gives modulus values of every value on specified columns.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:x%amount,columns)
	def power(self,amount=1,columns=[]):
		"""Gives power value of every value on specified columns by the specified amount.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:pow(x,amount),columns)
	def round(self,ndigits=1,columns=[]):
		"""Gives round value of every value on specified columns.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:round(x,ndigits),columns)
	def sum(self,axis=0):
		"""Returns a tuple with all sums of specified axis.

None values will accept as 0."""
		data=self.clone()
		if axis in ["x",1]: pass
		elif axis in ["y",0]: data.transpose()
		else: raise ValueError("Axis must be 'x', 1 or 'y', 0")
		result = [sum(0 if cell is None else cell for cell in row) for row in data]
		return tuple(result)
	def summary(self,column):
		"""Returns a string data that shows minimum, 1st quarter, median, 3rd quarter, maximum and mean values of specified column."""
		return f"""*** Column {column} ***
Minimum\t\t: {self.min(column)}
1st Quarter\t: {self.quartiles(column)[0]}
Median\t\t: {self.median(column)}
3rd Quarter\t: {self.quartiles(column)[1]}
Maximum\t\t: {self.max(column)}
Mean \t\t: {self.mean(column)}"""
	def summaries(self,*columns):
		"""Summary method for seeing more than one column at the same time. Leave arguments blank to get all columns."""
		if not columns: columns=self.allColumns
		result = "".join(f"""\n*** {name} ***
Minimum\t\t: {self.min(column)}
1st Quarter\t: {self.quartiles(column)[0]}
Median\t\t: {self.median(column)}
2ns Quarter\t: {self.quartiles(column)[1]}
Maximum\t\t: {self.max(column)}
Mean \t\t: {self.mean(column)}""" for column, name in enumerate(self.columns))

		return result.replace("\n","",1)
class StrBase(__SubBase__):
	def __repr__(self): return f"<StrBase with {len(self)} row"+("s" if len(self)>1 else "")+">" if len(self) else "<StrBase with no content>"
	def __convert__(self,input_):
		try:
			return None if input_ is None else str(input_).strip()
		except: return None
	def compare(self,With:str,operator:str,byColumn:int):
		"""Compare strings by ascii values.

Operator must be <, <=, ==, !=, >= or >."""
		if not len(self):
			return self
		if operator not in {"<", "<=", "==", "!=", ">=", ">"}:
			raise ValueError("Operator must be <, <=, ==, !=, >= or >.")
		With = With
		for _ in self.getColumn(byColumn):
			exec(f"if cell {operator} With: result.append(self[index])")
		result = []
		final=type(self)(*result)
		final._axisnames=self._axisnames
		final._axisbackup=self._axisbackup
		return final
class FloatBase(__NumBase__):
	def __repr__(self): return f"<FloatBase with {len(self)} row"+("s" if len(self)>1 else "")+">" if len(self) else "<FloatBase with no content>"
	def __convert__(self,input_):
		try: return (((float(input_) if input_!="e" else e) if input_!="-e" else -e) if input_!="pi" else pi) if input_!="-pi" else -pi
		except: return None
	def floor(self,columns=[]):
		"""Gives floor value of every value on specified columns by the specified amount.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:int(x),columns)
	def ceil(self,columns=[]):
		"""Gives ceil value of every value on specified columns by the specified amount.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:int(x)+1 if x!=int(x) else x,columns)
	def format(self,ndigits:int=2,columns=[]):
		"""Changes digists of values on specified columns.

CAUTION! This method may cause data correction loss.

If columns parameter is [], it applies to all columns."""
		self.apply(lambda x:format(x,f".{ndigits}f"),columns)
	def print(self,ndigits:int=2,prefix:str=None,suffix:str=None,align:bool=True,countingStarts:int=0):
		"""Prints all of the data in a pretty looking table.

Disabling alignment may be faster but uglier for big databases."""
		if ndigits<1: ndigits=2
		if prefix!=None:
			print(prefix, end="")
		if align:
			lencol = [max(len(max(("None" if i is None else "inf" if i == inf else "-inf" if i == -inf else f"{int(i)}." + "0" * ndigits for i in self.getColumn(col)), key=len)), len(self.columns[col])) for col in range(self.columnCount)]

		lendigit=len(str(len(self)+countingStarts))
		print(self.__repr__()+"\nItems = [")
		if len(self):
			if align:
				print(" * [ ".rjust(lendigit+4), end="")
				for data,lc in zip(self.columns,lencol):
					print(f"{data}".center(lc),end="" if data==self.columns[-1] else " | ")
				print(" ]")
				for n,row in enumerate(self):
					print(f" {n+countingStarts} [ ".rjust(lendigit+4),end="")
					base=[(self.__convert__(format(j,f".{ndigits}f").rjust(lc)) if len(str(j).split(".")[1])>=ndigits else str(j).split(".")[0]+"."+str(j).split(".")[1].ljust(ndigits,"0")) if "." in str(j) else j for j in row]
					for data,lc,n in zip(base,lencol,range(self.columnCount)):
						print(str(data).rjust(lc),end=" " if n==self.columnCount-1 else " | ")
					print("]")
			else:
				print(" *".rjust(lendigit+1)+" [ "+", ".join(self.columns)+" ]")
				for n,row in enumerate(self):
					print(f" {n+countingStarts} [ ".rjust(lendigit+4),end="")
					base=[(self.__convert__(format(j,f".{ndigits}f")) if len(str(j).split(".")[1])>=ndigits else str(j).split(".")[0]+"."+str(j).split(".")[1].ljust(ndigits,"0")) if "." in str(j) else j for j in row]
					for data in base:
						print(data, end=" " if data==base[-1] else ", ")
					print("]")
		if suffix!=None:
			print(f"] {suffix}")
		else: print("]")
	def head(self,ndigits:int=2,count:int=5,prefix:str="",suffix:str="",align:bool=True,countingStarts:int=0):
		"""Prints first n rows in a table."""
		type(self)(*self[:count],colNames=self.columns).print(ndigits,prefix,suffix,align,countingStarts)
	def tail(self,ndigits:int=2,count:int=5,prefix:str="",suffix:str="",align:bool=True,countingStarts:int=0):
		"""Prints last n rows in a table."""
		type(self)(*self[-count:],colNames=self.columns).print(ndigits,prefix,suffix,align,countingStarts+len(self)-count)
	def section(self,ndigits:int=2,start:int=0,end:int=0,prefix:str="",suffix:str="",align:bool=True,countingStarts:int=0):
		"""Prints rows between start and stop values in a table. End point includes."""
		type(self)(*self[start:end+1],colNames=self.columns).print(ndigits,prefix,suffix,align,countingStarts+start)

class IntBase(__NumBase__):
	def __repr__(self): return f"<IntBase with {len(self)} row"+("s" if len(self)>1 else "")+">" if len(self) else "<IntBase with no content>"
	def __convert__(self,input_):
		try: return (((((((((int(input_) if input_!=-inf else -inf) if input_!=inf else inf) if input_!="inf" else inf) if input_!="-inf" else -inf) if input_!="e" else 3) if input_!="-e" else -3) if input_!=e else 3) if input_!=-e else -3) if input_!="pi" else 3) if input_!="-pi" else -3
		except: return None

def saveDB(obj,filename):
	"""This function can be use to store any type of object."""
	with open(filename,"wb") as outp: dump(obj,outp,5)
def loadDB(filename):
	"""This function can be use to restore any type of object."""
	with open(filename,"rb") as inp:
		return load(inp)
def saveSecure(obj,filename):
	"""This function can be use to store any type of object in encoded format."""
	with open(filename,"w") as outp: outp.write(b64encode(dumps(obj,5)).decode())
def saveToString(obj) -> str:
	"""Returns a string to store any type of object in encoded format."""
	return b64encode(dumps(obj,5)).decode()
def loadSecure(filename):
	"""This function can be use to restore any type of encoded object."""
	with open(filename,"r") as inp:
		return loads(b64decode(inp.read()))
