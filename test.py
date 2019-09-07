
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
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/juntaekim/Downloads/MLserving93-84b701a1ee3a.json"
#from mypackage.model import mymodel




# json_request = request.get_json()
# url = json_request.get('url')
resp = urlopen('https://raw.githubusercontent.com/ryfeus/gcf-packs/master/tensorflow2.0/example/test.png')
image = np.asarray(bytearray(resp.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
img = torch.tensor(image).float().unsqueeze(1).reshape(-1, 1, 28, 28)


client = storage.Client()
bucket = client.get_bucket(bucket_or_name='upload-bigquery')
blobs = bucket.list_blobs(prefix='model_param.pth')
for blob in blobs:
	filename = os.path.basename(blob.name)
	print(filename)
	#blob.download_to_filename('model.pth')

# MODEL_URL = 'https://storage.cloud.google.com/upload-bigquery/model.pth?hl=ko'
# r = requests.get(MODEL_URL)


# file = open("model.pth", 'wb')
# file.write(r.content)
# file.close()

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

checkpoint = torch.load('save_model/model_param.pth')
model = Net()
model.load_state_dict(checkpoint['model'])
#model = torch.load('model.pth')
model.eval()

_, predicted = torch.max(out.data, -1)

print(predicted)