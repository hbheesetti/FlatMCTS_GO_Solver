from board_base import EMPTY, BLACK, WHITE
import random

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

    def simulate(self, state, move):
        num_wins = 0
        num_draws = 0
        for _ in range(self.NUM_SIMULATION):
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
        return num_wins * (self.NUM_SIMULATION + 1) + num_draws