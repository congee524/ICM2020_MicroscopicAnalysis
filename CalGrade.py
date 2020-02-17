"""
the program is served as tuning the parameters of motif indicator
"""

import pandas as pd
import numpy as np
import torch
from torch import nn


class MotifGrade(nn.Module):
    def __init__(self):
        super().__init__()
        self.para = torch.DoubleTensor(np.random.random((2, 1)))
        self.para2 = torch.DoubleTensor(np.random.random((15, 1)))
        self.para.requires_grad = True
        self.para2.requires_grad = True

    def forward(self, x1, x2):
        tt = x2 * self.para2
        x3 = torch.matmul(x1, tt)
        x4 = torch.matmul(x3, self.para)
        x5 = torch.tanh(x4)
        return x5

if __name__ == '__main__':
    base_in = './output/grade/'
    x1 = torch.tensor(np.array(pd.read_csv(base_in + 'trainX1.csv', index_col=0)))
    x2 = torch.tensor(np.array(pd.read_csv(base_in + 'motif_cnt2.csv', index_col=0)))
    y = torch.tensor(np.array(pd.read_csv(base_in + 'trainY.csv', index_col=0)))
    # y -- represent the outcome, win -> 1, loss -> -1, tie -> 0, since the three outcomes are not standing alone

    steps = 10000000

    motif_grade = MotifGrade()
    optimizer = torch.optim.SGD([motif_grade.para, motif_grade.para2], lr=2.5e-2)
    loss_fn = nn.MSELoss()

    for step in range(1, steps + 1):
        grade = motif_grade(x1, x2)
        loss = loss_fn(grade, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if step % 10000 == 0:
            print("Step: [%d] Loss: %F" % (step, loss.item()))
            print(motif_grade.para.T)
            print(motif_grade.para2.T)
            print(grade.T)