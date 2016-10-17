##imports###########################
import Automata
####################################

############################################################################
# Compute and return automaton B_\varphi for any given automaton A_\varphi##
#(Returns DFA that accepts all extensions of words accepted by ##############
#### the DFA phi provided as input.)#########################################
############################################################################
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
     
    return Automata.DFA( phi.S,
                phi.Q,
                phi.q0,
                lambda q: q in finalSet, 
                lambda q, a: deltaDict[(q, a)])
########################################################################
  
#############################################################################################################
###### Function to pre-compute emptiness check for each state in the automaton C= A_\varphi*neg(B_varphi). ##        
###### Input: Automaton C = A_\varphi*neg(B_varphi) ######################################################### 
###### Output: A dictionary containing an entry for each state in the product C.#############################
######   (For each state, if the language accepted from the considered state is empty, #######################
######   then the value corresponding to that state is true and the value is false otherwise.)################
##############################################################################################################         
def computeEmptinessDict(autC):
    dictEnf = {}
    for state in autC.Q:
        autC.makeInit(state) 
        if autC.isEmpty():
            dictEnf[state] = True
        else:
            dictEnf[state] = False
    return dictEnf
########################################################################
########################################################################         


################################################################################
################################################################################
###Enforcer takes two DFA A_\psi, A_\varphi and an input sequence of events#####
####Computes the output sequence sigmaS incrementally.##########################
################################################################################
################################################################################         
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
    autC =  Automata.DFAProduct([psi, autB], lambda (o1, o2) : o1 and o2).getDFA()

    ## Pre-compute emptiness check before entering the loop (starting online monitoring/processing input event sequence).###
    dictEnf = computeEmptinessDict(autC)
    
    ## ONLINE monitoring/Process the given input sequence test sequence sigma and computing output sigmaS incrementally###
    for event in sigma:
        print "event is.."+str(event)
        p=psi.step1(event)
        q=phi.step1(event)
        
        # emptiness check result corresponding to state (p,q) in the automaton C. #
        isEmpty = dictEnf[(p,q)]
        
        if isEmpty == True:
            for a in sigmaC:
                sigmaS.append(a)
            sigmaS.append(event)
            sigmaC= []
        else:
            sigmaC.append(event)
        print "output sigmaS is.."+str(sigmaS)
########################################################################
########################################################################         


            
