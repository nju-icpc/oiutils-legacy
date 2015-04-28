oi-fc
=======

OI-FC is an enhanced version of cmp/diff that allow user to specify simple "fc scripts" to compare output files (e.g., comparing floats within certain error tolerance).

Command line usage:

	oi [-h] [-s S] file1 file2
	
	positional arguments:
	  file1       the first file
	  file2       the second file
	optional arguments:
	  -h, --help  show this help message and exit
	  -s S        the comparison script


## Why we need oi-fc?

Many times we have to write small special judge scripts to compare two program's outputs (e.g., floating point numbers within a specific error tolerance). We have observed that for most of the times, such procedure can be simplified to just writing a one-line *comparision script*.

Note that oi-fc does not resolve every problem. It is no more than an enhanced version of `fc`, and is not intended to implement complex judging logics.

## Examples

These examples matches the typical application scenarios of `oi-fc`. Comparison is conducted line by line (`[]` encloses a description of a line), and token by token (`s`, `d`, `f` indicates a token and `{}` encloses the comparison function).

Following are typical comparison scripts:

* `[s+]+`: Split line with whitespaces and compare them, the default and most common approach.
* `[!s]+`: Compare the whole line as a string, useful for ASCII arts or charts.
* `[f{abs(a-b)<1e-5}+]+`: Compare floats with 1e-5 inaccuracy tolerance.
* `[s2f{abs(a-b)<1e-5}2]+`: Mixed outputs like `Case #1: 1.000000 3.000001`.
* `[s+]2[f{abs(a-b)<1e-5}+]+`: Two lines of string, remaining as floats.

As the comparison function can be arbitrary valid Python lambda expression, one can also write more complicated scripts:

* `[!s{ a.strip().upper() == b.strip().upper() }]`: Line comparison with letter case ignored.
* `[!s{ sorted([int(i) for i in a.strip().split(' ')]) == sorted([int(i) for i in b.strip().split(' ')]) }]`: Comparing a line of unordered integers.


## FC-Script

### Syntax

* `<FCScript>` ::= `<LineDesc>` `<LineDesc>` ...
* `<LineDesc>` ::= `[` `!` `<TokenDesc>` `<TokenDesc>` `...` `]` `<RepDesc>`
* `<TokenDesc>` ::= `<TokenType>` `<Lambda>` `<RepDesc>`
* `<TokenType>` ::= `s` | `d` | `u` | `f` | `e`
* `<RepDesc>` ::= `<Empty>` | `+` | `1` | `2` | `3` | ...
* `<Lambda>` ::= `<Empty>` | `{``<Code>``}`
* `<Code>` ::= arbitrary python code snippet
* `<Empty>` ::= empty

### Semantics

the `<FCScript>` is consisted of a listing of line descriptions (i.e., `<LineDesc>`s), while each line descriptor describes the comparison rule for a specific amount of lines.

For each line descriptor, it specifies a list of token descriptors enclosed in brackets (list of `<TokenDesc>` and a repetition amount (`<RepDesc>`). If starts with `!`, the full line of source files will be considered as a single token. Otherwise, a line will be split to tokens with whitespaces as separators.

A token descriptor is defined by three parts: (1) the type of that token `<TokenType>`; (2) the repetition amount of that token `<RepDesc>`; (3) an optional comparison script `<Lambda>`.

#### Token types
The following types are supported:

* `s`: string, by default.
* `d`, `u`, `f`: signed, unsigned integer and float. Note that integers can also be compared them using `s` (string comparison). Therefore, use `d` and `u` only if you are defining your own comparison function, as the default string comparator is much faster.
* `j` : json object.
* `e` : python object and scripts (unsafe, use them carefully).

#### Repetition

For `<RepDesc>`, `+` denotes that the pattern can repeat an arbitrary amount of times. Otherwise the pattern occurs exactly `<RepDesc>` times. A few notes:

* `'+'` qualifier for token is only allowed to occur once in a line descriptor, and so does line descriptor and the whole script.
* If `'+'` is not explicitly declared, the last object is considered as '+' object.

#### Comparison Function

Any lambda function can be used to compare two tokens. You can use variable `a` and `b` to refer to the two tokens in the files to be compared.


TODO list
--------

* General optimization to make it run faster in most cases.
* Various fixes.
* More or well-optimized token types.
