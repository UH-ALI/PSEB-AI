import matplotlib.pyplot as plt
df["score"].hist(bins=[0, 20, 40, 60, 80, 100])

print(df["city"].value_counts()["Lahore"])
print(df.sort_values("score", ascending=False).head(3))
print((df["score"] >= 50).sum())

print(df[['scores'], ['hours']].corr())
what's wrong above?
