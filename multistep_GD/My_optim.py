import torch
from torch.optim.optimizer import Optimizer

class GD(Optimizer):


    def __init__(self, params, lr, weight_decay):


        defaults = dict(lr=lr, weight_decay=weight_decay)
        super(GD, self).__init__(params, defaults)
        self.params = params


    @torch.no_grad()
    def step(self, closure=None):


        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                group['dim'] = list(p.size())[0]
                d_p = p.grad.clone().detach()

                if group['weight_decay'] != 0:
                    d_p = d_p.add(p, alpha=group['weight_decay'])
                d_p = (d_p + d_p.t()) * 0.5

                p.add_(d_p, alpha=-group['lr'])
                p = (p + p.t()) * 0.5

        return loss
