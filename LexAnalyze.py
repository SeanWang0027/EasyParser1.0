class DFANode(object):
    # Initialize a DFANode object with a name and a boolean value for isFinal
    def __init__(self, name=None, isFinal=0):
        super(DFANode, self).__init__()
        self.name,self.isFinal,self.edge = name,isFinal,{}
    # Add an edge to the DFANode object with an alpha and a target
    def addEdge(self, alpha, target):
        # If the alpha is already in the edge, add the target to the set
        if alpha in self.edge:
            self.edge[alpha].add(target)
        # Otherwise, create a new set and add the target to it
        else:
            nextNodes = set()
            nextNodes.add(target)
            self.edge[alpha] = nextNodes

class DFA(object):
    def __init__(self, terminators):
        super(DFA, self).__init__()
        self.terminators = terminators
        self.status = {}

class NFANode(object):
    def __init__(self, name=None, isFinal=0):
        super(NFANode, self).__init__()
        self.name,self.isFinal,self.edge = name,isFinal,{}
    def addEdge(self, alpha, target):
        if alpha in self.edge:
            self.edge[alpha].add(target)
        else:
            nextNodes = set()
            nextNodes.add(target)
            self.edge[alpha] = nextNodes

class NFA(object):
    def __init__(self, terminators=None):
        super(NFA, self).__init__()
        self.terminators,self.status = terminators,{}

class LRDFANode(object):
    def __init__(self, id):
        self.id,self.itemSet = id,list()
 
    def addItemSetBySet(self, itemSet):
        for i in itemSet:
            if i in self.itemSet:
                continue 
            else:
                self.itemSet.append(i)

digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
symbol = ['!', ',', ';', '[', ']',
          '(', ')', '{', '}', '+', '-', '*', '/', '%', '^', '&', '|', '=', '<', '>']
keyword = ['int', 'double', 'char', 'float', 'break', 'continue',
           'do', 'while', 'if', 'else', 'for', 'void', 'return']

class LexAnalyze(object):
    "LexAnalyzer"
    def __init__(self):
        self.productions = [] 
        self.alphabets = {} 
        self.keywords = {}
        self.NFA = None
        self.DFA = None
        self.alphabets['alphabet'] = alphabet
        self.alphabets['digit'] = digit
        self.alphabets['symbol'] = symbol
        for word in keyword:
            self.keywords[word] = 'keyword'

    def removenote(self, string):
        "用于调用，去除注释"
        CrossLine = False
        a, b = string.find('//'), string.find('/*')
        if a != -1 and (a < b or b == -1):
            string = string[:a]
        elif b != -1:
            c = string[b+2:].find('*/')
            if c > b+1:
                string = string[c+4:]
                CrossLine, string = self.removenote(string)
            else:
                CrossLine = True
                string = string[:b]
        return CrossLine, string

    def Preprocessing(self, sourcecode):
        "去除注释"
        sourcecode = sourcecode.split('\n')
        lines = [i.strip() for i in sourcecode]
        newcode = list()
        CrossLine_note_Flag = False
        for i in lines:
            if len(i) == 0:
                continue
            if not CrossLine_note_Flag:
                CrossLine_note_Flag, i = self.removenote(i)
                if len(i):
                    newcode.append(i)
            else:
                if i.find('*/') != -1:
                    i = i[i.index('*/')+2:]
                    CrossLine_note_Flag, i = self.removenote(i)
                    if len(i):
                        newcode.append(i)
        return newcode

    def readLexGrammar(self, filename):
        "读取词法规则"
        line_num = 0
        for line in open(filename, 'r'):
            line = line.split('\n')[0].strip()
            index = line.find(':')
            cur_left = line[0:index]
            cur_right = line[index + 1:len(line)]
            line_num += 1

            production = dict()
            production['left'] = cur_left
            index = cur_right.find(' ')

            # 右边有非终结符
            if index != -1:
                production['input'] = cur_right[0:index]
                production['right'] = cur_right[index + 1:len(cur_right)]

            # 右边没有非终结符
            else:
                production['input'] = cur_right
                production['right'] = None
            self.productions.append(production)

    def createNFA(self):
        "创建NFA"
        all_status = dict()

        def getNFANode(name, isFinal):
            if name in all_status:
                node = all_status[name]
            else:
                node = NFANode(name=name, isFinal=isFinal)
            return node
        start_node = getNFANode('start', 0)
        end_node = getNFANode('end', 1)
        all_status['start'] = start_node
        all_status['end'] = end_node
        for prod in self.productions:
            now = prod['left']
            alpha = prod['input']
            next = prod['right']
            now_node = getNFANode(now, 0)
            # 右边有非终结符，指向对应节点
            if next is not None:
                target_node = getNFANode(next, 0)
                all_status[next] = target_node
            # 输入字符不是由 'digit' 'nonzero_digit' 'alphabet' 表示的终结符，即alpha自身是一个终结符
            if alpha not in self.alphabets.keys():
                if next is None:
                    now_node.addEdge(alpha, 'end')
                else:
                    if next in self.alphabets.keys():
                        for val in self.alphabets[next]:
                            now_node.addEdge(alpha, val)
                    else:
                        now_node.addEdge(alpha, next)
            # 输入字符是由 'digit' 'nozero_digit' 'alphabet' 表示的终结符
            else:
                for val in self.alphabets[alpha]:
                    if next is None:
                        now_node.addEdge(val, 'end')
                    else:
                        if next in self.alphabets.keys():
                            for tval in self.alphabets[next]:
                                now_node.addEdge(alpha, tval)
                        else:
                            now_node.addEdge(alpha, next)
                            now_node.addEdge(val, next)
            # 更新NFA中的节点信息
            all_status[now] = now_node

        # NFA的终结符集合
        terminators = list()
        for i in range(ord(' '), ord('~') + 1):#全部合法的文本字符
            terminators.append(chr(i))
        self.NFA = NFA(terminators)
        self.NFA.status = all_status

    def createDFA(self):
        "创建对应的DFA"
        all_status = dict()

        def getDFANode(name, isFinal):
            if name in all_status:
                return all_status[name]
            else:
                node = DFANode(name, isFinal)
            return node

        for node_name in self.NFA.status['start'].edge['$']:
            start_node = getDFANode('start', 0)
            dfa_node = getDFANode(node_name, 0)
            start_node.addEdge('$', node_name)
            all_status['start'] = start_node
            all_status[node_name] = dfa_node

            # 记录DFA节点是否已经访问过
            is_visit = list()
            queue = list()

            # 最初的NFA节点集合，即DFA节点
            nfa_node_set = list()
            if node_name not in nfa_node_set:
                nfa_node_set.append(node_name)
            queue.append((nfa_node_set, node_name))

            # BFS
            while queue:
                node_name = queue.pop(0)
                now_node_set = node_name[0]
                now_node_name = node_name[1]
                now_dfa_node = getDFANode(now_node_name, 0)

                # move(I,alpha)  寻找后续状态
                for alpha in self.NFA.terminators:

                    # next节点的NFA节点集合
                    target_set = list()
                    for nfa_node_name in now_node_set:
                        nfa_node = self.NFA.status[nfa_node_name]

                        # 有出边
                        if alpha in nfa_node.edge.keys():
                            for name in nfa_node.edge[alpha]:
                                if name not in target_set:
                                    target_set.append(name)

                    # 如果target_set为空，则直接返回
                    if not target_set:
                        continue
                    next_node_name = ''
                    isFinal = 0
                    tmp_list = list(target_set)
                    target_list = sorted(tmp_list)
                    for tar in target_list:
                        next_node_name = '%s$%s' % (next_node_name, tar)
                        isFinal += int(self.NFA.status[tar].isFinal)

                    # 如果集合中有一个NFA的终态，该节点就是DFA的终态
                    if isFinal > 0:
                        isFinal = 1
                    next_dfa_node = getDFANode(next_node_name, isFinal)
                    now_dfa_node.addEdge(alpha, next_node_name)
                    all_status[now_node_name] = now_dfa_node
                    all_status[next_node_name] = next_dfa_node

                    # 该状态已经访问过，则继续
                    if next_node_name in is_visit:
                        continue

                    # 该状态未访问过，则放入队列中
                    else:
                        if next_node_name not in is_visit:
                            is_visit.append(next_node_name)
                        queue.append((target_set, next_node_name))

        # DFA的终结符集合
        terminators = list()
        for i in range(ord(' '), ord('~') + 1):#全部合法的文本字符
            terminators.append(chr(i))
        self.DFA = DFA(terminators)
        self.DFA.status = all_status

    def runOnDFA(self, line, pos):
        "开始分析"
        if line[pos] in self.alphabets['alphabet'] or line[pos] == '_':
            final_pos = pos
            final_str = ''
            while final_pos < len(line) and line[final_pos] not in self.alphabets['symbol'] and line[final_pos] != ' ':
                final_str += line[final_pos]
                final_pos += 1

            cur_pos = 0
            token = ''
            now_node = self.DFA.status['identifier']
            while cur_pos < len(final_str) and final_str[cur_pos] in now_node.edge.keys():
                token += final_str[cur_pos]
                now_node = self.DFA.status[list(
                    now_node.edge[final_str[cur_pos]])[0]]
                cur_pos += 1

            if cur_pos >= len(final_str) and now_node.isFinal > 0:

                if token in self.keywords.keys():
                    token_type = self.keywords[token]
                else:
                    token_type = 'identifier'
                return final_pos - 1, token_type, token, 'OK'
            else:
                return final_pos - 1, None, '', '标识符不合法'

        elif line[pos] in self.alphabets['digit']:

            # 判断是否为复数
            final_pos = pos
            final_str = ''
            while final_pos < len(line) and (line[final_pos] not in self.alphabets['symbol'] or line[final_pos] == '+'
                                             or line[final_pos] == '-') and line[final_pos] != ' ':
                final_str += line[final_pos]
                final_pos += 1

            cur_pos = 0
            token = ''
            now_node = self.DFA.status['complex']
            while cur_pos < len(final_str) and final_str[cur_pos] in now_node.edge.keys():
                token += final_str[cur_pos]
                now_node = self.DFA.status[list(
                    now_node.edge[final_str[cur_pos]])[0]]
                cur_pos += 1

            if cur_pos >= len(final_str) and now_node.isFinal > 0:
                token_type = 'number'
                return final_pos - 1, token_type, token, 'OK'

            # 判断是否为科学计数形式常量
            final_pos = pos
            final_str = ''
            while final_pos < len(line) and (line[final_pos] not in self.alphabets['symbol'] or line[final_pos] == '+'
                                             or line[final_pos] == '-') and line[final_pos] != ' ':
                final_str += line[final_pos]
                final_pos += 1

            cur_pos = 0
            token = ''
            now_node = self.DFA.status['scientific']
            while cur_pos < len(final_str) and final_str[cur_pos] in now_node.edge.keys():
                token += final_str[cur_pos]
                now_node = self.DFA.status[list(
                    now_node.edge[final_str[cur_pos]])[0]]
                cur_pos += 1

            if cur_pos >= len(final_str) and now_node.isFinal > 0:
                token_type = 'number'
                return final_pos - 1, token_type, token, 'OK'

            # 判断是否为整型常量
            final_pos = pos
            final_str = ''
            while final_pos < len(line) and line[final_pos] not in self.alphabets['symbol'] and line[final_pos] != ' ':
                final_str += line[final_pos]
                final_pos += 1

            cur_pos = 0
            token = ''
            now_node = self.DFA.status['integer']
            while cur_pos < len(final_str) and final_str[cur_pos] in now_node.edge.keys():
                token += final_str[cur_pos]
                now_node = self.DFA.status[list(
                    now_node.edge[final_str[cur_pos]])[0]]
                cur_pos += 1

            if cur_pos >= len(final_str) and now_node.isFinal > 0:
                token_type = 'number'
                return final_pos - 1, token_type, token, 'OK'

            return final_pos - 1, None, '', '标识符或常量不合法'

        else:
            cur_pos = pos
            token = ''
            token_type = 'limiter'
            now_node = self.DFA.status['limiter']

            # 逐个向后读取字符，并进行状态转移
            while cur_pos < len(line) and line[cur_pos] in now_node.edge.keys():
                token += line[cur_pos]
                now_node = self.DFA.status[list(
                    now_node.edge[line[cur_pos]])[0]]
                cur_pos += 1

            # 如果到达终态，则获得一个单词
            if now_node.isFinal > 0:
                return cur_pos - 1, token_type, token, 'OK'

            cur_pos = pos
            token = ''
            token_type = 'operator'
            now_node = self.DFA.status['operator']

            # 逐个向后读取字符，并进行状态转移
            while cur_pos < len(line) and line[cur_pos] in now_node.edge.keys():
                token += line[cur_pos]
                now_node = self.DFA.status[list(
                    now_node.edge[line[cur_pos]])[0]]
                cur_pos += 1

            # 如果到达终态，则获得一个单词
            if now_node.isFinal > 0:
                return cur_pos - 1, token_type, token, 'OK'

            cur_pos = pos
            while cur_pos < len(line) and line[cur_pos] not in self.alphabets['symbol'] \
                    and line[cur_pos] not in self.alphabets['digit'] and line[cur_pos] not in self.alphabets['alphabet'] \
                    and line[cur_pos] != '_' and line[cur_pos] != ' ':
                cur_pos += 1
            return cur_pos - 1, None, '', '非法文本字符'

    def analyze(self, codelist, TokenTable_path):
        "顶层函数"
        line_num = 0
        lex_error = False
        token_table = list()
        error_message=None
        for line in codelist:
            pos = 0
            line_num += 1
            while pos < len(line):
                # 跳过tab，回车，换行，空格
                while pos < len(line) and line[pos] in ['\t', '\n', ' ', '\r']:
                    pos += 1
                if pos < len(line):
                    pos, token_type, token, message = self.runOnDFA(line, pos)
                    if token_type is None:
                        error_message='Lexical error at line %s, column %s : %s' % (str(line_num), str(pos), message)
                        print(error_message)
                        lex_error = True
                        # break
                    else:
                        token_table.append((line_num, token_type, token))
                    pos += 1

        # 如果未出错，那么写入token表文件
        if not lex_error:
            output = open(TokenTable_path, 'w+')
            for line_num, token_type, token in token_table:
                output.write('%d %s %s\n' % (line_num, token_type, token))
            output.close()
            print("Lex analyze complete!")
            return True,error_message
        else:
            print("Lex analyze failed!")
        return False,error_message