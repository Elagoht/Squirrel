# Change Log

## v0.0.0 "Begining"

* All basic features added

## v0.0.1 "Math Prof"

* Operator sign error fixed.
* Empty database errors fixed.
* Apply method fixed. Now it automatically fills nulls with None and leaving None values same.
* Compare method added to all Database types. Strings are sorting by ascii values.
* Percentile method added.
* Summary and summaries methods added.
 
## v0.0.2 "Manipulator"

* Column names added and optimized for methods such as transpose, rotate.
* Save and load functions added to use this module like a read database.
* Truncate method added. 
* Clone method updated for column name feature.

## v0.0.3 "Seek and Sort"

* Sorting by key method added.
* Unused modules removed.
* Saving CSVs now support column name exports.
* Integers on ValueBase are now not converted to float.
* Query method now supports case sensitivity for exact and nonexact both.
* Fetch and fetchOne methods added alongside query, they returns list instead of Squirrel object.
* FetchX and FetchXOne methods added alongside queries, same thing as above.
* Section method added to print specific rows in database.

## v0.1 "Special Delivery"

* Visual improvements on print, head, tail, section methods.
* Now that methods print row numbers.
* You can determine where counting will start while table creation.
* Alignment parameter added methods above to get prettier or faster display.
* Versions now have a name instead of only numbers.
* Every single method now have documentation.
* Sum method fixed. None values now accepted as 0.
* Summaries method now shows column names instead of column index.
* Column names for databases with null values creation fixed.
* Column names duplication error fixed. Now they must be unique.
* StrBase now not takes None as "None".
* Creating databases from existing ones columns is possible now.
* You can do the same thing by specifying column range.
