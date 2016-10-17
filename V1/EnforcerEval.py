##############################################################################################
#### Version used for evaluation / benchmarks ################################################
#### Execute off-line computation (i.e., computing automaton C from A_\varphi and A\psi,######
####### and emptiness check table for every state in automaton C)#############################
######### 1000 times and compute averages. ###################################################
###Contains some additional code compared to "Enforcer.py" for benchmarking.################## 
##############################################################################################

##imports###########################
import Automata
import sys
#import decimal
import time
import cPickle
#import timeit
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
    ## For measuring time and computing averages.###
    start1 = time.clock()
    totalTime = 0
    totalProduct = 0
    totalEmpt = 0
    totalMem = 0
    
    ### In this for loop, the offline computation (computing automaton C and the emptiness check table) #####
    ####### is repated for 1000 times and average values are reported/printed at the end of this for loop. ##  
    for x in range(0, 1000):
        start = time.clock()
        ## autB is automaton that accepts all extensions of words accepted by phi.##
        autB = getAutB(phi)
        autB.complement()

        ## autC is the product of psi and complement of autB###
        autC =  Automata.DFAProduct([psi, autB], lambda (o1, o2) : o1 and o2).getDFA()
        
        ## total time to compute the product.
        totalProduct = totalProduct + (time.clock()- start)        
        
        start2= time.clock()
        ## Pre-compute emptiness check before entering the loop and starting processing of events.
        dictEnf = computeEmptinessDict(autC)
        end = time.clock()
        ## Total time to compute emptiness table.
        totalEmpt = totalEmpt + (end-start2)
        
        dictEnf_as_string = cPickle.dumps(dictEnf)           
        
        ## total offline time.
        totalTime = totalTime+ (end-start)
        ## total size of the dictionary containing emptiness check results for each state in automaton C.##
        totalMem = totalMem+ sys.getsizeof(dictEnf_as_string)
    
    ## Compute and print averages. ## 
    print "NUMBER OF ENTRIES IN DICT/EMPTINESS TABLE.." + str(dictEnf.__len__())
    print "AVERAGE MEMORY IN BYTES IS.."+str(totalMem/1000)
    print "AVERAGE TOTAL TIME PRODUCT.."+str(totalProduct/1000)
    print "AVERAGE TOTAL TIME EMPTINESS TABLE.."+str(totalEmpt/1000)
    print "AVERAGE TOTAL TIME IS.."+str(totalTime/1000)
    
    ## P keeps track of current state of automaton psi.###
    ## q keeps track of current state of automaton phi.###
    p=psi.q0
    q=phi.q0
    
    ##Initially sigmaC, and sigmaS are empty.###
    sigmaC= []
    sigmaS=[]
    ## ONLINE monitoring/process the given input sequence test sequence sigma and computing output sigmaS incrementally. ###
    for event in sigma:
        print "event is.."+str(event)
        p=psi.step1(event)
        q=phi.step1(event)

        #st = time.clock()
        tmp = dictEnf[(p,q)]
        #end1 = time.clock()
        
        #print "time for DICT query.." + str(end1-st)
        if tmp == True:
            for a in sigmaC:
                sigmaS.append(a)
            sigmaS.append(event)
            sigmaC= []
        else:
            sigmaC.append(event)
        print "output sigmaS is.."+str(sigmaS)
########################################################################
########################################################################         


            
