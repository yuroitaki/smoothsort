# Scope
A Python implementation of Dijkstra's smoothsort algorithm.

# Details
- Implemented in-place sorting with an auxiliary array to store the location of each Leonardo heap
- Cater for all primitive data types, and some iterables (list, array, set, tuple)
- -  For other data types, a custom `compare_key` function needs to be supplied
- Input array supplied must be of Python built-in `list` type
- Input array must only contain homogeneous data types