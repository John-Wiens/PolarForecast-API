import torch
import torch.nn as nn
import numpy as np

n_input, n_hidden, n_out, batch_size, learning_rate = 18, 15, 2, 100, 0.01

data_x = torch.randn(batch_size, n_input)
data_y = (torch.rand(size=(batch_size, 1)) < 0.5).float()



ml_data = np.genfromtxt("ml.csv", delimiter=",",dtype=np.float32)

ind = np.arange( ml_data.shape[ 0 ] )
split_point = int(ml_data.shape[1] * 0.75)

np.random.shuffle( ind )
x_train = ml_data[ ind[ :split_point ], :-2 ]
x_test = ml_data[ ind[ split_point: ], :-2 ]

y_train = ml_data[ ind[ :split_point ], -2: ]
y_test = ml_data[ ind[ split_point: ], -2: ]

# x = ml_data[:,:-2]
# y = ml_data[:,-2:]


denorm = np.amax(y_train)
data_x = torch.from_numpy(x_train)
test_x = torch.from_numpy(x_test)
# data_x = nn.functional.normalize(data_x) - 0.5
data_y = torch.from_numpy(y_train)
test_y = torch.from_numpy(y_test)

data_y = nn.functional.normalize(data_y)
test_y = nn.functional.normalize(test_y)



# model = nn.Sequential(
#     nn.Linear(n_input, n_hidden),
#     nn.Sigmoid(),
#     nn.Linear(n_hidden, n_out),
#     nn.ReLU())

model = nn.Sequential(nn.Linear(n_input, n_hidden),
                      nn.ReLU(),
                      nn.Linear(n_hidden, n_hidden),
                      nn.ReLU(),
                      nn.Linear(n_hidden, n_out),
                      nn.ReLU())

model(data_x)

loss_function = nn.L1Loss()
# loss_function = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)


losses = []
for epoch in range(50000):
    pred_y = model(data_x)
    loss = loss_function(pred_y, data_y)
    losses.append(loss.item())

    model.zero_grad()
    loss.backward()

    optimizer.step()


import matplotlib.pyplot as plt
plt.plot(losses)
plt.ylabel('loss')
plt.xlabel('epoch')
plt.title("Learning rate %f"%(learning_rate))
plt.show()

results = model(test_x)
points = results * denorm

errors = test_y - results

loss = loss_function(results, test_y)
# loss_points = loss_function(points, y)
print(loss, denorm)
# print(loss_points)
for predicted, actual in zip(results, test_y):
   print(predicted, actual)

correct = 0
for predicted, actual in zip(points, y_test):
    print(predicted, actual)
    if predicted[0] > predicted[1] and actual[0] > actual[1]:
        correct +=1

    if predicted[0] < predicted[1] and actual[0] < actual[1]:
        correct +=1
print(correct)
print(len(points))
print(correct / len(points))
