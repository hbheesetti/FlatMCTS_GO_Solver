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

    def genmove(self, state, color, rand):
        assert not state.endOfGame()
        rule, moves = self.ruleBasedMoves(state, color, rand)
        numMoves = len(moves)
        score = [0] * numMoves
        for i in range(numMoves):
            move = moves[i]
            print(move)
            score[i] = self.simulate(state, move, rand)
        bestIndex = score.index(max(score))
        best = moves[bestIndex]
        assert best in state.legalMoves()
        return best
    
    def ruleBasedMoves(self, board: GoBoard, color, rand: bool) -> Tuple[str, List[int]]:
        """
        return: (MoveType, MoveList)
        MoveType: {"Win", "BlockWin", "OpenFour", "Capture", "Random"}
        MoveList: an unsorted List[int], each element is a move
        """
        if rand == False:
            rule, moves = board.detect_n_in_row(color)
            if len(moves) > 0:
                return rule, moves
        result = board.get_empty_points()
        return "Random", result

    def simulate(self, state, move, rand):
        num_wins = 0
        num_draws = 0
        for _ in range(self.numSimulations):
            board_copy = state.copy()
            board_copy.play_move(move, state.current_player)
            winner = board_copy.detect_five_in_a_row()
            while winner == EMPTY and len(board_copy.get_empty_points()) != 0:
                _,moves = self.ruleBasedMoves(board_copy, board_copy.current_player, rand)
                print(moves)
                random_move = random.choice(moves)
                board_copy.play_move(random_move, board_copy.current_player)
                winner = board_copy.detect_five_in_a_row()
            if winner == state.current_player:
                num_wins += 1
            elif winner == EMPTY:
                num_draws += 1
        return num_wins * (self.numSimulations + 1) + num_draws