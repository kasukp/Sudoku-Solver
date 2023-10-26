from time import perf_counter


def get_sudoku():
    """ Gets Sudoku board from string of 81 digits. """
    while True:
        sudoku_numbers = input("Please enter all 81 "
                                "digits of sudoku in a single line: \n"
                                "(Left to right, top to bottom, "
                                "use 0 (Zero) for empty cells)\n")
        if sudoku_numbers.isdecimal() is False:
            print("\nInput is not a valid sudoku, "
                "all characters must be numbers.\n")
            continue
        if (length := len(sudoku_numbers)) != 81:
            print("\nInsufficient data, check if all cells were entered\n"
                  f"Input contained {length} digits\n")
            continue
        return [int(i) for i in sudoku_numbers]


def basic_rules_pass(valid):
    """ Eliminates illegal candidates 
        from each cell's list of possibles 
        using basic sudoku rules of:
        "Once per row, column, and box" """

    for idx, cell in enumerate(valid):
        if cell != []:
            current_row = idx // 9
            current_column = idx % 9
            current_box = current_column // 3*3 + (current_row // 3*3) * 9

            current_row_values = [i for i in sudoku[current_row*9:
                                                    current_row*9 + 9] 
                                                    if i != 0]
            current_column_values = [sudoku[i] 
                                        for i in range(current_column, 81, 9)
                                        if sudoku[i] != 0]
            current_box_values = [i for j in range(3) 
                                    for i in sudoku[current_box + (j*9):
                                                    current_box + (j*9) + 3] 
                                                    if i != 0]

            valid[idx] = [i for i in cell if i not in current_row_values
                                            and i not in current_column_values
                                            and i not in current_box_values]
    return valid


def get_candidates():
    """ Creates lists of all valid inputs for each empty cell """
    valid_candidates = [[] for i in range(81)]
    for idx, i in enumerate(sudoku):
        valid_candidates[idx] = list(range(1,10)) if i == 0 else []
    return basic_rules_pass(valid_candidates)


def solve_cell():
    """ Sets cell to last available valid value """
    for idx, cell in enumerate(candidates):
        if len(cell) == 1:
            sudoku[idx] = cell[0]
            candidates[idx] = []


sudoku = get_sudoku()
start = perf_counter()
candidates = get_candidates()

runs = 0
while sum(sudoku) != 405:
    solve_cell()
    candidates = basic_rules_pass(candidates)
    runs += 1
    if runs > 100:
        print(candidates)
        print("\nFailed to solve sudoku.")
        break
else:
    print("\nSolve successful.")
for i in range(9):
    for j in range(9):
        print(sudoku[j + i*9], end="  ")
    print()
end = perf_counter()
print(f"Elapsed time: {(end - start) * 1000:.4f}ms")
