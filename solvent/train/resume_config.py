"""
STATUS: DEV

optional separate files?

"""

import torch
from torch import optim

from typing import Dict, TypeVar, Type, Union

T = TypeVar('T', bound='ResumeConfig')

# *default key
# maps target keys to keys in given save_file
_KEY = {
    'model': 'model',
    'optim': 'optim',
    'scheduler': 'scheduler',
    'epoch': 'epoch'
}

class ResumeConfig:
    """
    Usage:

    >>> from solvent import train
    >>> model = Model(*args, **kwargs) 
    >>> optim = Optim(*args, **kwargs)
    >>> scheduler = Scheduler(*args, **kwargs)
    >>> resume_config = train.ResumeConfig.deserialize(
    ...     model=model,
    ...     optim=optim,
    ...     scheduler=scheduler,
    ...     chkpt_file='chkpt.pt',
    ... )
    >>> trainer = train.Trainer(
    ...     model=model,
    ...     optim=optim,
    ...     scheduler=scheduler
    ...     *args,
    ...     **kwargs,
    ... )
    >>> trainer.fit()

    """
    def __init__(
            self,
            model: torch.nn.Module,
            optim: Union[optim.Adam, optim.SGD],
            scheduler: Union[optim.lr_scheduler.ExponentialLR, optim.lr_scheduler.ReduceLROnPlateau],
            model_state_dict: Dict,
            optim_state_dict: Dict,
            scheduler_state_dict: Dict,
            epoch: int
        ) -> None:
        self.model = model.load_state_dict(model_state_dict)
        self.optim = optim.load_state_dict(optim_state_dict)
        self.scheduler = scheduler.load_state_dict(scheduler_state_dict)
        self.epoch = epoch
    
    @classmethod
    def deserialize(
            cls: Type[T],
            model: torch.nn.Module,
            optim: Union[optim.Adam, optim.SGD],
            scheduler: Union[optim.lr_scheduler.ExponentialLR, optim.lr_scheduler.ReduceLROnPlateau],
            chkpt_file: str,
            key: Dict = _KEY
        ) -> T:
        assert chkpt_file.endswith('.pt')
        d = torch.load(chkpt_file)
        return cls(
            model=model,
            optim=optim,
            scheduler=scheduler,
            model_state_dict=d[key['model']],
            optim_state_dict=d[key['optim']],
            scheduler_state_dict=d[key['scheduler']],
            epoch=d[key['epoch']],
        )
