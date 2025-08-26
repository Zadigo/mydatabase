# Frontend Application

Created with Nuxt 4, this application provides the main interface for helping users create a database
with any CSV file in a user-friendly design and powerful features.

Since it becomes possible to transform your files into a database, you can then use it as a backend for your own application,
as datasource for external Api calls or simply to display the in a more convinient way for colleagues.

## Features ✨

- Import and export CSV files
- Create and manage databases
- Define relationships between tables
- Query data using a powerful query language

## Structure 🌳

The Google/Excel sheets or CSV files are organised under a database. A database is a collection of related 
files that can be easily managed and manipulated as you would with a normal database.

Each database can contain multiple tables, and each table can have its own set of fields and records.
A table is just a different name for Google/Excel sheets and CSV files.

### tables 📁

There are three sorts of tables in a database:

* __Data Table__: This is where the actual data is stored. Each row represents a single record, and each column represents a field within that record.
* __Graph Table__: This table is used to store data in a graph format, allowing for more complex relationships between records.

### Foreign Keys 🔑

Contrarily to traditional CSV or Json files, where is no real relationship between the data entries, 
this application us logically link multiple files between them and query their data as if they were one. It becomes therefore possible to
create relationships between a CSV file and another one, just like in a relational database.

[!NOTE]
The files should generally contain the same amount of rows otherwise the relationships may not work as expected.
However, it is possible to create relationships between files with different number of rows, but the user should be aware that
this may lead to unexpected behavior and should be tested thoroughly.

### Triggers ⚡

Just like a traditional database, it is possible to create triggers that will be executed when a certain event occurs on your data. Generally
speaking, in traditional databases, you have nine trigger possibilities. We support the following ones:

* `before insert`
* `after insert`
* `before update`
* `after update`
* `before delete`
* `after delete`
* `before select`
* `after select`

This application allows triggers on each table individually and works at the column level.

Triggers are saved in the Django database as `column_name.before_delete.trigger_name`. Internal triggers are prefixed with `internal_`
and triggers that require HTTP requests are prefixed with `http_` for external API calls with N8N or Zapier.

Triggers are saved as comma separated values. For example, on `age` we could have triggers `before_insert,after_delete`

### Functions ⚙️

Traditional relational database also use functions to perform operations on the data. This application allows you to create functions that can be used
in your queries. Here is the list of built-in functions that are found on any database:

* Aggregate Functions
    - `COUNT`: Returns the number of rows that match a specified criterion.
    - `SUM`: Returns the total sum of a numeric column.
    - `AVG`: Returns the average value of a numeric column.
    - `MIN`: Returns the smallest value of the selected column.
    - `MAX`: Returns the largest value of the selected column.

* String Functions:
    - `UPPER`: Converts a string to uppercase.
    - `LOWER`: Converts a string to lowercase.
    - `LENGTH`: Returns the length of a string.
    - `TRIM`: Removes whitespace from both ends of a string.
    - `GROUP_CONCAT`: Returns a concatenated string of non-null values from a group.
    - `COALESCE`: Returns the first non-null value in a list of arguments.
    - `EXTRACT`: Retrieves subparts from a date/time value.

* Date Functions:
    - `NOW`: Returns the current date and time.
    - `DATE`: Returns the date part of a date/time expression.
    - `TIME`: Returns the time part of a date/time expression.
    - `DATETIME`: Returns the date and time part of a date/time expression.
    - `STRFTIME`: Formats a date/time value as a string.
    - `CURRENT_TIMESTAMP`: Returns the current date and time.
    - `CURRENT_DATE`: Returns the current date.
    - `CURRENT_TIME`: Returns the current time.

* Miscellaneous Functions:
    - `RANDOM`: Returns a random value.
    - `MD5`: Returns the MD5 hash of a string.
    - `SHA256`: Returns the SHA256 hash of a string.
    - `SHA512`: Returns the SHA512 hash of a string.
    - `BLAKE2B`: Returns the BLAKE2B hash of a string.
    - `BLAKE3`: Returns the BLAKE3 hash of a string.

The functions to apply on a column are saved in the Django database as `column_name.function_name`. For example, on a column
called `firstname` on which we want to apply an `UPPER` function, we would save it as `firstname.upper`.


### Constraints 🔒

You can force a column to respect a certain format or condition by applying checks and constraints on it.

For instance if we need a column age to always be between 18 and 25 then it will saved in the database as `age.between(18,25)`. Other examples
include:

* `age.greater_than(18)`
* `age.greater_than_equal(18)`
* `age.less_than(18,25)`
* `age.less_than_equal(18,25)`
* `email.unique()`
* `name.not_empty()`


### Windows or conditionals 🔲

Finally, windows are just sections of the document that are cached in memory for faster access. 
They allow you to define a specific range of rows to operate on, rather than the entire dataset. This can greatly improve 
performance for certain types of queries for the end user.

Here are some example of a window logic saved in the database: `window.if(age.greater_than(18)).and(age.less_than(25))`. Some other examples include:

* `window.if(email.unique())`
* `window.if(name.not_empty())`

Windows conditions can be negated: `window.ifnot(<condition>)` or `window.if(<condition>).andnot(<condition>)`.

A window can also be used to display conditional data based on a condition for example consider
`window.if(age.greater_than(18)).and(age.less_than(25)).then(22)`. What will happen is that if the age is between 18 and 25, 
then the value 22 will be displayed instead of the actual age.

[!NOTE]

Windows are not the same as traditional SQL window functions. They are a way to define a specific context for your queries, 
but they do not change the underlying data or how it is stored.

Here is the list of all window functions:

* `window.if()` and `window.ifnot()`: starts a conditional window
* `.then(<value>)`: specifies the value to return if the condition is met
* `.and(<condition>)` or `.andnot(<condition>)`: attaches an additional condition to the window
* `.or(<condition>)` or `.ornot(<condition>)`: attaches an alternative condition to the window

Comparators are:

* `<column_name>.greater_than(<value>)`: checks if the column is greater than a value
* `<column_name>.greater_than_equal(<value>)`: checks if the column is greater than or equal to a value
* `<column_name>.less_than(<value>)`: checks if the column is less than a value
* `<column_name>.less_than_equal(<value>)`: checks if the column is less than or equal to a value
* `<column_name>.equal(<value>)`: checks if the column is equal to a value
* `<column_name>.not_equal(<value>)`: checks if the column is not equal to a value
* `<column_name>.is_null()`: checks if the column is null
* `<column_name>.is_not_null()`: checks if the column is not null
* `<column_name>.is_empty()`: checks if the column is empty
* `<column_name>.is_not_empty()`: checks if the column is not empty
* `<column_name>.is_blank()`: checks if the column is blank (empty or whitespace)
* `<column_name>.in()`: checks if the column is in a list of values
* `<column_name>.not_in()`: checks if the column is not in a list of values
* `<column_name>.between(<value1>,<value2>)`: checks if the column is between two values
* `<column_name>.not_between(<value1>,<value2>)`: checks if the column is not between two values
