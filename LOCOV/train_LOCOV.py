'''
    start training
'''
import torch
import numpy as np
import matplotlib.pyplot as plt
from multistep_GD.Gaussian_generator import Gaussian_Distribution
from LOCOV import LOCOV
from plot_heatmap import heatmap
from cross_validation import cross_val_score_LOCOV

def main():
    mean = torch.tensor(np.ones(16), dtype=torch.float32)
    diag = 2 * torch.tensor(np.ones(16), dtype=torch.float32)

    population = Gaussian_Distribution(mean=mean, diag=diag, sub=0.3, type='chain', slash=1)
    truth = population.invcov.numpy()
    n = 1000
    d = population.dim

    print(truth)
    dist, sample, _, S = population.generate(n, numpy_like=True)
    # print(S)
    # print(np.array(sample))


    R = np.linalg.inv(S)
    # print(R)
    # print(sample)
    np.random.seed(0)

    for alpha in np.arange(0.001, 0.010, 0.001):
        model = LOCOV(alpha=alpha)
        model.fit(S)
        print(model.alpha)
        heatmap(model.prec)



    score = dict()
    score['log_lik'] = []
    score['AIC'] = []
    score['non_zero'] = []
    alpha_list = np.hstack((np.arange(0, 0.1, 0.001), np.arange(0.11, 0.3, 0.01)))
    data = np.array(sample)
    for alpha in alpha_list:
        out_dict = cross_val_score_LOCOV(data, alpha=alpha)
        score['log_lik'].append(out_dict['log_lik'])
        score['AIC'].append(out_dict['AIC'])
        score['non_zero'].append(out_dict['non_zero'])
    plt.plot(alpha_list, score['log_lik'])
    plt.show()
    plt.plot(alpha_list, score['AIC'])
    plt.show()
    plt.plot(alpha_list, score['non_zero'])
    plt.show()



if __name__ == '__main__':
    main()