#######imports########################################
import sys
sys.path.append("../")
import Enforcer
import DFAinclusion
import copy
######################################################


###############################################################################
###Define DFA describing property to enforcer phi##############################
######### (actions, states, initial state, final states, transition function)###
##This DFA defines "There should be atleast one "a|b" action, before action "c" can occur. 
###The sequence should end with a "c" action.####################################
###############################################################################
phi = DFAinclusion.DFA(
['a', 'b', 'c'],
['q2','q0', 'q1', 'q3' ],
'q0',
lambda q: q in ['q2'],
lambda q, a: {
        ('q0', 'a') : 'q1',
        ('q0', 'b') : 'q1',
        ('q0', 'c') : 'q3',
        ('q1', 'a') : 'q1',
        ('q1', 'b') : 'q1',
        ('q1', 'c') : 'q2',
        ('q2', 'a') : 'q3',
        ('q2', 'b') : 'q3',
        ('q2', 'c') : 'q3',
        ('q3', 'a') : 'q3',
        ('q3', 'b') : 'q3',
        ('q3', 'c') : 'q3',
    }[(q, a)]
)
###############################################################################


#########################################################################################
###Define DFA describing input property psi##############################################
######### (actions, states, initial state, final states, transition function)############
##This DFA accepts any sequence over alphabet Sigma.###
#########################################################################################
psi = DFAinclusion.DFA(
['a', 'b', 'c'],
['q0'],
'q0',
lambda q: q in ['q0'],
lambda q, a: {
        ('q0', 'a') : 'q0',
        ('q0', 'b') : 'q0',
        ('q0', 'c') : 'q0',
    }[(q, a)]
)
###############################################################################


###############################################################################
###Invoke the enforcer with properties psi, phi, and some test input sequence #
######### (psi, phi, input sequence sigma)#######################################
###############################################################################


####Input sigma = aac######
print "input sequence is aac"  
Enforcer.enforcer(copy.copy(psi), copy.copy(phi), ['a', 'a', 'c'])
print "######################" 

####Input sigma = bbc#####
print "input is bbc"
Enforcer.enforcer(copy.copy(psi), copy.copy(phi), ['b', 'b', 'c'])
print "######################"

####Input sigma = abc#####
print "input is abc"
Enforcer.enforcer(copy.copy(psi), copy.copy(phi), ['a', 'b', 'c'])
print "######################"

####Input sigma = bac#####
print "input is bac"
Enforcer.enforcer(copy.copy(psi), copy.copy(phi), ['b', 'a', 'c'])
print "######################"

####Input sigma = caab#####
print "input is caab"
Enforcer.enforcer(copy.copy(psi), copy.copy(phi), ['c', 'a', 'a', 'b'])
print "######################"
















