import discord
from discord.ext import commands
import typing
import tensorflow as tf
import numpy as np
import keras
from sklearn.model_selection import train_test_split


class Mimic():
    model: keras.models.Sequential
    mean: np.floating[typing.Any]
    std: np.floating[typing.Any]

    def __init__(self, x: list[str], y_i: list[int]):
        self.mean = np.mean(y_i)
        self.std = np.std(y_i)
        y = y_i

        vocab_size = 10000
        sequence_length = 20
        vectorize_layer = keras.layers.TextVectorization(
            max_tokens=vocab_size,
            output_mode='int',
            output_sequence_length=sequence_length
        )
        vectorize_layer.adapt(x)

        # print(x)
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2)
        x_train = tf.convert_to_tensor(x_train)
        y_train = tf.convert_to_tensor(y_train)
        x_test = tf.convert_to_tensor(x_test)
        y_test = tf.convert_to_tensor(y_test)
        print(x_train, x_test, y_train, y_test)

        print("Creating model")
        embedding_dim = 16
        self.model = keras.models.Sequential([
            vectorize_layer,
            keras.layers.Embedding(
                vocab_size, embedding_dim, name="embedding"),
            keras.layers.GlobalAveragePooling1D(),
            keras.layers.Dense(8, activation='relu'),
            keras.layers.Dense(5, activation='relu'),
            keras.layers.Dense(1)
        ])

        print("Compiling")
        self.model.compile(
            optimizer='adam',
            loss=keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=['accuracy']
        )

        print("Fitting")
        tensorboard_callback = keras.callbacks.TensorBoard(log_dir="logs")
        self.model.fit(x_train, y_train, epochs=25,
                       callbacks=[tensorboard_callback])
        self.model.summary()

mimic = None


@commands.hybrid_command(name="train")
async def train(ctx: commands.Context) -> None:
    messages = [message async for message in ctx.channel.history(limit=200) if not message.author.bot]
    # for message in messages: print(message.author, ": ", message.content)
    x = [message.content for message in messages]
    y = [message.author.id for message in messages]
    global mimic
    mimic = Mimic(x, y)

    await ctx.message.channel.send("Trained model!")


@commands.hybrid_command(name="evaluate")
async def evaluate(ctx: commands.Context, text: str) -> None:
    if mimic is None:
        await ctx.message.channel.send("No model found.")
    assert(isinstance(mimic, Mimic))
    predictions = mimic.model.predict(tf.convert_to_tensor(list(text)))
    print(predictions)
    predictions = [prediction * mimic.std + mimic.mean for prediction in predictions]
    print(predictions)
    response = np.mean(predictions)
    assert(isinstance(ctx.guild, discord.Guild))
    ids = set([member.id for member in ctx.guild.members])
    closestId: int = min(ids, key=lambda x: abs(x - int(response)))
    print(response, closestId)
    closestUser: discord.User = await commands.UserConverter().convert(ctx, str(closestId))
    await ctx.message.channel.send(closestUser.display_name + " would say '" + text + "'")


async def setup(bot: commands.Bot):
    bot.add_command(train)
    bot.add_command(evaluate)
