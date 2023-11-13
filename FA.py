class DFANode(object):
    def __init__(self, name=None, isFinal=0):
        super(DFANode, self).__init__()
        self.name,self.isFinal,self.edge = name,isFinal,{}
    def addEdge(self, alpha, target):
        if alpha in self.edge:
            self.edge[alpha].add(target)
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