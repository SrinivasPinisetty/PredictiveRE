##imports###########################
import DFAinclusion
####################################

########################################################################
##Returns DFA that accepts all extensions of words accepted by 
####the DFA phi provided as input##
########################################################################
def getAutB(phi):
    deltaDict = {}
    finalSet = set() 
   
    for q in phi.Q:
        if phi.F(q):
            finalSet.add(q)
                  
    for q in phi.Q:
        for a in phi.S:
            if q in finalSet:
                deltaDict[(q, a)] = q
            else:
                deltaDict[(q, a)] = phi.d(q, a)
                
    return DFAinclusion.DFA( phi.S,
                phi.Q,
                phi.q0,
                lambda q: q in finalSet, 
                lambda q, a: deltaDict[(q, a)])
########################################################################
########################################################################         


########################################################################
###Enforcer takes two DFA psi, phi and an input sequence of events######
####Computes the output sequence sigmaS incrementally.##################
########################################################################
def enforcer(psi, phi, sigma):
    
    ##Initially sigmaC, and sigmaS are empty.###
    sigmaC= []
    sigmaS=[]
    
    ## P keeps track of current state of automaton psi.###
    ## q keeps track of current state of automaton phi.###
    p=psi.q0
    q=phi.q0
    
    ## autB is automaton that accepts all extensions of words accepted by phi##
    autB = getAutB(phi)
    autB.complement()
    
    ## autC is the product of psi and complement of autB###
    autC =  DFAinclusion.DFAProduct([psi, autB], lambda (o1, o2) : o1 and o2).getDFA()
        
    ## Process the given input sequence sigma and compute output sigmaS incrementally###
    for event in sigma:
        print "event is.."+str(event)
        p=psi.step1(event)
        q=phi.step1(event)
        autC.makeInit((p,q)) 
        if autC.isEmpty():
            for a in sigmaC:
                sigmaS.append(a)
            sigmaS.append(event)
            sigmaC= []
        else:
            sigmaC.append(event)
        print "output sigmaS is.."+str(sigmaS)
########################################################################
########################################################################            
            
