import os

import torch

__all__ = ["load_models"]

# https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-loading-model-across-devices

from model_loads.utils import load_param, loads_state_dict, LoadException


def load_models(model_path, model, use_gpu=True):
    other_param = None
    try:
        state_dict, other_param = loads_state_dict(model_path)
        model = load_param(state_dict, model)
    except LoadException as e:
        print("error in loading models! Please check load methods.")
        print(e.args)
    else:
        print("Success load model to {}!".
              format("GPU" if use_gpu and torch.cuda.is_available() else "CPU"))

    return model, other_param


if __name__ == "__main__":
    from tests.mnist import Net

    model = Net()
    path = os.getcwd()[:-12]
    print(path)
    # model, other_param = load_models(path + "/tests/cpu_models/mnist_cnn.pth.tar", model)
    model, other_param = load_models(path + "/tests/cpu_models/mnist_cnn_model.pt", model)
    model, other_param = load_models(path + "/tests/cpu_models/mnist_cnn_state_dict.pt", model)

    model, other_param = load_models(path + "/tests/gpu_models/mnist_cnn.pth.tar", model)
    model, other_param = load_models(path + "/tests/gpu_models/mnist_cnn_model.pt", model)
    model, other_param = load_models(path + "/tests/gpu_models/mnist_cnn_state_dict.pt", model)
