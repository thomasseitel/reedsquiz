from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

BASE_DIR = Path(__file__).resolve().parent


def make_question_1():
    fig, ax = plt.subplots()
    x = np.linspace(-10, 10, 1000)
    ax.plot(x, x**2)
    ax.grid(True, linestyle="--")
    ax.axvline(x=0, color="k", linestyle="-", linewidth=2.0)
    ax.axhline(y=0, color="k", linestyle="-", linewidth=2.0)
    plt.ylim(-5, 15)
    plt.savefig(str(BASE_DIR / "question1.png"))

    (answer,) = ax.plot(x, 2 * x)
    plt.savefig(str(BASE_DIR / "question1_a.png"))
    answer.remove()

    (answer,) = ax.plot(x, x**2)
    plt.savefig(str(BASE_DIR / "question1_b.png"))
    answer.remove()

    (answer,) = ax.plot(x, x**3)
    plt.savefig(str(BASE_DIR / "question1_c.png"))


make_question_1()
