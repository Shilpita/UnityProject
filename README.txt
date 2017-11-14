1. strt.py accepts two arguments:
        -Name of the Input text file to be reduced
        -Name of the Paramter text file where variable values are given

2. Compile and run the code as python script
      $ python strt.py InputText.txt Param.txt

3. InputText.txt ,Param.txt and ParamCycle.txt files cover all the test cases as mentioned in the instruction documents.
   Param.txt does not contain any cycles in the variable references.
   ParamCycle.txt contains a cyclic variable reference.

4. $ python strt.py InputText.txt Param.txt
    ****** OUTPUT ********

    value1 {{var3}} equals value3 is good. value3 {{var1}}: "value1 {{var3}} equals value3", and value5 even : can be used here are awesome.
    test escaped braces: {{var3}}
    vars{{var7}} doesnt exist!workswithoutspaces.
    Hello again {{var3}} equals value3 and value1 {{var3}} equals value3. {{var8}}
    {{var3}}
    {{lb var2}}
    {{lb}}


5. $ python strt.py InputText.txt ParamCycle.txt
****** OUTPUT ********
   Cycle Detected
Process finished with exit code 1

