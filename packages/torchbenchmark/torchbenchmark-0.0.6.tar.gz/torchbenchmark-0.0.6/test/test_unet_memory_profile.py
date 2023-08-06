import torch
from torchvision import models

from torchbenchmark.network.core.unet import UNet

network_name = "resnet152"

num_classes = 1000

net = UNet(n_channels=3, n_classes=num_classes)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
vgg = models.alexnet().to(device)



import torchbenchmark.estimator.model_estimator as est

input_size = (3, 227, 227)
mest = est.ModelEstimator(name='alexnet', model=net, input_size=input_size, batch_size=2 ,save=True, save_path='stats/alexnet_info_dummy.info')

mest.generate_summary()