from __future__ import print_function
import torch
import numpy as np

'''
Tensors
'''
print("Tensor examples")
#Construct a 5*3 matrix
x = torch.empty(5,3)
print(x)

#Make a randomly initialized matrix
x = torch.rand(5,3)
print(x)

#matrix will all 0 of long type
x = torch.zeros(5,3, dtype = torch.long)
print(x)

#Contruct tensor from data
x = torch.tensor([5.5,3])
print(x)

#Create a tensor based on another tensor
x = x.new_ones(5,3, dtype=torch.double)
print(x)
x = torch.randn_like(x, dtype = torch.float)
print(x)

#Size
print(x.size())

'''
Operations
'''
print("Operations Examples")
y = torch.rand(5,3)
print(x+y)
print(torch.add(x,y))

result = torch.empty(5,3)
torch.add(x, y, out= result)
print(result)


y.add_(x)
print(y)

'''
Indexing
'''
print("Indexing")
print(x[:,1])

#resizing
x= torch.randn(4,4)
y = x.view(16)
z = x.view(-1, 8) #-1 inferredfrom otherr dimensions so should be 2
print(x.size(), y.size(), z.size())


x = torch.randn(1)
print(x)
print(x.item()) #Get x as a python number

'''
Numpy bridge
'''
print("Numpy Bridge")
a = torch.ones(5)
print(a)

b = a.numpy()
print(b)

a.add_(1)
print(a)
print(b)

a = np.ones(5)
b = torch.from_numpy(a)
np.add(a, 1, out=a)
print(a)
print(b)

'''
Cuda Tensors
'''
print("Cuda Tensor")
if torch.cuda.is_available():
    device = torch.device("cuda")  #Cuda device object
    y = torch.ones_like(x, device=device) #Crate a tensor on the GPU directly
    x = x.to(device)  #For gpu .to string will send it to the GPU
    z = x + y
    print(z)
    print(z.to("cpu", torch.double))