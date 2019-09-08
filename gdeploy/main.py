'''
	code by Juntae Kim
	reference : https://github.com/graykode/mnist-flow/blob/master/gfunction/main.py
'''
import os
import numpy as np
import requests
import cv2
import torch
from torch import nn
from torch.nn import functional as F

from google.cloud import storage
from PIL import Image
from io import BytesIO
from urllib.request import urlopen

def predict(request):
	print('Request', request)

	json_request = request.get_json()
	url = json_request.get('url')
	resp = urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")

	if len(image) != 784:
		return "Not correct Image size"
		
	img = torch.tensor(img).float().reshape(-1, 1, 28, 28)

	os.mkdir('/tmp/save_model')
	client = storage.Client()
	bucket = client.get_bucket(bucket_or_name='upload-bigquery')
	blobs = bucket.list_blobs(prefix='model_param.pth')
	for blob in blobs:
		filename = os.path.basename(blob.name)
		blob.download_to_filename('/tmp/save_model/model_param.pth')

	class Net(nn.Module):
		def __init__(self):
		    super(Net, self).__init__()
		    self.conv1 = nn.Conv2d(1, 20, 5, 1)
		    self.conv2 = nn.Conv2d(20, 50, 5, 1)
		    self.fc1 = nn.Linear(4*4*50, 512)
		    self.fc2 = nn.Linear(512, 10)

		def forward(self, x):
		    x = F.relu(self.conv1(x))
		    x = F.max_pool2d(x, 2, 2)
		    x = F.relu(self.conv2(x))
		    x = F.max_pool2d(x, 2, 2)
		    x = x.view(-1, 4*4*50)
		    x = F.relu(self.fc1(x))
		    x = self.fc2(x)
		    return F.log_softmax(x, dim=1)

	model = Net()
	checkpoint = torch.tensor('/tmp/save_model/model_param.pth')

	model.load_state_dict(checkpoint['model'])
 
	out = model(img)

	_, predicted = torch.max(out.data, 1)

	
	return predicted