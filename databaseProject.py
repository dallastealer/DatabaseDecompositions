import re


def containsAll(str, set):
    return 0 not in [c in str for c in set]


def bcnf(relation, dep, newRelations):
    # GET RID OF UNWANTED CHARACTERS IN INPUTTED RELATION
    relationStripped = relation
    for c in [',', '(', ')', ' ']:
        relationStripped = relationStripped.replace(c, '')
    relationStripped = sorted(relationStripped)
    relationStripped = ''.join(relationStripped)
    print(f"\nRELATION PASSED INTO FUNCTION IS {relationStripped}\n")
    # NEEDED VARIABLES TO MAKE SURE ONLY FINAL DECOMPOSITIONS ARE APPENDED
    splitHappened = False
    potentialAdditions = []
    # CHECK IF CLOSURE OF RHS IS SUPERKEY
    for lhs in dep.keys():
        counter = 0
        closure = lhs
        while counter < len(dep):
            for compLHS in dep.keys():
                if compLHS in closure and dep[compLHS] not in closure:
                    closure += dep[compLHS]
            counter += 1
        closure = sorted(closure)
        closure = ''.join(closure)
        if closure != relationStripped:
            splitHappened = True
            # SPLITTING IF CLOSURE IS NOT SUPERKEY
            splitLeft = closure
            splitRight = lhs
            for i in relationStripped:
                if i not in closure and i not in lhs:
                    splitRight += i
            splitLeft = ''.join(sorted(splitLeft))
            splitRight = ''.join(sorted(splitRight))
            print(
                f"{lhs} caused split left into {splitLeft} and right into {splitRight}")
            # FINDING WHICH DEPENDENCIES ARE ASSOCIATED WITH EACH SPLIT
            rightDep = {}
            leftDep = {}
            for d in dep.keys():
                fullDependency = d + dep[d]
                if containsAll(splitLeft, set(fullDependency)):
                    print(
                        f"DEPENDENCY {d} -> {dep[d]} PRESERVED IN LEFT SPLIT")
                    leftDep[d] = dep[d]
                elif containsAll(splitRight, set(fullDependency)):
                    print(
                        f"DEPENDENCY {d} -> {dep[d]} PRESERVED IN RIGHT SPLIT")
                    rightDep[d] = dep[d]
                else:
                    print(f"FUNCTIONAL DEPENDENCY {d} -> {dep[d]} WAS LOST")
            # RUN BCNF RECURSIVELY
            if len(leftDep) > 0:
                bcnf(splitLeft, leftDep, newRelations)
            else:
                newRelations.append(splitLeft)
            if len(rightDep) > 0:
                bcnf(splitRight, rightDep, newRelations)
            else:
                newRelations.append(splitRight)
            break
        else:
            print(f"RELATION {lhs} -> {dep[lhs]} PRODUCES A SUPERKEY")
            potentialAdditions.append(relationStripped)
    if not splitHappened:
        for i in potentialAdditions:
            newRelations.append(i)
    return newRelations


# THIS IS WHERE 3NF DECOMPOSITION CODE WILL GO
""" def findKeys(relation, dep):
    relationStripped = relation
    for c in [',', '(', ')', ' ']:
        relationStripped = relationStripped.replace(c, '')
    relationStripped = sorted(relationStripped)
    relationStripped = ''.join(relationStripped)
    # CHECK FOR WHICH ATTRIBUTES MUST BE PRESENT IN KEYS
    neededAtts = []
    attsInKeys = ""
    for lhs in dep.keys():
        attsInKeys += dep[lhs]
    for c in relationStripped:
        if c not in attsInKeys:
            neededAtts.append(c)
    foundSuperKeys = [] """


# Get user input
print('INPUT YOUR RELATION')
print('EXAMPLE FORMAT: (A, B, C, D)')

relation = input()

numOfDep = int(input("\nINPUT NUMBER OF FUNCTIONAL DEPENDENCIES: "))

print('INPUT FUNCTIONAL DEPENDENCIES')
funcDep = {}

for i in range(numOfDep):
    print('\nINPUT LEFT HAND SIDE')
    print('EXAMPLE FORMAT: A or AB\n')
    LHS = input()
    LHS = ''.join(sorted(LHS))
    print('\nINPUT RIGHT HAND SIDE\n')
    RHS = input()
    RHS = ''.join(sorted(RHS))
    funcDep[LHS] = RHS

print('\nYOUR RELATION AND FUNCTIONAL DEPENDENCIES\n')
print("R" + relation + '\n')
for i in funcDep.keys():
    print(f"{i} -> {funcDep[i]}")

decompMethod = int(
    input('\nCHOOSE YOUR ALGORITHM\n1. Boyce-Codd Normal Form\n2.Third Normal Form\n(INPUT 1 OR 2)'))
if decompMethod == 1:
    test = []
    answer = bcnf(relation, funcDep, test)
    print("\nTHE BCNF DECOMPOSITION RESULTED IN\n")
    for i in range(len(answer)):
        formattedAnswer = re.sub(r'([A-Z])(?!$)', r'\1, ', answer[i])
        print(f"R{i+1}({formattedAnswer})\n")
elif decompMethod == 2:
    pass
    #threeNF(relation, funcDep)

    # ask if they want DCFM or 3NF

    # Produce output
