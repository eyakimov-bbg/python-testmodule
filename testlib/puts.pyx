cdef extern from "stdio.h":
    cdef int puts(const char *)


def py_puts(s: str):
    puts(s.encode())
