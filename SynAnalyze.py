import json
import os
import copy
from pyecharts import options as opts
from pyecharts.charts import Tree

os.system('g++ ./Lextax_more.cpp -o word') 
os.system('./word')

start_symbol = ""  # initial set
symbol = set()  # whole set
terminal_symbol = set()  # terminal symbol set
non_terminal_symbol = set()  # unterminal symbol set

produce = [] 
project = [] 
new_project = [] 
first_item = {} 

closure = []  
closureSet = []  

goto = []

first = {} 
first_empty = [] 

firstFile = open(r'./syntax/first.txt', 'w', encoding="utf-8")
analyzeFile = open(r'./syntax/StackInfo.txt', 'w', encoding="utf-8")
lrFile = open(r'./syntax/lr.txt', 'w', encoding="utf-8")
closureFile = open(r'./syntax/closure.txt', 'w', encoding="utf-8")


statusStack = [0]
charStack = ['#']
tempVarCnt = {}
midCode = {}

pointer = 0
tree = []

cntNode = -1
nodeStack = [] 

def find_Goto(i):
    '''
    This function finds the goto set of a given symbol.
    It takes in the symbol's index.
    '''
    global symbol, closure

    # Iterate through the closure set of the given symbol
    for j in closureSet[i]:
        # Get the item from the new project
        item = new_project[j]
        try:
            # Get the character at the current point
            nowCharacter = item["right"][item["point"]]
            # If the character is not in the goto set, add it
            if nowCharacter not in goto[i]:
                goto[i][nowCharacter] = [j + len(terminal_symbol)]
            # Otherwise, add the item's index to the goto set
            else:
                goto[i][nowCharacter].append(j + len(terminal_symbol))
        # If there is no character, pass
        except:
            pass
    # Iterate through the symbol
    for j in symbol:
        # If the symbol is in the goto set
        if j in goto[i]: 
            # Create a new set
            newSet = set()
            # Iterate through the goto set
            for itemOrd in goto[i][j]:
                # Add the closure of the item to the new set
                newSet |= closure[itemOrd]
            # If the new set is in the closure set
            if newSet in closureSet:
                # Set the goto set to the index of the new set in the closure set
                goto[i][j] = closureSet.index(newSet)
            # Otherwise, add the new set to the closure set and set the goto set to the index of the new set in the closure set
            else:
                closureSet.append(newSet)
                goto.append({})
                goto[i][j] = len(closureSet) - 1

# Define a function to find the closure of a given item
def find_closure(i, ini):
    # Declare the global variable closure
    global closure

    # Get the item from the new_project list
    item = new_project[i]
    try:
        # Get the character at the current point
        nowCharacter = item["right"][item["point"]]
        # Initialize beta and alpha
        beta = ""
        alpha = item["accept"]
        # Initialize the set fir
        fir = set()
        try:
            # Get the beta string
            beta = item["right"][(item["point"] + 1):]
            # Add the alpha to the beta string
            beta += [alpha]
            # Iterate through the beta string
            for sym in beta:
                # Add the first set of the symbol to the set fir
                fir |= first[sym]
                # Check if the symbol is in the first_empty set
                if sym not in first_empty:
                    # Break out of the loop
                    break
        # If the character is not in the first_item set
        except:
            # Set the set fir to the alpha set
            fir = set(alpha)
        # Check if the character is in the first_item set
        if nowCharacter in first_item:
            # Iterate through the set of the character
            for j in first_item[nowCharacter]:
                # Check if the item is in the closure set
                if j not in closure[ini] and new_project[j]["accept"] in fir:
                    # Print the item
                    # print(j)
                    # Add the item to the closure set
                    closure[i].add(j)
                    closure[ini].add(j)
                    # Recursively call the find_closure function
                    closure[i] |= find_closure(j, ini)
    # If the character is not in the first_item set
    except:
        # Add the item to the closure set
        closure[i].add(i)
        # Return the closure set
        return {i}
    # Return the closure set
    return closure[i]

def convert_productions(file_path):
    global terminal_symbol,symbol,produce
    # Open the file containing the productions and store the lines in a list
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            # Strip the line of any whitespace and replace the new line character with a space
            line = line.strip().replace('\n', ' ')
            # If the line is empty, skip it
            if line == "":
                continue
            # Split the line at the ':' character and store the result in a list
            line = line.split(':')
            # If the list has less than 3 elements, skip it
            if len(line) < 3:
                continue
            # Add the terminal symbol to the set
            terminal_symbol.add(line[1])
            # Add the symbol to the set
            symbol.add(line[1])
            # If the third element of the list is '$', add the production to the list of productions
            if line[2] == '$':
                produce.append({"left": line[1], "right": [], "order": int(line[0])})
            # Otherwise, add the production to the list of productions and add the symbols in the right hand side of the production to the set
            else:
                produce.append({"left": line[1], "right": line[2].split(' '), "order": int(line[0])})
                symbol |= (set(line[2].split(' ')))

def initial_first_set():
    #This function initializes the first set of each symbol
    global non_terminal_symbol,terminal_symbol,first
    #Loop through each non-terminal symbol
    for item in non_terminal_symbol:
        #Set the first set of the non-terminal symbol to an empty set
        first[item] = set()
    #Loop through each terminal symbol
    for item in terminal_symbol:
        #Set the first set of the terminal symbol to the terminal symbol
        first[item] = {item}

def bfs():
    #This function performs a breadth-first search on the produce set
    global produce,terminal_symbol,first_empty
    #Create an empty queue
    bfs_queue = []
    #Loop through each item in the produce set
    for item in produce:
        try:
            #Get the symbol from the right side of the item
            sym = item["right"][0]
            #Check if the symbol is a terminal symbol
            if sym in terminal_symbol:
                #If it is, add the terminal symbol to the left side of the item in the first set
                first[item["left"]].add(sym)
        #If the symbol is not found, add the left side of the item to the empty queue
        except:
            first_empty.append(item["left"])
            bfs_queue.append(item["left"])

    #Create a copy of the produce set
    proCopy = copy.deepcopy(produce)
    #Loop until the queue is empty
    while len(bfs_queue) > 0:
        #Pop the last item from the queue
        sym = bfs_queue.pop(-1)
        #Loop through each item in the produce set
        for i, item in zip(range(len(proCopy)), proCopy):
            #Check if the left side of the item is equal to the symbol
            if item["left"] == sym:
                #If it is, set the right side of the item to an empty list
                proCopy[i]["right"] = []
            #Check if the symbol is in the right side of the item
            elif sym in item["right"]:
                #If it is, remove the symbol from the right side of the item
                proCopy[i]["right"].remove(sym)
                #Check if the right side of the item is empty
                if len(proCopy[i]["right"]) == 0:
                    #If it is, check if the left side of the item is in the first empty set
                    if item["left"] not in first_empty:
                        #If it isn't, add the left side of the item to the first empty set
                        first_empty.append(item["left"])
                        #Add the left side of the item to the queue
                        bfs_queue.append(sym)

def fis():
    global produce,first,first_empty
    fis = 1
    while fis:
        fis = 0
        for item in produce:
            for sym in item["right"]:
                if not first[item["left"]].issuperset(first[sym]):
                    fis = 1
                    first[item["left"]] |= first[sym]
                if sym not in first_empty:
                    break

def project_list():
    global produce,project,terminal_symbol,closure,new_project
    #Loop through the produce list and add each item to the project list
    for order, i in zip(range(len(produce)), produce):
        #Loop through the right list of each item in the produce list
        for j in range(len(i["right"]) + 1):
            #Add the item to the project list
            project.append({"left": i["left"], "right": i["right"], "order": i["order"], "point": j, "origin": order, "isTer": (j == len(i["right"]))})

    for i, item in zip(range(len(project)), project):
        for sym in terminal_symbol:
            # Create a new set for each item in the project
            closure.append(set())
            # Create a deep copy of the item
            new_project.append(copy.deepcopy(item))
            # Set the accept symbol of the new item to the symbol passed in
            new_project[-1]["accept"] = sym

def variable_item(closureFile):
    global new_project,first_item,closure,closureSet,goto
    #Loop through the new_project list and assign each item to the variable item
    for i, item in zip(range(len(new_project)), new_project):
        #Check if the point value of the item is 0
        if item["point"] == 0:
            #Check if the left value of the item is in the first_item dictionary
            if item["left"] in first_item:
                #If it is, add the current item index to the set of the left value
                first_item[item["left"]].add(i)
            else:
                #If not, create a set with the current item index and assign it to the left value
                first_item[item["left"]] = {i}

    # 求每个项目的闭包
    print("Single Project's closure：", file=closureFile)
    for i, item in zip(range(len(new_project)), new_project):
        print("%-4d " % i, item, file=closureFile)
        closure[i].add(i)
        closure[i] = find_closure(i, i)
        if item["origin"] == 0 and item["accept"] == '#' and item["point"] == 0:
            closureSet.append(closure[i])
        print("  ", closure[i], file=closureFile)


    goto.append({})
    i = 0
    while (i < len(closureSet)):
        find_Goto(i)
        i += 1

#Define a function to print the LR(1) Analyzer
def print2lr(filename):
    #Declare global variables
    global terminal_symbol,start_symbol,closureSet,new_project,goto,non_terminal_symbol
    #Print the LR(1) Analyzer
    print("LR(1) Analyzer:", file=filename)
    #Sort the terminal and non-terminal symbols
    ts = sorted(list(terminal_symbol - {start_symbol}))
    nts = sorted(list(non_terminal_symbol - {start_symbol}))
    #Print the terminal and non-terminal symbols
    print("   ", '  '.join(map(lambda x: (x + "  ")[:3], ts)), "", '  '.join(map(lambda x: (x + "  ")[:3], nts)), file=filename)
    #Loop through the closure set
    for i in range(len(closureSet)):
        #Print the index of the closure set
        print("%-3d" % i, end=" ", file=filename)
        #Loop through the items in the closure set
        for item in closureSet[i]:
            #Store the item in a variable
            k = item
            #Update the item
            item = new_project[item]
            #Check if the item is terminal
            if item["isTer"] == True:
                #Check if the item's accept symbol is in the goto set
                if item["accept"] in goto[i]:
                    #Print a warning if the item's accept symbol is in the goto set
                    print("Warning:", "%d号项目集族的\t%s\t符号冲突，冲突的产生式为\t%d\t" % (i, item["accept"], k), new_project[k])
                else:
                    #Add the item's accept symbol to the goto set
                    goto[i][item["accept"]] = -item["origin"]
        #Loop through the terminal symbols
        for j in ts:
            try:
                #Check if the item is in the goto set
                if goto[i][j] > 0:
                    #Print the index of the item in the goto set
                    print("s%-3d" % goto[i][j], end=" ", file=filename)
                if goto[i][j] < 0:
                    #Print the index of the item in the goto set
                    print("r%-3d" % -goto[i][j], end=" ", file=filename)
                if goto[i][j] == 0:
                    #Print "acc" if the item is in the goto set
                    print("acc ", end=" ", file=filename)
            except:
                #Print "    " if the item is not in the goto set
                print("    ", end=" ", file=filename)
        #Loop through the non-terminal symbols
        for j in nts:
            try:
                #Print the index of the item in the goto set
                print("%-4d" % goto[i][j], end=" ", file=filename)
            except:
                #Print "    " if the item is not in the goto set
                print("    ", end=" ", file=filename)
        #Print a new line
        print(file=filename)

#Define a function called generate_names that takes in a filepath as an argument
def generate_names(filepath):
    #Declare global variables
    global terminal_symbol,start_symbol,non_terminal_symbol,closureSet,new_project,goto
    #Create a sorted list of terminal symbols
    ts = sorted(list(terminal_symbol - {start_symbol}))
    #Create a sorted list of non-terminal symbols
    nts = sorted(list(non_terminal_symbol - {start_symbol}))
    #Loop through the closure set
    for i in range(len(closureSet)):
        #Loop through the items in the closure set
        for item in closureSet[i]:
            #Set k to the item
            k = item
            #Set the item to the new project
            item = new_project[item]
            #Check if the item is a terminal symbol
            if item["isTer"] == True:
                #Check if the accept symbol is in the goto set
                if item["accept"] in goto[i]:
                    #If it is, do nothing
                    pass
                else:
                    #If it isn't, add the accept symbol to the goto set
                    goto[i][item["accept"]] = -item["origin"]
    #Create an empty string
    names = ""
    #Open the file at the given filepath
    with open(filepath, encoding="utf-8") as f:
        #Read the file
        names = f.read()
    #Strip the whitespace from the file
    names = names.strip().replace(' ', "").split('\n')
    #Reverse the order of the names
    names = names[::-1]
    #Filter out any empty strings
    names = list(filter(lambda x: x != "", names))
    #Return the names
    return names

def generate_stack(originalpath,filepath):
    inp = "" 
    with open(originalpath, encoding="utf-8") as f:
        inp = f.read()
    inp = inp.strip().split('\n')
    inp = list(filter(lambda x: x != "", inp))
    inp += ['#']
    print(inp, " has an analyze Stack：", file=filepath)
    return inp

#Define a function called writeAnalyze that takes in a filepath as an argument
def writeAnalyze(filepath):
    #Declare global variables
    global statusStack,charStack,inp,pointer,goto,tree,cntNode,nodeStack
    #Print the status stack, character stack, and input string up to the pointer
    print("%-10s %-10s %-10s" % (' '.join(map(lambda x: str(x), statusStack)), ' '.join(charStack), ' '.join(inp[pointer:])), file=filepath)
    #Loop until the pointer is out of bounds
    while True:
        #Set c to the character at the pointer
        c = inp[pointer]
        try:
            #Set num to the value of the goto dictionary at the status stack and the character
            num = goto[statusStack[-1]][c]
            #If num is 0, print "Accepted" and set the tree dictionary at the status stack and the character to the character stack
            if num == 0:
                print("Accepted", file=filepath)
                tree[statusStack[-1]]["name"] = charStack[-1]
                break
            #If num is greater than 0, append the value of num to the status stack, create a new node in the tree dictionary, increment the node count, set the name of the node to the character, and append the node to the node stack
            elif num > 0: 
                statusStack.append(num)
                tree.append({})
                cntNode += 1
                tree[cntNode]["name"] = c
                nodeStack.append(cntNode)
                charStack.append(c)
                pointer += 1

                #If the character is an identifier or a number, append the node count + 1 to the children list of the node and set the name of the node to the name of the node
                if c in ["identifier", "number"]:
                    tree[cntNode]["children"] = [cntNode + 1]
                    tree.append({})
                    cntNode += 1
                    nam = names.pop()
                    tree[cntNode]["name"] = nam
                    if c == "identifier":
                        print("用identifier归约:", file=filepath) 

                    elif c == "number":
                        print("用number归约:", file=filepath)

            #If num is less than 0, set the order of the item to the value of num, set the right list of the item to an empty list, set the left of the item to the character, set the order of the item to 0, and set the left list of the item to the left of the item
            elif num < 0:
                item = produce[-num] 
                order = item["order"]

                if item["right"] == []:  
                    charStack += [item["left"]]
                    statusStack.append(goto[statusStack[-1]][item["left"]])

                    tree.append({})
                    cntNode += 1
                    tree[cntNode]["children"] = [cntNode + 1]
                    tree[cntNode]["name"] = item["left"]
                    nodeStack.append(cntNode)

                    tree.append({})
                    cntNode += 1
                    tree[cntNode]["children"] = []
                    tree[cntNode]["name"] = ''

                else:
                    #Set k to the length of the right list of the item
                    k = len(item["right"])
                    #Set the status stack, character stack, and input string to the values before the loop
                    statusStack = statusStack[:-k]
                    charStack = charStack[:-k] + [item["left"]]
                    statusStack.append(goto[statusStack[-1]][item["left"]])
                    tree.append({})
                    cntNode += 1
                    tree[cntNode]["children"] = []

                    #Loop through the right list of the item
                    for i in range(k):
                        #Set nowNode to the node in the node stack
                        nowNode = nodeStack.pop()
                        #Append the node to the children list of the node
                        tree[cntNode]["children"].append(nowNode)

                    #Reverse the children list of the node
                    tree[cntNode]["children"] = tree[cntNode]["children"][::-1]
                    #Set the name of the node to the left of the item
                    tree[cntNode]["name"] = item["left"]
                    #Append the node to the node stack
                    nodeStack.append(cntNode)
        #If an exception is thrown, print "error" and raise the exception
        except Exception as e:
            print("error", file=analyzeFile)
            raise e
        #Print the status stack, character stack, and input string up to the pointer
        print("%-10s \t\t %-10s \t\t %-10s" % (' '.join(map(lambda x: str(x), statusStack)), ' '.join(charStack), ' '.join(inp[pointer:])), file=analyzeFile)

def outp(now):
    # print(now)
    if not tree[now]:
        return {}
    di = {}
    di["name"] = tree[now]["name"].replace("_", "_  \n") + ' '

    di["children"] = []
    if ("children" not in tree[now]) or (not tree[now]["children"]):
        return di
    for child in tree[now]["children"]:
        di["children"].append(outp(child))

    return di

def print_tree(outpTree):
    treeData = [outpTree]
    c = (
        Tree().add(
            "",
            treeData,
            orient="TB",
            initial_tree_depth=-1,
            # collapse_interval=10,
            symbol_size=3,
            is_roam=True,
            edge_shape="polyline",
            # is_expand_and_collapse=False,
            label_opts=opts.LabelOpts(
                position="top",
                horizontal_align="right",
                vertical_align="middle",
                # rotate='15',
                font_size=15)).set_global_opts(title_opts=opts.TitleOpts(title="Syntax Tree:Conducted by EasyParser")).render("./syntax/SynTree.html"))

#convert process
convert_productions("./program/productions.txt")

start_symbol = produce[0]["left"]
symbol |= terminal_symbol
symbol -= {''}
terminal_symbol -= {''}
non_terminal_symbol = terminal_symbol
terminal_symbol = symbol - non_terminal_symbol
terminal_symbol |= {'#'}

#Call the initial_first_set function
initial_first_set()
#bfs process
bfs()
#log fis
print(first_empty, file=firstFile)
#first set
fis()
#log fis
for item in non_terminal_symbol:
    print("%s\n%s" % (item, " ".join(list(first[item]))), " $" if item in first_empty else "", "\n", file=firstFile)
#project list
project_list()
#variable list
variable_item(closureFile)
#Action-Goto Table
print2lr(lrFile)
#load names
names = generate_names('./log/names.txt')
#load stack
inp = generate_stack("./log/processed_sourceCode.txt", analyzeFile)
#initialize tree
for i in range(len(closureSet)):
    tree.append({})
#generate the process of analyzing
writeAnalyze(analyzeFile)

outpTree = outp(cntNode)

print_tree(outpTree)