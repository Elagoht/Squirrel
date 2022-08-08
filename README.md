# Squirrel Module

## Table of Content

1. [Introduction](#0)
1. [Installation](#1)
1. [Setting Up](#2)
1. [Documentary](#3)
1. [Feature List](#4)
1. [Examples](#5)

<h2 id="0">Introduction</h2>

Squirrel is the best way to work with 2 dimensional lists. It is a lightweight alternative for pandas. Pandas is a fully functional module that supports lots of data visualisation module. But, if you want to use pandas in your project and if you planning to publish your project as an executable file, pandas needs lots of disk space. I realized it when I finished one of my project and I was proud of myself... So I had to reprogram it, with my own module. Also Squirrel can be used as a database module.

You can still use squirrel instead of pandas on your data science projects if you want to reduce the app file size.

<h2 id="1">Installation</h2>

Fow now, before I upload it to PyPi, you can download squirrel.py and move to your workspace and import with command below in the [Setting Up](#2) section.

<h2 id="2">Setting Up</h2>

Write the command below to import squirrel in your worksheet.

```py
import squirrel as sq
from squirrel import inf,pi,e
```

<h2 id="3">Documentary</h2>

There is 4 basic data storage class. All of them supports 2 dimensional list methods. They are:

* ValueBase
* StrBase
* FloatBase
* IntBase

> ValueBase determines which data type entered itself.

> StrBase automatically converts entered data to string.

> FloatBase automatically converts entered data to float, pi, e or infinite.

> IntBase automatically converts entered data to to integer or infinite.

If any data cannot convert to specified data type, it returns _**None**_.

IntBase, FloatBase, StrBase classes inherits ValueBase class's features.

IntBase and FloatBase classes has more methods than other classes. That methods provides lots of math function.

<h2 id="4">Feature List</h2>

### Features
#### Basic Features

|         Feature          |                     Example                    |
| ------------------------ | ---------------------------------------------- |
| getitem, setitem         | Allows you get and set specified row.          |
| add                      | Adds a row.                                    |
| remove                   | Removes a single cell in a row.                |
| removeRow                | Removes a whole row.                           |
| addMany                  | Adds multiple row in a time.                   |
| indexof                  | Finds index number of a given row.             |
| sort                     | Sorts data by specified column.                |
| replace                  | Replaces old values with new specified amount. |
| fillNull                 | Fills null places with None.                   |
| fillNone                 | Fills None (and nulls) with specified value.   |
| csv support              | Able to read, add and write csv files.         |
| data                     | Returns a copy of data as 2D lists.            |
| apply                    | Apply a function that return new values.       |
| applyMany                | Apply more functions at the same time.         |
| allColumns               | Returns a range object zero to column count.   |
| print                    | Prints all data in database as pretty display. |
| head                     | Prints first nth data.                         |
| tail                     | Prints last nth data.                          |
| section                  | Prints specified section of data.              |
| columns                  | Returns all column names in a list.            |
| allColumns               | Returns a range object for all columns.        |
| c                        | Returns integer value of column.               |
| renameColumns            | Renames columns.                               |
| range                    | Returns a range object by taking column names. |

#### Math Features

|         Feature          |                     Example                    |
| ------------------------ | ---------------------------------------------- |
| inf, pi, e               | Yess infinite pie!                             |
| None for NA              | None value used for NA.                        |
| median                   | Returns median value of specified column.      |
| mean                     | Returns mean value of specified column.        |
| mod                      | Returns mode values of specified column.       |
| min                      | Returns min value of specified column.         |
| max                      | Returns max value of specified column.         |
| quartiles                | Returns 1st, 3rt quartile of specified column. |
| abs                      | Converts values their absolute value.          |
| oppositeSign             | Multiply values on specified columns with -1.  |
| increase                 | Increases all values on specified column.      |
| decrease                 | Decreases all values on specified column.      |
| multiply                 | Multiplies all values on specified column.     |
| divide                   | Divides all values on specified column.        |
| floorDivide              | Floor divides all values on specified column.  |
| modulus                  | Moduluses all values on specified column.      |
| sum                      | Returns sums of all values on specified axis.  |
| compare                  | Compares values and applies a query by math.   |
| compareMany              | Applies more than one compare.                 |


#### Some Useful Features

|         Feature          |                     Example                    |
| ------------------------ | ---------------------------------------------- |
| transpose                | Transposes rows and columns.                   |
| mirror                   | Flips the database on the y-axis.              |
| flip                     | flips the database on the x-axis.              |
| rotate                   | Rotates database 90, 180 and 270 degrees.      |
| removeDuplicates         | Removes duplicate rows from database.          |
| swap                     | Swaps two instances' positions.                |
| swapRow                  | Swaps two rows' positions.                     |
| moveUp                   | Swaps item with upper one.                     |
| moveDown                 | Swaps item with lower one.                     |
| moveLeft                 | Swaps item with item on the left.              |
| moveRight                | Swaps item with item on the right.             |

#### Working With More Than One Database

|         Feature          |                     Example                    |
| ------------------------ | ---------------------------------------------- |
| merge                    | Merges two database.                           |
| split                    | Returns same type of databases in a tuple.     |

#### DataBase Features

|         Feature          |                     Example                    |
| ------------------------ | ---------------------------------------------- |
| count                    | Counts specified value.                        |
| query                    | Searchs values matched with quert string.      |
| multiple query           | Applies multiple queries.                      |
| election                 | Just keep query results.                       |
| multiple election        | Just keep multiple query result.               |
| fetch                    | Gives search result as list objects.           |
| fetch one                | Gives the first search result as list object.  |  
| fetch by multi query     | Gives multiple filter results as list objects. |  
| fetch one by multi query | Gives multiple filter results as list objects. |  
| clone                    | Gives a copy of database                       |
| cloneFromColumns         | Gives specified columns of database.           |
| cloneFromColumnRange     | Gives specified column range of database.      |
| truncate                 | Empties database.                              |
| saveDB                   | Saves database to a .sqr file.                 |
| loadDB                   | Loads a database from a .sqr file.             |
| saveSecure               | Saves database as base64 encrypted .sqs file.  |
| loadSecure               | Loads a database from a .sqs file.             |

<h2 id="5">Examples</h2>

### ValueBase for Examples

```py
db=sq.ValueBase(
    ["Elagoht",17],    # Any type of iterable will be accepted.
    {"Furkan":0,21:0}, # Dictionaries only gives keys.
    ("Baytekin","1"),  
    {10,20})           # Using sets does not make sense if you work with numeric and string values in same column.
db.print()

# Output
<ValueBase with 4 rows>
Items = [
 * [  Column 0  | Column 1 ]
 0 [ "Elagoht"  | 17       ]
 1 [ "Furkan"   | 21       ]
 2 [ "Baytekin" | "1"      ]
 3 [ 10         | 20       ]
]
```

### RenameColumns -> None

```py
db.renameColumns("Name","ID")
db.print()

# Output
<ValueBase with 4 rows>
Items = [
 * [    Name    |  ID ]
 0 [ "Elagoht"  | 17  ]
 1 [ "Furkan"   | 21  ]
 2 [ "Baytekin" | "1" ]
 3 [ 10         | 20  ]
]

# First column shows column names and it has stars to be separated from others.
```

### C -> Int

```py
print(db.c("Name"))

# Output 
0 

# Returns integer value of column. Works like "enumerate" item.
```

### Query -> Valuebase | StrBase | IntBase | FloatBase

```py
search=db.query("2",False,[db.c("ID")]) # This means search for "2" on only ID column.
search.print() # Query method returns a database, so you can use database methods to result object.

# Output
<ValueBase with 2 rows>
Items = [
 * [   Name   | ID ]
 0 [ "Furkan" | 21 ]
 1 [ 10       | 20 ]
]
```

### Fetch -> List

```py
search=db.fetch("2",False,[db.c("ID")]) # Same query parameters with above.
print(search) # Fetch method returns a list that contains lists.

# Output
[['Furkan', 21], [10, 20]]
```

### Remove -> None

```py    
search=db.query("2",False,[0,1]) # This gives 2 entries.
db-=search[1] # Removes the 2nd one.
db.print()

# Output
<ValueBase with 3 rows>
Items = [
 * [    Name    |  ID ]
 0 [ "Elagoht"  | 17  ]
 1 [ "Furkan"   | 21  ]
 2 [ "Baytekin" | "1" ]
]
```

### IndexOf -> int

```py
print(db.indexof(
    db.query("2",False,db.range("Name","ID"))[0]
    # Given row must be exact, so you can use query and indices.
    # range method returned range(0,1) object which Name=0 ID=1.
))

# Output
1
```

### Sort -> None

```py
db.sort(0)
db.print("Hello this is a prefix string: ","Hello, this is a suffix string.")

# Output
Hello this is a prefix string: <ValueBase with 3 rows>
Items = [
 * [    Name    |  ID ]
 0 [ "Baytekin" | "1" ]
 1 [ "Elagoht"  | 17  ]
 2 [ "Furkan"   | 21  ]
] Hello, this is a suffix string.
```

### Mirror -> None | Valuebase | StrBase | IntBase | FloatBase

```py
db.mirror()
db.print()

#Output
<ValueBase with 3 rows>
Items = [
 * [  ID |    Name    ]
 0 [ 17  | "Elagoht"  ]
 1 [ 21  | "Furkan"   ]
 2 [ "1" | "Baytekin" ]
]
```

### Flip -> None | Valuebase | StrBase | IntBase | FloatBase

```py
db.flip()
db.print()

#Output
<ValueBase with 3 rows>
Items = [
 * [  ID |    Name    ]
 0 [ "1" | "Baytekin" ]
 1 [ 21  | "Furkan"   ]
 2 [ 17  | "Elagoht"  ]
]
```
### Rotate -> None | Valuebase | StrBase | IntBase | FloatBase

```py
db.rotate(-1)
db.renameColumns("Column","Names","Changed")
db.print()

#Output
<ValueBase with 2 rows>
Items = [
 * [   Column   |  Names   |  Changed  ]
 0 [ "Baytekin" | "Furkan" | "Elagoht" ]
 1 [ "1"        | 21       | 17        ]
]
```

### Transpose -> None | Valuebase | StrBase | IntBase | FloatBase

```py
db.transpose()
db.print()

#Output
<ValueBase with 3 rows>
Items = [
 * [     ID     | Name ]
 0 [ "Baytekin" | "1"  ]
 1 [ "Furkan"   | 21   ]
 2 [ "Elagoht"  | 17   ]
]
```

### Example IntBase

```py
db=sq.IntBase([1,2,pi],colNames=["First","Second","Third"]) # Instead of renameColumns, we used colNames parameter to name columns.
db+=(2,-(-pi),4)
db+=["pi",4,5]
db.addMany([4,5,6],(5,6,7),(6,7,8),{7:0,8:1,9:2})
db.print()

#Output
<IntBase with 7 rows>
Items = [
 * [ First | Second | Third ]
 0 [ 1     | 2      | 3     ]
 1 [ 2     | 3      | 4     ]
 2 [ 3     | 4      | 5     ]
 3 [ 4     | 5      | 6     ]
 4 [ 5     | 6      | 7     ]
 5 [ 6     | 7      | 8     ]
 6 [ 7     | 8      | 9     ]
]
```

### Some of Math Methods

```py
print("Quartiles\t:",       db.quartiles(0),"\n"
      "Mean\t\t:"   ,       db.mean(1)     ,"\n"
      "Median\t\t:" ,       db.median(1)   ,"\n"
      "Modes\t\t:"  ,       db.modes(1)    ,"\n"
      "Maximum\t\t:",       db.max(1)      ,"\n"
      "Minimum\t\t:",       db.min(1)      ,"\n"
      "18th Percentile\t:", db.percentile(18,1))

#Output
Quartiles       : (2.5, 5.5)
Mean            : 5.0
Median          : 5
Modes           : (2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
Maximum         : 8.0
Minimum         : 2.0
18th Percentile : 3.08
```

### Summary -> String

```py
print(db.summary(0))

#Output
*** Column 0 ***
Minimum         : 1.0
1st Quarter     : 2.5
Median          : 4
3rd Quarter     : 5.5
Maximum         : 7.0
Mean            : 4.0
```

### Summaries -> String

```py
print(db.summaries())

#Output
*** First ***
Minimum         : 1.0
1st Quarter     : 2.5
Median          : 4
2ns Quarter     : 5.5
Maximum         : 7.0
Mean            : 4.0
*** Second ***
Minimum         : 2.0
1st Quarter     : 3.5
Median          : 5
2ns Quarter     : 6.5
Maximum         : 8.0
Mean            : 5.0
*** Third ***
Minimum         : 3.0
1st Quarter     : 4.5
Median          : 6
2ns Quarter     : 7.5
Maximum         : 9.0
Mean            : 6.0
```

### Change DataBase Type

```py
db=db.changeType(sq.FloatBase)
db.increase(.2)
db.print()

#Output
<FloatBase with 7 rows>
Items = [
 * [ First | Second | Third ]
 0 [  1.20 |   2.20 |  3.20 ]
 1 [  2.20 |   3.20 |  4.20 ]
 2 [  3.20 |   4.20 |  5.20 ]
 3 [  4.20 |   5.20 |  6.20 ]
 4 [  5.20 |   6.20 |  7.20 ]
 5 [  6.20 |   7.20 |  8.20 ]
 6 [  7.20 |   8.20 |  9.20 ]
]
```

### Split -> Tuple(Valuebase | StrBase | IntBase | FloatBase, Valuebase | StrBase | IntBase | FloatBase)

```py
db0,db1=db.split(5)

db0.print(2,"","I am the first part.")
db1.print(2,"","I am the last part.")

#Output
<FloatBase with 5 rows>
Items = [
 * [ First | Second | Third ]
 0 [  1.20 |   2.20 |  3.20 ]
 1 [  2.20 |   3.20 |  4.20 ]
 2 [  3.20 |   4.20 |  5.20 ]
 3 [  4.20 |   5.20 |  6.20 ]
 4 [  5.20 |   6.20 |  7.20 ]
] I am the first part.
<FloatBase with 2 rows>
Items = [
 * [ First | Second | Third ]
 0 [  6.20 |   7.20 |  8.20 ]
 1 [  7.20 |   8.20 |  9.20 ]
] I am the last part.
```

### Compare -> IntBase | FloatBase

```py
db.compare(5,"<=",0).print()
# Get rows that are less than/equal to 5 in the first column.

#Output
<FloatBase with 4 rows>
Items = [
 * [ First | Second | Third ]
 0 [  1.20 |   2.20 |  3.20 ]
 1 [  2.20 |   3.20 |  4.20 ]
 2 [  3.20 |   4.20 |  5.20 ]
 3 [  4.20 |   5.20 |  6.20 ]
]
```

### CompareMany -> IntBase | FloatBase

```py
db.compareMany([7,1,4],("<=",">","!="),(0,0,0)).print()
# Get rows that are less than/equal to 7 in the first row, more than 1 in the second row, and not equal to 4 in the third row.

#Output
<FloatBase with 6 rows>
Items = [
 * [ First | Second | Third ]
 0 [  1.20 |   2.20 |  3.20 ]
 1 [  2.20 |   3.20 |  4.20 ]
 2 [  3.20 |   4.20 |  5.20 ]
 3 [  4.20 |   5.20 |  6.20 ]
 4 [  5.20 |   6.20 |  7.20 ]
 5 [  6.20 |   7.20 |  8.20 ]
]
```

### Apply -> None

```py
db.apply(lambda x:pow(x,2) if x%2 else -x,[])

# Empty list for applying all columns. Simply doing not fill this parameter doas same.

# It means if the value is odd, take square, else multiply with minus one.
db.print()

#Output
<FloatBase with 7 rows>
Items = [
 * [ First | Second | Third ]
 0 [  1.44 |   4.84 | 10.24 ]
 1 [  4.84 |  10.24 | 17.64 ]
 2 [ 10.24 |  17.64 | 27.04 ]
 3 [ 17.64 |  27.04 | 38.44 ]
 4 [ 27.04 |  38.44 | 51.84 ]
 5 [ 38.44 |  51.84 | 67.24 ]
 6 [ 51.84 |  67.24 | 84.64 ]
]
```

### Determine if a row in Database. -> Bool

```py
print(
    [1.44, 4.840000000000001, 10.240000000000002] in db, # This is a float problem does in all programming languages.
    [1,+2,3] in db,
sep="\n")

#Output
True
False
```

### Example IntBase for Missing Values

```py
db=sq.IntBase((1,2,3),colNames=["These","Are","Columns"])
db+=3,
db+=4,5
db+=6,2,1

db.print()

#Output
<IntBase with 4 rows>
Items = [
 * [ These | Are  | Columns ]
 0 [ 1     | 2    | 3       ]
 1 [ 3     | ]
 2 [ 4     | 5    | ]
 3 [ 6     | 2    | 1       ]
]
```

Row 1 ends in 1st column and row 2 ends in 2nd column because there are null data.

### FillNull -> None

```py
db.fillNull()
db.print()

#Output
<IntBase with 4 rows>
Items = [
 * [ These | Are  | Columns ]
 0 [ 1     | 2    | 3       ]
 1 [ 3     | None | None    ]
 2 [ 4     | 5    | None    ]
 3 [ 6     | 2    | 1       ]
]
```

### FillNone -> None

```py
db.fillNone(-1)
db.print()

#Output
<IntBase with 4 rows>
Items = [
 * [ These | Are | Columns ]
 0 [ 1     | 2   | 3       ]
 1 [ 3     | -1  | -1      ]
 2 [ 4     | 5   | -1      ]
 3 [ 6     | 2   | 1       ]
]
```

Replaced all None values with -1.

### CloneFromColumns -> Valuebase | StrBase | IntBase | FloatBase

```py
db.cloneFromColumns(0,db.c("Columns")).print()

#Output
<IntBase with 4 rows>
Items = [
 * [ These | Columns ]
 0 [ 1     | 3       ]
 1 [ 3     | -1      ]
 2 [ 4     | -1      ]
 3 [ 6     | 1       ]
]
```

### CloneFromColumnRange -> Valuebase | StrBase | IntBase | FloatBase

```py
db.cloneFromColumnRange(1,db.c("Columns")).print()

#Output
<IntBase with 4 rows>
Items = [
 * [ Are | Columns ]
 0 [ 2   | 3       ]
 1 [ -1  | -1      ]
 2 [ 5   | -1      ]
 3 [ 2   | 1       ]
]
```
