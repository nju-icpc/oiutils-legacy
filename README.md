Oiutils
=======
Oiutils is a collection of *portable* command-line tools for programming contest aid, program-based contest hosting and teaching support. We tried to keep every tool minimum, do one thing and do it well, and we encourage users piping these tools together to achieve their goals.

Oiutils is designed to support grading system for Olympiad in Informatics in Jiangsu, as well as Online Judge backend at Nanjing University.

## Tools Overview

### Source code: compile and judge

* **oi-compile**: compile a source code into binary. This script automatically tries to compile a single source file  into an executable using right compiler according to its file extension.
* **oi-sandbox**: run any command with specified time and memory limit. Memory consumption and time usage are returned.
* **oi-fc**: an enhanced version of cmp/diff that allow user to specify simple "fc scripts" to compare output files (e.g., comparing floats within certain error tolerance).
* **oi-judge**: a simple script that (1) create a temporary directory, (2) put test input and executable in this directory, (3) run the executable with time and memory limit, and (4) calls an evaluation script to return judge results.

### Programming contest hosting
* **oi-run**: synthesize a Makefile for a specified contest recipie and programmer's submissions. Everything (including dependency) is managed by the Makefile: the source compilation task, test runs for each test case, and ranklist generation. A few interesting features:
	1. The Makefile is *incremental* such that an entire ACM-ICPC  contest can be hosted using this procedure by repeatedly invoking `oi-run` when new submissions are arrived.
	2. Redjuging is greatly simplified: modifying a test data yields all test runs depending on it to be re-executed, and invoking `make` manages the rejudge automatically.
	3. Judging reports can be generated for each individual contestant, which are useful in a formal OI contest.  

### Source code: contestant aids

### Code synthesis

### Visualization
* oi-vis

## Installation

Install using the following command:

	python setup.py install

There are a few dependences: pyyaml, psutil.

## Credits

* `oi-fc` is implemented by [Zihan Xu](https://github.com/Sojiv).

## Future

* Collecting/distributing files (send & receive)
* Scheduling a contest, e.g., Seat arrangements (oi sched)
