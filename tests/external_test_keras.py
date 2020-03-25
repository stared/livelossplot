from random import randint

from keras import Sequential
from keras.layers import LSTM, Dense
from numpy import argmax
from numpy import array

from livelossplot import MainLogger, PlotLossesKeras
from livelossplot.outputs import BaseOutput

NUM_OF_GENERATED = 5


class CheckOutput(BaseOutput):
    def send(self, logger: MainLogger):
        assert isinstance(logger, MainLogger)
        grouped_log_history = logger.grouped_log_history(raw_names=True, raw_group_names=True)
        print(grouped_log_history['accuracy'].keys())
        assert len(grouped_log_history['accuracy']) == 2
        assert grouped_log_history['accuracy'].get('val_accuracy') is not None


def generate_sequence(length=5):
    return [randint(0, NUM_OF_GENERATED - 1) for _ in range(length)]


def one_hot_encode(sequence, n_unique=NUM_OF_GENERATED):
    encoding = list()
    for value in sequence:
        vector = [0 for _ in range(n_unique)]
        vector[value] = 1
        encoding.append(vector)
    return array(encoding)


def one_hot_decode(encoded_seq):
    return [argmax(vector) for vector in encoded_seq]


def generate_data():
    sequence = generate_sequence()
    encoded = one_hot_encode(sequence)
    X = encoded.reshape(encoded.shape[0], 1, encoded.shape[1])
    return X, encoded


def test_keras():
    callback = PlotLossesKeras(outputs=(CheckOutput(), ))
    model = Sequential()
    model.add(LSTM(5, input_shape=(1, NUM_OF_GENERATED)))
    model.add(Dense(NUM_OF_GENERATED, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    X_train, Y_train = generate_data()
    X_test, Y_test = generate_data()
    model.fit(X_train, Y_train, epochs=2, validation_data=(X_test, Y_test), callbacks=[callback], verbose=False)
