from typing import List
import numpy as np


# should take in a list of people, a list of expenses (including who was involved), and a list of who paid for each expense
def calculate(persons: List[str], expenses: List[float], paid_by: List[str], involved: List[List[str]]) -> List[List[float]]:
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
    expenses = [100, 200, 300]
    paid_by = ["A", "B", "C"]
    involved = [["A", "B", "C"], ["A", "B", "C"], ["A", "B", "C"]]
    print(calculate(persons, expenses, paid_by, involved))


if __name__ == "__main__":
    main()