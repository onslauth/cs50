import itertools
import random


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

    def __init__(self, cells, count ):
        print( f"\nSentence( { cells }, { count } )" )
        self.cells = set(cells)
        self.count = count

        self.mines = set( )
        self.safes = set( )

        self.cell = None

        if self.count == 0:
            self.safes.update( self.cells )
            self.cells = set( )
            print( "  count == 0, all cells safe" )
            print( f"  self.cells: { self.cells }" )
            print( f"  self.safes: { self.safes }" )
            print( f"  self.mines: { self.mines }" )

        if len( cells ) == count:
            self.mines.update( self.cells )
            self.cells = set( )
            print( "  len( cells ) == count, all cells mines" )
            print( f"  self.cells: { self.cells }" )
            print( f"  self.safes: { self.safes }" )
            print( f"  self.mines: { self.mines }" )

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"Sentence: {self.cells} = {self.count}\n  original_cell: { self.cell }\n  safes: { self.safes }\n  mines: { self.mines }"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell not in self.cells:
            return

        print( f"\nmark_mine: { cell }" )

        self.mines.add( cell )
        self.cells.remove( cell )

        if len( self.mines ) == self.count:
            print( f"  remaining sentence is all safes:" )
            print( f"    self.mines: { self.mines }" )
            print( f"    self.safes: { self.safes }" )
            print( f"    self.cells: { self.cells }" )
            print( f"    self.count: { self.count }" )
            print( "" )

            self.safes.update( self.cells )
            self.cells = set( )

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if cell not in self.cells:
            return

        print( f"\nmark_safe: { cell }" )

        self.safes.add( cell )
        self.cells.remove( cell )

        if len( self.cells ) + len( self.mines ) == self.count:

            print( f"  remaining sentence is all mines:" )
            print( f"    self.mines: { self.mines }" )
            print( f"    self.safes: { self.safes }" )
            print( f"    self.cells: { self.cells }" )
            print( f"    self.count: { self.count }" )
            print( "" )

            self.mines.update( self.cells )
            self.cells = set( )


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

    def add_knowledge(self, cell, count):
        print( f"\nadd_knowledge:" )
        print( f"  cell:  { cell }" )
        print( f"  count: { count }" )

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
        #1 Mark the cell as a move
        self.moves_made.add( cell )
        print( "\nAdded cell to moves_made" )
        print( f"  self.moves_made: { self.moves_made }" )

        #2.0 Mark the cell as safe
        self.safes.add( cell )
        print( "\nAdded cell to safes" )
        print( f"  self.safes: { self.safes }" )

        #2.1 Update sentences and mark cell as safe
        print( f"Updating knowledge with safe cell {cell}" )
        self.update_knowledge_with_safe( cell )
        self.find_and_mark_new_known_cells( )

        #2.2 Add new sentence if not empty
        new_cells, new_count = self.create_new_cells( cell, count )

        if len( new_cells ) == 0:
            print( "\nNew sentence is empty" )
        else:
            print( "\nAdding new sentence:" )
            sentence = Sentence( new_cells, new_count )
            sentence.cell = cell
            print( sentence )
            self.knowledge.append( sentence )
            self.find_and_mark_new_known_cells( )

        self.infer_new_sentences( )
        self.find_and_mark_new_known_cells( )

    def infer_new_sentences( self ):
        print( "\ninfer_new_sentences:" )

        if len( self.knowledge ) <= 1:
            print( "  len( knowledge ) <= 1, returning" )
            return

        s = self.knowledge[ -1 ]
        print( f"  s:" )
        print( s )

        if len( s.cells ) == 0:
            return

        for i in range( 0, len( self.knowledge ) - 1 ):
            print( f"\n  i: { i }" )
            k = self.knowledge[ i ]
            print( "  k:" )
            print( k )

            if s.cells.issubset( k.cells ):
                print( "  S is SUBSET of K" )
                subset = k.cells - s.cells
                count  = ( k.count - len( k.mines ) ) - ( s.count - len( s.mines ) )

                if len( subset ) == 0:
                    print( "  len( subset ) == 0, continuing" )
                    continue

                print( "  subset is valid" )

                sentence = Sentence( subset, count )
                sentence.cell = "Inferred subset"
                print( "  sentence:" )
                print( sentence )
                self.knowledge.append( sentence )
            

    def find_and_mark_new_known_cells( self ):
        print( "\nfind_and_mark_new_known_cells" )
        new_mines = self.get_new_mines( )
        new_safes = self.get_new_safes( )

        print( "\nIterating over new safes and mines" )
        print( f"  self.safes: { self.safes }" )
        print( f"  self.mines: { self.mines }" )
        print( f"  new_safes:  { new_safes }" )
        print( f"  new_mines:  { new_mines }" )

        print( "\nBEFORE WHILE" )
        while len( new_safes ) > 0 or len( new_mines ) > 0:
            for c in new_safes:
                print( f"\n  safe: { c }" )
                self.safes.add( c )
                for k in self.knowledge:
                    k.mark_safe( c )

            for c in new_mines:
                print( f"\n  mine: { c }" )
                self.mines.add( c )
                for k in self.knowledge:
                    k.mark_mine( c )

            print( "Getting new safes and mines:" )
            new_safes = self.get_new_safes( )
            new_mines = self.get_new_mines( )
            print( f"  self.safes: { self.safes }" )
            print( f"  self.mines: { self.mines }" )
            print( f"  new_safes:  { new_safes }" )
            print( f"  new_mines:  { new_mines }" )

        print( "\nAFTER WHILE\n\n" )

    def get_new_safes( self ):
        safes = set( itertools.chain( *[ x.known_safes( ) for x in self.knowledge ] ) )
        safes -= self.safes
        return safes

    def get_new_mines( self ):
        mines = set( itertools.chain( *[ x.known_mines( ) for x in self.knowledge ] ) )
        mines -= self.mines
        return mines

    def update_knowledge_with_safe( self, cell ):
        print( f"\nupdate_knowledge_with_safe:" )
        print( f"  cell: { cell }" )

        for k in self.knowledge:
            print( f"  k: { k }" )
            k.mark_safe( cell )


    def create_new_cells( self, cell, count ):
        print( "\ncreate_new_cells:" )
        print( f"  cell:  { cell }" )
        print( f"  count: { count }" )

        lower_i = cell[ 0 ] - 1
        upper_i = cell[ 0 ] + 1

        lower_j = cell[ 1 ] - 1
        upper_j = cell[ 1 ] + 1

        if lower_i < 0:
            lower_i = 0
        if upper_i >= self.height:
            upper_i = self.height - 1

        if lower_j < 0:
            lower_j = 0
        if upper_j >= self.width:
            upper_j = self.width - 1


        print( f"  lower_i: { lower_i }" )
        print( f"  upper_i: { upper_i }" )
        print( f"  lower_j: { lower_j }" )
        print( f"  upper_j: { upper_j }" )

        new_count = count
        new_cells = set( )
        for i in range( lower_i, upper_i + 1 ):
            for j in range( lower_j, upper_j + 1 ):
                cell = ( i, j )
                new_cells.add( cell )

        new_cells -= self.safes 

        intersection = new_cells.intersection( self.mines )
        new_cells -= intersection
        new_count -= len( intersection )

        return new_cells, new_count


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print( "\nmake_safe_move:" )
        moves = self.safes - self.moves_made
        print( f"  moves: { moves }" )
        if len( moves ) == 0:
            print( "  no safe move to make" )
            return None

        move = list( moves )[ 0 ]
        print( f"  making move: { move }" )

        return move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        print( "\nmake_random_move:" )
        print( f"  len( self.moves_made ): { len( self.moves_made ) }" )
        print( f"  len( self.mines ):      { len( self.mines ) }" )
        print( f"  used: { len( self.moves_made ) + len( self.mines ) }" )
        print( f"  height: { self.height }, width: { self.width }, cells: { self.height * self.width }" )

        if len( self.moves_made ) + len( self.mines ) == self.height * self.width:
            return None

        while True:
            i = random.randrange( self.height )
            j = random.randrange( self.width )
            cell = ( i, j )
            print( f"  cell: { cell }" )
            if cell not in self.moves_made and cell not in self.mines:
                print( f"  making move: { cell }" )
                return cell

    def find_knowledge( self, cell ):
        print( "\n\nfind_knowledge:" )
        print( f"  cell: { cell }" )

        for k in self.knowledge:
            if cell in k.cells:
                print( "  cell in k.cells" )
                print( k )
            elif cell in k.safes:
                print( "  cell in k.safes" )
                print( k )
            elif cell in k.mines:
                print( "  cell in k.mines" )
                print( k )
            


