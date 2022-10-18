import random
import os.path
import shutil


class RandomGenerator:

    def __init__(self, lower_size, greater_size, n):

        self.lower_size = lower_size
        self.greater_size = greater_size
        self.n = n

        # self.start_file_path = "D:/Sem 05 - Online/Intelligent Systems/assignments/modified n puzzle/190530H-modified-n-puzzle/starts"
        # self.goal_file_path = "D:/Sem 05 - Online/Intelligent Systems/assignments/modified n puzzle/190530H-modified-n-puzzle/goals"
        #
        # RandomGenerator.remove_files(self.start_file_path)
        # RandomGenerator.remove_files(self.goal_file_path)
        #
        # self.start_files = self.get_files(n, "start")
        # self.goal_files = self.get_files(n, "goal")
        # self.out_files = self.get_files(n, "out")

        self.start_puzzles = []
        self.goal_puzzles = []

    # @staticmethod
    # def remove_files(folder):
    #
    #     for filename in os.listdir(folder):
    #         file_path = os.path.join(folder, filename)
    #         try:
    #             if os.path.isfile(file_path) or os.path.islink(file_path):
    #                 os.unlink(file_path)
    #             elif os.path.isdir(file_path):
    #                 shutil.rmtree(file_path)
    #         except Exception as e:
    #             print('Failed to delete %s. Reason: %s' % (file_path, e))
    #
    # @staticmethod
    # def get_files(n, file_type):
    #
    #     files = []
    #
    #     file_name_prefix = ""
    #     if file_type == "start":
    #         file_name_prefix += "Start_Configuration_"
    #     elif file_type == "goal":
    #         file_name_prefix += "Goal_Configuration_"
    #     else:
    #         file_name_prefix += "out_"
    #
    #     for i in range(n):
    #         files.append(file_name_prefix + str(i + 1) + ".txt")
    #
    #     return files
    #
    # @staticmethod
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

    @staticmethod
    def get_start_puzzle(size):  # TODO: add to self.start_puzzles

        chars = ['-', '-']
        for j in range(size * size - 2):
            chars.append(j + 1)

        puzzle = []
        used_chars = []

        for rows in range(size):

            row = []

            while len(row) < size:

                rand_ind = random.randint(0, len(chars) - 1)
                selected_char = chars[rand_ind]

                if selected_char == '-' and used_chars.count('-') < 2:

                    row.append(selected_char)
                    used_chars.append(selected_char)

                elif selected_char not in used_chars:

                    row.append(selected_char)
                    used_chars.append(selected_char)

            puzzle.append(row)

        return puzzle
        # return RandomGenerator.reformat(puzzle)

    @staticmethod
    def get_goal_puzzle(start_puzzle):

        goal_puzzle = [x[:] for x in start_puzzle]

        move_limit = random.randint(1, 5)
        moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        move_count = 0

    def generate(self):

        for i in range(self.n):

            size = random.randint(self.lower_size, self.greater_size)

            start_puzzle = RandomGenerator.get_start_puzzle(size)
            goal_puzzle = RandomGenerator.get_start_puzzle(start_puzzle)

            self.start_puzzles.append(start_puzzle)
            self.goal_puzzles.append(goal_puzzle)

            # self.write_puzzle(i, start_puzzle, "start")
            # self.write_puzzle(i, goal_puzzle, "goal")

    # def write_puzzle(self, n, puzzle, puzzle_type):
    #
    #     if puzzle_type == "start":
    #         write_file_path = os.path.join(self.start_file_path, self.start_files[n])
    #     else:
    #         write_file_path = os.path.join(self.goal_file_path, self.goal_files[n])
    #
    #     with open(write_file_path, "w") as file:
    #         file.writelines(puzzle)
    #         file.close()


# rg = RandomGenerator(3, 10, 5)
# rg.generate()
