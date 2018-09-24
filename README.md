# fast_array

Move N-Sized arrays of `ctypes` between processes using `multiprocessing.Value`s.

This us much faster than using a `multiprocessing.Pipe`, but can functionally acomplish the same thing.
