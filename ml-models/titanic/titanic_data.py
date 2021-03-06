import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split


def load_data():
    # Loads sanitised data
    data = pd.read_csv("./data/train.csv")
    median_age = data["Age"].median()
    data["Age"].fillna(median_age, inplace=True)
    features = data[["Pclass", "Age", "Sex"]]
    labels = data[["Survived"]]
    train_f, test_f, train_l, test_l = train_test_split(
        features, labels, test_size=0.2)

    return (train_f, train_l), (test_f, test_l)


def input_fn_train(features, labels, batch_size):
    # Input function for training the model
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    # Return the dataset.
    return dataset


def input_fn_eval(features, labels, batch_size):
    # Input function for evaluating the model
    features = dict(features)
    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)

    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    # Return the dataset.
    return dataset
