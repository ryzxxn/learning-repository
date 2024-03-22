x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
model.add(tf.keras.layers.Dense(128, activation = 'relu'))
model.add(tf.keras.layers.Dense(10, activation = 'softmax'))
# Compile the model
model.compile(optimizer=r'adam', loss=r'sparse_categorical_crossentropy', metrics=[r'accuracy'])
model.fit(x_train, y_train, epochs=20)
model.save('model.keras')