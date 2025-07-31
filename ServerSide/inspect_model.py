import tensorflow as tf

model = tf.keras.models.load_model('drowsiness_model.h5')
print("Model expects input shape:", model.input_shape)
model.summary()  # Look at the very first layer
