#######imports###########
import sys
sys.path.append("../")
import Enforcer
import EnforcerEval
import Automata
import copy
#########################

#########################################################################################
### Model of DataSync protocol described in the paper. ###################################
###Defines DFA describing input property psi. #############################################
######### (actions, states, initial state, final states, transition function)############
##### Set of actions Sigma = {a1.inform, a2.inform, a1.ack, a2.ack}######################
#########################################################################################
psi = Automata.DFA(
# actions
['a1Inform', 'a2Inform', 'a1Ack', 'a2Ack'],
# locations
['q0', 'q1', 'q2', 'q3'],
# initial location
'q0',
# accepting locations
lambda q: q in ['q0'],
# transitions
lambda q, a: {
        ('q0', 'a1Inform') : 'q1',
        ('q0', 'a2Inform') : 'q3',
        ('q0', 'a1Ack') : 'q3',
        ('q0', 'a2Ack') : 'q3',
        ('q1', 'a2Inform') : 'q2',
        ('q1', 'a2Ack') : 'q0',
        ('q1', 'a1Inform') : 'q3',
        ('q1', 'a1Ack') : 'q3',
        ('q2', 'a1Inform') : 'q1',
        ('q2', 'a1Ack') : 'q0',
        ('q2', 'a2Inform') : 'q3',
        ('q2', 'a2Ack') : 'q3',
        ('q3', 'a1Inform') : 'q3',
        ('q3', 'a2Inform') : 'q3',
        ('q3', 'a1Ack') : 'q3',
        ('q3', 'a2Ack') : 'q3',    
    }[(q, a)]
)
###############################################################################


###############################################################################
###Define DFA describing property to enforcer phi.##############################
######### (actions, states, initial state, final states, transition function)##
##This DFA defines property varphi_1 described in the paper 
####"Every a1.inform should eventually end with an a1.ack or a2.ack". 
###Set of actions Sigma = {a1.inform, a2.inform, a1.ack, a2.ack}.##############
###############################################################################
phi1 = Automata.DFA(
['a1Inform', 'a2Inform', 'a1Ack', 'a2Ack'],

['q1', 'q0', 'q2'],

'q0',

lambda q: q in ['q0'],

lambda q, a: {
        ('q0', 'a1Inform') :'q1',
        ('q0', 'a2Inform') :'q0',
        ('q0', 'a1Ack') :'q0',
        ('q0', 'a2Ack') :'q0',
        ('q1', 'a1Inform') :'q1',
        ('q1', 'a2Inform') :'q1',
        ('q1', 'a1Ack') :'q0',
        ('q1', 'a2Ack') :'q0',
        ('q2', 'a1Inform') :'q2',
        ('q2', 'a2Inform') :'q2',
        ('q2', 'a1Ack') :'q2',
        ('q2', 'a2Ack') :'q2',
     }[(q, a)]
)
###############################################################################
#
#
###############################################################################
###Invoke the enforcer with properties psi, "phi = phi1", and some test input sequence #
######### (psi, phi, input sequence sigma)#######################################
###############################################################################
####Input sigma =  a1Inform. a2Inform.a1Ack #####
###############################################################################
EnforcerEval.enforcer(copy.copy(psi), copy.copy(phi1),  ['a1Inform', 'a2Inform', 'a1Ack' ] )
###############################################################################







