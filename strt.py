#************************************************************************
# String Templating Module
#
# Algorithms: 
#      +) DFA for pattern matching
#      +) DFS for Cycle Detection
#      +) Ordered Reduction of Parameter List
#
# Sept, 2017
#************************************************************************
#!/usr/bin/python

import re
import sys

regex ='(?<=\{{)(?!lb)\w+(?=\}})'

# States of DFA

START = 0
INI = 1
BEGIN = 2
CONSUME = 3
FIN = 4
EXIT =  5

#Test Cases
'''
print DFA('lb')
print DFA('{lb}')
print DFA('{{lb}}')
print DFA('{{a}}')
print DFA('{{ablb}}')
print DFA('{{ablb}')
print DFA('{{**k}}')
print DFA('{{**k}}{{ab}}abc')
print DFA('{{lb} var1}}{{var1}}')
print DFA('{{{{lb}}}}')
print DFA('{{lb}} {{lb}}')
'''

# Function : Performs Template base Substitution 
#            based on Finite State Automata
# @param : word
# @param : parameter dictionary 
# 
def DFA(word, pmap):
    value = ''
    string = ''
    stack = ''
    STATE = START
    for i in word:

       if STATE is START:
          value = '' 
          stack = ''
          if i is '{':
              stack += i
              STATE = INI
          else:
              string += i 

       elif STATE is INI:
          if i is '{':
              stack += i
              value = ''
              STATE = BEGIN
          else:
              string += '{' 
              string += i 
              STATE = START

       elif STATE is BEGIN:        
          if re.match('\w+', i) is not None:
               value += i
               stack += i
               STATE = CONSUME
          elif i is '{':
               string += stack 
               stack = i
               STATE = INI
          else:
               string += '{{'
               string += i
               STATE = START

       elif STATE is CONSUME:        
          if re.match('\w+', i) is not None:
               value += i
               stack += i
          elif i is '}':
               stack += i
               STATE = FIN
          elif i is '{':
               string += stack
               stack = i
               STATE = INI
          else:
               string += '{{'
               string += value
               string += i
               STATE = START

       elif STATE is FIN:
          if i is '}':
              if value == 'lb':
                 string += '{'
              elif value in pmap:
                 string += pmap[value]
              else:
                 string += ('{{' + value + '}}') 
          elif i is '{':
               string += stack
               stack = i
               STATE = INI
          else:
              string += '{{'
              string += value
              string += '}'
              string += i
          STATE = START

       else:
           assert 0

    if STATE is START:
       stack = ''

    if stack is not '':
       string += stack

    return string

#Function for DFS
#@param : node key
#@visited : visited list
#except : raises exception on Cycle Detection
#
def DFS(key, visited):
     global adj_list

     if key in visited:
         raise Exception('Cycle Detected')

     if key not in adj_list:
         #print 'Invalid key'
         return

     visited.append(key)
     for i in adj_list[key]:
         DFS(i, visited) 
         visited.append(i)

#Function to Detect Cycles
#@param : parameter dictionary
#except : raises exception on Cycle Detection
#
def DetectCycle(pmap):
    global adj_list

    adj_list = dict()
    
    for i in pmap:
       r = re.findall(regex, pmap[i])
       adj_list[i] = r

    #for i in adj_list:
    #    print i + ':' + str(adj_list[i])

    try:
       for i in adj_list:
           visited = []
           DFS(i, visited)
    except Exception, e:
       print str(e)
       sys.exit(1)
    
#Test Case for Cycle Detection
def TestSubstitute():
    global pmap

    pmap = dict()
    pmap['var1'] = 'value1 {{var2}}'
    pmap['var2'] = '{{lb}}{{lb}}var3}} equals {{var3}}'
    pmap['var3'] = 'value3'
    pmap['var4'] = '{{lb}}{{lb}}var1}}: "{{var1}}"'
    DetectCycle(pmap)

#Function for templatae substituition in a Sentence
#
def ProcessLine(line):
   global pmap

   new_string = ''
   string_list = line.split()
   start = True
   for i in string_list:
      if start is True: 
          start = False
      else:
          new_string += ' '
      new_string += DFA(i, pmap)
   return new_string   

#Driver Function for template substituition of Parameter List
#
def ReduceInOrder():
   global pmap
   global adj_list

   resolved_list = []
   unresolved_list = []

   for i in adj_list:
       unresolved_list.append(i)

   while len(unresolved_list) > 0:
      for i in unresolved_list:
         members = adj_list[i] 
         resolved = True
         if not members:
            resolved = True
         else:   
           for k in members:
              if k not in adj_list: 
                  continue
              if k not in resolved_list:
                  resolved = False
                  break
         
         if resolved is True:
           pmap[i] = ProcessLine(pmap[i]) 
           resolved_list.append(i)
           index = unresolved_list.index(i)
           del unresolved_list[index]

#TestSubstitute()
#ReduceInOrder()

#Driver Function to process parameter File
#
def ProcessParams(filename):
    global pmap
    pmap = dict()
    with open(filename) as f:
       for line in f:
          line = line.strip('\n')
          string_list = line.split(':',1)
          pmap[string_list[0]] = string_list[1]

    DetectCycle(pmap)
    #print 'No Cycle Detected'
    ReduceInOrder()
    #print '\n*******Substituted Params*********\n'
    #for i in pmap:
    #   print i + ':' + pmap[i]

#Driver Function to process Input File
#
def ProcessFile(filename):
    print "\n****** OUTPUT ******** \n"
    with open(filename) as fi:
       for line in fi:
          line = line.strip('\n')
          print ProcessLine(line)

def main():
    if len(sys.argv) < 3:
            print("Few parameters to Program")
            print ("Usage : cmd <input_file_name> <param_file_name>")
            sys.exit()
    ProcessParams(sys.argv[2])        
    ProcessFile(sys.argv[1])        

#Main Routine
main()    
