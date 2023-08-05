# Python4DBI

###### In Memory Of Edson de Sousa (14/04/94 - 16/08/18), i will see you again

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [API](#api)
	* [Cursor](#cursor)
		* [Properties](#properties)
			* [row_number](#row_number)
			* [row_count](#row_count)
			* [description](#description)
		* [Methods](#methods)
			* [close](#close)
			* [prepare_statement](#prepare_statement)
			* [set_input_sizes](#set_input_sizes)
			* [set_output_size](#set_output_size)
			* [execute](#execute)
			* [fetch_one](#fetch_one)
			* [fetch_many](#fetch_many)
			* [fetch_all](#fetch_all)
			* [start_transaction](#start_transaction)
			* [cancel_transaction](#cancel_transaction)
			* [rollback](#rollback)
			* [commit](#commit)
			* [validate_transaction](#validate_transaction)
			* [send_messages_in_base_64](#send_messages_in_base_64)
			* [set_protocol_version](#set_protocol_version)
			* [set_preferred_image_types](#set_preferred_image_types)
			* [use_debug](#use_debug)
			* [set_fmt](#set_fmt)
			* [print_result](#print_result)
	* [Database Interface](#database-interface)
		* [Methods](#methods-1)
			* [connect](#connect)
			* [close](#close-1)
			* [cursor](#cursor-1)
			* [connected](#connected)
			* [get_socket](#get_socket)
			* [get_socket_timeout](#get_socket_timeout)
			* [get_host](#get_host)
			* [get_port](#get_port)
			* [get_user](#get_user)
			* [get_password](#get_password)
	* [View](#view)
		* [Methods](#methods-2)
			* [print_result](#print_result-1)
* [Example](#example)

## General info
* 4D is an incredibly productive development platform that lets you focus on your data model and your business rules.
* The 4D framework takes care of running your application code natively on macOS and Windows.
* The 4DBI is written in pure python and allows a python program to use SQL to access one or more databases from a 
single application without using the 4D ODBC driver.
* 4D and 4D Server both provide a native SQL server that enables this functionality.

## Technologies
Project is created with:
* Python
* texttable - https://github.com/foutaise/texttable/


## Setup
To run this project, install it locally using pip:

```
$ pip install python4DBI
```


## API
### Cursor

It consists of pure application logic, which interacts with the database.
It includes all the information to represent data to the end user.

#### Properties
###### row_number

		Return: int or None

This read-only attribute provides the current 0-based index of the cursor in the result set
or None if the index cannot be determined


###### row_count

		Return: int

This read-only attribute specifies the number of rows that the last .execute*()

###### description

		Return: List

A Cursor object's description attribute returns information about each of the result columns of a query.


#### Methods
###### close

		Return: None

Close the current 4D SQL server cursor

###### prepare_statement

		Params: query ( str )
		Return: int

Checks if the statement is valid should always be execute before an execute statement
returns FOURD_OK or FOURD_ERROR

###### set_input_sizes

**Not implemented!**

		Params: size ( int )
		Return: None

This can be used before a call to .execute*() to predefine memory areas for the operation's parameters.

###### set_output_size

**Not implemented!**

		Params: size ( int )
		Return: None

Set a column buffer size for fetches of large columns (e.g. LONGs, BLOBs, etc.).
the column is specified as an index into the result sequence.
Not specifying the column will set the default size for all large columns in the cursor.

###### execute

		Params: query (str), params (dict), page_size (int), on_before_execute (funtion), on_executed (funtion), *args, **kwargs
		Return: None

Prepare and execute a database operation (query or command).

###### fetch_one


		Return: List or None

Fetch the next row of a query result set, returning a single sequence, or None when no more data is available.

###### fetch_many

		Params: size (int)
		Return: Two-dimensional List or None

Fetch the next set of rows of a query result, returning a sequence of sequences (e.g. a list of tuples).
An empty sequence is returned when no more rows are available.

###### fetch_all

		Return: Two-dimensional List or None

Fetch all (remaining) rows of a query result.
Note that the cursor's array size attribute can affect the performance of this operation.


###### start_transaction

		Return: None

Opens a transaction

###### cancel_transaction

		Return: None

Rollback an open transaction
Same operation as rollback method

###### rollback

		Return: None

Rollback an open transaction
Same operation as cancel_transaction method

###### commit

		Return: None

Commits an open transaction
Same operation as validate_transaction method

###### validate_transaction

		Return: None

Commits an open transaction
Same operation as commit method

###### send_messages_in_base_64

		Params: use_b64 (bool)
		Return: None

Sets the base 64 mode

###### set_protocol_version

		Params: protocol_version (str)
		Return: None

Sets the 4D SQL server protocol version

###### set_preferred_image_types

		Params: preferred_image_types (str)
		Return: None

Sets the preferred image type
>Currently only supports 'png' pr 'jpg' formats

###### use_debug

		Params: debug (bool)
		Return: None

Sets the debug mode

###### set_fmt


		Params: fmt (str)
		Return: None
		
###### print_result

		Params: headers (List), rows (List), max_width (int)
		Return: None

Prints a 4D SQL server cursor result

Sets the type of binary architecture
>Currently supports the following formats:
>
>'<' little-endian for MAC OS X - RVLB
>
>'>'	big-endian for Windows - BLVR

### Database Interface

It acts as an intermediary between view and model

#### Methods
###### connect

		Params:	** kwargs
		Return: None

Opens a socket connection to the 4D SQL Server

kwargs supported are:

* socket_timeout : int (default 10)
* dsn : str (default '')
* host : str (default '127.0.0.1')
* port : int (default 19812)
* user : str (default '')
* password : str (default '')

###### close

		Return: None

Closes the current 4D SQL server socket connection

###### cursor

		Return: _python4DCursor object

Returns a 4D SQL server cursor object

###### connected

			Return: bool

Returns true if the socket is connected to the 4D SQL server and false otherwise

###### get_socket

		Return: self._socket object

Returns the current socket object

###### get_socket_timeout

		Return: int

Returns the current socket timeout

###### get_host

		Return: str

Returns the current to 4D SQL server host

###### get_port

		Return: int

Returns the current to 4D SQL server port

###### get_user

		Return: str

Returns the current to 4D SQL server user

###### get_password

		Return: str

Returns the current to 4D SQL server password


### View

It represents the model’s data to user.

#### Methods

###### print_result

		Params: headers (List), rows (List), max_width (int)
		Return: None

Prints a 4D SQL server cursor result
4D SQL server header description is a list of tuples [(str, obj)], so print_result is expecting to a list in that format as header

## Example

```

import time
from python4DBI.python4DBI import python4DBI

con = python4DBI()
con.connect(user='theUser', password='thePassword')
cursor = con.cursor()

t0 = time.time()
cursor.execute(query='SELECT * FROM EMPLOYEES')
if cursor.row_count > 0:
    result = cursor.fetch_all()
    con.print_result(headers=cursor.description, rows=result)
t1 = time.time()
total = t1-t0
```
```
+------------+--------+----------+----------+----------+----------+----------+----------+-----------+------+---------+-----------+--------+-------+-------+------+
| EmployeeID | Last   | Name     | First    | Name     | Address1 | Address2 | Zip      | Code      | City | Country | Telephone | Mobile | Phone | Birth | Date |
+------------+--------+----------+----------+----------+----------+----------+----------+-----------+------+---------+-----------+--------+-------+-------+------+
| 1          | Barros | Marciano | Address1 | Address2 | 9000     | FUNCHAL  | Portugal | 3.510e+09 |      | None    |           | None   | None  |       |      |
+------------+--------+----------+----------+----------+----------+----------+----------+-----------+------+---------+-----------+--------+-------+-------+------+

Execution time : 0.022388219833374023
```
