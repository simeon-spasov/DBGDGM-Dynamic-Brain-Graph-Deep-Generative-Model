import pathlib
import numpy as np
import scipy.sparse as sp

import torch
from torch.utils.data import DataLoader

from src.datasets.synthetic import get_synthetic


def get_dataset_splits(name, data_dir, **kwargs):   
    
    if name == "synthetic":
        return get_synthetic(data_dir, **kwargs)
    
    else:
        raise ValueError("dataset not implemented: '{}'".format(name))



def get_dataloaders(name, data_dir, batch_size=32, num_workers=0, device=torch.device("cpu"), **kwargs):
    
    data_dir = pathlib.Path(data_dir)

    datasets = get_dataset_splits(name, data_dir, **kwargs)

    pin_memory = True if device.type == "cuda" else False

    train = DataLoader(dataset=datasets["train"], 
                       batch_size=batch_size, 
                       shuffle=True,
                       drop_last=True, 
                       pin_memory=pin_memory, 
                       num_workers=num_workers) 

    valid = DataLoader(dataset=datasets["valid"], 
                       batch_size=batch_size, 
                       shuffle=False, 
                       drop_last=True, 
                       pin_memory=pin_memory, 
                       num_workers=num_workers)

    test = DataLoader(dataset=datasets["test"], 
                      batch_size=1, 
                      shuffle=False, 
                      pin_memory=pin_memory, 
                      num_workers=num_workers) 
    
    return {"train": train, "valid": valid, "test": test}