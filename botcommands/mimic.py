import discord
from discord.ext import commands

from typing import Any
from numpy.typing import NDArray

import numpy as np

from sklearn.preprocessing import LabelEncoder
from keras.api.layers import TextVectorization
from keras.api.utils import to_categorical
from keras._tf_keras.keras.preprocessing.text import Tokenizer
from keras.api.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.api.models import Sequential
from keras.api.layers import Dense
from keras.api.layers import Embedding
from keras.api.layers import GlobalAveragePooling1D
from keras.api.layers import Dropout
from keras.api.layers import Flatten
from keras.api.optimizers import SGD
from keras.api.optimizers import Adam


class Mimic():
    model: Sequential
    classes: Any
    
    @staticmethod
    def preprocessfeatures(x: list[str]):
        return tf.convert_to_tensor(x)

    @staticmethod
    def preprocess(x: list[str], y: list[str], vocab_size: int, max_len: int):
        vectorize_layer = TextVectorization(
            max_tokens=vocab_size,
            output_mode='int',
            output_sequence_length=max_len,
            vocabulary=list(set(x))
        )
        le = LabelEncoder()
        le.fit(y)
        Mimic.classes = le.classes_
        num_classes = le.classes_.size  # type: ignore
        y_full = le.transform(y)
        y_full = to_categorical(y_full)

        x_train, x_test, y_train, y_test = train_test_split(
            x, y_full, train_size=0.8)
        return vectorize_layer, num_classes, x_train, x_test, y_train, y_test

    @staticmethod
    def fitAndEvaluate(epochs, batch_size, x_train, y_train, x_test, y_test):
        # es = EarlyStopping(monitor='loss', min_delta=0.005, patience=10, verbose=1, mode='auto')
        print(f"\nFitting fold")
        Mimic.model.fit(x_train, y_train, epochs=epochs,
                        shuffle=True, batch_size=batch_size,
                        verbose=0,
                        # callbacks=[es]
                        )
        print(f"\nTest evaluation")
        Mimic.model.evaluate(x_test, y_test)

    @staticmethod
    def makeModel(x: list[str], y: list[str]):
        vocab_size = 1000
        max_len = 30
        vectorize_layer, num_classes, x_train, x_test, y_train, y_test = Mimic.preprocess(
            x, y, vocab_size, max_len)

        x_train = tf.convert_to_tensor(x_train)
        y_train = tf.convert_to_tensor(y_train)
        x_test = tf.convert_to_tensor(x_test)
        y_test = tf.convert_to_tensor(y_test)

        embedding_dim = 256
        Mimic.model = Sequential([
            vectorize_layer,
            Embedding(
                vocab_size, embedding_dim, trainable=True),
            Dense(512, activation='relu'),
            GlobalAveragePooling1D(),
            Dense(256, activation='relu'),
            Dense(128, activation='relu'),
            Dense(64, activation='relu'),
            Dense(num_classes, activation='softmax'),
        ])
        opt = Adam(learning_rate=0.001)
        epochs = 120
        batch_size = 100
        Mimic.model.compile(loss="categorical_crossentropy",
                            optimizer=opt, metrics=['accuracy'])

        Mimic.fitAndEvaluate(epochs, batch_size,
                             x_train, y_train, x_test, y_test)


@commands.hybrid_command(name="train")
async def train(ctx: commands.Context) -> None:
    messages = [message async for message in ctx.channel.history(limit=200) if not message.author.bot]
    x = [message.content for message in messages]
    y = [str(message.author.id) for message in messages]
    Mimic.makeModel(x, y)
    await ctx.message.channel.send("Trained model!")


@commands.hybrid_command(name="evaluate")
async def evaluate(ctx: commands.Context, text: str) -> None:
    if Mimic.model is None:
        await ctx.message.channel.send("No model found.")
    print(text)
    predictions = Mimic.model.predict(Mimic.preprocessfeatures([text]))
    print(Mimic.model)
    print(predictions)
    closestGlobalName = Mimic.classes[np.argmax(predictions, axis=1)][0]
    print(closestGlobalName)
    closestUser: discord.User = await commands.UserConverter().convert(ctx, closestGlobalName)
    await ctx.message.channel.send(closestUser.display_name + " would say '" + text + "'")


async def setup(bot: commands.Bot):
    bot.add_command(train)
    bot.add_command(evaluate)
