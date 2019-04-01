from utility import generate_training_data
from keras.models import Sequential
from keras.layers import Dense
import numpy as np

print("Generating Training Datasets")
training_data_x, training_data_y = generate_training_data()
print("Datasets Generated")
model = Sequential()
model.add(Dense(units=9,input_dim=7))
model.add(Dense(units=15, activation='relu'))
model.add(Dense(output_dim=3,  activation = 'softmax'))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.fit((np.array(training_data_x).reshape(-1,7)),( np.array(training_data_y).reshape(-1,3)), batch_size = 256,epochs= 3)

model.save_weights('dnn_model.h5')
model_json = model.to_json()
with open('model.json', 'w') as json_file:
    json_file.write(model_json)