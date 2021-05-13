import operator as op

# Precomputed list of Leonardo numbers to save constant computation time
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
    """
    Get leonardo number using order of a Leonardo heap
    :param heap_order (int):
    :return: leonardo_number (int)
    """
    try:
        leonardo_number = LEONARDO_NUMBERS[heap_order]
    except IndexError:
        raise ValueError('HEAP_ORDER_BIGGER_THAN_MAX_LIMIT')
    else:
        return leonardo_number


def _get_right_child_index(node_index):
    """
    Get the index of the right child of a node
    :param node_index (int):
    :return: right_child_index (int)
    """
    right_child_index = node_index - 1
    if right_child_index < 0:
        raise ValueError('RIGHT_CHILD_DOES_NOT_EXIST')
    return right_child_index


def _get_left_child_index(node_index, heap_order):
    """
    Get the index of the left child of a node
    :param node_index (int):
    :param heap_order (int):
    :return: left_child_index (int)
    """
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
    """
    Get the heap order of the right child of a node
    :param heap_order (int):
    :return: right_child_heap_order (int)
    """
    right_child_heap_order = heap_order - 2
    if right_child_heap_order < 0:
        raise ValueError('RIGHT_CHILD_DOES_NOT_EXIST')
    return right_child_heap_order


def _get_left_child_heap_order(heap_order):
    """
    Get the heap order of the left child of a node
    :param heap_order (int):
    :return: left_child_heap_order (int)
    """
    left_child_heap_order = heap_order - 1
    # A heap with order 1 doesn't have any children
    if left_child_heap_order < 0 or heap_order == 1:
        raise ValueError('LEFT_CHILD_DOES_NOT_EXIST')
    return left_child_heap_order


def _get_left_root_index(root_index, heap_order):
    """
    Get the index of the root on the neighbouring left of the current root
    :param root_index (int):
    :param heap_order (int):
    :return: left_root_index (int)
    """
    root_heap_size = _get_leonardo_number(heap_order)
    left_root_index = root_index - root_heap_size
    if left_root_index < 0:
        raise ValueError('LEFT_ROOT_DOES_NOT_EXIST')
    return left_root_index


def _swap_node(arr, left_index, right_index):
    """
    Swap the position of nodes/elements in an array
    :param arr (list):
    :param left_index (int):
    :param right_index (int):
    :return:
    """
    arr[left_index], arr[right_index] = arr[right_index], arr[left_index]


def _compare_node(left_node, right_node, operation, **kwargs):
    """
    Compare the value of left node and right node of any arbitrary data type

    This is done by using
    (1) standard built-in mathematical comparison operator (<=, >, >=).

    If (1) fails, then look for custom user-defined compare_key function
    to extract valid value for comparison using comparison operator

    :param left_node (*): can be of any data type
    :param right_node (*): can be of any data type
    :param operation (operator): mathematical comparison operator (<=, >, >=)
    :param kwargs (dict):
        compare_key (func): user-defined compare_key function to extract valid value
                                for comparison using comparison operator
    :return: comparison_result (bool)
    """
    try:
        return operation(left_node, right_node)
    except TypeError:
        compare_key = kwargs.get('compare_key', None)
        if compare_key is None or not callable(compare_key):
            raise TypeError('NO_COMPARE_KEY_FOR_UNSUPPORTED_DATA_TYPE')
        return operation(
            compare_key(left_node),
            compare_key(right_node)
        )


def _enqueue_node(heap_orders):
    """
    Store the order of each Leonardo heap created when enqueueing node from array
    to keep track the position of each heap in the original array
    :param heap_orders (list):
    :return:
    """
    heap_orders_len = len(heap_orders)
    # Case 1: Order of final two heaps are consecutive Leonardo numbers
    if heap_orders_len > 1 and (heap_orders[-2] - heap_orders[-1] == 1):
        heap_orders.pop()
        heap_orders[-1] += 1
    # Case 2: Order of the final heap is 1
    elif heap_orders_len >= 1 and heap_orders[-1] == 1:
        heap_orders.append(0)
    # Rest of the scenarios
    else:
        heap_orders.append(1)


def _trinkle(arr, heap_orders, root_index, heap_order_index, **kwargs):
    """
    Recursive function to sort the root nodes of Leonardo heaps created so far
    to ensure that they are in ascending order from left to right
    :param arr (list): array to be sorted
    :param heap_orders (list): auxiliary array to store the order of each heap
    :param root_index (int): index of the current root
    :param heap_order_index (int): index of the current heap order in heap_orders array
    :param kwargs (dict):
    :return:
    """
    # Case 1: No neighbouring root node to compare as current root node is the leftmost
    if heap_order_index == 0:
        return root_index, heap_order_index

    left_root_index = _get_left_root_index(root_index, heap_orders[heap_order_index])

    # Case 2: Current root node is already bigger or equal to left root node
    if _compare_node(arr[left_root_index], arr[root_index], op.le, **kwargs):
        return root_index, heap_order_index

    # Ensure that current node has children before inspecting them
    if heap_orders[heap_order_index] > 1:
        left_child_index = _get_left_child_index(
            root_index,
            heap_orders[heap_order_index]
        )
        right_child_index = _get_right_child_index(root_index)

        # Case 3: Either of current children node is already bigger or equal to left
        # root node - no sorting required as subsequent sifting will preserve the order
        if _compare_node(
            arr[left_root_index],
            arr[left_child_index],
            op.le,
            **kwargs
        ) or _compare_node(
            arr[left_root_index],
            arr[right_child_index],
            op.le,
            **kwargs
        ):
            return root_index, heap_order_index

    # Case 4: Left root node is bigger than current root node and its children
    # - swap both the root nodes and continue trinkling process
    # from the left root node position
    _swap_node(arr, left_root_index, root_index)
    return _trinkle(arr, heap_orders, left_root_index, heap_order_index - 1, **kwargs)


def _sift(arr, root_index, heap_order, **kwargs):
    """
    Recursive function to ensure the max heap property is preserved - each parent node
    is bigger or equal to its child nodes
    :param arr (list): array to be sorted
    :param root_index (int): index of the current root node
    :param heap_order (int): order of the current heap
    :param kwargs (dict):
    :return:
    """
    # Case 1: Current root node doesn't have any children
    if heap_order <= 1:
        return

    largest_node_index = root_index
    largest_node_heap_order = heap_order
    left_child_index = _get_left_child_index(root_index, heap_order)
    right_child_index = _get_right_child_index(root_index)

    # Check if left child node is bigger than current root node
    if _compare_node(arr[largest_node_index], arr[left_child_index], op.lt, **kwargs):
        largest_node_index = left_child_index
        largest_node_heap_order = _get_left_child_heap_order(heap_order)

    # Check if right child node is bigger than current root node or left child node
    if _compare_node(arr[largest_node_index], arr[right_child_index], op.lt, **kwargs):
        largest_node_index = right_child_index
        largest_node_heap_order = _get_right_child_heap_order(heap_order)

    # Case 2: Current root node is larger or equal to any of its children nodes
    if largest_node_index == root_index:
        return

    # Case 3: Current root is smaller than either of its children nodes
    # - swap the bigger child node with the root node, and continue the sifting
    # process from the child node position
    _swap_node(arr, root_index, largest_node_index)
    _sift(arr, largest_node_index, largest_node_heap_order, **kwargs)


def _leonardo_heapify(arr, arr_len, **kwargs):
    """
    Create a series of Leonardo heaps from the array to be sorted
    :param arr (list): array to be sorted
    :param arr_len (int): length of the array
    :param kwargs (dict):
    :return: heap_orders (list): auxiliary array to store the order of each heap
    """
    print(f'Heapifying array into Leonardo heaps')
    heap_orders = []
    # Start from the leftmost element until the rightmost element in the array
    for node_index in range(arr_len):
        _enqueue_node(heap_orders)
        heap_order_index = len(heap_orders) - 1

        root_index, heap_order_index = _trinkle(
            arr,
            heap_orders,
            node_index,
            heap_order_index,
            **kwargs
        )

        _sift(
            arr,
            root_index,
            heap_orders[heap_order_index],
            **kwargs
        )
    return heap_orders


def _dequeue_node(arr, arr_len, heap_orders, **kwargs):
    """
    Sort the array by dequeueing the max node from Leonardo heaps
    :param arr (list): array to be sorted
    :param arr_len (int): length of the array
    :param heap_orders (list): auxiliary array to store the order of each heap
    :param kwargs:
    :return:
    """
    print(
        f'Dequeueing max nodes from Leonardo heaps with these orders: {heap_orders[:10]}'
    )
    # Start from the rightmost element as it is the biggest
    for node_index in range(arr_len - 1, 0, -1):
        # Remove the last heap order stored
        dequeued_heap_order = heap_orders.pop()
        # Case 1: If last heap order is 1 or 0, do nothing as no sifting/trinkling required
        # Case 2: Children nodes of the last root node is exposed - sifting/trinkling required
        if dequeued_heap_order != 1 and dequeued_heap_order != 0:
            # Store the heap orders of exposed children nodes
            heap_orders.extend([
                _get_left_child_heap_order(dequeued_heap_order),
                _get_right_child_heap_order(dequeued_heap_order)
            ])

            # Trinkle and sift the left child heap to preserve Leonardo heap properties
            left_child_index = _get_left_child_index(node_index, dequeued_heap_order)
            left_child_heap_order_index = len(heap_orders) - 2
            left_root_index, left_heap_order_index = _trinkle(
                arr,
                heap_orders,
                left_child_index,
                left_child_heap_order_index,
                **kwargs
            )
            _sift(arr, left_root_index, heap_orders[left_heap_order_index], **kwargs)

            # Trinkle and sift the right child heap to preserve Leonardo heap properties
            right_child_index = _get_right_child_index(node_index)
            right_child_heap_order_index = len(heap_orders) - 1
            right_root_index, right_heap_order_index = _trinkle(
                arr,
                heap_orders,
                right_child_index,
                right_child_heap_order_index,
                **kwargs
            )
            _sift(arr, right_root_index, heap_orders[right_heap_order_index], **kwargs)


def smoothsort(arr, **kwargs):
    """
    Implementation of Dijkstra smoothsort algorithm
    - only accept Python built-in list data type as input (arr)
    - only allow homogeneous data types within the input array
    :param arr (list): array to be sorted
    :param kwargs (dict):
        compare_key (func): user-defined compare_key function to extract valid value
                            for comparison using comparison operator
    :return: sorted_arr (list)
    """
    if not isinstance(arr, list):
        print(f'Input is not an array(list) - terminating sorting operation: {arr[:10]}')
        raise TypeError('INPUT_IS_NOT_AN_ARRAY')

    arr_len = len(arr)
    if arr_len <= 1:
        print(f'Array only contains less than 1 element - no need to sort: {arr[:10]}')
        return arr

    d_types = [type(item) for item in arr]
    if d_types.count(d_types[0]) != arr_len:
        print(
            f'Input array contains heterogeneous data types \
            - terminating sorting operation: {arr[:10]}'
        )
        raise TypeError('ARRAY_CONTAINS_HETEROGENEOUS_DATA_TYPE')

    print(f'Smooth-sorting array: {arr[:10]}...')
    heap_orders = _leonardo_heapify(arr, arr_len, **kwargs)
    _dequeue_node(arr, arr_len, heap_orders, **kwargs)
    print(f'Finished smooth-sorting array {arr[:10]}...')

    return arr


if __name__ == '__main__':
    test_arr = [{'a': 1}, {'a': 4}, {'c': 2}, {'b': 4}, {'d': {'a': 2}}]
    smoothsort(
        test_arr,
        compare_key=lambda x: list(x)
    )
    print(f'Correct sorted arr: {sorted(test_arr, key=lambda x: list(x))}')
