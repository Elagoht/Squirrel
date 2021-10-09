# Squirrel Module

![Squirrel Logo](https://raw.githubusercontent.com/Elagoht/Squirrel/main/squirrel.png)

## Table of Content

1. [Introduction](#0)
1. [Installation](#1)
2. [Setting Up](#2)
2. [Documentary](#3)
2. [Feature List](#4)
2. [Examples](#5)

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

|         Feature         |                     Example                    |
| ----------------------- | ---------------------------------------------- |
| getitem, setitem        | Allows you get and set specified row.          |
| add                     | Adds a row.                                    |
| remove                  | Removes a row.                                 |
| addMany                 | Adds multiple row in a time.                   |
| indexof                 | Finds index number of a given row.             |
| sort                    | Sorts data by specified column.                |
| replace                 | Replaces old values with new specified amount. |
| fillNull                | Fills null places with None.                   |
| fillNone                | Fills None (and nulls) with specified value.   |
| csv support             | Able to read, add and write csv files.         |
| data                    | Returns a copy of data as 2D lists.            |
| apply                   | Apply a function that return new values.       |
| applyMany               | Apply more functions at the same time.         |
| allColumns              | Returns a range object zero to column count.   |
| print                   | Prints all data in database as pretty display. |
| head                    | Prints first nth data as pretty display.       |
| tail                    | Prints last nth data as pretty display.        |
| columns                 | Returns all column names in a list.            |
| allColumns              | Returns a range object for all columns.        |
| c                       | Returns integer value of column.               |
| renameColumns           | Renames columns.                               |
| range                   | Returns a range object by taking column names. |

#### Math Features

|         Feature         |                     Example                    |
| ----------------------- | ---------------------------------------------- |
| inf, pi, e              | Yess infinite pie!                             |
| None for NA             | None value used for NA.                        |
| median                  | Returns median value of specified column.      |
| mean                    | Returns mean value of specified column.        |
| mod                     | Returns mode values of specified column.       |
| min                     | Returns min value of specified column.         |
| max                     | Returns max value of specified column.         |
| quartiles               | Returns 1st, 3rt quartile of specified column. |
| abs                     | Converts values their absolute value.          |
| oppositeSign            | Multiply values on specified columns with -1.  |
| increase                | Increases all values on specified column.      |
| decrease                | Decreases all values on specified column.      |
| multiply                | Multiplies all values on specified column.     |
| divide                  | Divides all values on specified column.        |
| floorDivide             | Floor divides all values on specified column.  |
| modulus                 | Moduluses all values on specified column.      |
| sum                     | Returns sums of all values on specified axis.  |
| compare                 | Compares values and applies a querry by math.  |
| compareMany             | Applies more than one compare.                 |


#### Some Useful Features

|         Feature         |                     Example                    |
| ----------------------- | ---------------------------------------------- |
| count                   | Counts specified value.                        |
| query                   | Searchs values matched with quert string.      |
| multiple query          | Applies multiple queries.                      |
| transpose               | Transposes rows and columns.                   |
| mirror                  | Flips the database on the y-axis.              |
| flip                    | flips the database on the x-axis.              |
| rotate                  | Rotates database 90, 180 and 270 degrees.      |
| removeDuplicates        | Removes duplicate rows from database.          |

#### Working With More Than One Database

|         Feature         |                     Example                    |
| ----------------------- | ---------------------------------------------- |
| merge                   | Merges two database.                           |
| split                   | Returns same type of databases in a tuple.     |

#### DataBase Features

|         Feature         |                     Example                    |
| ----------------------- | ---------------------------------------------- |
| clone                   | Gives a copy of database                       |
| truncate                | Empties database.                              |
| saveDB                  | Saves database to a .sqr file.                 |
| loadDB                  | Loads a database from a .sqr file.             |
| saveSecure              | Saves database as base64 encrypted .sqs file.  |
| loadSecure              | Loads a database from a .sqs file.             |


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
Items=[
*['Column 0', 'Column 1']*
 ['Elagoht', 17]
 ['Furkan', 21]
 ['Baytekin', '1']
 [10, 20]
]
```

### RenameColumns -> None

```py
db.renameColumns("Name","ID")
db.print()

# Output
<ValueBase with 4 rows>
Items=[
*['Name', 'ID']*    
 ['Elagoht', 17]
 ['Furkan', 21]
 ['Baytekin', '1']
 [10, 20]
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
Items=[
*['Name', 'ID']*
 ['Furkan', 21]
 [10, 20]
]
```

### Remove -> None

```py    
search=db.query("2",False,[0,1]) # This gives 2 entries.
db-=search[1] # Removes the 2nd one.
db.print()

# Output
<ValueBase with 3 rows>
Items=[
*['Name', 'ID']*
 ['Elagoht', 17]
 ['Furkan', 21]
 ['Baytekin', '1']
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
Hello this is a prefix string: <ValueBase with 4 rows>
Items=[
*['Name', 'ID']*
 ['Baytekin', '1']
 ['Elagoht', 17]
 ['Furkan', 21]
] Hello, this is a suffix string.
```

### Mirror -> None | Valuebase | StrBase | IntBase | FloatBase

```py
db.mirror()
db.print()

#Output
<ValueBase with 4 rows>
Items=[
*['ID', 'Name']*
 ['1', 'Baytekin']
 [17, 'Elagoht']
 [21, 'Furkan']
]
```

### Flip -> None | Valuebase | StrBase | IntBase | FloatBase

```py
db.flip()
db.print()

#Output
<ValueBase with 3 rows>
Items=[
*['ID', 'Name']*
 [21, 'Furkan']
 [17, 'Elagoht']
 ['1', 'Baytekin']
]
```
### Rotate -> None | Valuebase | StrBase | IntBase | FloatBase

```py
db.rotate(-1)
db.renameColumns("Column","Names","Changed")
db.print()

#Output
<ValueBase with 2 rows>
Items=[
*['Column', 'Names', 'Changed']* # Column names changed but other names backed up for future rotation/transposation.
 ['Furkan', 'Elagoht', 'Baytekin']
 [21, 17, '1']
]
```

### Transpose -> None | Valuebase | StrBase | IntBase | FloatBase

```py
db.transpose()
db.print()

#Output
<ValueBase with 3 rows>
Items=[
*['ID', 'Name']*
 ['Furkan', 21]
 ['Elagoht', 17]
 ['Baytekin', '1']
]
```

### Example IntBase

```py
db=sq.IntBase([1,2,pi],colNames=["First","Second","Third"]) # Instead of renameColumns, we used colNames parameter to name columns.
db+=(2,-(-pi),4)
db+=["pi",4,5]
db.addMany([4,5,6],(5,6,7),(6,7,8),{7:0,8:1,9:2})
db.print()

db.print()

#Output
<IntBase with 7 rows>
Items=[
*['First', 'Second', 'Third']*
 [1, 2, 3]
 [2, 3, 4]
 [3, 4, 5]
 [4, 5, 6]
 [5, 6, 7]
 [6, 7, 8]
 [7, 8, 9]
]
```

### Some of Math Methods

```py
db.print()
print("Quartiles\t:",       db.quartiles(0),"\n"
      "Mean\t\t:"   ,       db.mean(1)     ,"\n"
      "Median\t\t:" ,       db.median(1)   ,"\n"
      "Modes\t\t:"  ,       db.modes(1)    ,"\n"
      "Maximum\t\t:",       db.max(1)      ,"\n"
      "Minimum\t\t:",       db.min(1)      ,"\n"
      "18th Percentile\t:", db.percentile(18,1))

#Output
<IntBase with 7 rows>
Items=[
*['First', 'Second', 'Third']*
 [1, 2, 3]
 [2, 3, 4]
 [3, 4, 5]
 [4, 5, 6]
 [5, 6, 7]
 [6, 7, 8]
 [7, 8, 9]
]
Quartiles       : (2.0, 6.0) 
Mean            : 5.0 
Median          : 5 
Modes           : (2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0) 
Maximum         : 8.0 
Minimum         : 2.0
18th Percentile : 3.08
```

### Summary -> String

```py
print(db.summaries())

#Output
*** Column 0 ***
Minimum         : 1.0
1st Quarter     : 2.5
Median          : 4
2ns Quarter     : 5.5
Maximum         : 7.0
Mean            : 4.0
*** Column 1 ***
Minimum         : 2.0
1st Quarter     : 3.5
Median          : 5
2ns Quarter     : 6.5
Maximum         : 8.0
Mean            : 5.0
*** Column 2 ***
Minimum         : 3.0
1st Quarter     : 4.5
Median          : 6
2ns Quarter     : 7.5
Maximum         : 9.0
Mean            : 6.0
```

### RemoveDuplicates -> None | Valuebase | StrBase | IntBase | FloatBase

```py
db+=(2,-(-pi),4) 
# Second row added as a new row.
db.removeDuplicates(True)
db.print()

#Output
<IntBase with 7 rows>
Items=[
*['First', 'Second', 'Third']*
 [1, 2, 3]
           # Other one has deleted.
 [3, 4, 5]
 [4, 5, 6]
 [5, 6, 7]
 [6, 7, 8]
 [7, 8, 9]
 [2, 3, 4] 
           # Started from bottom and fist one has kept.
]
```

### Change DataBase Type

```py
db=sq.FloatBase(*db)
db.print()

#Output
<FloatBase with 7 rows>
Items=[
*['First', 'Second', 'Third']*
 [1.00, 2.00, 3.00]
 [2.00, 3.00, 4.00]
 [3.00, 4.00, 5.00]
 [4.00, 5.00, 6.00]
 [5.00, 6.00, 7.00]
 [6.00, 7.00, 8.00]
 [7.00, 8.00, 9.00]
]
```

### Split -> Tuple(Valuebase | StrBase | IntBase | FloatBase, Valuebase | StrBase | IntBase | FloatBase)

```py
db0,db1=db.split(5)

db0.print(2,"","I am the first part.")
db1.print(2,"","I am the last part.")

#Output
<FloatBase with 5 rows>
Items=[
*['First', 'Second', 'Third']*
 [1.00, 2.00, 3.00]
 [2.00, 3.00, 4.00]
 [3.00, 4.00, 5.00]
 [4.00, 5.00, 6.00]
 [5.00, 6.00, 7.00]
] I am the first part.
<FloatBase with 2 rows>
Items=[
*['First', 'Second', 'Third']*
 [6.00, 7.00, 8.00]
 [7.00, 8.00, 9.00]
] I am the last part.
```

### Compare -> IntBase | FloatBase

```py
db.compare(5,"<=",0).print()
# Get rows that are less than/equal to 5 in the first column.

#Output
<FloatBase with 5 rows>
Items=[
*['First', 'Second', 'Third']*
 [1.00, 2.00, 3.00]
 [2.00, 3.00, 4.00]
 [3.00, 4.00, 5.00]
 [4.00, 5.00, 6.00]
 [5.00, 6.00, 7.00]
]
```

### CompareMany -> IntBase | FloatBase

```py
db.compareMany([7,1,4],("<=",">","!="),(0,0,0)).print()
# Get rows that are less than/equal to 7 in the first row, more than 1 in the second row, and not equal to 4 in the third row.

#Output
<FloatBase with 6 rows>
Items=[
*['First', 'Second', 'Third']*
 [1.00, 2.00, 3.00]
 [3.00, 4.00, 5.00]
 [4.00, 5.00, 6.00]
 [5.00, 6.00, 7.00]
 [6.00, 7.00, 8.00]
 [7.00, 8.00, 9.00]
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
Items=[
*['First', 'Second', 'Third']*
 [1.00, -2.00, 9.00]
 [-2.00, 9.00, -4.00]
 [9.00, -4.00, 25.00]
 [-4.00, 25.00, -6.00]
 [25.00, -6.00, 49.00]
 [-6.00, 49.00, -8.00]
 [49.00, -8.00, 81.00]
]
```

### Determine if a row in Database. -> Bool

```py
print(
    [1,-2,9] in db,
    [1,+2,3] in db,
sep="\n")

#Output
True
False
```

### Example IntBase for Missing Values

```py
db=sq.IntBase((1,))
db+=3,
db+=4,5
db+=6,2,1

db.print()

#Output
<IntBase with 4 rows>
Items=[
*['Column 0', 'Column 1', 'Column 2']*
 [1]
 [3]
 [4, 5]
 [6, 2, 1]
]
```

### FillNull -> None

```py
db.fillNull()
db.print()

#Output
<IntBase with 4 rows>
Items=[
*['Column 0', 'Column 1', 'Column 2']*
 [1, None, None]
 [3, None, None]
 [4, 5, None]
 [6, 2, 1]
]
```

### FillNone -> None

```py
db.fillNone(-1)
db.print()

#Output
<IntBase with 4 rows>
Items=[
*['Column 0', 'Column 1', 'Column 2']*
 [1, -1, -1]
 [3, -1, -1]
 [4, 5, -1]
 [6, 2, 1]
]
```