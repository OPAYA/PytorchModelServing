# import os

# from google.cloud import storage

# import argparse
# import logging

# import torch
# import torch.nn as nn
# import torch.nn.functional as F

# model = None


# class Net(nn.Module):
#     def __init__(self, hidden_size):
#         super(Net, self).__init__()
#         self.conv1 = nn.Conv2d(1, 20, 5, 1)
#         self.conv2 = nn.Conv2d(20, 50, 5, 1)
#         self.fc1 = nn.Linear(4*4*50, hidden_size)
#         self.fc2 = nn.Linear(hidden_size, 10)

#     def forward(self, x):
#         x = F.relu(self.conv1(x))
#         x = F.max_pool2d(x, 2, 2)
#         x = F.relu(self.conv2(x))
#         x = F.max_pool2d(x, 2, 2)
#         x = x.view(-1, 4*4*50)
#         x = F.relu(self.fc1(x))
#         x = self.fc2(x)
#         return F.log_softmax(x, dim=1)

# def save_deploying():
#     storage_client = storage.Client()
#     bucket = storage_client.get_bucket(bucket_or_name='upload-bigquery')
#     blobs = bucket.list_blobs(prefix='model.pth')
#     for blob in blobs:
#         filename = os.path.basename(blob.name)
#         print('Download File {}'.format(filename))
#         blob.download_to_filename('deploying_model/{}'.format(filename))

# def predict(url):
#     global model
#     # Model load which only happens during cold starts
#     if model is None:
#         save_deploying()

#     response = requests.get(url)
#     input_np = (numpy.array(Image.open(BytesIO(response.content)))/255)[numpy.newaxis,:,:,numpy.newaxis]
    
#     model = torch.load('deploying_model/model.pth')
#     model.eval()
#     with torch.no_grad():
#         outputs = model(input_np)
#         _, predicted = torch.max(outputs.data, 1)
#         print('Image is {}'.format(predicted))

def predict_mnist(request):

    parameters = [
        URL,
    ]

    if request.get_json():
        json_request = request.get_json()
        for parameter in parameters:
            if not json_request.get(parameter) is None:
                continue
            raise BadRequest('invalid request parameter: %s' % parameter)

        url = json_request.get(URL)

    else:
        raise BadRequest('invalid arguments error')

    predicted_class = predict(url)

    data = {
        CLASS: predicted_class,
    }

    res = {
        CODE: 200,
        MESSAGE: 'OK',
        DATA: data,
    }
    return jsonify(res)
