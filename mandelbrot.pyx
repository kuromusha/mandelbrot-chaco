import numpy as np
cimport numpy as cnp
cimport cython


cdef int mandelbrot_escape(double x, double y, unsigned int n):
    """ Mandelbrot set escape time algorithm in real and complex components
    """
    cdef double z_x = x
    cdef double z_y = y
    cdef unsigned int i
    for i in range(n):
        z_x, z_y = z_x**2 - z_y**2 + x, 2*z_x*z_y + y
        if z_x**2 + z_y**2 >= 4.0:
           return i
    return -1


@cython.boundscheck(False) # turn off bounds-checking for entire function
def generate_mandelbrot(cnp.ndarray[cnp.float64_t, ndim=1] xs,
                        cnp.ndarray[cnp.float64_t, ndim=1] ys,
                        unsigned int n):
    """ Generate a mandelbrot set """
    cdef unsigned int i,j
    cdef unsigned int N = len(xs)
    cdef unsigned int M = len(ys)

    cdef cnp.ndarray[cnp.int64_t, ndim=2] d = np.empty(dtype=np.int64, shape=(M, N))
    for j in range(M):
        for i in range(N):
            d[j, i] = mandelbrot_escape(xs[i], ys[j], n)
    return d
