# Change Log

## v0.0.0

* All basic features added

## v0.0.1

* Operator sign error fixed.
* Empty database errors fixed.
* Apply method fixed. Now it automatically fills nulls with None and leaving None values same.
* Compare method added to all Database types. Strings are sorting by ascii values.
* Percentile method added.
* Summary and summaries methods added.
 
## v0.0.2

* Column names added and optimized for methods such as transpose, rotate.
* Save and load functions added to use this module like a read database.
* Truncate method added. 
* Clone method updated for column name feature.

## v0.0.3

* Sorting by key method added.
* Unused modules removed.
* Saving CSVs now support column name exports.
* Integers on ValueBase are now not converted to float.
* Query method now supports case sensitivity for exact and nonexact both.
* Fetch and fetchOne methods added alongside query, they returns list instead of Squirrel object.
* FetchX and FetchXOne methods added alongside queries, same thing as above.