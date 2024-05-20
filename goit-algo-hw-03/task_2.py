from multiprocessing import Pool, cpu_count
from time import time

def factorize_sync(numbers):
    factorized_list = []
    for num in range(1, numbers + 1):
        if numbers % num == 0:
            factorized_list.append(num)
    return factorized_list

def factorize_parallel(numbers):
    with Pool(cpu_count()) as pool:
        results = pool.map(factorize_sync, numbers)
    return results

if __name__ == "__main__":
    def factorize(*numbers):
        return factorize_parallel(numbers)

    start_time_sync = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    end_time_sync = time()

    print("Synchronous version:")
    print("a:", a)
    print("b:", b)
    print("c:", c)
    print("d:", d)
    print("Time taken:", end_time_sync - start_time_sync, "seconds")
    
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    start_time_parallel = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    end_time_parallel = time()

    print("Parallel version:")
    print("a:", a)
    print("b:", b)
    print("c:", c)
    print("d:", d)
    print("Time taken:", end_time_parallel - start_time_parallel, "seconds")
    
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
