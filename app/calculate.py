from typing import List, Union, Dict, Tuple
import numpy as np
from collections import defaultdict


def _generate_debt_lists(matrix: np.ndarray) -> Tuple[List[Union[float, int]]]:
    """ Generate lists of credits and debts from a matrix.

    This function takes an upper triangular matrix, where each element represents how much the row person owes the column person.

    Args:
        matrix (np.ndarray): an upper triangular 2D NumPy matrix

    Returns:
        A tuple of two lists. The first list contains a list of lists of the form [amount, person] indicating the amount that a person is owed. The second list contains a list of lists of the form [amount, person] indicating the amount that a person owes, where the amount is negative.
    """
    balances = defaultdict(float)
    n = matrix.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            balances[i] -= matrix[i, j]
            balances[j] += matrix[i, j]
    positives = [[amt, person] for person, amt in balances.items() if amt > 0]
    negatives = [[amt, person] for person, amt in balances.items() if amt < 0]
    return positives, negatives


def _simplify(matrix: np.ndarray) -> np.ndarray:
    """ Simplify a matrix to reduce the number of transactions needed.

    Args:
        matrix (np.ndarray): an upper triangular square 2D NumPy matrix

    Returns:
        A simplified version of the matrix, where the number of transactions needed to settle the debts is minimized.
    """
    positives, negatives = _generate_debt_lists(matrix)
    
    global_best_transaction_count = float('inf')
    global_best_transactions = None
    
    def update_best_transactions(positives: List[List[Union[float, int]]], negatives: List[List[Union[float, int]]], transactions: List[List[Union[float, int]]]) -> None:
        """ Finds the smallest number of transactions needed to settle the debts, and the transactions needed to do so.

        This function recursively finds the smallest number of transactions needed to settle the debts, and the transactions needed to do so. It does so by trying all possible combinations of transactions, and keeping track of the best one using a nonlocal variable.

        Args:
            positives (List[List[Union[float, int]]]): a list of lists of the form [amount, person] indicating the amount that a person is owed
            negatives (List[List[Union[float, int]]]): a list of lists of the form [amount, person] indicating the amount that a person owes, where the amount is negative
            transactions (List[List[Union[float, int]]]): a list of lists of the form [person1, person2, amount] indicating a transaction where person1 pays person2 the amount
        
        Returns:
            None
        """
        nonlocal global_best_transaction_count, global_best_transactions

        if len(positives) == 0 and len(negatives) == 0 or len(transactions) >= global_best_transaction_count:
            if len(transactions) < global_best_transaction_count:
                global_best_transaction_count = len(transactions)
                global_best_transactions = transactions
            return
        
        for i in range(len(positives)):
            for j in range(len(negatives)):
                pamt, pperson = positives[i]
                namt, nperson = negatives[j]
                if pamt == -namt: # find 2 equal transactions
                    update_best_transactions(positives[:i] + positives[i + 1:], negatives[:j] + negatives[j + 1:], transactions + [(nperson, pperson, pamt)])
                elif pamt > -namt: # negative cannot pay full amount
                    positives[i][0] += namt
                    update_best_transactions(positives, negatives[:j] + negatives[j + 1:], transactions + [(nperson, pperson, -namt)])
                    positives[i][0] -= namt
                else: # negative can pay full amount and more
                    negatives[j][0] += pamt
                    update_best_transactions(positives[:i] + positives[i + 1:], negatives, transactions + [(nperson, pperson, pamt)])
                    negatives[j][0] -= pamt
        return

    update_best_transactions(positives, negatives, [])
    new_matrix = np.zeros_like(matrix)
    for nperson, pperson, amt in global_best_transactions:
        new_matrix[nperson, pperson] += amt
    return new_matrix
        
    
def _calculate(persons: List[str], expenses: List[float], paid_by: List[str], involved: List[List[str]]) -> np.ndarray:
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
    return _simplify(matrix)


def calculate_debts(persons: List[str], expenses: List[float], paid_by: List[str], involved: List[List[str]]) -> List[List[Union[str, float]]]:
    """ Wrapper for _calculate that returns a more easily parsable list of debts.

    This function takes in payment information (who paid, who was involved, how much was paid), and calculates how much each person owes each other.

    Args:
        persons (List[str]): a list of names of all people involved in the payments
        expenses (List[float]): a list of the amounts paid for each expense
        paid_by (List[str]): a list of names of the people who paid for each expense
        involved (List[List[str]]): a list of lists of names of people involved in each expense, including the person who paid

    Returns:
        A list of lists of the form [person1, person2, amount] indicating that person1 owes person2 the amount
    """
    debt_matrix = _calculate(persons, expenses, paid_by, involved)
    n = debt_matrix.shape[0]
    debts = []
    for i in range(n):
        for j in range(i + 1, n):
            if debt_matrix[i, j] != 0:
                debts.append([persons[i], persons[j], debt_matrix[i, j]])
    return debts


def main():
    persons = ["A", "B", "C", "D", "E", "F"]
    expenses = [6, 2, 12, 8, 22]
    paid_by = ["D", "D", "E", 'E', 'F']
    involved = [["A", "D"], ["B", "D"], ['B', 'E'], ['C', 'E'], ['C', 'F']]
    debts = calculate_debts(persons, expenses, paid_by, involved)
    for f, t, amt in debts:
        print(f"{f} owes {t} ${amt:.2f}")


if __name__ == "__main__":
    main()