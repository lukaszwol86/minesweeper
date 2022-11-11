import itertools
import random

#import sys
#sys.setrecursionlimit(10000)

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.cells:
            if len(self.cells) == self.count:
                return self.cells
            return None



    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if self.cells and cell in self.cells:
            self.cells = self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if self.cells and cell in self.cells:
            self.cells = self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()


        # List of sentences about the game known to be true
        self.knowledge = []
        self.subsets = []
        self.checked_nodes = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        if [cell,count] not in self.checked_nodes:
            self.checked_nodes.append([cell,count])
        equation = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.mines:
                        count -= 1
                    elif (i, j) not in self.safes:
                        equation.append((i, j))
        if len(equation) != 0:
            new_sentence = Sentence(equation,count)
            self.check_knowledge(new_sentence)
        self.update_all_knowledge()
        self.check_new_solutions()
        self.check_all_nodes()
#            if self.check_knowledge(new_sentence):
#                self.new_knowledge(new_sentence)



    def check_knowledge(self,new_sentence):
        mines = new_sentence.known_mines()
        empty = new_sentence.known_safes()
        if mines != None:
            for mine in mines:
                self.mark_mine(mine)
            #return None
        elif empty != None:
            for emp in empty:
                self.mark_safe(emp)
            #return None
        else:
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)
                self.new_knowledge(new_sentence)
                self.check_new_solutions()
            #return True

    def new_knowledge(self,new_sentence):
        temp_sent = self.knowledge.copy()
        for sentence in temp_sent:  #[:-1]
            if not sentence.cells:
                1
                # self.knowledge.remove(sentence)
            if sentence.cells and new_sentence.cells:
                if sentence.cells != new_sentence.cells:
                    if len(sentence.cells) < len(new_sentence.cells):
                        min_s = sentence
                        max_s = new_sentence
                    else:
                        min_s = new_sentence
                        max_s = sentence

                    if min_s.cells.issubset(max_s.cells):
                        subset = list(max_s.cells - min_s.cells)
                        diff = max_s.count - min_s.count
                        if subset:
                            #print(f"Subset {subset}")
                            new_sent2 = Sentence(subset, diff)
                            if subset not in self.subsets:
                                self.subsets.append(subset)
                                self.check_knowledge(new_sent2)
                                self.check_new_solutions()




    def update_all_knowledge(self):
        if self.knowledge:
            n_know = len(self.knowledge)
            if n_know>1:
                for i in range(n_know):
                    for j in range(n_know):
                        sent1 = self.knowledge[i]
                        sent2 = self.knowledge[j]

                        if i!=j and sent1.cells != sent2.cells and sent1.cells and sent2.cells:
                            if len(sent1.cells) < len(sent2.cells):
                                min_s = sent1
                                max_s = sent2
                            else:
                                min_s = sent2
                                max_s = sent1

                            if min_s.cells.issubset(max_s.cells):
                                subset = list(max_s.cells - min_s.cells)
                                diff = max_s.count - min_s.count
                                if subset not in self.subsets:
                                    self.subsets.append(subset)
                                    #print(f"Subset {subset}")
                                    new_sent2 = Sentence(subset, diff)
                                    self.check_knowledge(new_sent2)
                                    self.new_knowledge(new_sent2)
                                    self.check_new_solutions()

    def check_new_solutions(self):
        #for node in self.checked_nodes:
         #   self.add_knowledge(node[0],node[1])

        for knowledge in self.knowledge:
            self.check_knowledge(knowledge)

    def check_all_nodes(self):
        for node in self.checked_nodes:
            equation = []
            count = node[1]
            cell = node[0]
            for i in range(cell[0] - 1, cell[0] + 2):
                for j in range(cell[1] - 1, cell[1] + 2):
                    # Ignore the cell itself
                    if (i, j) == cell:
                        continue
                    if 0 <= i < self.height and 0 <= j < self.width:
                        if (i, j) in self.mines:
                            count -= 1
                        elif (i, j) not in self.safes:
                            equation.append((i, j))
            if len(equation) != 0:
                new_sentence = Sentence(equation, count)
                mines = new_sentence.known_mines()
                empty = new_sentence.known_safes()
                if mines != None:
                    for mine in mines:
                        self.mark_mine(mine)
                    # return None
                elif empty != None:
                    for emp in empty:
                        self.mark_safe(emp)









    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        moves = self.safes - self.moves_made
        if not moves:
            return None
        else:
            #print(f"Mines are here {self.mines}")
            #print(f"Safe moves are {moves}")
            #print(f"Safe move {list(moves)[0]}")
            return list(moves)[0]


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if self.make_safe_move()==None:
            all_cells = set()
            for i in range(self.height):
                for j in range(self.width):
                    all_cells.add((i, j))
            left_moves = all_cells - self.safes - self.moves_made - self.mines
            if not left_moves:
                return None
            else:
                selected = random.choice(list(left_moves))
                #print(f"Mines are here {self.mines}")
                #print(f"Random move {selected}")
                return selected