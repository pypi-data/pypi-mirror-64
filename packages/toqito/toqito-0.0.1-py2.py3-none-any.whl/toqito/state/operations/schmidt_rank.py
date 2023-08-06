"""Computes the Schmidt rank of a bipartite vector."""
from typing import List, Union
import numpy as np

from toqito.super_operators.partial_trace import partial_trace


def schmidt_rank(
    vec: np.ndarray, dim: Union[int, List[int], np.ndarray] = None
) -> float:
    r"""
    Compute the Schmidt rank.

    For complex Euclidean spaces :math:`\mathcal{X}` and :math:`\mathcal{Y}`, a
    pure state :math:`u \in \mathcal{X} \otimes \mathcal{Y}` possesses an
    expansion of the form:

    .. math::
        u = \sum_{i} \lambda_i v_i w_i

    where :math:`v_i \in \mathcal{X}` and :math:`w_i \in \mathcal{Y}` are
    orthonormal states.

    The Schmidt coefficients are calculated from

    .. math::
        A = \text{Tr}_{\mathcal{B}}(u^* u).

    The Schmidt rank is the number of non-zero eigenvalues of A. The Schmidt
    rank allows us to determine if a given state is entangled or separable.
    For instance:

        - If the Schmidt rank is 1: The state is separable
        - If the Schmidt rank > 1: The state is entangled.

    Compute the Schmidt rank of the vector `vec`, assumed to live in bipartite
    space, where both subsystems have dimension equal to `sqrt(len(vec))`.

    The dimension may be specified by the 1-by-2 vector `dim` and the rank in
    that case is determined as the number of Schmidt coefficients larger than
    `tol`.

    References:
        [1] Wikipedia: Schmidt rank
        https://en.wikipedia.org/wiki/Schmidt_decomposition#Schmidt_rank_and_entanglement

    :param vec: A bipartite vector to have its Schmidt rank computed.
    :param dim: A 1-by-2 vector.
    :return: The Schmidt rank of vector `vec`.
    """
    eps = np.finfo(float).eps
    slv = int(np.round(np.sqrt(len(vec))))

    if dim is None:
        dim = slv

    if isinstance(dim, int):
        dim = np.array([dim, len(vec) / dim])
        if np.abs(dim[1] - np.round(dim[1])) >= 2 * len(vec) * eps:
            raise ValueError(
                "Invalid: The value of `dim` must evenly divide "
                "`len(vec)`; please provide a `dim` array "
                "containing the dimensions of the subsystems"
            )
        dim[1] = np.round(dim[1])

    rho = vec.conj().T * vec
    rho_a = partial_trace(rho, 2)

    # Return the number of non-zero eigenvalues of the
    # matrix that traced out the second party's portion.
    return len(np.nonzero(np.linalg.eigvalsh(rho_a))[0])
