'''
    code by Juntae Kim
    reference : https://github.com/graykode/mnist-flow/blob/master/load_bq.py
'''
import os
import numpy as np
from google.cloud import bigquery


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/juntaekim/Downloads/MLserving93-84b701a1ee3a.json"
client = bigquery.Client()


if not os.path.exists('data/x_test.npy'):
    test_query = ("SELECT image, label FROM mnist.test ORDER BY RAND()")
    test_query_job = client.query(
        test_query,
    )

    x_test = []
    y_test = []

    for row in test_query_job:
        image = np.asarray(row.image.split(',')).astype(np.uint8)
        label = np.asarray(row.label).astype(np.uint8)

        x_test.append(image)
        y_test.append(label)

    x_test = np.asarray(x_test)
    y_test = np.asarray(y_test)
    
    np.save('data/x_test', x_test)
    np.save('data/y_test', y_test)


if not os.path.exists('data/x_train.npy'):
    train_query = ("SELECT image, label FROM mnist.train ORDER BY RAND()")
    train_query_job = client.query(
        train_query,
    )

    x_train = []
    y_train = []

    for row in train_query_job:
        image = np.asarray(row.image.split(',')).astype(np.uint8)
        label = np.asarray(row.label).astype(np.uint8)

        x_train.append(image)
        y_train.append(label)

    x_train = np.asarray(x_train)
    y_train = np.asarray(y_train)
    np.save('data/x_train', x_train)
    np.save('data/y_train', y_train)
