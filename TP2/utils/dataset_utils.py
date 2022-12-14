import numpy as np
import math


def DivideDatasetDfToTrainAndTest(dataset_df, train_percentage):
    np.random.shuffle(dataset_df.values)
    train_dataset_df = dataset_df.head(math.ceil(len(dataset_df)*(train_percentage)))
    test_dataset_df = dataset_df.tail(math.floor(len(dataset_df)*(1- train_percentage)))

    return train_dataset_df, test_dataset_df

def DivideDatasetToTrainAndTest(dataset, train_percentage):
    np.random.shuffle(dataset)
    train_dataset = dataset[:math.ceil(len(dataset)*(train_percentage))]
    test_dataset = dataset[math.floor(len(dataset)*(train_percentage)):]

    return train_dataset, test_dataset
    