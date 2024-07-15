from colorama import init, Fore, Style

# Initialize colorama
init()

# Define the initial register values
registers = {
    "$s1": -10,
    "$s2": -10,
    "$s3": -10,
    "$s4": -10,
    "$s5": -10,
    "$s6": -10,
    "$s7": -10,
    "$t4": -10
}


def stallFetch(pipOut):
    nStart = 0
    clockcyle = 0
    for pip in pipOut:
        if len(pip) > clockcyle:
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
        if len(pip) > clockcyle:
            clockcyle = len(pip)
    for i in range(start + 1, clockcyle + 1):
        for pip in pipOut:
            if i < 2:
                if pip[i - 1] == "ID":
                    nStart += 1
            else:
                if i < len(pip):
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
        output.append("IF")
        output.append("ID")
        output.append("EX")
        output.append("ME")
        output.append("WB")
    elif index == 2:
        flagH = hazard(input, index, inputList)
        if flagH == 1:
            output.append("IF")
            output.append("ID")
            output.append("st")
            output.append("EX")
            output.append("ME")
            output.append("WB")
        else:
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


def execute_instruction(instruction):
    global registers
    op, args = instruction[0], instruction[1:]
    if op == "sub":
        test = registers[args[1]]
        test2 = registers[args[2]]
        registers[args[0]] = registers[args[1]] - registers[args[2]]
    elif op == "ori":
        registers[args[0]] = registers[args[1]] | int(args[2].replace("#", ""))
    elif op == "lw":
        # Simulating a memory read, using args[2] as base register and immediate offset
        registers[args[0]] = registers[args[2]] + int(args[1].replace("#", ""))
    elif op == "add":
        registers[args[0]] = registers[args[1]] + registers[args[2]]


def print_pipeline_output(pipOut):
    # Find the maximum length of any pipeline stage to align columns
    max_length = max(len(pip) for pip in pipOut)

    # Color map
    color_map = {
        "IF": Fore.GREEN,
        "ID": Fore.YELLOW,
        "EX": Fore.CYAN,
        "ME": Fore.MAGENTA,
        "WB": Fore.BLUE,
        "st": Fore.RED
    }

    # Print header
    header = "Cycle".ljust(6) + " | " + " | ".join([f"Stage {i + 1}".ljust(4) for i in range(max_length)])
    print(header)
    print("-" * len(header))

    # Print each pipeline stage
    for i, pip in enumerate(pipOut, start=1):
        cycle_str = str(i).ljust(6)
        stages_str = " | ".join([color_map.get(stage, "") + stage.ljust(4) + Style.RESET_ALL for stage in pip])
        print(f"{cycle_str} | {stages_str}")


def print_register_values():
    print("\nFinal Register Values:")
    for reg, val in registers.items():
        print(f"{reg}: {val}")


# file path
file_path = "C:\\Users\\beta\\Downloads\\pp.txt"

# Open file for reading
with open(file_path, 'r') as file:
    code = file.read()
lines = code.splitlines()
inputList = []
pipOut = []

# Iterate the input file
for line in lines:
    input = line.split(" ")
    ins = input[0]
    args = input[1].split(",")
    listCons = [ins, args[0], args[1], args[2]]
    inputList.append(listCons)

for i in inputList:
    index = inputList.index(i) + 1
    output = pipline(i, index, inputList, pipOut)
    pipOut.append(output)
    execute_instruction(i)

# Print the pipeline output beautifully
print_pipeline_output(pipOut)

# Print final register values
# print_register_values()
