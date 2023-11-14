#include <iostream>
#include <map>
#include <string>
#include <fstream>

#include <regex>
using namespace std;

void err(string s) {
    cout << "\nERROR: " << s << endl;
    exit(0);
}

int cnt;
map<string, int> word;
string wordList[] = {"!=", "(",  ")", "*",  "+", ",",  "-",    "/",  "+=",  "-=",    "*=",     "/=",   "%=",    "^=", "&=", "|=", ";",
                     "<",  "<=", "=", "==", ">", ">=", "else", "if", "int", "float", "return", "void", "while", "{",  "}",  "||", "&&"};

void init() {
    cnt = 70;
    for (auto i : wordList) word[i] = ++cnt;
}

ofstream program("./log/processed_sourceCode.txt");
ofstream iden("./log/names.txt");

int searchReserve(string s) {
    auto iter = word.find(s);
    return (iter != word.end()) ? iter->second : -1;  
}

void Scanner(string resProgram, int &pointer) {
    int syn = 0;
    string token = "";
    char ch; 
    ch = resProgram[pointer];
    while (ch == ' ') ch = resProgram[++pointer];
    if (isalpha(resProgram[pointer]) || isdigit(resProgram[pointer])) {
        if (isalpha(resProgram[pointer])) {                                                                      
            while (isalpha(resProgram[pointer]) || isdigit(resProgram[pointer])) token += resProgram[pointer++];
            syn = searchReserve(token);                                                                  
            if (syn == -1) {
                iden << token << endl;
                token = "identifier";
            }
        } else {
            while (isdigit(resProgram[pointer])) token += resProgram[pointer++]; 
            syn = searchReserve(token);
            if (syn == -1) {
                iden << token << endl;
                token = "number";
            }
        }
    } else { 
        token = resProgram[pointer];
        token += resProgram[pointer + 1];
        if ((syn = searchReserve(token)) != -1) {  // != <= == >=
            pointer += 2;
        } else {
            token = resProgram[pointer];
            if ((syn = searchReserve(token)) != -1) {  // ( ) * + , - / ; < >
                pointer += 1;
            } else
                err("unknown character " + to_string(int(token[0])) + " " + token);
        }
    }
    program << token << endl;
}

string filterResource(string r) {
    r = regex_replace(r, regex("(\\s){2,}"), " ");

    string filStr = "";
    for (int i = 0; i <= r.length(); i++) {
        if (r[i] == '/' && r[i + 1] == '/') 
            while (r[i] != '\n') i++;
        if (r[i] == '/' && r[i + 1] == '*') { 
            i += 2;
            while (i + 1 < r.length() && (r[i] != '*' || r[i + 1] != '/')) ++i;
            if (i + 1 >= r.length()) err("Not Found! */");
            i += 2;
        }
        filStr += r[i];
    }

    filStr = regex_replace(filStr, regex("[\n\t\v\r]"), "");

    return filStr;
}

int main() {
    ifstream t("./program/program.cc");
    string str((std::istreambuf_iterator<char>(t)), std::istreambuf_iterator<char>());

    string resProgram = filterResource(str);

    init();      
    int pointer = 0; 
    while (pointer < resProgram.length()) {
        Scanner(resProgram, pointer);
        if (!resProgram[pointer]) break;
    }

    for (auto i : word) {
        printf("%03d  ", i.second);
        cout << i.first << endl;
    }
    return 0;
}