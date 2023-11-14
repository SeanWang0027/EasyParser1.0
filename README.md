# EasyParser1.0
## How to use it?
Before you use this `repo`, please use `git clone` to download the whole project to your own computer.
And before everything starts, you should first create 2 directories:
```shell
cd ./EasyParser1.0
mkdir log
mkdir syntax
```
Just directly use the command below.
```shell
python ./main.py
```
The program you need to change is in `./program/program.cc`.
## Dependencies
You probably need to install `pyecharts`. Just use the command:
```shell
pip install pyecharts
```
## Results
Check the Syntax tree in the following directory where it is established as an `HTML` file :`./syntax/SynTree.html`.

You can find the `Action/Goto Table` here: `./syntax/lr.txt`.

And check the `Stack of Analysis` here: `./syntax/StackInfo.txt`.

The productions are listed here: `./program/productions.txt`.