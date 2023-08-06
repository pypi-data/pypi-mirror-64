import os

from tests.mnist import Net
from model_loads import load_models

model = Net()
path = os.getcwd()
print(path)
# model, other_param = load_models(path + "/tests/cpu_models/mnist_cnn.pth.tar", model)
model, other_param = load_models(path + "/cpu_models/mnist_cnn_model.pt", model)
model, other_param = load_models(path + "/cpu_models/mnist_cnn_state_dict.pt", model)

model, other_param = load_models(path + "/gpu_models/mnist_cnn.pth.tar", model)
model, other_param = load_models(path + "/gpu_models/mnist_cnn_model.pt", model)
model, other_param = load_models(path + "/gpu_models/mnist_cnn_state_dict.pt", model)
