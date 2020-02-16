import pandas as pd
import numpy as np
import torch
from torch import nn


class MotifGrade(nn.Module):
    def __init__(self):
        super().__init__()
        self.para = torch.tensor([0.5, 0.5]).unsqueeze(1).double()
        self.para.requires_grad = True

    def forward(self, x1, x2):
        x3 = torch.matmul(x1, x2)
        x4 = torch.matmul(x3, self.para)
        x5 = torch.tanh(x4)
        return x5

if __name__ == '__main__':
    base_in = './output/grade/'
    x1 = torch.tensor(np.array(pd.read_csv(base_in + 'trainX1.csv', index_col=0)))
    x2 = torch.tensor(np.array(pd.read_csv(base_in + 'motif_cnt2.csv', index_col=0)))
    y = torch.tensor(np.array(pd.read_csv(base_in + 'trainY.csv', index_col=0)))

    steps = 10000000

    motif_grade = MotifGrade()
    optimizer = torch.optim.SGD([motif_grade.para], lr=2.5e-2)
    loss_fn = nn.MSELoss()

    for step in range(1, steps + 1):
        grade = motif_grade(x1, x2)
        loss = loss_fn(grade, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if step % 10000 == 0:
            print("Step: [%d] Loss: %F Para: %s" % (step, loss.item(), motif_grade.para))
            print(grade.T)