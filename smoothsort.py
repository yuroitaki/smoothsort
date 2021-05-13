import random

LEONARDO_NUMBERS = [
    1, 1, 3, 5, 9, 15, 25, 41, 67, 109, 177, 287, 465, 753, 1219,
    1973, 3193, 5167, 8361, 13529, 21891, 35421, 57313, 92735,
    150049, 242785, 392835, 635621, 1028457, 1664079, 2692537,
    4356617, 7049155, 11405773, 18454929, 29860703, 48315633,
    78176337, 126491971, 204668309, 331160281, 535828591, 866988873,
    1402817465, 2269806339, 3672623805, 5942430145, 9615053951,
    15557484097, 25172538049, 40730022147, 65902560197, 106632582345,
    172535142543, 279167724889, 451702867433, 730870592323,
    1182573459757, 1913444052081, 3096017511839, 5009461563921,
    8105479075761, 13114940639683, 21220419715445, 34335360355129,
    55555780070575, 89891140425705, 145446920496281, 235338060921987,
    380784981418269, 616123042340257, 996908023758527, 1613031066098785,
    2609939089857313, 4222970155956099, 6832909245813413,
    11055879401769513, 17888788647582927, 28944668049352441,
    46833456696935369, 75778124746287811, 122611581443223181,
    198389706189510993, 321001287632734175, 519390993822245169,
    840392281454979345, 1359783275277224515, 2200175556732203861,
    3559958832009428377, 5760134388741632239, 9320093220751060617,
    15080227609492692857
]


def _get_leonardo_number(heap_order):
    try:
        leonardo_number = LEONARDO_NUMBERS[heap_order]
    except IndexError:
        raise ValueError('HEAP_ORDER_BIGGER_THAN_MAX_LIMIT')
    else:
        return leonardo_number


def _get_right_child_index(node_index):
    right_child_index = node_index - 1
    if right_child_index < 0:
        raise ValueError('RIGHT_CHILD_DOES_NOT_EXIST')
    return right_child_index


def _get_left_child_index(node_index, heap_order):
    try:
        right_child_index = _get_right_child_index(node_index)
    except ValueError:
        raise ValueError('LEFT_CHILD_DOES_NOT_EXIST')
    else:
        right_child_heap_size = _get_leonardo_number(
            _get_right_child_heap_order(heap_order)
        )
        return right_child_index - right_child_heap_size


def _get_right_child_heap_order(heap_order):
    right_child_heap_order = heap_order - 2
    if right_child_heap_order < 0:
        raise ValueError('RIGHT_CHILD_DOES_NOT_EXIST')
    return right_child_heap_order


def _get_left_child_heap_order(heap_order):
    left_child_heap_order = heap_order - 1
    if left_child_heap_order < 0 or heap_order == 1:
        raise ValueError('LEFT_CHILD_DOES_NOT_EXIST')
    return left_child_heap_order


def _get_left_root_index(root_index, heap_order):
    root_heap_size = _get_leonardo_number(heap_order)
    left_root_index = root_index - root_heap_size
    if left_root_index < 0:
        raise ValueError('LEFT_ROOT_DOES_NOT_EXIST')
    return left_root_index


def _swap_node(arr, left_index, right_index):
    arr[left_index], arr[right_index] = arr[right_index], arr[left_index]


def _enqueue_node(heap_orders):
    heap_orders_len = len(heap_orders)
    if heap_orders_len > 1 and (heap_orders[-2] - heap_orders[-1] == 1):
        heap_orders.pop()
        heap_orders[-1] += 1
    elif heap_orders_len >= 1 and heap_orders[-1] == 1:
        heap_orders.append(0)
    else:
        heap_orders.append(1)


def _trinkle(arr, heap_orders, root_index, heap_order_index):
    if heap_order_index == 0:
        return root_index, heap_order_index

    left_root_index = _get_left_root_index(root_index, heap_orders[heap_order_index])

    if arr[left_root_index] <= arr[root_index]:
        return root_index, heap_order_index

    if heap_orders[heap_order_index] > 1:
        left_child_index = _get_left_child_index(
            root_index,
            heap_orders[heap_order_index]
        )
        right_child_index = _get_right_child_index(root_index)

        if arr[left_root_index] <= arr[left_child_index] or (
            arr[left_root_index] <= arr[right_child_index]
        ):
            return root_index, heap_order_index

    _swap_node(arr, left_root_index, root_index)
    return _trinkle(arr, heap_orders, left_root_index, heap_order_index - 1)


def _sift(arr, root_index, heap_order):
    if heap_order <= 1:
        return

    largest_node_index = root_index
    largest_node_heap_order = heap_order
    left_child_index = _get_left_child_index(root_index, heap_order)
    right_child_index = _get_right_child_index(root_index)

    if arr[largest_node_index] < arr[left_child_index]:
        largest_node_index = left_child_index
        largest_node_heap_order = _get_left_child_heap_order(heap_order)

    if arr[largest_node_index] < arr[right_child_index]:
        largest_node_index = right_child_index
        largest_node_heap_order = _get_right_child_heap_order(heap_order)

    if largest_node_index == root_index:
        return

    _swap_node(arr, root_index, largest_node_index)
    _sift(arr, largest_node_index, largest_node_heap_order)


def _leonardo_heapify(arr, arr_len):
    print(f'Heapifying array into Leonardo heaps')
    heap_orders = []
    for node_index in range(arr_len):
        _enqueue_node(heap_orders)
        heap_order_index = len(heap_orders) - 1
        root_index, heap_order_index = _trinkle(
            arr,
            heap_orders,
            node_index,
            heap_order_index
        )
        _sift(
            arr,
            root_index,
            heap_orders[heap_order_index]
        )
    return heap_orders


def _dequeue_node(arr, arr_len, heap_orders):
    print(
        f'Dequeueing max nodes from Leonardo heaps with these orders: {heap_orders[:10]}'
    )
    for node_index in range(arr_len - 1, 0, -1):
        dequeued_heap_order = heap_orders.pop()
        if dequeued_heap_order != 1 and dequeued_heap_order != 0:
            heap_orders.extend([
                _get_left_child_heap_order(dequeued_heap_order),
                _get_right_child_heap_order(dequeued_heap_order)
            ])

            left_child_index = _get_left_child_index(node_index, dequeued_heap_order)
            left_child_heap_order_index = len(heap_orders) - 2
            left_root_index, left_heap_order_index = _trinkle(
                arr,
                heap_orders,
                left_child_index,
                left_child_heap_order_index
            )
            _sift(arr, left_root_index, heap_orders[left_heap_order_index])

            right_child_index = _get_right_child_index(node_index)
            right_child_heap_order_index = len(heap_orders) - 1
            right_root_index, right_heap_order_index = _trinkle(
                arr,
                heap_orders,
                right_child_index,
                right_child_heap_order_index
            )
            _sift(arr, right_root_index, heap_orders[right_heap_order_index])


def smoothsort(arr):
    if type(arr) != list:
        print(f'Input is not an array - terminating sorting operation: {arr}')
        raise TypeError('INPUT_IS_NOT_AN_ARRAY')
    arr_len = len(arr)
    if arr_len <= 1:
        print(f'Array only contains less than 1 element - no need to sort: {arr}')
        return arr
    print(f'Smooth-sorting array: {arr[:10]}...')
    heap_orders = _leonardo_heapify(arr, arr_len)
    _dequeue_node(arr, arr_len, heap_orders)
    print(f'Finished smooth-sorting array')
    return arr


def test_smoothsort(arr):
    sorted_arr = smoothsort(arr)
    benchmark_sorted_arr = sorted(arr)
    print(f'Correct sorted array: {benchmark_sorted_arr[:10]}...')
    print(f'Smooth-sorted array: {sorted_arr[:10]}...')
    assert sorted_arr == benchmark_sorted_arr


if __name__ == '__main__':
    test_arr_0 = [2, 4, 3, 1, 5]

    test_arr_1 = [-2, 4, 3, 1, -5]

    test_size = 2000
    test_arr_2 = list(range(test_size))
    random.shuffle(test_arr_2)

    test_arr_3 = list(range(test_size))

    test_arr_4 = [0 for i in range(test_size)]

    test_arr_5 = ['abb', 'abb', 'bc', 'ghhl', 'ghh1']

    test_arr_6 = ['a', 'a', 'a', 'a', 'a']

    test_arr_7 = [-2.56, 2.344, 3.2, 1, -5]

    test_smoothsort(test_arr_7)
