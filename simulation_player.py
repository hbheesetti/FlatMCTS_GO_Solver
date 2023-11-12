from board_base import EMPTY, BLACK, WHITE
import random
from board_util import GoBoardUtil
from board import GoBoard
from typing import List, Tuple

class SimulationPlayer(object):
    def __init__(self, numSimulations):
        self.numSimulations = numSimulations

    def name(self):
        return "Simulation Player ({0} sim.)".format(self.numSimulations)

    def genmove(self, state):
        assert not state.endOfGame()
        moves = state.legalMoves()
        numMoves = len(moves)
        score = [0] * numMoves
        for i in range(numMoves):
            move = moves[i]
            score[i] = self.simulate(state, move)
        #print(score)
        bestIndex = score.index(max(score))
        best = moves[bestIndex]
        #print("Best move:", best, "score", score[best])
        assert best in state.legalMoves()
        return best
    
    def generateRuleBasedMoves(self, board: GoBoard, color) -> Tuple[str, List[int]]:
        """
        return: (MoveType, MoveList)
        MoveType: {"Win", "BlockWin", "OpenFour", "BlockOpenFour", "Random"}
        MoveList: an unsorted List[int], each element is a move
        """
        self.board = board
        result = self.board.get_empty_points()
        return ("Random", result)

    def simulate(self, state, move):
        num_wins = 0
        num_draws = 0
        for _ in range(self.numSimulations):
            board_copy = state.copy()
            board_copy.play_move(move, state.current_player)
            winner = board_copy.detect_five_in_a_row()
            while winner == EMPTY and len(board_copy.get_empty_points()) != 0:
                moves = self.generateRuleBasedMoves(board_copy, board_copy.current_player)[1]
                random_move = random.choice(moves)
                board_copy.play_move(random_move, board_copy.current_player)
                winner = board_copy.detect_five_in_a_row()
            if winner == state.current_player:
                num_wins += 1
            elif winner == EMPTY:
                num_draws += 1
        return num_wins * (self.numSimulations + 1) + num_draws