#!/usr/bin/python
'''
dna alignment
11/28/14

Implementing dictionaries instead of 2d lists for speed improvement
Also removing traceback matrix since only need the score, not the 
alignment
'''

import sys
        
def cell_decision(matrix_dict, row, col, match, mismatch, gap_open, gap_extend, s1, s2):
    '''
    given a cell in the matrix chooses the optimal path
    and set the value for that cell
    '''
    if s1[row-1] == s2[col-1]:
        diagonal = matrix_dict[row-1,col-1] + match
    else:
        diagonal = matrix_dict[row-1,col-1] + mismatch
        
    # adding a gap in s1, looking left
    left_score = -10e10
    for temp_col in xrange(col):
        gap_length = col - temp_col
        gap_cost = gap_open + gap_extend * (gap_length -1)
        temp_score = matrix_dict[row,temp_col] + gap_cost
        if temp_score > left_score:
            left_score = temp_score
            
    # adding a gap in s2, looking up
    up_score = -10e10
    for temp_row in xrange(row):
        gap_length = row - temp_row
        gap_cost = gap_open + gap_extend * (gap_length -1)
        temp_score = matrix_dict[temp_row,col] + gap_cost
        if temp_score > up_score:
            up_score = temp_score

    matrix_dict[row,col] = max(diagonal, left_score, up_score)
    
def align(s1, s2):
    match = 3
    mismatch = -3
    gap_open = -8
    gap_extend = -1
    
    n_rows = len(s1) + 1
    n_cols = len(s2) + 1
    matrix_dict = {}
    initialize_matrix(matrix_dict, n_rows, n_cols, gap_open, gap_extend)
    
    for row in xrange(1,n_rows):
        for col in xrange(1,n_cols):
            cell_decision(matrix_dict, row, col, match, mismatch, gap_open, gap_extend, s1, s2)
    return matrix_dict[n_rows-1,n_cols-1]
    
def initialize_matrix(matrix_dict, n_rows, n_cols, gap_open, gap_extend):
    '''
    initializes a dict representation of a matrix
    '''
    matrix_dict[0,0] = 0
    matrix_dict[0,1] = gap_open
    matrix_dict[1,0] = gap_open
    for col in xrange(n_cols - 2):
        matrix_dict[0,col+2] = matrix_dict[0,col+1] + gap_extend
    for row in xrange(n_rows - 2):
        matrix_dict[row+2,0] = matrix_dict[row+1,0] + gap_extend 
        
with open(sys.argv[1]) as FH:
    for line in FH:
        s1, s2 = line.split('|')
        s1 = s1.strip()
        s2 = s2.strip()
        print align(s1, s2)
