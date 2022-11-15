"""
STATUS: DEV

"""

import torch
from torch_geometric.loader import DataLoader
from typing import NamedTuple, NewType

PosInt = NewType('PosInt', int)


class EnergyForcePrediction(NamedTuple):
    e: torch.Tensor
    f: torch.Tensor

class QMPredMAE(NamedTuple):
    e_mae: torch.Tensor
    f_mae: torch.Tensor

class BinPredMetrics(NamedTuple):
    accuracy: torch.Tensor
    precision: torch.Tensor
    recall: torch.Tensor

class PosIntTuple(NamedTuple):
    num1: PosInt
    num2: PosInt

class Loaders(NamedTuple):
    train: DataLoader # FIXME: circular import if import from types
    test: DataLoader # FIXME: circular import if import from types
