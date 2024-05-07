from discord.ext import commands
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split


@commands.hybrid_command(name="test")
async def test(ctx: commands.Context) -> None:
    messages = [message async for message in ctx.channel.history(limit=123) if not message.author.bot]
    for message in messages:
        print(message.author, ": ", message.content)
    x = np.array([message.author.id for message in messages])
    y = np.array([tf.constant(message.content) for message in messages])
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    print("Creating model")
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_dim=1),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10)
    ])

    print("Compiling")
    predictions = model(x_train)
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    loss_fn(y_train, predictions)
    model.compile(
        optimizer='adam',
        loss=loss_fn,
        metrics=['accuracy']
    )

    print("Fitting")
    history = model.fit(x_train, y_train, epochs=5)
    print(history)
    metrics = model.evaluate(x_test,  y_test, verbose=2)
    print(metrics)


async def setup(bot: commands.Bot):
    bot.add_command(test)
