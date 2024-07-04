import random
import math
from typing import List, Tuple

def evaluation(board: List[int]) -> int:
    n = len(board)
    conflicts = 0
    #conflicts
    for i in range(n):
        for j in range(i + 1, n):

            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

            if board[i] == board[j]:
                conflicts += 1
    return conflicts


# finding neighbors
def neighbors(board: List[int]) -> List[List[int]]:
    n = len(board)
    neighbor_list = []
    for i in range(n):
        for j in range(n):
            if j != board[i]:
                new_board = board.copy()
                new_board[i] = j
                neighbor_list.append(new_board)
    return neighbor_list


def best_neighbor(population: List[List[int]], eval_type: int, sideway_moves: bool) -> Tuple[List[int], int]:
    best = None
    best_eval = float('inf')
    for board in population:
        eval_score = evaluation(board)
        if eval_score < best_eval or (sideway_moves and eval_score == best_eval):
            best = board
            best_eval = eval_score
    return best, best_eval


def random_state(n: int) -> List[int]:
    state = list(range(n))
    random.shuffle(state)
    return state


def temp(t: int) -> float:
    return max(0.01, min(1, 1.0 - math.log10((t + 1) / 1000)))


def hill_climbing(n: int, eval_type: int, random_restarts: int, sideway_moves: int) -> Tuple[List[int], int, int]:
    best_board = None
    best_eval = float('inf')
    moves = 0

    for r in range(random_restarts):
        current_board = random_state(n)
        current_eval = evaluation(current_board)
        steps = 0

        while True:
            population = neighbors(current_board)
            next_board, next_eval = best_neighbor(population, eval_type, sideway_moves > 0)
            if next_eval < current_eval:
                current_board = next_board
                current_eval = next_eval
                moves += 1
                steps += 1
            elif next_eval == current_eval and sideway_moves > 0:
                current_board = next_board
                current_eval = next_eval
                moves += 1
                steps += 1
                sideway_moves -= 1
            else:
                break

        if current_eval < best_eval:
            best_eval = current_eval
            best_board = current_board

        if best_eval == 0:
            break

    return best_board, best_eval, moves


def simulated_annealing(n: int, eval_type: int) -> Tuple[List[int], int, int]:
    current_board = random_state(n)
    current_eval = evaluation(current_board)
    best_board = current_board
    best_eval = current_eval
    moves = 0
    t = 0

    while temp(t) > 0.01:
        population = neighbors(current_board)
        next_board = random.choice(population)
        next_eval = evaluation(next_board)
        delta_eval = next_eval - current_eval

        if delta_eval < 0 or random.uniform(0, 1) < math.exp(-delta_eval / temp(t)):
            current_board = next_board
            current_eval = next_eval
            moves += 1

        if current_eval < best_eval:
            best_eval = current_eval
            best_board = current_board

        if best_eval == 0:
            break

        t += 1

    return best_board, best_eval, moves


def main():
    print("solving n_queens problem with simulated annealing algorithm")
    n = int(input("num of queens:"))
    print("choose evaluation type:")
    print("num of all conflicts = 0")
    print("num of rows and diagonals that have conflicts = 1")
    print("conflicts of per queen = 2")
    eval_type = int(input("choose from {0, 1, 2}:"))
    algorithm = input("hill_climbing or simulated_annealing: ")
    if algorithm == "hill_climbing":
        random_restarts = int(input("num of restarts:"))
        sideway_moves = int(input("num of side away moves:"))
        solution, eval_score, moves = hill_climbing(n, eval_type, random_restarts, sideway_moves)
    elif algorithm == "simulated_annealing":
        solution, eval_score, moves = simulated_annealing(n, eval_type)
    else:
        print("algorithm is not true")
        return

    #result
    print("best answer:", solution)
    print("final evaluation:", eval_score)
    print("total movements:", moves)

if __name__ == '__main__':
    main()
