from collections import OrderedDict

 
def CheckTerminal(char): #check if is terminal
    if(char.isupper() or char == "^"):
        return False
    else:
        return True

def insert(gram, lhs, rhs):
    #Check if its terminal or non-terminal
     #append both (or) rhs together under the same non-termenal on the lhs 
    if(lhs in gram and rhs not in gram[lhs] and gram[lhs] != "null"):
        gram[lhs].append(rhs)
    elif(lhs not in gram or gram[lhs] == "null"): #incase there is a new non-terminal or first non-terminal
        gram[lhs] = [rhs]


    

    return gram
	
def Find_First(lhs, gram, grammar_first):
    Right_Hand_Side = gram[lhs]
    
    for i in Right_Hand_Side: # looping on all the rhs
        k = 0
        flag = 0
        current = []
        confirm = 0
        flog = 0
        if(lhs in gram and "^" in grammar_first[lhs]):
            flog = 1
        while(1):	
            check = []
            if(k>=len(i)):
                if(len(current)==0 or flag == 1 or confirm == k or flog == 1):
                  
                    grammar_first = insert(grammar_first, lhs, "^")
                  
                break				
            if(i[k].isupper()):
                if(grammar_first[i[k]] == "null"):
                  
                    #recursion after divining into the non-terminal to get its first return to the previous function with a solved non-terminal
                    grammar_first = Find_First(i[k], gram, grammar_first) 
                    

                for j in grammar_first[i[k]]:
                    
                    grammar_first = insert(grammar_first, lhs, j)
                    
                    check.append(j)
                    
            else:
                grammar_first = insert(grammar_first, lhs, i[k])
                check.append(i[k]) #i
                
            if(i[k]=="^"):
                flag = 1
            current.extend(check)
            
            if("^" not in check):
                if(flog == 1):
                    grammar_first = insert(grammar_first, lhs, "^")
                break
            else:
                confirm += 1
                k+=1
               
    return(grammar_first)

def rec_follow(k, next_i, grammar_follow, i, grammar, Start, grammar_first, lhs):
    if(len(k)==next_i):
        if(grammar_follow[i] == "null"):
            grammar_follow = follow(i, grammar, grammar_follow, Start)
        for x in grammar_follow[i]:
            grammar_follow = insert(grammar_follow, lhs, x)
    else:
        if(k[next_i].isupper()):
            for x in grammar_first[k[next_i]]:
                if(x=="^"):
                    grammar_follow = rec_follow(k, next_i+1, grammar_follow, i, grammar, Start, grammar_first, lhs)		
                else:
                    grammar_follow = insert(grammar_follow, lhs, x)
        else:
            grammar_follow = insert(grammar_follow, lhs, k[next_i])

    return(grammar_follow)

def follow(lhs, grammar, grammar_follow, start):
    for i in grammar:
        j = grammar[i]
        for k in j:
            if(lhs in k):
                next_i = k.index(lhs)+1
                grammar_follow = rec_follow(k, next_i, grammar_follow, i, grammar, start, Grammar_First, lhs)
    if(lhs==start):
        grammar_follow = insert(grammar_follow, lhs, "$")
    return(grammar_follow)

def show_dict(dictionary): #printing whats inside the grammar or first or follow in a readable way 
    for key in dictionary.keys():
        print(key+"  :  ", end = "")
        for item in dictionary[key]:
            if(item == "^"):
                print("Epsilon, ", end = "")
            else:
                print(item+", ", end = "")
        print("\b\b")

def get_rule(NON_Term, Term, grammar, grammar_first):
     #getting the Right hand side of each non terminal also looping on all of the non terminal one by one 
    for rhs in grammar[NON_Term]:
        #print(rhs) #cheking what is in the right hand side
        for rule in rhs: #looping on the first element of each right hand side
            
            if(rule == Term): # if the rule is terminal 
                string = NON_Term+"="+rhs
                return string
            #if rule is non-terminal and the terminal is in the grammer first of this non-terminal call all of this production 
            elif(rule.isupper() and Term in grammar_first[rule]): 
                string = NON_Term+"="+rhs
                return string
                
def Generate_Table(Term, NON_Term, grammar, grammar_first, grammar_follow):
    Parse_Table = [[""]*len(Term) for i in range(len(NON_Term))]
    
    for non_term in NON_Term:
        for term in Term:
            if term in grammar_first[non_term]: #if the terminal exist in the grammar first 
                rule = get_rule(non_term, term, grammar, grammar_first) #get the rule of this non_terminal
                
                
            elif("^" in grammar_first[non_term] and term in grammar_follow[non_term]):
                rule = non_term+"=^"
                
            else:
                rule = ""
                
            Parse_Table[NON_Term.index(non_term)][Term.index(term)] = rule
    return(Parse_Table)

def parsing_table(parse_table, Term, NON_Term):
    print("\t\t\t\t",end = "") 
    for terminal in Term: 
        print(terminal+"\t\t", end = "") #printing the terminals
    print("\n\n")
    
    for non_terminal in NON_Term: 
        print("\t\t"+non_terminal+"\t\t", end = "") #printing the non-terminals
        for terminal in Term:
            #printing the grammer in the parsing table 
            print(parse_table[NON_Term.index(non_terminal)][Term.index(terminal)]+"\t\t", end = "")
        print("\n")


def STRING_Parsing(expr, parse_table, terminals, non_terminals):
    stack = ["$"]
    stack.insert(0, non_terminals[0])
    print("\t\t\tMatched\t\t\tStack\t\t\tInput\t\t\tAction\n")
    print("\t\t\t-\t\t\t", end = "")
    for i in stack:
        print(i,  end = "")
    print("\t\t\t", end = "")
    print(expr+"\t\t\t", end = "")
    print("-")

    matched = "-"
    while(True):
        action = "-"

        if(stack[0] == expr[0] and stack[0] == "$"): # if $ is found break out as this string is accepted 
            break

        elif(stack[0] == expr[0]): # the one for poping if found a match
            if(matched == "-"):
                matched = expr[0]
            else:    
                matched = matched + expr[0]
            action = "Matched "+expr[0]
            expr = expr[1:] #all but the first one 
            stack.pop(0)

        else:
            #getting the array inside of the array which is the expresion 
            action = parse_table[non_terminals.index(stack[0])][terminals.index(expr[0])] 
            stack.pop(0)
            i = 0
            for item in action[2:]:
                if(item != "^"):
                    stack.insert(i,item)
                i+=1

        print("\t\t\t"+matched+"\t\t\t", end = "")
        for i in stack:
            print(i,  end = "")
        print("\t\t\t", end = "")
        print(expr+"\t\t\t", end = "")
        print(action)





#################################       Main        #################################





Grammar = OrderedDict()
Grammar_First = OrderedDict()
Grammar_Follow = OrderedDict()

Grammar_File = open('grammar1.txt')
#loop i line by line in grammar then append it together side by side
for i in Grammar_File: 
    i = i.replace("\n", "")
    Left_Hand_Side = ""
    Right_Hand_Side = ""
    flag = 1
    for j in i: #loop the very line and see who is the lhs and who is the rhs
        if(j=="="):
            flag = 0
            continue
        if(flag==1):
            Left_Hand_Side = Left_Hand_Side + j
        else:
            Right_Hand_Side = Right_Hand_Side + j
            
    Grammar = insert(Grammar, Left_Hand_Side, Right_Hand_Side)
    Grammar_First[Left_Hand_Side] = "null" #putting null in order to later on replace the null with the right answer in first
    Grammar_Follow[Left_Hand_Side] = "null" #putting null in order to later on replace the null with the right answer in follow

print("Grammar\n")
show_dict(Grammar)

for lhs in Grammar: #loop on the empty lhs to find each first of each terminal
    if(Grammar_First[lhs] == "null"):
        Grammar_First = Find_First(lhs, Grammar, Grammar_First)
        
print("\n\n\n")
print("First\n")
show_dict(Grammar_First)


start = list(Grammar.keys())[0]
for lhs in Grammar:
    if(Grammar_Follow[lhs] == "null"):
        Grammar_Follow = follow(lhs, Grammar, Grammar_Follow, start)
        
print("\n\n\n")
print("Follow\n")
show_dict(Grammar_Follow)


NON_Term = list(Grammar.keys())
Term = []
for i in Grammar:
    for rule in Grammar[i]: #looping on the rhs of the grammar
        for char in rule: #looping in each char in the rhs
            
            if(CheckTerminal(char) and char not in Term): #checking on all of the terminals and putting them in one variable 
                Term.append(char)

Term.append("$")




print("\n\n\n\n\t\t\t\t\t\t\tParse Table\n\n")
ParsingTable = Generate_Table(Term, NON_Term, Grammar, Grammar_First, Grammar_Follow)
parsing_table(ParsingTable, Term, NON_Term)


Test_Expr = "(a+a)$"

print("\n\n\n\n\n\n")
print("\t\t\t\t\t\t\tParsing\n\n")
STRING_Parsing(Test_Expr, ParsingTable, Term, NON_Term)