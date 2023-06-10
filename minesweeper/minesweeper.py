import itertools
import random
import copy

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
        self.safe = set()
        self.mine = set()
        
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.mine
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.safe
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.mine.add(cell)
            self.cells.discard(cell)
            self.count -= 1

        return
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.safe.add(cell)
            self.cells.discard(cell)
        return
        raise NotImplementedError


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

    def update_knowledge(self , new_sentence):
        

        updated = False
        if len(new_sentence.cells) == 0:
            for sentence in self.knowledge:
                if self.check_sentence(sentence):
                    updated = True
            if updated == True:
                self.update_knowledge(Sentence(set(),0))
        elif len(self.knowledge) == 0:
            if len(new_sentence.cells) > 0:
                self.knowledge.append(new_sentence)
        else :
            old_knowledge = self.knowledge
            for sentence in old_knowledge:
                if len(sentence.cells) == 0:
                    continue
            
                if new_sentence.cells.issubset(sentence.cells):
                    sentence.cells -= new_sentence.cells
                    sentence.count -= new_sentence.count

                elif sentence.cells.issubset(new_sentence.cells):
                    derived = Sentence(new_sentence.cells-sentence.cells, new_sentence.count - sentence.count)
                    print(f"Derived = {derived}")
                    updated = True
                    if not self.check_sentence(derived) and derived not in self.knowledge:
                        self.update_knowledge(derived)
            if updated == False:
                if len(new_sentence.cells) > 0:
                    self.knowledge.append(new_sentence)
            elif updated == True:
                self.update_knowledge(Sentence(set(),0))
            

        return

    def check_sentence(self , sentence):
        cell_set = copy.deepcopy(sentence.cells)
        if sentence.count <= 0 and len(sentence.cells) > 0:
            for cell in cell_set:
                self.mark_safe(cell)
            return True
        
        elif sentence.count == len(sentence.cells) and len(sentence.cells) > 0:
            for cell in cell_set:
                self.mark_mine(cell)
            return True
        
        return False
    
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

        nearby_cells = set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                
                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i,j) in self.safes:
                        continue
                    elif (i,j) in self.mines:
                        count -= 1
                    else: nearby_cells.add((i,j))

        new_sentence = Sentence(nearby_cells , count)
        print(new_sentence)
        
        if self.check_sentence(new_sentence):
            self.update_knowledge(Sentence(set(),0))
        else:
            self.update_knowledge(new_sentence)
        print("knowledge = [")
        for s in self.knowledge:
            print(s)
        print(" ]")
        return
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print(f"safe = {self.safes - self.moves_made}")
        print(f"mines = {self.mines}")
        avaliable_moves = self.safes - self.moves_made
        if len(avaliable_moves) == 0:
            return None
        else :  
            move = random.choice(tuple(avaliable_moves))
            print(f"move_made = {move}")
            return move


        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        print(f"mines = {self.mines}")
        print(f"safe = {self.safes - self.moves_made}")
        avaliable_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    avaliable_moves.add((i,j))
        
        if len(avaliable_moves) == 0:
            print("No avaiable move")
            return None
        else :  
            move = random.choice(tuple(avaliable_moves))
            print(f"move_made = {move}")
            return move

        raise NotImplementedError
