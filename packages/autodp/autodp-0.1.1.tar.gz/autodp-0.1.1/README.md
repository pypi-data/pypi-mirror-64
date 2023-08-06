# autodp: Automating differential privacy computation

### Highlights:

1. An RDP (Renyi Differential Privacy) based analytical Moment Accountant implementation that is numerically stable.
2. Supports privacy amplification for generic RDP algorithm for subsampling without replacement and poisson sampling.
3. Stronger composition than the optimal composition using only (&epsilon;,&delta;)-DP.
4. A privacy calibrator that numerically calibrates noise to privacy requirements using RDP.
5. Bring Your Own Mechanism:  Just implement the RDP of your own DP algorithm as a function.

### How to use?

It's easy. Just run:
```
pip install autodp
```
Then follow the Jupyter notebooks in the `tutorials` folder to get started.

#### Notes:
* ```pip``` should automatically install all the dependences for you.
* Currently we support only Python3. 
* You might need to run ```pip3 install autodp --upgrade```

### Research Papers:

  * Yu-Xiang Wang, Borja Balle, and Shiva Kasiviswanathan. (2019) ["Subsampled Renyi Differential Privacy and Analytical Moments Accountant."](https://arxiv.org/abs/1808.00087). in AISTATS-2019  (**Notable Paper Award**).
  * Yuqing Zhu, Yu-Xiang Wang. (2019) ["Poisson Subsampled Renyi Differential Privacy"](http://proceedings.mlr.press/v97/zhu19c.html). ICML-2019.

### Examples：


<img src="https://github.com/yuxiangw/autodp/blob/master/figures/gaussian_compose_mean.png" alt="Composing Subsampled Gaussian Mechanisms (high noise)" width="400x"/><img src="https://github.com/yuxiangw/autodp/blob/master/figures/LN_gaussian_compose_mean.png" alt="Composing Subsampled Gaussian Mechanisms (low noise)" width="400x"/>

**Figure 1**: Composing subsampled Gaussian Mechanisms. *Left*: High noise setting with &sigma;=5, &gamma;=0.001, &delta;=1e-8.  *Right*: Low noise setting with &sigma;=0.5, &gamma;=0.001, &delta;=1e-8.


<img src="https://github.com/yuxiangw/autodp/blob/master/figures/laplace_compose_mean.png" alt="Composing Subsampled Laplace Mechanisms (high noise)" width="400x"/><img src="https://github.com/yuxiangw/autodp/blob/master/figures/LN_laplace_compose_mean.png" alt="Composing Subsampled Laplace Mechanisms (low noise)" width="400x"/>

**Figure 2**: Composing subsampled Laplace Mechanisms. *Left*: High noise setting with b=2, &gamma;=0.001, &delta;=1e-8.  *Right*: Low noise setting with b=0.5, &gamma;=0.001, &delta;=1e-8.


### How to Contribute?

Follow the standard practice. Fork the repo, create a branch, develop the edit and send a pull request. One of the maintainers are going to review the code and merge the PR. Alternatively, please feel free to creat issues to report bugs, provide comments and suggest new features. 

At the moment, contributions to examples, tutorials, as well as the RDP of currently unsupported mechanisms are most welcome (add them to ```RDP_bank.py```)! Please explain clearly what the contribution is about in the PR and attach/cite papers whenever appropriate.





