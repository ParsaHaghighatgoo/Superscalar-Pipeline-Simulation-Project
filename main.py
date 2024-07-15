# Parsa Haghighatgoo
# 40030644

# stall in table = st


# todo
# table
# mem
# alu
# tozihat va commnet v doc
# bouns va branch
# final valuse memory and regs
# note memory read or write
# display ex
# report decoded section
# report fetch section


def stallFetch(pipOut):
    nStart = 0
    clockcyle = 0
    for pip in pipOut:
        if (len(pip) > clockcyle):
            clockcyle = len(pip)
    for i in range(1, clockcyle + 1):
        for pip in pipOut:
            if i < 2:
                if pip[i - 1] == "IF":
                    nStart += 1
            else:
                if pip[i - 1] == "IF" or (pip[i - 1] == "st" and pip[i - 2] == "IF"):
                    nStart += 1
        if nStart < 3:
            return i
        else:
            nStart = 0
    return nStart


def stallDecode(pipOut, start):
    nStart = 0
    clockcyle = 0
    for pip in pipOut:
        if (len(pip) > clockcyle):
            clockcyle = len(pip)
    for i in range(start+1, clockcyle + 1):
        for pip in pipOut:
            if i < 2:
                if pip[i - 1] == "ID":
                    nStart += 1
            else:
                if i<len(pip):
                    if pip[i - 1] == "ID" or (pip[i - 1] == "st" and pip[i - 2] == "ID"):
                        nStart += 1
                else:
                    continue
        if nStart < 2:
            return i
        else:
            nStart = 0
    return nStart


def hazard(input, index, inputList):
    flagr1 = 0
    if input[2] == inputList[index - 2][1]:
        flagr1 = 1
    elif input[3] == inputList[index - 2][1]:
        flagr1 = 1
    return flagr1


def pipline(input, index, inputList, pipOut):
    output = []
    if index == 1:
        # output = "IF |ID |EX |ME |WB"
        output.append("IF")
        output.append("ID")
        output.append("EX")
        output.append("ME")
        output.append("WB")

    elif index == 2:
        flagH = hazard(input, index, inputList)
        if flagH == 1:
            # output = "IF |ID |st |EX |ME |WB"
            output.append("IF")
            output.append("ID")
            output.append("st")
            output.append("EX")
            output.append("ME")
            output.append("WB")
        else:
            # output = "IF |ID |EX |ME |WB"
            output.append("IF")
            output.append("ID")
            output.append("EX")
            output.append("ME")
            output.append("WB")
    else:
        flagF = stallFetch(pipOut)
        flagH = hazard(input, index, inputList)
        if flagF > 1:
            for i in range(flagF - 1):
                output.append("st")
        output.append("IF")
        start = len(output)
        flagD = stallDecode(pipOut, flagF)
        dstalls = flagD - len(output) - 1
        if dstalls > 0:
            for i in range(dstalls):
                output.append("st")
        output.append("ID")
        if flagH == 1:
            output.append("st")
        output.append("EX")
        output.append("ME")
        output.append("WB")

    return output


# file path
file_path = "pp.txt"

# open file for reading it
with open(file_path, 'r') as file:
    code = file.read()
lines = code.splitlines()
inputList = []
pipOut = []

# iterate the input file
for line in lines:
    input = line.split(" ")
    ins = input[0]
    args = input[1].split(",")
    listCons = []
    listCons.append(ins)
    listCons.append(args[0])
    listCons.append(args[1])
    listCons.append(args[2])
    inputList.append(listCons)

print(inputList)
for i in inputList:
    index = inputList.index(i) + 1
    output = pipline(i, index, inputList, pipOut)
    pipOut.append(output)
i = 1
for pip in pipOut:
    print(i)
    print(pip)
    i += 1

