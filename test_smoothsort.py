import random
from smoothsort import smoothsort


def run_smoothsort(arr):
    sorted_arr = smoothsort(arr)
    benchmark_sorted_arr = sorted(arr)
    print(f'Correct sorted array: {benchmark_sorted_arr[:10]}...')
    print(f'Smooth-sorted array: {sorted_arr[:10]}...')
    assert sorted_arr == benchmark_sorted_arr


def test_smoothsort_integer():
    test_arr = [2, 4, 3, 1, 5]
    run_smoothsort(test_arr)


def test_smoothsort_decimal():
    test_arr = [-2.56, 2.344, 3.2, 1, -5]
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


if __name__ == '__main__':
    test_smoothsort_string()