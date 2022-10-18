# def reformat(puzzle):
#
#     puzzle_size = len(puzzle)
#     str_puzzle = ""
#
#     for r in range(puzzle_size):
#
#         for c in range(puzzle_size):
#
#             if c < puzzle_size - 1:
#                 str_puzzle += str(puzzle[r][c]) + '\t'
#             elif r < puzzle_size - 1:
#                 str_puzzle += str(puzzle[r][c]) + '\n'
#             else:
#                 str_puzzle += str(puzzle[r][c])
#
#     return str_puzzle
#
#
# a = [[27, 31, 34, 57, 12, 30, 51, 37], [40, 45, 0, 4, 16, 17, 29, 20], [61, 54, 24, 19, 22, '-', 26, '-'], [1, 35, 11, 55, 41, 28, 10, 38], [25, 48, 58, 36, 32, 53, 50, 46], [7, 14, 15, 21, 59, 5, 47, 8], [52, 33, 23, 43, 2, 18, 13, 6], [42, 60, 44, 39, 3, 9, 49, 56]]
#
# rw = reformat(a)
#
# with open("out_test.txt", "w") as file:
#     file.writelines(rw)
#     file.close()

a = 4

for i in range(a):
    print(i)
