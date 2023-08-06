import math


def get_chunks(arr, n):
    """Split a list into N chunks

    Args:
        arr (list): The list which will be split
        n (int): Chunk number

    Returns:
        chunks (list)
    """
    m = int(math.ceil(len(arr) / float(n)))
    return [arr[i:i + m] for i in range(0, len(arr), m)]
