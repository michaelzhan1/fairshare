from typing import List
import numpy as np
from collections import defaultdict
import networkx as nx

def simplify_matrix_min_transactions(mat):
    n = mat.shape[0]
    simplified_mat = np.copy(mat)

    # Step 1: Create a directed graph and add edges based on matrix values
    G = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            if i != j and simplified_mat[i, j] > 0:
                G.add_edge(i, j, weight=simplified_mat[i, j])

    # Step 2: Use the Floyd-Warshall algorithm to find the shortest paths
    path_lengths = nx.floyd_warshall_numpy(G, weight='weight')

    # Step 3: Generate the simplified matrix with minimum transactions
    simplified_mat_min_transactions = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                min_amount = simplified_mat[i, j]
                min_path = nx.shortest_path(G, i, j, weight='weight')
                for k in range(len(min_path) - 1):
                    u = min_path[k]
                    v = min_path[k + 1]
                    min_amount = min(min_amount, simplified_mat[u, v])
                simplified_mat_min_transactions[i, j] = min_amount

    return simplified_mat_min_transactions


def _simplify(matrix: np.ndarray) -> np.ndarray:
    """ Simplify a debt matrix to reduce the number of transactions.

    This function takes in a debt matrix and simplifies it by reducing the number of transactions needed to balance the debt.

    Args:
        matrix (np.ndarray): an upper triangular 2D NumPy array representing the debt matrix
    
    Returns:
        A simplified version of the inputted matrix
    """
    balances = defaultdict(float)
    for i in range(matrix.shape[0]):
        for j in range(i + 1, matrix.shape[1]):
            balances[j] += matrix[i, j]
            balances[i] -= matrix[i, j]
    print(balances)
    
    zeros = [i for i, balance in balances.items() if balance == 0]
    for i in zeros:
        matrix[i, :] = 0
        matrix[:, i] = 0

    positives = [i for i, balance in balances.items() if balance > 0]
    negatives = [i for i, balance in balances.items() if balance < 0]

    for i in positives:
        for j in negatives:
            # if the positive balance can take on the negative balance:
            if balances[i] + balances[j] > 0:
                pass
    return matrix



def calculate(persons: List[str], expenses: List[float], paid_by: List[str], involved: List[List[str]]) -> np.ndarray:
    """ Calculate how much each person owes or is owed, based on inputted payments.

    This function takes in payment information (who paid, who was involved, how much was paid), and calculates how much each person owes each other.

    Args:
        persons (List[str]): a list of names of all people involved in the payments
        expenses (List[float]): a list of the amounts paid for each expense
        paid_by (List[str]): a list of names of the people who paid for each expense
        involved (List[List[str]]): a list of lists of names of people involved in each expense, including the person who paid

    Returns:
        An upper triangular 2D NumPy matrix of dimensions (len(persons), len(persons)), where each element represents the balance between the row person and the column person. If the element is positive, the row person owes the column person that amount. If the element is negative, the column person owes the row person that amount. If the element is zero, the row person and the column person are even.

    Raises:
        ValueError: if the length of the ``expenses``, ``paid_by``, or ``involved`` lists are not equal
    """

    # check that the lengths of the lists are equal
    if not (len(expenses) == len(paid_by) == len(involved)):
        raise ValueError("The lengths of the expenses, paid_by, and involved lists must be equal.")
    
    # create a dictionary mapping each person to an ID, used for indexing the matrix
    person_to_id = {person: i for i, person in enumerate(persons)}
    n = len(persons)

    # create a matrix of zeros
    # matrix[i, j] represents how much person i owes person j
    matrix = np.zeros((n, n))

    # for each expense, add the amount to the matrix for all people involved that are not the person who paid
    for expense, paid_by, involved in zip(expenses, paid_by, involved):
        # calculate the amount each person owes
        amount = expense / len(involved)

        # add the amount to the matrix for each person involved
        for person in involved:
            if person != paid_by:
                matrix[person_to_id[person], person_to_id[paid_by]] += amount

    # simplify the matrix to only include the upper triangular part
    # if A owes B $10 and B owes A $5, then A owes B $5
    for i in range(n):
        for j in range(i):
            matrix[j, i] -= matrix[i, j]
            matrix[i, j] = 0

    return matrix


def main():
    persons = ["A", "B", "C"]
    expenses = [30, 60, 90]
    paid_by = ["A", "B", "C"]
    involved = [["A", "B", "C"], ["A", "B", "C"], ["A", "B", "C"]]
    matrix = np.array(
        [
            [10, 30],
            [0, 20],
        ]
    )
    print(_simplify(matrix))
    print(simplify_matrix_min_transactions(matrix))


if __name__ == "__main__":
    main()