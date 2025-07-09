
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy.abc import x
import streamlit as st

def generate_function(level):
    import random
    if level == "Easy":
        num = x - random.randint(1, 5)
        den = x + random.randint(1, 5)
    elif level == "Medium":
        num = (x - random.randint(1, 5)) * (x + random.randint(1, 5))
        den = (x - random.randint(6, 9)) * (x + random.randint(6, 9))
    else:
        num = (x**2 - 1)*(x - random.randint(2, 3))
        den = (x**2 - 4)*(x + random.randint(2, 3))
    return num / den

def get_features(expr):
    expr = sp.simplify(expr)
    num, den = sp.fraction(expr)

    holes = []
    asymptotes = []
    x_intercepts = list(sp.solve(num, x))
    y_intercept = expr.subs(x, 0)

    canceled = sp.gcd(num, den)
    if canceled != 1:
        hole_x = list(sp.solve(canceled, x))
        for val in hole_x:
            holes.append((float(val), float(expr.subs(x, val))))

    den_roots = sp.solve(den, x)
    for val in den_roots:
        if val not in holes:
            asymptotes.append(float(val))

    end_behavior = sp.limit(expr, x, sp.oo)

    return {
        "x_intercepts": [float(i) for i in x_intercepts],
        "y_intercept": float(y_intercept),
        "holes": holes,
        "asymptotes": asymptotes,
        "end_behavior": end_behavior
    }

def graph_function(expr):
    fig, ax = plt.subplots()
    f = sp.lambdify(x, expr, modules=["numpy"])
    X = np.linspace(-10, 10, 1000)
    Y = []

    for val in X:
        try:
            Y.append(f(val))
        except:
            Y.append(np.nan)

    ax.plot(X, Y, color="blue")
    features = get_features(expr)
    for a in features["asymptotes"]:
        ax.axvline(x=a, color="red", linestyle="--")
    for h in features["holes"]:
        ax.plot(h[0], h[1], 'ko')
    ax.grid(True)
    st.pyplot(fig)
