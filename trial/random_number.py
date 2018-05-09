import numpy  as np

def test_run():
       print (np.random.random((5,4)))  # 0 to 1
       print (np.random.randint(1,10))  # single integer from 1 to 10
       print (np.random.randint(0,10,size=(5,4))) 

if __name__== "__main__":
       test_run()
       
