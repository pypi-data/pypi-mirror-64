import numpy as np
import scipy.optimize
import warnings


def luriegold(R: np.ndarray,
              n_max_post_fit: int = 5) -> (np.ndarray, np.ndarray, dict):
    # pre-optimization step
    C = luriegold_fit(R, maxiter=1000, debug=False)

    # post-optimization step
    k = 0
    while k < n_max_post_fit:
        if np.all(np.diag(C) == 1.0):
            break
        C = np.array(luriegold_fit(C, maxiter=200, debug=False))
        k = k + 1
    # final check
    if not np.allclose(np.diag(C), 1.0):
        warnings.warn(
            "Some diagonals are not 1.0. Try to increase n_max_post_fit")

    # done
    return C


def luriegold_fit(R: np.ndarray,
                  maxiter: int = 1000,
                  debug: bool = False) -> (np.ndarray, np.ndarray, dict):
    """Lurie-Goldberg Algorithm to adjust a correlation
    matrix to be semipositive definite

    Philip M. Lurie and Matthew S. Goldberg (1998), An Approximate Method
       for Sampling Correlated Random Variables from Partially-Specified
       Distributions, Management Science, Vol 44, No. 2, February 1998, pp
       203-218, URL: http://www.jstor.org/stable/2634496
    """

    # subfunctions
    def xtocorr(x: np.ndarray,
                idx: np.ndarray,
                L: np.ndarray) -> (np.ndarray, np.ndarray):
        L[idx] = x  # impute x into 0s matrix
        C = np.dot(L, L.T)
        return C, L

    def objectivefunc(x: np.ndarray,
                      R: np.ndarray,
                      idx: np.ndarray,
                      mat: np.ndarray) -> float:
        C, _ = xtocorr(x, idx, mat)
        f = np.sum((R - C)**2)
        return f

    def nlcon_diagone(x: np.ndarray,
                      idx: np.ndarray,
                      mat: np.ndarray) -> np.ndarray:
        C, _ = xtocorr(x, idx, mat)
        return np.abs(1.0 - np.diag(C))

    # dimension of the correlation matrix
    d = R.shape[0]
    n = int((d**2 + d) / 2.)

    # the lower triangular matrix without values
    mat = np.zeros((d, d), dtype=np.float64)
    idx = np.tril(np.ones((d, d)), k=0) > 0

    # start values of the optimization are Ones
    x0 = np.ones(shape=(n, )) / n

    # the diagonals need to be 1s
    condiag = {'type': 'eq', 'args': (idx, mat), 'fun': nlcon_diagone}

    # optimization
    algorithm = 'SLSQP'
    opt = {'disp': False, 'maxiter': maxiter, 'ftol': 1e-10}

    # run the optimization
    res = scipy.optimize.minimize(
        objectivefunc, x0,
        args=(R, idx, mat),
        constraints=[condiag],
        method=algorithm,
        options=opt)

    # Compute Correlation Matrix
    C, L = xtocorr(res.x, idx, mat)

    # done
    if debug:
        return C, L, res
    else:
        return C
