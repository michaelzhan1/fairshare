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
        A 2D NumPy matrix of dimensions (len(persons), len(persons)), where each element represents how much the row person owes the column person.

    Raises:
        ValueError: if the length of the expenses, paid_by, or involved lists are not equal
    """

    person_to_id = {person: i for i, person in enumerate(persons)}
    n = len(persons)

    # create a matrix of zeros
    matrix = np.zeros((n, n))
    