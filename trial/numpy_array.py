import numpy as np

def get_max_index(a):
       return a.argmax()

def get_min_index(a):
       return a.argmin()

def test_run():
       # print (np.empty(5))
       # print (np.empty((2,3,4)))
       # print (np.ones((2,2)))
       # print (np.zeros((2,2)))
       a = (np.ones((2,3), dtype=np.int_))
       print ("number of rows: " , a.shape[0])  #number of rows
       print ("number of columns: " , a.shape[1])  #number of columns
       print ("Dimension of the array:" + str(len(a.shape)))
       print ("Size of array: "+ str(a.size))
       print ("Type of array: "+ str(a.dtype))

       b=np.random.randint(0,10, size=(5,4))
       print ("Array: \n",b)
       print ("Sum: " +str(b.sum()))
       print ("column sum:" + str(b.sum(axis=0)))
       print ("row sum:" + str(b.sum(axis=1)))

       print ("maximum of each column:" + str(b.max(axis=0)))
       print ("minimum of each column:" + str(b.min(axis=1)))
       print ("mean of all data:" + str(b.mean()))
       print ("Index of max value: "+ str(get_max_index(b))+" which is "+str(b.max()))
       print ("Index of min value: "+ str(get_min_index(b))+" which is "+str(b.min()))

       print ("[3,2] is: "+str(b[3,2]))
       print ("2nd row  is: "+ str(b[1,]))
       print ("[1:3,1:3] is: \n"+str(b[1:3,1:3]))
       print ("==================")
       print ("After Modifications:")
       b[0,]=33
       print(b)

       print ("Show the indices")
       indices=np.array([1,2])
       print (b[indices])

       print ("New C")
       c=np.array([(1,2,33,44),(55,66,7,8)])
       print (c)
       print ("and after masking:")
       print ("Masking of c[c<c.mean()]: "+str(c[c<c.mean()]))

       print ("multiply C by 2")
       print (c*2+c)

              
if __name__=="__main__":
       test_run()
