# nuruomino.py: Template para implementação do projeto de Inteligência Artificial 2024/2025.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 21:
# 109886 Miguel Morais
# 110375 Pedro Jerónimo

import sys
from search import (Problem, Node, depth_first_tree_search)

class NuruominoState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NuruominoState.state_id
        NuruominoState.state_id += 1

    def __lt__(self, other):
        """Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas."""

        return self.id < other.id
    
    def is_valid(self):
        """Devolve True caso o estado seja válido, False caso contrário."""

        return self.board.is_possible()
    
    def is_goal(self):
        """Devolve True caso o estado seja estado objetivo, False caso
        contrário."""

        return self.is_valid() and self.board.is_filled() and self.board.is_connected()

class Board:
    """Representação interna de um tabuleiro do Puzzle Nuruomino."""

    def __init__(self, grid, regions,  adjacents = list(), pieces = (), empty_regions = 0):
        self.grid = grid
        self.regions = regions
        self.n = len(grid)
        self.possible = True
        self.adjacents = adjacents
        self.pieces = pieces
        self.empty_regions = empty_regions
    
    def duplicate(self):
        """Devolve uma cópida da instância"""

        grid_duplicated = [[[] for _ in range(self.n)] for _ in range(self.n)]
        adjacents_duplicated = [[]]

        for i in range(len(grid_duplicated)):
            grid_duplicated[i] = self.grid[i].copy()
        for i in range(1, len(self.regions)):
            adjacents_duplicated.append(self.adjacents[i].copy())

        return Board(grid_duplicated, self.regions.copy(), adjacents_duplicated, self.pieces.copy(), self.empty_regions)
    
    def adjacent_positions(self, region) -> list:
        """Devolve as posições ortogonalmente adjacentes à região."""
        
        group = self.regions[region][0]
        positions = set()

        for r,c in group:
            for adj in self.adjacent_cell_positions(r, c):
                if adj not in group:
                    positions.add(adj)

        return positions

    def adjacent_values(self, region) -> list:
        """Devolve os valores das celulas ortogonalmente adjacentes à região."""

        positions = self.adjacent_positions(region)
        values = set()

        for position in positions:
            values.add(self.grid[position[0]][position[1]])

        return values
    
    adjacent_cells = dict()
    def adjacent_cell_positions(self, row:int, col:int) -> list:
        """Devolve as posições ortogonalmente adjacentes à célula."""

        if (row,col) in self.adjacent_cells:
            return self.adjacent_cells[(row,col)]

        n = self.n
        adj = []
        if row != 0:
            adj.append((row-1, col))
        if col != 0:
            adj.append((row, col-1))
        if col != n-1:
            adj.append((row, col+1))
        if row != n-1:
            adj.append((row+1, col))
        
        self.adjacent_cells[(row,col)] = adj

        return adj

    def check_square(self, row, column):
        """Devolve True se uma célula pertence a um tetramino 2x2,
        False caso contrário"""

        pieces = {'L', 'I', 'T', 'S'}

        if ((row - 1 >= 0 and column + 1 < self.n
             and self.grid[row - 1][column] in pieces
             and self.grid[row - 1][column + 1] in pieces
             and self.grid[row][column + 1] in pieces)
            or (row + 1 < self.n and column + 1 < self.n
                and self.grid[row][column + 1] in pieces
                and self.grid[row + 1][column + 1] in pieces
                and self.grid[row + 1][column] in pieces)
            or (row + 1 < self.n and column - 1 >= 0
                and self.grid[row + 1][column] in pieces
                and self.grid[row + 1][column - 1] in pieces
                and self.grid[row][column - 1] in pieces)
            or (row - 1 >= 0 and column - 1 >= 0
                and self.grid[row - 1][column] in pieces
                and self.grid[row - 1][column - 1] in pieces
                and self.grid[row][column - 1] in pieces)):
            return True
        
        return False

    def possible_pieces(self, region):
        """Devolve as peças possíveis para a região recebida."""

        region_pieces = []
        cells = self.regions[region][0]
        for r,c in cells:
            #L
            #0graus
            if((r, c + 1) in cells
               and (r, c + 2) in cells
               and (r + 1, c) in cells):
                region_pieces.append(('L', 
                                      ((r, c),
                                       (r, c + 1),
                                       (r, c + 2),
                                       (r + 1, c))))
                
            #90graus
            if((r - 1, c) in cells
               and (r - 2, c) in cells
               and (r, c + 1) in cells):
                region_pieces.append(('L', 
                                      ((r, c),
                                       (r - 1, c),
                                       (r - 2, c),
                                       (r, c + 1))))
            
            #180graus
            if((r, c - 1) in cells
               and (r, c - 2) in cells
               and (r - 1, c) in cells):  
                region_pieces.append(('L', 
                                      ((r, c),
                                       (r, c - 1),
                                       (r, c - 2),
                                       (r - 1, c))))
            
            #270graus
            if((r + 1, c) in cells
               and (r + 2, c) in cells
               and (r, c - 1) in cells):
                region_pieces.append(('L', 
                                      ((r, c),
                                       (r + 1, c),
                                       (r + 2, c),
                                       (r, c - 1))))
                
            #0graus-refletido
            if((r, c + 1) in cells
               and (r, c + 2) in cells
               and (r - 1, c) in cells):
                region_pieces.append(('L', 
                                      ((r, c),
                                       (r, c + 1),
                                       (r, c + 2),
                                       (r - 1, c))))
                
            #90graus-refletido
            if((r - 1, c) in cells
               and (r - 2, c) in cells
               and (r, c - 1) in cells):                                   
                region_pieces.append(('L', 
                                      ((r, c),
                                       (r - 1, c),
                                       (r - 2, c),
                                       (r, c - 1))))
            
            #180graus-refletido
            if((r, c - 1) in cells
               and (r, c - 2) in cells
               and (r + 1, c) in cells):
                region_pieces.append(('L', 
                                      ((r, c),
                                       (r, c - 1),
                                       (r, c - 2),
                                       (r + 1, c))))
            
            #270graus-refletido
            if((r + 1, c) in cells
               and (r + 2, c) in cells
               and (r, c + 1) in cells):
                region_pieces.append(('L', 
                                      ((r, c),
                                       (r + 1, c),
                                       (r + 2, c),
                                       (r, c + 1))))
            #I
            #0graus
            if((r, c + 1) in cells
               and (r, c + 2) in cells
               and (r, c + 3) in cells): 
                region_pieces.append(('I', 
                                      ((r, c),
                                       (r, c + 1),
                                       (r, c + 2),
                                       (r, c + 3))))

            #90graus
            if((r + 1, c) in cells
               and (r + 2, c) in cells
               and (r + 3, c) in cells):
                region_pieces.append(('I', 
                                      ((r, c),
                                       (r + 1, c),
                                       (r + 2, c),
                                       (r + 3, c))))

            #T
            #0graus
            if((r - 1, c) in cells
               and (r + 1, c) in cells
               and (r, c + 1) in cells):
                region_pieces.append(('T', 
                                      ((r, c),
                                       (r - 1, c),
                                       (r + 1, c),
                                       (r, c + 1))))
                
            #90graus
            if((r, c - 1) in cells
               and (r, c + 1) in cells
               and (r - 1, c) in cells):
                region_pieces.append(('T', 
                                      ((r, c),
                                       (r, c - 1),
                                       (r, c + 1),
                                       (r - 1, c))))
            
            #180graus
            if((r - 1, c) in cells
               and (r + 1, c) in cells
               and (r, c - 1) in cells):
                region_pieces.append(('T', 
                                      ((r, c),
                                       (r - 1, c),
                                       (r + 1, c),
                                       (r, c - 1))))
                
            #270graus
            if((r, c - 1) in cells
               and (r, c + 1) in cells
               and (r + 1, c) in cells):
                region_pieces.append(('T', 
                                      ((r, c),
                                       (r, c - 1),
                                       (r, c + 1),
                                       (r + 1, c))))
                
            #S
            #0graus
            if((r, c - 1) in cells
               and (r + 1, c - 1) in cells
               and (r + 1, c - 2) in cells):
                region_pieces.append(('S', 
                                      ((r, c),
                                       (r, c - 1),
                                       (r + 1, c - 1),
                                       (r + 1, c - 2))))
                
            #90graus
            if((r - 1, c) in cells
               and (r - 1, c - 1) in cells
               and (r - 2, c - 1) in cells):
                region_pieces.append(('S', 
                                      ((r, c),
                                       (r - 1, c),
                                       (r - 1, c - 1),
                                       (r - 2, c - 1))))
            
            #0graus-refletido
            if((r, c + 1) in cells
               and (r + 1, c + 1) in cells
               and (r + 1, c + 2) in cells):
                region_pieces.append(('S', 
                                      ((r, c),
                                       (r, c + 1),
                                       (r + 1, c + 1),
                                       (r + 1, c + 2))))
                
            #90graus-refletido
            if((r + 1, c) in cells
               and (r + 1, c - 1) in cells
               and (r + 2, c - 1) in cells):
                region_pieces.append(('S', 
                                      ((r, c),
                                       (r + 1, c),
                                       (r + 1, c - 1),
                                       (r + 2, c - 1))))

        return region_pieces
    
    def valid_pieces(self, region):
        """Devolve as peças ainda possíveis para a região recebida."""

        pieces = []
        for piece in self.pieces[region]:
            invalid = False

            adjacent_cells = set()
            for r,c in piece[1]:
                adjacent_cells.update(self.adjacent_cell_positions(r,c))
            for r,c in adjacent_cells:
                if (r,c) not in piece[1] and self.grid[r][c] == piece[0]:
                    invalid = True
                    break

            if not invalid:
                for r,c in piece[1]:
                    self.grid[r][c] = piece[0]

                for r,c in piece[1]:
                    if self.check_square(r, c):
                        invalid = True
                        break

                if not invalid:
                    region_backup = self.regions[region]
                    self.regions[region] = (piece[1], True)

                    adjacents_copy = [[]]
                    for i in range(1, len(self.regions)):
                        adjacents_copy.append(self.adjacents[i].copy())
                    
                    adjacent_regions = set()
                    for r,c in self.adjacent_positions(region):
                        if self.grid[r][c] == region:
                            continue
                        if self.grid[r][c] in ('L','I','T','S'):
                            for region2 in range(1,len(self.regions)):
                                if (r,c) in self.regions[region2][0]:
                                    adjacent_regions.add(region2)
                                    break
                        elif self.regions[self.grid[r][c]][1] == False:
                            adjacent_regions.add(self.grid[r][c])

                    for adjacent_region in self.adjacents[region]:
                        if adjacent_region not in adjacent_regions:
                            adjacents_copy[adjacent_region].remove(region)

                    adjacents_copy[region] = adjacent_regions

                    if not self.all_connected(adjacents_copy):
                        invalid = True

                    self.regions[region] = region_backup

                for r,c in piece[1]:
                    self.grid[r][c] = region 

                if not invalid:
                    pieces.append(piece)        

        return pieces

    def place_piece(self, piece, cells):
        """Coloca a peça recebida nas células especificadas."""

        piece_region = self.grid[cells[0][0]][cells[0][1]]

        self.regions[piece_region] = (list(cells), True)

        for r,c in cells:
            self.grid[r][c] = piece

        adjs = set()
        for r,c in self.adjacent_positions(piece_region):
            if self.grid[r][c] == piece_region:
                continue
            if self.grid[r][c] in ('L','I','T','S'):
                for region in range(1,len(self.regions)):
                    if (r,c) in self.regions[region][0]:
                        adjs.add(region) 
                        break
            elif self.regions[self.grid[r][c]][1] == False:
                adjs.add(self.grid[r][c])

        for adj in self.adjacents[piece_region]:
            if adj not in adjs:
                self.adjacents[adj].remove(piece_region)

        adjs_backup = self.adjacents[piece_region]
        self.adjacents[piece_region] = adjs

        pieces = ('L','I','T','S')
        for region in adjs_backup:
            if region not in pieces and self.regions[region][1] == False:
                new_pieces = self.valid_pieces(region)

                if len(new_pieces) == 0:
                    self.possible = False
                    return

                self.pieces[region] = new_pieces

        self.empty_regions -= 1

    def all_connected(self, adjacents):
        """Devolve True se todas as regiões formam uma componente conexa,
        False caso contrário, assumindo como lista de adjacências o
        argumento adjacents."""

        visited = set()
        stack = [1]

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            for neighbor in adjacents[current]:
                if neighbor in visited:
                    continue
                
                found_connection = False
                for adj in self.adjacent_positions(neighbor):
                    if adj in self.regions[current][0]:
                        stack.append(neighbor)
                        found_connection = True
                        break
                    if found_connection:
                        break

        return len(visited) == len(self.regions) - 1
    
    def is_possible(self):
        """Devolve True se o tabuleiro cumpre as regras de jogo, False caso
        contrário."""

        return self.possible
    
    def is_filled(self):
        """Devolve True se todas as regiões estão preenchidas, False caso
        contrário."""

        return self.empty_regions == 0
    
    def is_connected(self):
        """Devolve True se todas as regiões formam uma componente conexa,
        False caso contrário."""

        return self.all_connected(self.adjacents)

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""

        grid = sys.stdin.read().strip().splitlines()
        grid = [list(map(int, line.split())) for line in grid]

        regions = list()

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                cell = grid[i][j]
                while cell > len(regions) - 1:
                    regions.append([[], False])
                regions[cell][0].append((i, j))

        board = Board(grid, regions)

        return board
    
    def toString(self) -> str:
        """Devolve uma string representativa do tabuleiro."""

        text = ""
        for line in self.grid:
            text += '\t'.join(str(cell) for cell in line) + '\n'
        return text

class Nuruomino(Problem):
    def __init__(self, state: NuruominoState):
        """O construtor especifica o estado inicial."""
        super().__init__(state)

    def actions(self, state: NuruominoState):
        """Devolve uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        if state.is_valid() == False:
            return []
        
        min = float('inf')
        best_region = -1
        for region in range(1, len(state.board.regions)):
            if state.board.regions[region][1] == False:
                if len(state.board.pieces[region]) < min:
                    min = len(state.board.pieces[region])
                    best_region = region
                if len(state.board.pieces[region]) == min:
                    if len(state.board.adjacents[region]) > len(state.board.adjacents[best_region]):
                        best_region = region
                
        if min == float('inf'):
            return []
        return state.board.pieces[best_region]

    def result(self, state: NuruominoState, action):
        """Devolve o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        board = state.board.duplicate()
        board.place_piece(action[0], action[1])

        return NuruominoState(board)
        
    def goal_test(self, state: NuruominoState):
        """Devolve True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""

        if state.is_goal() == True:
            print(state.board.toString())
            return True
        return False

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""

        increment = 0
        if node.state.is_valid() == False:
            increment = float('inf')
        
        h = increment

        return h

board = Board.parse_instance()

adjacents = [[]]
pieces = [[]]
for region in range(1,len(board.regions)):
    adjacents.append(board.adjacent_values(region))
    pieces.append(board.possible_pieces(region))

board.adjacents = adjacents
board.pieces = pieces
board.empty_regions = len(board.regions) - 1

initial_state = NuruominoState(board)
problem = Nuruomino(initial_state)
depth_first_tree_search(problem)