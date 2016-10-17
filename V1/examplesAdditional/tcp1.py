#######imports###########
import sys
sys.path.append("../")
import Enforcer
import EnforcerEval
import Automata
import copy
#########################

#########################################################################################
### Model of TCP protocol connection ####################################################
#####(Reference Paper: "Protocol-based Testing of Firewalls".)###########################
### Defines DFA describing input property psi ###########################################
######### (actions, states, initial state, final states, transition function)############
##### Set of actions Sigma = {S: request to open a connection, ##########################
#############SA: agree to open a connection, A: acknowledge of receipt, F1: request to close a connection,
############# F2: request to close a connection, R: tear down connection, Ot: other}######
##### Set of states Q = {L:listen, CR: Connection Requested, CE: Connection established,
########################## DT: data transfer, CL: Closing, CLD: Closed, FA: Failure}#####
#########################################################################################
#########################################################################################
psi = Automata.DFA(
# actions
['S', 'SA', 'A', 'F1', 'F2', 'R', 'Ot'],
# locations
['L', 'CR', 'CE', 'DT', 'CL', 'CLD', 'FA'],
# initial location
'L',
# accepting locations
lambda q: q in ['CLD'],
# transitions
lambda q, a: {
        ('L', 'S') : 'CR',
        ('L', 'SA') : 'FA',
        ('L', 'A') : 'FA',
        ('L', 'F1') : 'FA',
        ('L', 'F2') : 'FA',
        ('L', 'R') : 'FA',
        ('L', 'Ot') : 'FA',

        ('CR', 'S') : 'CR',
        ('CR', 'SA') : 'CE',
        ('CR', 'A') : 'FA',
        ('CR', 'F1') : 'FA',
        ('CR', 'F2') : 'FA',
        ('CR', 'R') : 'FA',
        ('CR', 'Ot') : 'FA',        
 
        ('CE', 'S') : 'CE',
        ('CE', 'SA') : 'CE',
        ('CE', 'A') : 'DT',
        ('CE', 'F1') : 'FA',
        ('CE', 'F2') : 'FA',
        ('CE', 'R') : 'FA',
        ('CE', 'Ot') : 'FA',        
    
        ('DT', 'S') : 'FA',
        ('DT', 'SA') : 'FA',
        ('DT', 'A') : 'DT',
        ('DT', 'F1') : 'CL',
        ('DT', 'F2') : 'FA',
        ('DT', 'R') : 'CLD',
        ('DT', 'Ot') : 'FA',  
    
        ('CL', 'S') : 'FA',
        ('CL', 'SA') : 'FA',
        ('CL', 'A') : 'CL',
        ('CL', 'F1') : 'CL',
        ('CL', 'F2') : 'CLD',
        ('CL', 'R') : 'CLD',
        ('CL', 'Ot') : 'FA',  
        
        ('CLD', 'S') : 'FA',
        ('CLD', 'SA') : 'FA',
        ('CLD', 'A') : 'CLD',
        ('CLD', 'F1') : 'CLD',
        ('CLD', 'F2') : 'CLD',
        ('CLD', 'R') : 'CLD',
        ('CLD', 'Ot') : 'FA',  
        
        ('FA', 'S') : 'FA',
        ('FA', 'SA') : 'FA',
        ('FA', 'A') : 'FA',
        ('FA', 'F1') : 'FA',
        ('FA', 'F2') : 'FA',
        ('FA', 'R') : 'FA',
        ('FA', 'Ot') : 'FA',  
    }[(q, a)]
)
###############################################################################

###############################################################################
###Define DFA describing property to enforcer phi##############################
##Property is: "Each connection should start with S. At most 4 consecutive S actions are allowed."##
######### (actions, states, initial state, final states, transition function)##
###Set of actions Sigma = {'S', 'SA', 'A', 'F1', 'F2', 'R', 'Ot'}.##############
###############################################################################
phi1 = Automata.DFA(
['S', 'SA', 'A', 'F1', 'F2', 'R', 'Ot'],

['l0', 'l1', 'l2', 'l3', 'l4', 'l5' ],

'l0',

lambda q: q in ['l0'],

lambda q, a: {
        
        ('l0', 'S') : 'l1',
        ('l0', 'SA') : 'l5',
        ('l0', 'A') : 'l5',
        ('l0', 'F1') : 'l5',
        ('l0', 'F2') : 'l5',
        ('l0', 'R') : 'l5',
        ('l0', 'Ot') : 'l5',
        
        ('l1', 'S') : 'l2',
        ('l1', 'SA') : 'l0',
        ('l1', 'A') : 'l0',
        ('l1', 'F1') : 'l0',
        ('l1', 'F2') : 'l0',
        ('l1', 'R') : 'l0',
        ('l1', 'Ot') : 'l0',
        
        ('l2', 'S') : 'l3',
        ('l2', 'SA') : 'l0',
        ('l2', 'A') : 'l0',
        ('l2', 'F1') : 'l0',
        ('l2', 'F2') : 'l0',
        ('l2', 'R') : 'l0',
        ('l2', 'Ot') : 'l0',

        ('l3', 'S') : 'l4',
        ('l3', 'SA') : 'l0',
        ('l3', 'A') : 'l0',
        ('l3', 'F1') : 'l0',
        ('l3', 'F2') : 'l0',
        ('l3', 'R') : 'l0',
        ('l3', 'Ot') : 'l0',

        ('l4', 'S') : 'l5',
        ('l4', 'SA') : 'l0',
        ('l4', 'A') : 'l0',
        ('l4', 'F1') : 'l0',
        ('l4', 'F2') : 'l0',
        ('l4', 'R') : 'l0',
        ('l4', 'Ot') : 'l0',

        ('l5', 'S') : 'l5',
        ('l5', 'SA') : 'l5',
        ('l5', 'A') : 'l5',
        ('l5', 'F1') : 'l5',
        ('l5', 'F2') : 'l5',
        ('l5', 'R') : 'l5',
        ('l5', 'Ot') : 'l5',
     }[(q, a)]
)
###############################################################################
#
###############################################################################
###Invoke the enforcer with properties psi, phi, and some test input sequence #
######### (psi, phi, input sequence sigma)#######################################
###############################################################################

####Input sigma =  'S'. 'SA'. 'A'. 'F1'. 'F2'  #####
print "input sequence is 'S', 'SA', 'A', 'F1', 'F2'  "  
EnforcerEval.enforcer(copy.copy(psi), copy.copy(phi1), ['S', 'SA', 'A', 'F1', 'F2' ])
print "######################" 
###############################################################################









