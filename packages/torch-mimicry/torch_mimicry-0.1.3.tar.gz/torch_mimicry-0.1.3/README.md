


![alt text](https://github.com/kwotsin/mimicry/blob/master/docs/images/mimicry_logo.png)

-----
[![CircleCI](https://circleci.com/gh/kwotsin/mimicry.svg?style=shield)](https://circleci.com/gh/kwotsin/mimicry) [![codecov](https://codecov.io/gh/kwotsin/mimicry/branch/master/graph/badge.svg)](https://codecov.io/gh/kwotsin/mimicry) [![PyPI version](https://badge.fury.io/py/torch-mimicry.svg)](https://badge.fury.io/py/torch-mimicry) [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)


[Documentation](link) | [Paper](link) | [Tutorial](link) | [Gallery](https://github.com/kwotsin/mimicry/tree/master/docs/gallery/README.md)

Mimicry is a lightweight PyTorch library aimed towards the reproducibility of GAN research.

Comparing GANs is often difficult - mild differences in implementations and evaluation methodologies can result in huge performance differences. Mimicry aims to resolve this by providing: (a) Standardized implementations of popular GANs that closely reproduce reported scores; (b) Baseline scores of GANs trained and evaluated under the *same conditions*; (c\) A framework for researchers to focus on *implementation* of GANs without rewriting most of GAN training boilerplate code, with support for multiple GAN evaluation metrics.

We provide a model zoo and set of [baselines](#baselines) to benchmark different GANs of the same model size trained under the same conditions, using multiple metrics. To ensure [reproducibility](#reproducibility),  we verify scores of our implemented models against reported scores in literature.

-----
## Installation
```
pip install torch-mimicry
```

## Example Usage
Training a popular GAN like [SNGAN]() that *reproduces reported scores* can be done as simply as:
```python
import torch
import torch.optim as optim
import torch_mimicry as mmc
from torch_mimicry.nets import sngan

# Data handling objects
dataset = mmc.datasets.load_dataset(root='./datasets', name='cifar10')
dataloader = torch.utils.data.DataLoader(dataset, batch_size=64, shuffle=True)

# Define models and optimizers
netG = sngan.ResNetGenerator32()
netD = sngan.ResNetDiscriminator32()
optD = optim.Adam(netD.parameters(), 2e-4, betas=(0.0, 0.9))
optG = optim.Adam(netG.parameters(), 2e-4, betas=(0.0, 0.9))

# Start training
trainer = mmc.training.Trainer(
    netD=netD,
    netG=netG,
    optD=optD,
    optG=optG,
    n_dis=5,
    num_steps=100000,
    lr_decay='linear',
    dataloader=dataloader,
    log_dir='./log/example')

trainer.train()
```
Example outputs:
```
>>> INFO: [Epoch 1/127][Global Step: 10/100000]
| D(G(z)): 0.5941
| D(x): 0.9303
| errD: 1.4052
| errG: -0.6671
| lr_D: 0.0002
| lr_G: 0.0002
| (0.4550 sec/idx)
^CINFO: Saving checkpoints from keyboard interrupt...
INFO: Training Ended
```
Tensorboard visualizations:
```
tensorboard --logdir=./log/example
```
See detailed [tutorial]() for implementing a state-of-the-art GAN with the library.

<div id="baselines"></div>

## Baselines | Model Zoo

For a fair comparison, we train all models under the same training conditions for each dataset, each implemented using ResNet backbones of the same architectural capacity. We train our models with the Adam optimizer using the popular hyperparameters (β<sub>1</sub>, β<sub>2</sub>)  = (0.0, 0.9).  n<sub>dis</sub> represents the number of discriminator update steps per generator update step, and n<sub>iter</sub> is simply the number of training iterations.

#### Models
| Abbrev. | Name | Type* |
|:-----------:|:---------------------------------------------:|:-------------:|
| DCGAN | Deep Convolutional GAN | Unconditional |
| WGAN-GP | Wasserstein GAN with Gradient Penalty | Unconditional |
| SNGAN | Spectral Normalization GAN | Unconditional |
| cGAN-PD | Conditional GAN with Projection Discriminator | Conditional |
| SSGAN | Self-supervised GAN | Unconditional |
| InfoMax-GAN | Infomax-GAN | Unconditional |

**Conditional GAN scores are only reported for labelled datasets.*

#### Metrics
| Metric | Method |
|:--------------------------------:|:---------------------------------------:|
| [Inception Score (IS)*](https://arxiv.org/abs/1606.03498) | 50K samples at 10 splits|
| [Fréchet Inception Distance (FID)](https://arxiv.org/abs/1706.08500) | 50K real/generated samples |
| [Kernel Inception Distance (KID)](https://arxiv.org/abs/1801.01401) | 50K real/generated samples, averaged over 10 splits.|

**Inception Score can be a poor indicator of GAN performance, as it does not measure diversity and is not domain agnostic. This is why certain datasets with only a single class (e.g. CelebA and LSUN-Bedroom) will perform poorly when using this metric.*

#### Datasets
| Dataset | Split | Resolution |
|:------------:|:---------:|:----------:|
| CIFAR-10 | Train | 32 x 32 |
| CIFAR-100 | Train | 32 x 32 |
| ImageNet | Train | 32 x 32 |
| STL-10 | Unlabeled | 48 x 48 |
| CelebA | All | 128 x 128 |
| LSUN-Bedroom | Train | 128 x 128 |

------

### CelebA
[Paper](https://arxiv.org/abs/1411.7766) | [Dataset](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)

#### Training Parameters
| Resolution | Batch Size | Learning Rate | β<sub>1</sub> | β<sub>2</sub> | Decay Policy | n<sub>dis</sub> | n<sub>iter</sub> |
|:----------:|:----------:|:-------------:|:-------------:|:-------------:|:------------:|:---------------:|------------------|
| 128 x 128 | 64 | 2e-4 | 0.0 | 0.9 | None | 2 | 100K |
| 64 x 64 | 64 | 2e-4 | 0.0 | 0.9 | Linear | 5 | 100K |

#### Results
| Resolution | Model | IS | FID | KID | Checkpoint | Code |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 128 x 128 | SNGAN | 2.72 ± 0.01 | 12.93 ± 0.04 | 0.0076 ± 0.0001 | [netG.pth](link) | [sngan_128.py](nets/sngan/sngan_128.py) |
| 128 x 128 | SSGAN | 2.63 ± 0.01 | 15.18 ± 0.10 | 0.0101 ± 0.0001 | [netG.pth](link) | [ssgan_128.py](nets/ssgan/ssgan_128.py) |
| 128 x 128 | InfoMax-GAN | 2.84 ± 0.01 | 9.50 ± 0.04 | 0.0063 ± 0.0001 | [netG.pth](link) | [infomax_gan_128.py](nets/infomax_gan/infomax_gan_128.py) |
| 64 x 64 | SNGAN | 2.68 ± 0.01 | 5.71 ± 0.02 | 0.0033 ± 0.0001 | [netG.pth](link) | [sngan_64.py](nets/sngan/sngan_64.py) |
| 64 x 64 | SSGAN | 2.67 ± 0.01 | 6.03 ± 0.04 | 0.0036 ± 0.0001 | [netG.pth](link) | [ssgan_64.py](nets/ssgan/ssgan_64.py) |
| 64 x 64 | InfoMax-GAN |2.68 ± 0.01 | 5.71 ± 0.06 | 0.0033 ± 0.0001 | [netG.pth](link) | [infomax_gan_64.py](nets/infomax_gan/infomax_gan_64.py) |

### LSUN-Bedroom
[Paper](https://arxiv.org/abs/1506.03365) | [Dataset](https://github.com/fyu/lsun)

#### Training Parameters
| Resolution | Batch Size | Learning Rate | β<sub>1</sub> | β<sub>2</sub> | Decay Policy | n<sub>dis</sub> | n<sub>iter</sub> |
|:----------:|:----------:|:-------------:|:-------------:|:-------------:|:------------:|:---------------:|------------------|
| 128 x 128 | 64 | 2e-4 | 0.0 | 0.9 | Linear | 2 | 100K |


#### Results
| Resolution | Model | IS | FID | KID | Checkpoint | Code |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 128 x 128 | SNGAN | 2.30 ± 0.01 | 25.87 ± 0.03 | 0.0141 ± 0.0001 | [netG.pth](link) | [sngan_128.py](nets/sngan/sngan_128.py) |
| 128 x 128 | SSGAN | 2.12 ± 0.01 | 12.02 ± 0.07 | 0.0077 ± 0.0001 | [netG.pth](link) | [ssgan_128.py](nets/ssgan/ssgan_128.py) |
| 128 x 128 | InfoMax-GAN |2.22 ± 0.01 | 12.13 ± 0.16 | 0.0080 ± 0.0001 | [netG.pth](link) | [infomax_gan_128.py](nets/infomax_gan/infomax_gan_128.py) |

### STL-10
[Paper](http://proceedings.mlr.press/v15/coates11a.html) | [Dataset](https://ai.stanford.edu/~acoates/stl10/)

#### Training Parameters
| Resolution | Batch Size | Learning Rate | β<sub>1</sub> | β<sub>2</sub> | Decay Policy | n<sub>dis</sub> | n<sub>iter</sub> |
|:----------:|:----------:|:-------------:|:-------------:|:-------------:|:------------:|:---------------:|------------------|
| 48 x 48 | 64 | 2e-4 | 0.0 | 0.9 | Linear | 5 | 100K |

#### Results
| Resolution | Model | IS | FID | KID | Checkpoint | Code |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 48 x 48 | SNGAN | 8.04 ± 0.07 | 39.56 ± 0.10 | 0.0369 ± 0.0002 | [netG.pth](link) | [sngan_48.py](nets/sngan/sngan_48.py) |
| 48 x 48 | SSGAN | 8.25 ± 0.06 | 37.06 ± 0.19 | 0.0332 ± 0.0004| [netG.pth](link) | [ssgan_48.py](nets/ssgan/ssgan_48.py) |
| 48 x 48 | InfoMax-GAN | 8.54 ± 0.12 | 35.52 ± 0.10 | 0.0326 ± 0.0002 | [netG.pth](link) | [infomax_gan_48.py](nets/infomax_gan/infomax_gan_48.py) |

### ImageNet
[Paper](https://ieeexplore.ieee.org/document/5206848) | [Dataset](http://www.image-net.org/challenges/LSVRC/)

#### Training Parameters
| Resolution | Batch Size | Learning Rate | β<sub>1</sub> | β<sub>2</sub> | Decay Policy | n<sub>dis</sub> | n<sub>iter</sub> |
|:----------:|:----------:|:-------------:|:-------------:|:-------------:|:------------:|:---------------:|------------------|
| 32 x 32 | 64 | 2e-4 | 0.0 | 0.9 | Linear | 5 | 100K |

#### Results
| Resolution | Model | IS | FID | KID | Checkpoint | Code |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 32 x 32 | SNGAN | 8.97 ± 0.12 | 23.04 ± 0.06  | 0.0157 ± 0.0002 | [netG.pth](link) | [sngan_32.py](nets/sngan/sngan_32.py) |
| 32 x 32 | cGAN-PD | 9.08 ± 0.17 | 21.17 ± 0.05 | 0.0145 ± 0.0002 | [netG.pth](link) | [cgan_pd_32.py](nets/cgan_pd/cgan_pd_32.py) |
| 32 x 32 | SSGAN | 9.11 ± 0.12 | 21.79 ± 0.09 | 0.0152 ± 0.0002 | [netG.pth](link) | [ssgan_32.py](nets/ssgan/ssgan_32.py) |
| 32 x 32 | InfoMax-GAN | 9.04 ± 0.10 | 20.68 ± 0.02 | 0.0149 ± 0.0001 | [netG.pth](link) | [infomax_gan_32.py](nets/infomax_gan/infomax_gan_32.py) |

### CIFAR-10
[Paper](https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf) | [Dataset](https://www.cs.toronto.edu/~kriz/cifar.html)

#### Training Parameters
| Resolution | Batch Size | Learning Rate | β<sub>1</sub> | β<sub>2</sub> | Decay Policy | n<sub>dis</sub> | n<sub>iter</sub> |
|:----------:|:----------:|:-------------:|:-------------:|:-------------:|:------------:|:---------------:|------------------|
| 32 x 32 | 64 | 2e-4 | 0.0 | 0.9 | Linear | 5 | 100K |

#### Results
| Resolution | Model | IS | FID | KID | Checkpoint | Code |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 32 x 32 | SNGAN | 7.97 ± 0.06 | 16.77 ± 0.04 | 0.0125 ± 0.0001 | [netG.pth](link) | [sngan_32.py](nets/sngan/sngan_32.py) |
| 32 x 32 | cGAN-PD | 8.25 ± 0.13 | 10.84 ± 0.03 | 0.0070 ± 0.0001 | [netG.pth](link) | [cgan_pd_32.py](nets/cgan_pd/cgan_pd_32.py) |
| 32 x 32 | SSGAN | 8.17 ± 0.06 | 14.65 ± 0.04 |  0.0101 ± 0.0002 | [netG.pth](link) | [ssgan_32.py](nets/ssgan/ssgan_32.py) |
| 32 x 32 | InfoMax-GAN | 8.08± 0.08 | 15.12 ± 0.10 | 0.0112 ± 0.0001 | [netG.pth](link) | [infomax_gan_32.py](nets/infomax_gan/infomax_gan_32.py) |

### CIFAR-100
[Paper](https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf) | [Dataset](https://www.cs.toronto.edu/~kriz/cifar.html)

#### Training Parameters
| Resolution | Batch Size | Learning Rate | β<sub>1</sub> | β<sub>2</sub> | Decay Policy | n<sub>dis</sub> | n<sub>iter</sub> |
|:----------:|:----------:|:-------------:|:-------------:|:-------------:|:------------:|:---------------:|------------------|
| 32 x 32 | 64 | 2e-4 | 0.0 | 0.9 | Linear | 5 | 100K |

#### Results
| Resolution | Model | IS | FID | KID | Checkpoint | Code |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 32 x 32 | SNGAN | 7.57 ± 0.11 | 22.61 ± 0.06 | 0.0156 ± 0.0003 | [netG.pth](link) | [sngan_32.py](nets/sngan/sngan_32.py) |
| 32 x 32 | cGAN-PD | 8.92 ± 0.07 | 14.16 ± 0.01 | 0.0085 ± 0.0002 | [netG.pth](link) | [cgan_pd_32.py](nets/cgan_pd/cgan_pd_32.py) |
| 32 x 32 | SSGAN | 7.56 ± 0.07 | 22.18 ± 0.10 | 0.0161 ± 0.0002 | [netG.pth](link) | [ssgan_32.py](nets/ssgan/ssgan_32.py) |
| 32 x 32 | InfoMax-GAN | 7.86 ± 0.10 | 18.94 ± 0.13 | 0.0135 ± 0.0004 | [netG.pth](link) | [infomax_gan_32.py](nets/infomax_gan/infomax_gan_32.py) |

-------

<div id="reproducibility"></div>

## Reproducibility
To verify our implementations, we reproduce reported scores in literature by re-implementing the models with the same architecture, training them under the same conditions and evaluate them on CIFAR-10 using the exact same methodology for computing FID.

As FID produces highly biased estimates (where using larger samples lead to a lower score), we reproduce the scores using the same sample sizes, where n<sub>real</sub> and n<sub>fake</sub> refers to the number of real and fake images used respectively for computing FID.

| Metric              | Model       | Score           | Reported Score | n<sub>real</sub>| n<sub>fake</sub>| Checkpoint |  Code |
|:-------------------:|:-----------:|:---------------:|:--------------:|:------------------:|:----:|:----:|:---:|
| FID                 | DCGAN       | 28.95 ± 0.42    | 28.12     [5]  | 10K  | 10K | [netG.pth]() | [dcgan_cifar.py]()
| FID				  | WGAN-GP     | 26.08 ± 0.12    | 29.3 <sup>†</sup> [7] | 50K | 50K | [netG.pth]() | [wgan_gp_32.py]()
| FID                 | SNGAN       | 23.90 ± 0.20    | 21.7 ± 0.21 [1]| 10K | 5K | [netG.pth]() | [sngan_32.py]()
| FID                 | cGAN-PD     | 17.84 ± 0.17    | 17.5 [2]      | 10K | 5K | [netG.pth]() | [cgan_pd_32.py]()
| FID                 | SSGAN       |  17.61 ± 0.14  | 17.88 ± 0.64 [3]     | 10K | 10K | [netG.pth]() | [ssgan_32.py]()
| FID                 | InfoMax-GAN | 17.14 ± 0.20    | 17.39 ± 0.08 [6]   | 50K | 10K | [netG.pth]() | [infomax_gan_32.py]()


*<sup>†</sup> Best FID was reported at 53K steps, but we find our score can improve till 100K steps to achieve 23.13 ± 0.13.*

## References
[[1] Spectral Normalization for Generative Adversarial Networks](https://arxiv.org/abs/1802.05957)

[[2] cGANs with Projection Discriminator](https://arxiv.org/abs/1802.05637)

[[3] Self-Supervised GANs via Auxiliary Rotation Loss](https://arxiv.org/abs/1811.11212)

[[4] Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks](https://arxiv.org/abs/1511.06434)

[[5] A Large-Scale Study on Regularization and Normalization in GANs](https://arxiv.org/abs/1807.04720)

[[6] InfoMax-GAN: Improving Adversarial Image Generation via Mutual Information Maximization and Contrastive Learning]()

[[7] GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium](https://arxiv.org/abs/1706.08500)
