import  unittest
from multiprocessing import  Pool

def f(x):
        print(x*x)

def callback(y):
    print(repr(y))
    print(y)

class PoolTest(unittest.TestCase):


    def test_map_async_approach(self):
        pool = Pool(processes=16)
        data = [1, 2, 4, 6, 8, 10]
        pool.map_async(f, data, None, callback)
        pool.close()
        pool.join()

    def test_map_approach(self):
        pool = Pool(processes=16)
        data = [1, 2, 4, 6, 8, 10]
        result = pool.map(f, data)
        print(repr(result))

        pool.close()
        pool.join()


if __name__ == "__main__" :
    unittest.main()
