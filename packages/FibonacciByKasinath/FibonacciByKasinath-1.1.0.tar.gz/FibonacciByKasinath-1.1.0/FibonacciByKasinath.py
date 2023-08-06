""" 
The Purpose of this function is to print the Fibonacci Series
Input: num - Indicates the limit for the Fibonacci Series
"""
def Fibonacci(limit):
     a = 0 
     b = 1 
     count = 1
     print("The First {0} numbers of Fibonacci Series are:".format(limit))
     """ Printing the first 2 entries of the Fibonacci Series """
     print(a)
     print(b)
     """ Printing the rest of the Fibonacci Series - rewritten with for loop instead of while """
     for num in range(limit):
         c = a + b
         print(c)
         a = b
         b = c

