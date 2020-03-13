# Author: Mahtab Zilaie
# Date: March 10, 2020
# Description: An abstract game board called xiangqi.


class Piece:
    """
    class that checks all pieces in game.
    """
    def __init__(self, color, name, position):
        """
        initializes data members
         """
        self.name = name
        self.position = position
        self.color = color

    def available_moves(self, start, color, game_board):
        pass

    def can_be_moved(self, start, end, color, game_board):
        pawn = game_board.get(start, None)
        if pawn is None:
            return False
        if pawn.color != color:
            return False
        if end in self.available_moves(start, color, game_board):
            return True
        return False

    def is_in_bounds(self, position):
        """checks if a position is on the board
        """
        x, y = position
        if x >= 0 and x < 9 and y >= 0 and y <= 9:
            return True
        return False

    def is_valid_position(self, position, color, game_board):
        """
        checks if position is valid
        """
        x, y = position
        if self.is_in_bounds((x, y)):
            if (x, y) not in game_board.keys() or game_board[(x, y)].color != color:
                return True
            return False
        return False

    def get_continuios_path(self, postion, color, game_board, intervals):
        x, y = postion
        results = []
        for X, Y in intervals:
            x_temp, y_temp = x + X, y + Y
            while self.is_valid_position((x_temp, y_temp), color, game_board):
                # print(str((x_temp,y_temp))+"is in bounds")

                target = game_board.get((x_temp, y_temp), None)
                if target is None:
                    results.append((x_temp, y_temp))
                elif target.color != color:
                    results.append((x_temp, y_temp))
                    break
                else:
                    break

                x_temp, y_temp = x_temp + X, y_temp + Y
        return results


class General(Piece):
    """
    class for chariot piece and  rules for specific piece
    """
    cardinals = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def available_moves(self, start, color, game_board):
        x, y = start
        moves = []
        for xx, yy in self.cardinals:
            x_temp, y_temp = xx + x, yy + y
            if (self.is_valid_position((x_temp, y_temp), color, game_board)):
                moves.append((x_temp, y_temp))
        return moves


class Horse(Piece):
    """
    class for horse piece
    """
    def getHorseList(self, position, game_board):
        x, y = position
        moves = []
        if game_board.get((x, y + 1), None) is None:
            moves.append((x + 1, y + 2))
            moves.append((x - 1, y + 2))
        if game_board.get((x, y - 1), None) is None:
            moves.append((x + 1, y - 2))
            moves.append((x - 1, y - 2))
        if game_board.get((x + 1, y), None) is None:
            moves.append((x + 2, y + 1))
            moves.append((x + 2, y - 1))
        if game_board.get((x - 1, y), None) is None:
            moves.append((x - 2, y + 1))
            moves.append((x - 2, y - 1))
        return moves

    def available_moves(self, start, color, game_board):
        moves = [(x, y) for (x, y) in self.getHorseList(start, game_board) if self.is_valid_position((x, y), color, game_board)]
        return moves


class Chariot(Piece):
    """
    class for chariot piece/ rules for specific piece
    """
    cardinals = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def available_moves(self, start, color, game_board):
        return self.get_continuios_path(start, color, game_board, self.cardinals)


class Advisor(Piece):
    diagonals = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def check_bound(self, position, color):
        x, y = position
        if color == 'red':
            return (x >= 3 and x <= 5 and y >= 0 and y <= 2)
        else:
            return (x >= 3 and x <= 5 and y >= 7 and y <= 9)

    def available_moves(self, start, color, game_board):
        x, y = start
        moves = []
        for position in self.diagonals:
            xx, yy = position
            x_temp, y_temp = x + xx, y + yy
            if (self.is_valid_position((x_temp, y_temp), color, game_board) and self.check_bound((x_temp, y_temp),
                                                                                                 color)):
                moves.append((x_temp, y_temp))
        return moves


class Elephant(Piece):
    """
    class for elephant piece that has rules for specific piece
    """
    diagonals = [(2, 2), (2, -2), (-2, 2), (-2, -2)]

    def check_bound(self, position, color):
        x, y = position
        if color == 'red':
            return (y >= 0 and y <= 4)
        else:
            return (y >= 5 and y <= 9)

    def available_moves(self, start, color, game_board):
        x, y = start
        moves = []
        for position in self.diagonals:
            xx, yy = position
            x_temp, y_temp = x + xx, y + yy
            if (self.is_valid_position((x_temp, y_temp), color, game_board) and self.check_bound((x_temp, y_temp),
                                                                                                 color)):
                moves.append((x_temp, y_temp))
        return moves


class Cannon(Piece):
    """
    class for cannon piece that has rules for specific piece
    """

    def get_continuios_pathCannon(self, postion, color, game_board, intervals):
        x, y = postion
        results = []
        for X, Y in intervals:
            x_temp, y_temp = x + X, y + Y
            while self.is_in_bounds((x_temp, y_temp)):
                # print(str((x_temp,y_temp))+"is in bounds")

                target = game_board.get((x_temp, y_temp), None)
                if target is None:
                    results.append((x_temp, y_temp))
                else:
                    while True:
                        x_temp, y_temp = x_temp + X, y_temp + Y
                        # print(x_temp, y_temp)
                        if self.is_in_bounds((x_temp, y_temp)):
                            target = game_board.get((x_temp, y_temp), None)
                            if target is None:
                                continue
                            else:
                                # print(x, y, target)
                                if color != target.color:
                                    results.append((x_temp, y_temp))
                                break
                        else:
                            break
                    break

                x_temp, y_temp = x_temp + X, y_temp + Y
        # print(results)
        return results

    def available_moves(self, start, color, game_board):
        intervals = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return self.get_continuios_pathCannon(start, color, game_board, intervals)


class Pawn(Piece):
    """
    class for pawn/soldier piece that has rules for specific piece
    """

    def __init__(self, color, name, position):
        self.color = color
        self.name = name
        self.position = position

    def available_moves(self, start, color, game_board):
        x, y = start
        isHMovable = False
        hori = []
        if color == 'red':
            if y > 4:
                isHMovable = True
                hori = [(1, 1), (-1, 1)]
        else:
            if y <= 4:
                isHMovable = True
                hori = [(1, -1), (-1, -1)]
        moves = []
        if color == 'red':
            if self.is_valid_position((x, y + 1), color, game_board):
                moves.append((x, y + 1))
        else:
            if self.is_valid_position((x, y - 1), color, game_board):
                moves.append((x, y - 1))
        if isHMovable:
            for xx, yy in hori:
                x_temp, y_temp = xx + x, yy + y
                if (self.is_valid_position((x_temp, y_temp), color, game_board)):
                    moves.append((x_temp, y_temp))

        return moves


class XiangqiGame:
    """
    class that determines status of XiangqiGame
    """
    x_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    y_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    def __init__(self):
        """
        initializes data members
        """
        self.turn = 'red'
        self.game_board = {}
        self.init()
    def is_in_bounds(self, pos):
        """
        validates if move is in bounds
        """
        x, y = pos
        return x >= 0 and x < 9 and y >= 0 and y < 10

    def is_valid(self, position, color, game_board):
        """
        validates if move is valid
        """
        x, y = position
        if self.is_in_bounds((x, y)):
            if (x, y) not in game_board or game_board[(x, y)].color != color:
                return True
            return False
        return False

    def ifKingSeesKing(self, game_board):
        general_one = None
        pos = None
        for key, value in game_board.items():
            if type(value) == General:
                general_one = value
                pos = key
                break
        intervals = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        x, y = pos
        for X, Y in intervals:
            x_temp, y_temp = x + X, y + Y
            while self.is_valid((x_temp, y_temp), general_one.color, game_board):

                target = game_board.get((x_temp, y_temp), None)
                if target is not None:
                    if type(target) == General and general_one.color != target.color:
                        return True
                    return False
                x_temp, y_temp = x_temp + X, y_temp + Y
        return False

    def init(self):
        pawns = [Chariot, Horse, Elephant, Advisor, General, Advisor, Elephant, Horse, Chariot]
        pawn_names_red = ["♖", "♘", "🐘", "♕", "♔", "♕", "🐘", "♘", "♖"]
        pawn_names_black = ["♜", "♞", "🐘", "♛", "♚", "♛", "🐘", "♞", "♜"]
        for i in range(0, 9, 2):
            self.game_board[(i, 3)] = Pawn('red', "♙", (i, 3))
        for i in range(9):
            self.game_board[(i, 0)] = pawns[i]('red', pawn_names_red[i], (i, 0))
        self.game_board[(1, 2)] = Cannon('red', "♗", (1, 2))
        self.game_board[(7, 2)] = Cannon('red', "♗", (7, 2))

        for i in range(0, 9, 2):
            self.game_board[(i, 6)] = Pawn('black', "♟", (i, 6))
        for i in range(9):
            self.game_board[(i, 9)] = pawns[i]('black', pawn_names_black[i], (i, 9))
        self.game_board[(1, 7)] = Cannon('black', "♝", (1, 7))
        self.game_board[(7, 7)] = Cannon('black', "♝", (7, 7))

    def is_in_check(self, color):
        """
        checks if team is in check
        """
        pawns = []
        generalPos = None
        for pos, pawn in self.game_board.items():
            if pawn.color != color:
                pawns.append(pawn)
            elif type(pawn) == General and color == pawn.color:
                generalPos = pos

        is_general_in_check = False
        for pawn in pawns:
            if pawn.can_be_moved(pawn.position, generalPos, pawn.color, self.game_board):
                is_general_in_check = True

        return is_general_in_check

    def check_if_lost(self, color):
        generalPos = None
        for pos, pawn in self.game_board.items():
            if pawn.color == color and type(pawn) == General:
                generalPos = pos

        # print(generalPos)

        moves = self.game_board[generalPos].available_moves(generalPos, color, self.game_board)
        # print(moves)
        x, y = generalPos
        for move in moves:

            self.game_board[move] = self.game_board[generalPos]
            del self.game_board[generalPos]
            if not self.is_in_check(color):
                self.game_board[generalPos] = self.game_board[move]
                del self.game_board[move]
                return False
            self.game_board[generalPos] = self.game_board[move]
            del self.game_board[move]
        return True

    def get_game_state(self):
        """
        returns status of game

        """
        if self.check_if_lost('black'):
            return 'RED_WON'
        if self.check_if_lost('red'):
            return 'BLACK_WON'
        else:
            return 'UNFINISHED'

    def make_move(self, start, end):
        """
        takes start move and end move
        """
        start_pos = (self.x_list.index(start[0]), self.y_list.index(start[1:]))
        end_pos = (self.x_list.index(end[0]), self.y_list.index(end[1:]))
        if (self.get_game_state() == 'RED_WON' or self.get_game_state() == 'BLACK_WON'):
            return False
        if (start_pos not in self.game_board.keys()):
            return False
        if (not self.game_board[start_pos].can_be_moved(start_pos, end_pos, self.turn, self.game_board)):
            return False
        self.game_board[end_pos] = self.game_board[start_pos]
        self.game_board[end_pos].position = end_pos
        del self.game_board[start_pos]
        if self.ifKingSeesKing(self.game_board):
            self.game_board[start_pos] = self.game_board[end_pos]
            self.game_board[start_pos].position = start_pos
            del self.game_board[end_pos]
            return False
        if self.turn == 'red':
            self.turn = 'black'
        else:
            self.turn = 'red'
        return True

    def print_board(self):
        """
        prints game board
        """
        print("  1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10")
        for i in range(0, 9):
            print("-" * 36)
            print(chr(i + 97), end="|")
            for j in range(0, 10):
                item = self.game_board.get((i, j))
                if item:
                    print(item.name + ' |', end=" ")
                else:
                    print('0' + ' |', end=" ")
            print()
        print("-" * 36)
