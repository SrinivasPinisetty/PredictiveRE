#####Imports####################
from itertools import izip
from copy import deepcopy
###############################


##function to sort a tuple###
def ts(x):
    return tuple(sorted(x))
#############################

############################################################
############################################################
class DFA:
    
    def __init__(self, S, Q, q0, F, d, e = ('.l',)):
        self.S = S
        self.Q = Q
        self.q0 = q0
        self.q = q0
        self.F = F
        self.d = d
        self.e = e # empty word

        self.reset()
        
    def complement(self):
        
        newSetF = set()
        
        for q in self.Q:
            if not self.F(q):
                newSetF.add(q)
                
        self.F = lambda q: q in newSetF

    def isEmpty(self):
        
        visited = set()
        
        def dfs(node):
            visited.add(node)
            for a in self.S:
                q = self.d(node, a)
                if q and q not in visited:
                    dfs(q)
                    
        dfs(self.q0)
        return all(not self.F(q) for q in visited)

    def show(self):
       
        print '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
        print 'alphabet:', sorted(self.S)
        print '\nstates:', sorted(self.Q)
        print '\ninit:', self.q0
        print '\nfinal:'
        for s in sorted(self.Q):
            if self.F(s):
                print s
        print '\ntransitions:'
        for s in sorted(self.Q):
            for a in self.S:
                self.reset(s)
                self.step(a)
                print (s, a), '->', self.q
            print
        print '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
        
        self.graph()

    def graph(self):
        
        print '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
        print
        for i, q in enumerate(sorted(self.Q)):
            fill = list('999')
            if q == self.q0:
                fill[1] = 'f'
            if self.F(q):
                fill[0] = 'f'
            if fill == list('999'):
                fill = list('fff')
            print '%s [label="%s" style="fill: #%s"];' % (i, q, ''.join(fill))
        print
        sQ = sorted(self.Q)
        for i, s in enumerate(sorted(self.Q)):
            for a in self.S:
                self.reset(s)
                self.step(a)
                print '%s -> %s [labelType = "html" label="<div style=\'width:20px; height:20px; background-color:white; z-index:100; border: 1.5px solid black; text-align: center; border-radius: 5px;\'>%s</div>" lineInterpolate="basis"]' % (i, sQ.index(self.q), a)
                #print '%s -> %s [label="%s"]' % (i, sQ.index(self.q), a)
            print
        print
        print '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'

    def reset(self, q = None):
        
        q = q or self.q0
        
        self.q = q


    def step1(self, a):
        #if a != '' and a != self.e:
        if a and a not in self.e:
            self.q = self.d(self.q, a)
            return self.q
            
    def makeInit(self, q):
        #if a != '' and a != self.e:
        #if a and a not in self.e:
        self.q0 = q
        
            
    def step(self, a):
        #if a != '' and a != self.e:
        if a and a not in self.e:
            self.q = self.d(self.q, a)

    def isInAcceptingState(self):
        return self.F(self.q)


    def accepts(self, w):
        
        #w = w.replace(self.e, '')
        
        #if w == '' or w == []:
        if not w or w == self.e:
            return self.F(self.q0)
            
        #if '.d' in w: 
        if w == ('.d',): 
            return False
        
        q = self.q
        
        self.reset()

        for a in w:
            self.step(a)
            
        ret = self.isInAcceptingState()
        
        self.reset(q)

        return ret

############################################################
############################################################


############################################################
############################################################
class DFAProduct:
        
    #def __init__(self, dfas, outFun = None, e = '.l'):
    def __init__(self, dfas, outFun = None, e = ('.l',)):
        
        outFun = outFun or str
        
        self.e = e
        
        self.S = dfas[0].S
        
        assert all(self.S == dfa.S for dfa in dfas)
        
        self.q0 = tuple(dfa.q0 for dfa in dfas)
        self.q = self.q0
        
        def d(q, a):
            return tuple(dfa.d(qi, a) for qi, dfa in izip(q, dfas))
        
        self.d = d

        def g(q):
            return outFun(tuple({False : 0, True : 1}[dfa.F(qi)] for qi, dfa in izip(q, dfas)))

        self.g = g
        
        self.reset()
        
        ## All loc
        states = set()
        for state1 in dfas[0].Q:
            for state2 in dfas[1].Q:
                states.add((state1,state2))
         
        #print states    
        self.Q = states
        # TODO: perform a DFS in order to identify Q (reachable product states) - DONE!
#
#        visited = set()
#        
#        def dfs(node):
#            visited.add(node)
#            for a in self.S:
#                q = self.d(node, a)
#                if q and q not in visited:
#                    dfs(q)
#
#        dfs(self.q0)
#
#        self.Q = visited

    def getDFA(self):
        
        deltaDict = {}
        
        for q in self.Q:
            for a in self.S:
                deltaDict[(q, a)] = self.d(q, a)
        
        finalSet = set()
        
        for q in self.Q:
            if self.g(q): # self.g must return True / False
                finalSet.add(q)
        
        #print deltaDict
        return DFA( self.S,
                    self.Q,
                    self.q0,
                    lambda q: q in finalSet, 
                    lambda q, a: deltaDict[(q, a)])
        
    def show(self):
       
        print '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
        print 'alphabet:', sorted(self.S)
        print '\nstates:', sorted(self.Q)
        print '\ninit:', self.q0
        print '\noutput:'
        for so in sorted(zip(self.Q, map(self.g, self.Q)), key = lambda (q, g): (g, q)):
            print so
        print '\ntransitions:'
        for s in sorted(self.Q):
            for a in self.S:
                self.reset(s)
                self.step(a)
                print (s, a), '->', self.q
            print
        print '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
        
        self.graph()
        
    def graph(self):
        
        print '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
        print
        for i, q in enumerate(sorted(self.Q)):
            fill = list('999')
            if q == self.q0:
                fill[1] = 'f'
            if self.g(q):
                fill[0] = 'f'
            if fill == list('999'):
                fill = list('fff')
            print '%s [label="%s" style="fill: #%s"];' % (i, '(' + ', '.join(q) + ')', ''.join(fill))
        print
        sQ = sorted(self.Q)
        for i, s in enumerate(sorted(self.Q)):
            for a in self.S:
                self.reset(s)
                self.step(a)
                print '%s -> %s [labelType = "html" label="<div style=\'width:20px; height:20px; background-color:white; z-index:100; border: 1.5px solid black; text-align: center; border-radius: 5px;\'>%s</div>" lineInterpolate="basis"]' % (i, sQ.index(self.q), a)
            print
        print
        print '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
        
    def reset(self, q = None):
        
        q = q or self.q0
        
        self.q = q
        self.o = self.g(q)

    def step(self, a):
        #if a != '' and a != self.e:
        if a and a != self.e:
            self.q = self.d(self.q, a)
            self.o = self.g(self.q)
             
    def transduce(self, w):
        
        if w == self.e:
            return self.o
        
        q = self.q
        
        self.reset()
        
        #ret = self.o
        ret = [self.o]
        
        for a in w:
            self.step(a)
            #ret += self.o
            ret.append(self.o)
            
        self.reset(q)

        return tuple(ret)
##################################################################################
##################################################################################


##################################################################################
    # return True if L(dfa1) includes L(dfa2)
    # and False otherwise
###################################################################################
def includesLang(dfa1, dfa2):
    dfa1c = deepcopy(dfa1)
    dfa1c.complement()
    diff = DFAProduct([dfa1c, dfa2], lambda (o1, o2) : o1 and o2).getDFA()
    return diff.isEmpty()
##################################################################################
##################################################################################
