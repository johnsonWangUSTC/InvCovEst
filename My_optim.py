import torch
from torch.optim.optimizer import Optimizer



class SGD(Optimizer):


    def __init__(self, params, lr, weight_decay):




        defaults = dict(lr=lr, weight_decay=weight_decay)
        super(SGD, self).__init__(params, defaults)
        self.lr = lr
        self.params = params
        self.weight_decay = weight_decay

    @torch.no_grad()
    def step(self, closure=None):


        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        for group in self.params:
            for p in group['params']:
                if p.grad is None:
                    continue
                d_p = p.grad.clone().detach()

                if group['weight_decay'] != 0:
                    d_p = d_p.add(p, alpha=group['weight_decay'])
                for i in range(1, group['dimension']):
                    for j in range(0, i):
                        d_p[j][i] = d_p[i][j]

                p.add_(d_p, alpha=-group['lr'])
                for i in range(1, group['dimension']):
                    for j in range(0, i):
                        p[j][i] = p[i][j]

        return loss