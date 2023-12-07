from LexAnalyze import LexAnalyze
import os
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog

def insert(table, result):
    for index, data in enumerate(result):
        if index != 0:
            table.insert('', END, values=data)

def SourceProGet():
    LexScr1.delete(1.0, END)
    source_path = filedialog.askopenfilename()
    sourcefile = open(source_path,'r',encoding = 'utf-8')
    for line in sourcefile:
        LexScr1.insert('end',line)

def write_in_file(codelist):
    with open('./program/program.cc',"w") as f: 
        for item in codelist:
            f.write(item+"\n")

def LexAnalyzeFunc():
    LexGrammar_path = './lextax/LexGra.txt'  
    TokenTable_path = './lextax/LexAnaResult.txt' 

    lex_ana = LexAnalyze()
    lex_ana.readLexGrammar(LexGrammar_path)
    lex_ana.createNFA()
    lex_ana.createDFA()

    codelist = lex_ana.Preprocessing(LexScr1.get(1.0,'end'))
    write_in_file(codelist)
    lex_ana.analyze(codelist, TokenTable_path)

def LexRuleDisplay():
    LexScr1.delete(1.0, END)
    LexGrammar_path = './lextax/LexGra.txt'  
    sourcefile = open(LexGrammar_path,'r',encoding = 'utf-8')
    for line in sourcefile:
        LexScr1.insert('end',line)

def LexResult():
    LexScr2.delete(1.0, END)
    TokenTable_path = './lextax/LexAnaResult.txt' 
    sourcefile = open(TokenTable_path,'r',encoding = 'utf-8')
    print(sourcefile)
    for line in sourcefile:
        LexScr2.insert('end',line)

def SynAnalyzeFunc():
    os.system('python ./SynAnalyze.py')

def SynRuleDisplay():
    SynScr1.delete(1.0, END)
    SynGrammar_path = './program/productions.txt'
    sourcefile = open(SynGrammar_path,'r',encoding = 'utf-8')
    for line in sourcefile:
        SynScr1.insert('end',line)

def SynFIRSTDisplay():
    SynScr1.delete(1.0, END)
    FirstSets_path = './syntax/first.txt'
    sourcefile = open(FirstSets_path,'r',encoding = 'utf-8')
    for line in sourcefile:
        SynScr1.insert('end',line)

def Synstackdisplay():
    SynScr2.delete(1.0, END)
    FirstSets_path = './syntax/StackInfo.txt'
    sourcefile = open(FirstSets_path,'r',encoding = 'utf-8')
    for line in sourcefile:
        SynScr2.insert('end',line)

if __name__ == '__main__':
    window = tk.Tk()
    window.title('EasyParser') 
    window.geometry('800x700') 

    Title = tk.Label(window, text = 'EasyParser', font=('Times New Roman', 40),fg='green', width=27, height=1)

    Title.place(x=125, y=20)

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