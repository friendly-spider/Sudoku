import copy
import csv
import sys
import os

# Opening sudoku from file
def take_sudoku():
    global ini_sudoku
    ini_sudoku = []
    diff_list=['Easy','Medium','Hard','Expert','Legendary']
    print("Difficulties available: ", diff_list)
    difficulty = input("Select difficulty: ")
    file = '{}.csv'.format(difficulty.lower())
    if not os.path.isfile(file):
        sys.exit("Difficulty not found.")
    with open(file) as file:
        reader = csv.reader(file)
        for row in reader:
            count = 0
            for i in row:
                if int(i) not in range(10):
                    sys.exit("The entered sudoku is invalid.(Found {} in sudoku)".format(i))
                row[count] = int(i)
                del i   
                count += 1
            ini_sudoku.append(row)
    for i in ini_sudoku:
        if len(ini_sudoku) != 9 or len(i) != 9:
            sys.exit("Invalid number of rows or columns in sudoku.")

# Check if the attempted position is valid
def validity(inp_sudoku,b,coord):
    row,col = coord
    inp_sudoku[row][col] = b
    # Check if there is repeated number in row
    a = []
    for i in inp_sudoku[row]:
        if i in a:
            inp_sudoku[row][col] = 0
            return False
        elif i != 0:
            a.append(i)
        
    # Check if there is repeated number in column
    a = []
    for i in range(len(inp_sudoku)):
        if inp_sudoku[i][col] in a:
            inp_sudoku[row][col] = 0
            return False
        elif inp_sudoku[i][col] != 0:
            a.append(inp_sudoku[i][col])

    # Check if there is repeated number in box
    box_row = row//3
    box_col = col//3
    a = []
    for i in range(box_row*3,box_row*3+3):
        for j in range(box_col*3,box_col*3+3):
            if inp_sudoku[i][j] in a:
                inp_sudoku[row][col] = 0
                return False
            elif inp_sudoku[i][j] != 0:
                a.append(inp_sudoku[i][j])
            
    inp_sudoku[row][col] = 0
    return True

# Display sudoku
def make_sudoku(inp_sudoku):
    print("    A B C   D E F   G H I")
    print("   _______________________")
    for i in range(len(inp_sudoku)):
        print(i+1, "|", end = " ")
        for j in range(len(inp_sudoku[i])):
            if inp_sudoku[i][j] != 0:
                print(inp_sudoku[i][j],end = " ")
            else:
                print("_",end = " ")
            if (j+1)%3 == 0 and j != 8:
                print("|",end=" ")
        print()
        if (i+1)%3 == 0 and i != 8:
            print("  |","-"*22)
    print()

# Finding blank spaces
def blanks(inp_sudoku):
    for i in range(len(inp_sudoku)):
        for j in range(len(inp_sudoku)):
            if inp_sudoku[i][j] == 0:
                return (i,j)
    return False

# Solving by recursion
def solve(inp_sudoku):
    blank = blanks(inp_sudoku)
    if not blank:
        return True
    else:
        row,col = blank
    for i in range(1,10):
        if validity(inp_sudoku,i,blank):
            inp_sudoku[row][col] = i
            if solve(inp_sudoku):
                return True
            inp_sudoku[row][col] = 0
                
    return False

# Creating a dictionary of possible numbers for each coordinate
def find_lops(inp_sudoku):
    global lops
    lops = {}
    for i in range(len(inp_sudoku)):
        for j in range(len(inp_sudoku[i])):
            if inp_sudoku[i][j] == 0:
                pos = []
                for k in range(1,10):
                    if validity(inp_sudoku,k,(i,j)):
                        pos.append(k)
                if len(pos) != 0:
                    lops[(i,j)] = pos       #row,col

# Initialise sudoku
def initial():
    take_sudoku()
    print("Given sudoku:")
    make_sudoku(ini_sudoku)
    
    global solved_sudoku
    solved_sudoku = copy.deepcopy(ini_sudoku)
    print("Loading...\n")
    solve(solved_sudoku)
    if blanks(solved_sudoku):
        sys.exit("The entered sudoku is invalid.(No valid solution)")

# Playing sudoku
def menu():
    strikes = 0
    print("\nINSTRUCTIONS:   1. Enter coordinates eg: A1, B5, F3, etc. (or a command)\n\t\t2. Enter a number.\nCommands available: Hint, Exit")
    while blanks(test_sudoku):
        print()
        coord = input("Enter coordinates: ")
        if coord.lower() == 'exit':
            break
        elif coord.lower() == 'hint':
            coord = input("Enter coordinates to use hint on: ")
            row = int(coord[1])-1
            col = ord(coord[0].upper())-ord('A')
            print("HINT: {} Can have values: {}\n".format(coord,lops[(row,col)]))
        elif len(coord) != 2 or not coord[0].isalpha() or not coord[1].isdigit(): # Validity check 1
            print("Enter coordinates like A1, B5, F3, etc.")
            continue
        row = int(coord[1])-1
        col = ord(coord[0].upper())-ord('A')
        if row not in range(9) or col not in range(9) or test_sudoku[row][col] != 0: # Validity check 2
            print("Please select a valid cell")
            continue
        else: # If coord is valid
            try:
                num = int(input("Enter a number from 1-9: "))
            except ValueError:
                print("Invalid number")
                continue
            if num not in range(10):
                print("Invalid number")
                continue
            elif solved_sudoku[row][col] == num: # If correct guess
                print("Correct!")
                test_sudoku[row][col] = num
                find_lops(test_sudoku)
                make_sudoku(test_sudoku)
            else:   # If incorrect guess
                print("Incorrect.")
                strikes += 1
                if num not in lops[(row,col)]:
                    print("HINT: {} Can have values: {}".format(coord,lops[(row,col)]))
    else:
        print("Congratulations! You have completed the sudoku with {} mistakes.".format(strikes))



# Main loop
initial()
inp = 0
while inp != 4:
    try:
        inp = int(input("Enter the corresponding number to:\n1. Play sudoku\n2. Change difficulty\n3. View solution\n4. Quit\n>>> "))
    except ValueError:
        print("Please enter the number corresponding to your choice.")
        continue
    if inp == 1:
        test_sudoku = copy.deepcopy(ini_sudoku)
        find_lops(test_sudoku)
        menu()
    elif inp == 2:
        initial()
    elif inp == 3:
        print("Solved sudoku:")
        make_sudoku(solved_sudoku)
        inp = 4
    elif inp != 4:
        print("Invalid choice\n")
