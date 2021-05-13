import pytest
import random
import array
from smoothsort import smoothsort


def run_smoothsort(arr, key=None):
    sorted_arr = smoothsort(arr, compare_key=key)
    benchmark_sorted_arr = sorted(arr, key=key)
    print(f'Correct sorted array: {benchmark_sorted_arr[:10]}...')
    print(f'Smooth-sorted array: {sorted_arr[:10]}...')
    assert sorted_arr == benchmark_sorted_arr


def test_smoothsort_redundant_arr():
    test_arr = []
    run_smoothsort(test_arr)


def test_smoothsort_invalid_input():
    test_arr = 'abcdge'
    with pytest.raises(TypeError):
        run_smoothsort(test_arr)


def test_smoothsort_heterogeneous_dtype():
    test_arr = [2, 3.1, 'b', 'a', False]
    with pytest.raises(TypeError):
        run_smoothsort(test_arr)


def test_smoothsort_integer():
    test_arr = [2, 4, 3, 1, -5]
    run_smoothsort(test_arr)


def test_smoothsort_float():
    test_arr = [-2.56, 2.344, 3.2, 1.0, -5.1]
    run_smoothsort(test_arr)


def test_smoothsort_load():
    test_size = 2000
    test_arr = list(range(test_size))
    random.shuffle(test_arr)
    run_smoothsort(test_arr)


def test_smoothsort_sorted_load():
    test_size = 2000
    test_arr = list(range(test_size))
    run_smoothsort(test_arr)


def test_smoothsort_same_load():
    test_size = 2000
    test_arr = [0 for i in range(test_size)]
    run_smoothsort(test_arr)


def test_smoothsort_string():
    test_arr = ['abb', 'abb', 'bc*', 'ghhl', 'ghh1', ' ']
    run_smoothsort(test_arr)


def test_smoothsort_same_string():
    test_arr = ['a', 'a', 'a', 'a', 'a']
    run_smoothsort(test_arr)


def test_smoothsort_boolean():
    test_arr = [False, True, False, True, False]
    run_smoothsort(test_arr)


def test_smoothsort_tuple():
    test_arr = [(2, 2), (3, 4), (1, 2), (1, 3), (2, 3, 4)]
    run_smoothsort(test_arr)


def test_smoothsort_lists():
    test_arr = [[1, 3, 5], [1, 3, 6], [3], [5, 2], [5, 1]]
    run_smoothsort(test_arr)


def test_smoothsort_sets():
    test_arr = [{1, 3, 5}, {1, 3, 6}, {3}, {5, 2}, {5, 1}]
    run_smoothsort(test_arr)


def test_smoothsort_arrays():
    test_arr_1 = array.array('I', [1, 3, 4])
    test_arr_2 = array.array('I', [1, 3, 5])
    test_arr = [test_arr_1, test_arr_2]
    run_smoothsort(test_arr)


def test_smoothsort_dicts():
    test_arr = [{'a': 1}, {'a': 4}, {'c': 2}, {'b': 4}, {'d': {'a': 2}}]
    compare_key = lambda x: list(x)
    run_smoothsort(
        test_arr,
        key=compare_key
    )


if __name__ == '__main__':
    test_smoothsort_string()