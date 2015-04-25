oi-fc
=======

OI-FC is an enhanced version of cmp/diff that allow user to specify simple "fc scripts" to compare output files (e.g., comparing floats within certain error tolerance).

Syntax
-------

The syntax of fc scripts are shown below:

* fc script: <line descriptors\>
* line descriptor: [!(Optional)<token descriptors\>] <mark of repetition\>(Optional)
	* If a line descriptor is started with symbol '!', the whole line is considered as a full token. Otherwise, lines are separated by whitespaces.
* token descriptor: <token type\><compare function\><mark of repetition\>(Optional)
* token type: The type of compared tokens, used as comparing types and parameters of compare funcions.
	* currently supported token types:
	1. s: string, by default.
	2. d, u : intergers. Don't abuse it since it may slow the comparison process.
	3. f : float, don't abuse for the same reason.
	4. e : python object and scripts. May have potential safety issues currently.
* mark of repetition: An integer or '+', '+' means it may repeat 0 ~ N times. 
	* '+' qualifier for token is only allowed to occur once in a line descriptor, and so does line descriptor and the whole script
	* If '+' is not explicitly declared, the last object is considered as '+' object.
* compare function: A lambda function to compare tokens. The two parameters are called 'a' and 'b'.

Examples
--------
* [s+]+
	* Split line with whitespaces and compare them, the default and most common approach.
* [!s]+
	* Compare the whole line as a string, useful for ASCII arts or charts.
* [f{abs(a-b)<1e-5}+]+
	* Compare floats with 1e-5 inaccuracy tolerance.
* [s2f{abs(a-b)<1e-5}2]+
	* "Case 1: 1.000000 3.000001" like output.
* [s+]2[f{abs(a-b)<1e-5}+]+
	* Two lines of string, remaining as floats.

TODO list
--------

* General optimization to make it run faster in most cases.
* Various fixes.
* More or well-optimized token types.