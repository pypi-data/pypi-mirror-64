"""Determines if a set of matrices are valid POVM operators."""
from typing import List
import numpy as np

from toqito.matrix.properties.is_psd import is_psd


def is_povm(mat_list: List[np.ndarray]) -> bool:
    r"""
    Determine if a list of matrices constitute a valid set of POVMs.

    A valid set of measurements are defined by a set of positive semidefinite
    operators

    .. math::
         \{P_a : a \in \Gamma\} \subset \text{Pos}(\mathcal{X})

    indexed by the alphabet :math:`\Gamma` of measurement outcomes satisfying
    the constraint that

    .. math::
        \sum_{a \in \Gamma} P_a = I_{\mathcal{X}}.

    References:
        [1] Wikipedia: POVM
        https://en.wikipedia.org/wiki/POVM

    :param mat_list: A list of matrices.
    :return: True if set of matrices constitutes a set of measurements, and
             False otherwise.
    """
    dim = mat_list[0].shape[0]

    mat_sum = np.zeros((dim, dim), dtype=complex)
    for mat in mat_list:
        # Each measurement in the set must be positive semidefinite.
        if not is_psd(mat):
            return False
        mat_sum += mat
    # Summing all the measurements from the set must be equal to the identity.
    if not np.allclose(np.identity(dim), mat_sum):
        return False
    return True
