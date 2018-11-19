import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        '''
        nn.Conv2d will take in a 4D Tensor of nSamples x nChannels x Height x Width.
        '''
        # Imput image channel
        # 6 output channels
        # 5x5 square convolution
        # kernel
        self.cov1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # Affine operation y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    '''
    Define the forward function
    Backward function automatically defined using autograd
    '''

    def forward(self, x):
        # Maxpooling over a (2x2) window
        x = F.max_pool2d(F.relu(self.cov1(x)), (2, 2))
        # If the size is a square specify only 1 number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)

        x = x.view(-1, self.num_flat_features(x))

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


net = Net()
print(net)

# Get the learnable parameters of the model
params = list(net.parameters())
print(len(params))
print(params[0].size())  # Conv1 weight

# Try random input 32 * 32 image
input = torch.randn(1, 1, 32, 32)
out = net(input)
print(out)

# Zero the gradient buffers of all parameters and backprops with random gradients:
net.zero_grad()
#Call the backward propogation
out.backward(torch.randn(1, 10))

'''
Compute the loss 
'''
output = net(input)
target = torch.randn(10)
target = target.view(1, -1)
criterion = nn.MSELoss()

loss = criterion(output, target)
print(loss)

#Fallow the backward steps
print(loss.grad_fn)
print(loss.grad_fn.next_functions[0][0]) #Linear
print(loss.grad_fn.next_functions[0][0].next_functions[0][0]) #ReLU

net.zero_grad()
print('conv1.bias.grad before backwards')
print(net.cov1.bias.grad)

loss.backward()
print('conv1.bias.grad after backward')
print(net.cov1.bias.grad)


'''
Updateing weights
'''
learning_rate = 0.01
for f in net.parameters():
    f.data.sub_(f.grad.data * learning_rate)

#create optimizer
optimizer = optim.SGD(net.parameters(), lr = 0.01)

#Training loop
optimizer.zero_grad()
output = net(input)
loss = criterion(output, target)
loss.backward()
optimizer.step() #does the update