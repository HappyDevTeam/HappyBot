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
from keras.api.layers import Flatten
from keras.api.optimizers import SGD


class Mimic():
    model: Sequential
    classes: Any

    @staticmethod
    def preprocessfeatures(x: list[str]):
        tokenizer = Tokenizer(num_words=300, filters=' ', oov_token='UNK')
        tokenizer.fit_on_texts(x)
        x_full = tokenizer.texts_to_sequences(x)
        x_full = pad_sequences(x_full, maxlen=200, padding='post')
        return x_full

    @staticmethod
    def preprocesslabels(y: list[str]):
        le = LabelEncoder()
        le.fit(y)
        num_classes = le.classes_.size  # type: ignore
        y_full = le.transform(y)
        y_full = to_categorical(y_full)
        return y_full, le.classes_, num_classes

    @staticmethod
    def makeModel(x: list[str], y: list[str]):
        print(x, y)
        x_full = Mimic.preprocessfeatures(x)
        y_full, Mimic.classes, num_classes = Mimic.preprocesslabels(y)
        print(y_full)
        x_train, x_test, y_train, y_test = train_test_split(
            x_full, y_full, train_size=0.8)
        x_train = tf.convert_to_tensor(x_train)
        y_train = tf.convert_to_tensor(y_train)
        x_test = tf.convert_to_tensor(x_test)
        y_test = tf.convert_to_tensor(y_test)
        print(x_train, x_test, y_train, y_test, sep="\n")

        vocab_size = 1000
        embedding_dim = 30
        Mimic.model = Sequential([
            Embedding(
                vocab_size, embedding_dim, trainable=True),
            Dense(512, activation='relu'),
            Flatten(),
            Dense(512, activation='relu'),
            Dense(num_classes, activation='sigmoid'),
        ])
        opt = SGD(learning_rate=0.000001)
        Mimic.model.compile(loss="categorical_crossentropy",
                    optimizer="adam", metrics=['accuracy'])

        # es = EarlyStopping(monitor='loss', min_delta=0.005, patience=1, verbose=1, mode='auto')
        Mimic.model.fit(x_train, y_train, epochs=30,
                shuffle=True, batch_size=30, verbose=2)#type: ignore

        scores = Mimic.model.evaluate(x_test, y_test)
        print(Mimic.model.metrics_names[0], Mimic.model.metrics_names[1])


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
