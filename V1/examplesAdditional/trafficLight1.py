#######imports###########
import sys
sys.path.append("../")
import Enforcer
import EnforcerEval
import Automata
import copy
#########################

#########################################################################################
### Model of a "simple" traffic light controller program ################################
### (Defines DFA describing input property psi) #########################################
######### (actions, states, initial state, final states, transition function)############
##### Set of actions Sigma = {'R: red', 'G: green', 'O: orange'} ########################
##### This DFA defines ((R.G.O)*| (G.O.R)* | (O.R.G)*) ################################## 
#########################################################################################

psi = Automata.DFA(
# actions
['red', 'green', 'orange'],
# locations
['q0', 'qr1', 'qr2', 'qrA3', 'qg1', 'qg2', 'qgA3', 'qo1', 'qo2', 'qoA3', 'qTR'],
# initial location
'q0',
# accepting locations
lambda q: q in ['q0',  'qrA3', 'qgA3', 'qoA3'],
# transitions
lambda q, a: {
        ('q0', 'red') : 'qr1',
        ('q0', 'green') : 'qg1',
        ('q0', 'orange') : 'qo1',
       
        ('qr1', 'green') : 'qr2',
        ('qr1', 'red') : 'qTR',
        ('qr1', 'orange') : 'qTR',

        ('qr2', 'green') : 'qTR',
        ('qr2', 'red') : 'qTR',
        ('qr2', 'orange') : 'qrA3',

        ('qrA3', 'green') : 'qTR',
        ('qrA3', 'red') : 'qr1',
        ('qrA3', 'orange') : 'qTR',
 
        ('qg1', 'green') : 'qTR',
        ('qg1', 'red') : 'qTR',
        ('qg1', 'orange') : 'qg2',

        ('qg2', 'green') : 'qTR',
        ('qg2', 'red') : 'qgA3',
        ('qg2', 'orange') : 'qTR',

        ('qgA3', 'green') : 'qg1',
        ('qgA3', 'red') : 'qTR',
        ('qgA3', 'orange') : 'qTR',

        ('qo1', 'green') : 'qTR',
        ('qo1', 'red') : 'qo2',
        ('qo1', 'orange') : 'qTR',

        ('qo2', 'green') : 'qoA3',
        ('qo2', 'red') : 'qTR',
        ('qo2', 'orange') : 'qTR',

        ('qoA3', 'green') : 'qTR',
        ('qoA3', 'red') : 'qTR',
        ('qoA3', 'orange') : 'qo1',
        
        ('qTR', 'red') : 'qTR',
        ('qTR', 'green') : 'qTR',
        ('qTR', 'orange') : 'qTR',    
    }[(q, a)]
)

###############################################################################
###Define DFA describing property to enforcer phi1##############################
######### (actions, states, initial state, final states, transition function)##
## This DFA defines property "Sequence should start with "red". 
###Set of actions Sigma = {red, green, orange}.################################
###############################################################################
phi1 = Automata.DFA(
['red', 'green', 'orange'],
['q0', 'q1', 'qTR' ],
'q0',
lambda q: q in ['q0', 'q1'],
lambda q, a: {
        ('q0', 'red') :'q1',
        ('q0', 'green') :'qTR',
        ('q0', 'orange') :'qTR',
        
        ('q1', 'red') :'q1',
        ('q1', 'green') :'q1',
        ('q1', 'orange') :'q1',
        
        ('qTR', 'red') :'qTR',
        ('qTR', 'green') :'qTR',
        ('qTR', 'orange') :'qTR',
     }[(q, a)]
)
##################################################################################

###############################################################################
###Invoke the enforcer with properties psi, phi, and some test input sequence #
######### (psi, phi, input sequence sigma)#######################################
###############################################################################
EnforcerEval.enforcer(copy.copy(psi), copy.copy(phi1),  ['red', 'green', 'orange' ] )









