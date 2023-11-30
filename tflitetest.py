
'''
# Load the Keras model (.h5 file)
model = tf.keras.models.load_model('lstm.h5')

# Convert the Keras model to TensorFlow Lite format with specified ops
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
converter._experimental_lower_tensor_list_ops = False  # Disable lower tensor list ops

tflite_model = converter.convert()

# Save the converted model to a .tflite file
with open('converted_model.tflite', 'wb') as f:
    f.write(tflite_model)'''
"""
import numpy as np
import tensorflow as tf

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path='converted_model.tflite')
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Prepare input data (replace this with your actual input data)
input_data = np.random.rand(1, 40, 8).astype(np.float32)

# Set the input tensor with the prepared input data
interpreter.set_tensor(input_details[0]['index'], input_data)

# Run inference
interpreter.invoke()

# Get the output tensor
output_data = interpreter.get_tensor(output_details[0]['index'])

# Use the output data
print("Output:", output_data)

"""


'''
# Load the Keras model (.h5 file)
model = tf.keras.models.load_model('lstm.h5')

# Convert the Keras model to TensorFlow Lite format with specified ops
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
converter._experimental_lower_tensor_list_ops = False  # Disable lower tensor list ops

tflite_model = converter.convert()

# Save the converted model to a .tflite file
with open('converted_model.tflite', 'wb') as f:
    f.write(tflite_model)'''

import numpy as np
from tflite_runtime.interpreter import Interpreter

# Load the TensorFlow Lite model
interpreter = Interpreter(model_path='converted_model.tflite')
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Prepare input data (replace this with your actual input data)
input_data = np.random.rand(1, 40, 8).astype(np.float32)

# Set the input tensor with the prepared input data
interpreter.set_tensor(input_details[0]['index'], input_data)

# Run inference
interpreter.invoke()

# Get the output tensor
output_data = interpreter.get_tensor(output_details[0]['index'])

# Use the output data
print("Output:", output_data)