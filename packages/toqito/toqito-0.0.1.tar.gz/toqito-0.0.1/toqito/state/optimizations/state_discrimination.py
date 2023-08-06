"""Calculates probability of state discrimination."""
from typing import List
import cvxpy as cvx
import numpy as np


def state_discrimination(states: List[np.ndarray], probs: List[float] = None) -> float:
    r"""
    Compute probability of state discrimination.

    The "quantum state discrimination" problem involves a collection of :math:
    `n` quantum states

    ..math::
        `\rho = \{ \rho_0, \ldots, \rho_n \},`

    as well as a list of corresponding probabilities

    ..math::
        `p = \{ p_0, \ldots, p_n \}`

    Alice chooses :math: `i` with probability `p_i` and creates the state
    :math: `rho_i`

    Bob wants to guess which state he was given from the collection of states.

    This function implements the following semidefinite program that provides
    the optimal probability with which Bob can conduct quantum state exclusion.

    ..math::
        ````
        \begin{align*}
            \text{maximize:} \quad & \sum_{i=0}^n p_i \ip{M_i}{\rho_i} \\
            \text{subject to:} \quad & M_0 + \ldots + M_n = \mathbb{I},\\
                                     & M_0, \ldots, M_n >= 0
            \end{align*}
        ```

    References:
    [1] Eldar, Yonina C.
        "A semidefinite programming approach to optimal unambiguous
        discrimination of quantum states."
        IEEE Transactions on information theory 49.2 (2003): 446-456.
        https://arxiv.org/abs/quant-ph/0206093

    :param states: A list of density operators (matrices) corresponding to
                   quantum states.
    :param probs: A list of probabilities where `probs[i]` corresponds to the
                  probability that `states[i]` is selected by Alice.
    :return: The optimal probability with which Bob can guess the state he was
             not given from `states`.
    """
    # Assume that at least one state is provided.
    if states is None or states == []:
        raise ValueError("InvalidStates: There must be at least one state " "provided.")

    # Assume uniform probability if no specific distribution is given.
    if probs is None:
        probs = [1 / len(states)] * len(states)
    if not np.isclose(sum(probs), 1):
        raise ValueError("Invalid: Probabilities must sum to 1.")

    dim_x, dim_y = states[0].shape

    # The variable `states` is provided as a list of vectors. Transform them
    # into density matrices.
    if dim_y == 1:
        for i, state_ket in enumerate(states):
            states[i] = state_ket * state_ket.conj().T

    obj_func = []
    measurements = []
    constraints = []
    for i, _ in enumerate(states):
        measurements.append(cvx.Variable((dim_x, dim_x), PSD=True))

        obj_func.append(probs[i] * cvx.trace(states[i].conj().T @ measurements[i]))

    constraints.append(sum(measurements) == np.identity(dim_x))

    objective = cvx.Maximize(sum(obj_func))
    problem = cvx.Problem(objective, constraints)
    sol_default = problem.solve()

    return 1 / len(states) * sol_default
