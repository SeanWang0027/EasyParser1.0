from LexAnalyze import LexAnalyze
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import StringVar
from tkinter import *
from tkinter import scrolledtext
from pandas import read_csv
from tkinter import ttk
from tkinter import messagebox
import csv
from tkinter import filedialog

#向分析表中插入数据
def insert(table, result):
    # 插入数据
    for index, data in enumerate(result):
        if index != 0:
            table.insert('', END, values=data)  # 添加数据到末尾

# 界面显示源程序
def SourceProGet():
    LexScr1.delete(1.0, END)
    source_path = filedialog.askopenfilename()
    sourcefile = open(source_path,'r',encoding = 'utf-8')
    for line in sourcefile:
        LexScr1.insert('end',line)

# 执行词法分析程序
def LexAnalyzeFunc():
    LexGrammar_path = './lextax/LexGra.txt'  # 词法规则文件相对路径
    TokenTable_path = './lextax/LexAnaResult.txt'  # 存储TOKEN表的相对路径

    lex_ana = LexAnalyze()
    lex_ana.readLexGrammar(LexGrammar_path)
    lex_ana.createNFA()
    lex_ana.createDFA()

    codelist = lex_ana.Preprocessing(LexScr1.get(1.0,'end'))
    lex_ana.analyze(codelist, TokenTable_path)

# 界面显示词法分析规则
def LexRuleDisplay():
    LexScr1.delete(1.0, END)
    LexGrammar_path = './LexGra.txt'  # 词法规则文件相对路径
    sourcefile = open(LexGrammar_path,'r',encoding = 'utf-8')
    for line in sourcefile:
        LexScr1.insert('end',line)

# 界面显示词法分析结果
def LexResult():
    LexScr2.delete(1.0, END)
    TokenTable_path = './lextax/LexAnaResult.txt'  # 存储TOKEN表的相对路径
    sourcefile = open(TokenTable_path,'r',encoding = 'utf-8')
    print(sourcefile)
    for line in sourcefile:
        LexScr2.insert('end',line)

# 执行语法分析程序
def SynAnalyzeFunc():
    os.system('python ./SynAnalyze.py')

# 界面显示语法分析规则
def SynRuleDisplay():
    SynScr1.delete(1.0, END)
    SynGrammar_path = './syntax/SynGra.txt'  # 词法规则文件相对路径
    sourcefile = open(SynGrammar_path,'r',encoding = 'utf-8')
    for line in sourcefile:
        SynScr1.insert('end',line)

# 界面显示语法分析FIRST集合
def SynFIRSTDisplay():
    SynScr1.delete(1.0, END)
    FirstSets_path = './syntax/FirstSets.txt'
    sourcefile = open(FirstSets_path,'r',encoding = 'utf-8')
    for line in sourcefile:
        SynScr1.insert('end',line)

# 界面显示语法分析分析栈
def Synstackdisplay():
    SynScr2.delete(1.0, END)
    FirstSets_path = './syntax/StackInfo.txt'
    sourcefile = open(FirstSets_path,'r',encoding = 'utf-8')
    for line in sourcefile:
        SynScr2.insert('end',line)

# 界面显示语法分析语法树
def SynTreedisplay():
    SynScr2.delete(1.0, END)
    FirstSets_path = './syntax/SynTree.txt'
    sourcefile = open(FirstSets_path,'r',encoding = 'utf-8')
    for line in sourcefile:
        SynScr2.insert('end',line)

if __name__ == '__main__':
    # 第1步，实例化object，建立窗口window
    window = tk.Tk()
    # 第2步，给窗口的可视化起名字
    window.title('EasyParser') 
    # 第3步，设定窗口的大小(长 * 宽)
    window.geometry('800x700')  # 这里的乘是小x

    #标题
    Title = tk.Label(window, text = 'EasyParser', font=('Times New Roman', 40),fg='green', width=27, height=1)
    #Title.pack()
    Title.place(x=125, y=20)

    #词法分析
    button1 = tk.Button(window, text = "Load Program", font=('Times New Roman', 12), fg="green", bg="blue", width=10, height=1, command=SourceProGet)
    button1.place(x=40, y=110)
    LexScr1 = scrolledtext.ScrolledText(window, width=55, height=13, font=("Times New Roman",12), bd =5)
    LexScr1.place(x=20,y=150)
    button2 = tk.Button(window, text = "Lexical Analysis", font=('Times New Roman', 12), fg="green", bg="blue", width=10, height=1, command=LexAnalyzeFunc)
    button2.place(x=140, y=110)
    button3 = tk.Button(window, text = "Lexical Rules", font=('Times New Roman', 12), fg="green", bg="blue", width=10, height=1, command=LexRuleDisplay)
    button3.place(x=240, y=110)
    LexScr2 = scrolledtext.ScrolledText(window, width=55, height=13, font=("Times New Roman",12), bd =5)
    LexScr2.place(x=400,y=150)
    button4 = tk.Button(window, text = "Lexical Result", font=('Times New Roman', 12), fg="green", bg="blue", width=14, height=1, command=LexResult)
    button4.place(x=530, y=110)

    #语法分析
    buttonSyn = tk.Button(window, text = "Syntax Analysis", font=('Times New Roman', 12), fg="green", bg="blue", width=10, height=1, command=SynAnalyzeFunc)
    buttonSyn.place(x=40, y=380)

    button5 = tk.Button(window, text = "Syntax Rules", font=('Times New Roman', 12), fg="green", bg="blue", width=10, height=1, command=SynRuleDisplay)
    button5.place(x=140, y=380)
    button6 = tk.Button(window, text = "FIRST Set", font=('Times New Roman', 11), fg="green", bg="blue", width=10, height=1, command=SynFIRSTDisplay)
    button6.place(x=240, y=380)
    SynScr1 = scrolledtext.ScrolledText(window, width=55, height=13, font=("Times New Roman",12), bd =5)
    SynScr1.place(x=20,y=420)

    button7 = tk.Button(window, text = "Syntax Stack", font=('Times New Roman', 12), fg="green", bg="blue", width=14, height=1, command=Synstackdisplay)
    button7.place(x=530, y=380)
    SynScr2 = scrolledtext.ScrolledText(window, width=55, height=13, font=("Times New Roman",12), bd =5)
    SynScr2.place(x=400,y=420)

    window.mainloop()