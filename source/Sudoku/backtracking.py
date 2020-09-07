import sys

def show(arr): 
    for i in range(9): 
        for j in range(9): 
            print(arr[i][j], end=" ")
        print() 

def find_empty_location(arr, l): 
    for row in range(9): 
        for col in range(9): 
            if(arr[row][col]== 0): 
                l = [row, col]
                return True
    return False

def used_in_row(arr, row, num): 
    for i in range(9): 
        if(arr[row][i] == num): 
            return True
    return False

def used_in_col(arr, col, num): 
    for i in range(9): 
        if(arr[i][col] == num): 
            return True
    return False
    
def used_in_box(arr, row, col, num): 
    for i in range(3): 
        for j in range(3): 
            if(arr[i + row][j + col] == num): 
                return True
    return False

def is_valid(arr, row, col, num): 
    # Check if 'num' is not already placed in current row, 
    # current column and current 3x3 box 
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) \
        and not used_in_box(arr, row - row % 3, col - col % 3, num)

def solve_sudoku_backtracking(arr): 
    # 'l' is a list variable that keeps the record of row and col in find_empty_location Function     
    l =[0, 0] 
    # If there is no unassigned location, we are done     
    if(not find_empty_location(arr, l)): 
        return True
      
    # Assigning list values to row and col that we got from the above Function  
    row, col = l
      
    for num in range(1, 10): 
        if is_valid(arr, row, col, num):             
            # make tentative assignment 
            arr[row][col]= num 
            # return, if success, ya ! 
            if(solve_sudoku_backtracking(arr)): return True
            # failure, unmake & try again 
            arr[row][col] = 0
              
    # this triggers backtracking         
    return False  

if __name__=="__main__": 

    # assigning values to the grid 
    grid =[[7,8,0,4,0,0,1,2,0],
            [6,0,0,0,7,5,0,0,9],
            [0,0,0,6,0,1,0,7,8],
            [0,0,7,0,4,0,2,6,0],
            [0,0,1,0,5,0,9,3,0],
            [9,0,4,0,6,0,0,0,5],
            [0,7,0,3,0,0,0,1,2],
            [1,2,0,0,0,7,4,0,0],
            [0,4,9,2,0,6,0,0,7]] 

    grid = [[0, 0, 0, 3, 0, 0, 0, 0, 0], [3, 0, 0, 0, 0, 0, 4, 5, 8], [0, 0, 0, 8, 5, 6, 0, 7, 9], [2, 0, 0, 1, 8, 0, 9, 0, 5], [0, 1, 9, 0, 3, 0, 7, 4, 0], [6, 0, 4, 0, 9, 7, 0, 0, 1], [1, 7, 0, 4, 6, 2, 0, 0, 0], [9, 4, 3, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 3, 0, 0, 0]]
    # if success print the grid 
    if(solve_sudoku_backtracking(grid)): 
        show(grid) 
    else: 
        print("No solution exists")