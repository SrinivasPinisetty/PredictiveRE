=============================================
Predictive Runtime Enforcement
=============================================
-= About =-

- Module "Automata.py" contains all the functionality related to defining DFAs, operations on DFAs, 
  and functionality for checking language inclusion of DFAs etc.
- Module "Enforcer.py" contains implementation of predictive enforcement algorithm. 
- Module "EnforcerEval.py" contains implementation of predictive enforcement algorithm with some additional code for performance evaluation. 

- The directory /examplesUsage/ contains a couple of simple examples. These examples illustrate how to define DFAs (phi and psi), 
  and invoking enforcer with some input sequences, and check the input-output behaviour of the enforcer.      

- The directory /examplesAdditional/ contains all the examples that were used for evaluating the performance 
   (NOTE: naming of each example in this directory corresponds to the naming used in the evaluation table/section in the paper).
- In the directories containing examples (/examplesUsage/ and /examplesAdditional/), in each example file, 
   documentation/notes about properties is provided. 


-= INSTALLATION =-

1. Install Python.

-= USAGE =-

1. To run the examples in /examplesUsage/ directory (or in /examplesAdditional/ directory) via command prompt, go to /examplesUsage/ directory (or examplesAdditional/ directory), 
and you can invoke each script in this directory. 
For example if test1.py is under the directory /examplesUsage, you can invoke it using command "python test1.py".

2. If you prepare more examples, please add them under /examplesAdditional directory. 
Please see one of the examples in /tests directory to follow how to define intended DFAs, how to invoke the enforcer method etc.

3. If you find some issues, please describe them in BUGS.txt file available in this directory.




