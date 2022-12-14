import numpy as np

MIN_ERROR_TRESHOLD = np.exp(-1000000)
PREDICTION_THRESHOLD = 0.01

class Perceptron:
    def __init__(self, input_dim, learning_rate, epochs, act_func = lambda x: x, deriv_act_func = lambda x: 1):
        self.weights = np.random.uniform(low=0, high=0.3, size=1 + input_dim)
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.act_func = act_func
        self.deriv_act_func= deriv_act_func

    def classify(self, example):
        return self.act_func(np.dot(self.weights, np.append(1, example)))

    def test(self, test_data):
        correct_predictions = 0
        for example in test_data:
            if abs(self.classify(example[:-1]) - example[-1]) < PREDICTION_THRESHOLD:
                correct_predictions += 1

        return correct_predictions / len(test_data)

    def cuadratic_error(self, data):
        error = 0
        for example in data:
            error += (1 / 2) * pow(example[-1] - self.classify(example[:-1]), 2)

        return error

    def train_batch(self, train_data, test_data = None):
        continue_condition = lambda i, error_min: i < len(train_data)
        return self.train(train_data, continue_condition, test_data=test_data)

    def train_online(self, train_data, test_data = None):
        continue_condition = lambda i, error_min: error_min > MIN_ERROR_TRESHOLD and i < len(train_data)        
        return self.train(train_data, continue_condition, lambda: np.random.choice(len(train_data)), test_data)

    def write_to_csv(self, iteration, train_epoch_error, train_epoc_accuracy, test_epoch_error, test_epoc_accuracy):
        self.writer.writerow([str(iteration), 
                            str(train_epoch_error), str(train_epoc_accuracy), 
                            str(test_epoch_error), str(test_epoc_accuracy)])

    def train(self, train_data, continue_condition, next_example_idx_generator = None, test_data = None):
        # test_data is only used to calculate the error in each epoch for the test_dataset, NOT for training

        error_min = float('inf')
        w_min = self.weights
        iterations = 0

        train_accuracies = []
        test_accuracies = []
        train_errors = []
        test_errors = []

        for epoch in range(self.epochs):
            epoch_error_min = float('inf')
            iteration = 0

            while continue_condition(iteration, error_min):
                example = train_data[next_example_idx_generator() if next_example_idx_generator is not None else iteration]
                inputs = np.append(1, example[:-1])
                expected_output = example[-1]
                output = self.act_func(np.dot(self.weights, inputs))

                delta_w = self.learning_rate * (expected_output - output) * inputs * self.deriv_act_func(output)
                self.weights += delta_w
                epoch_error = self.cuadratic_error(train_data)
                if epoch_error < epoch_error_min:
                    epoch_error_min = epoch_error
                    epoch_w_min = self.weights

                iteration += 1

            # use best epoch weights
            self.weights = epoch_w_min

            if test_data is not None:
                epoch_test_accuracy = self.test(test_data)
                test_accuracies.append(epoch_test_accuracy)
                
                epoch_test_error = self.cuadratic_error(test_data)
                test_errors.append(epoch_test_error)
            else: epoch_test_accuracy = epoch_test_error = None

            train_accuracies.append(self.test(train_data))
            train_errors.append(epoch_error_min)

            if epoch_error_min < error_min:
                error_min = epoch_error_min
                w_min = self.weights

            iterations += iteration # add epoc iterations to total iterations

        self.weights = w_min

        max_train_accuracy = max(train_accuracies)
        max_test_accuracy = max(test_accuracies)
        min_train_error = min(train_errors)
        min_test_error = min(test_errors)
        print(f'Error min en training: {min_train_error}\nError min en test: {min_test_error}\
            \nAccuracy max en training: {max_train_accuracy}\nAccuracy max en test: {max_test_accuracy}\
            \nIterations: {iterations}')

        return train_accuracies, test_accuracies, train_errors, test_errors

        