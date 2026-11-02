# import numpy as np
# temps = np.array([31,34,36,38,33,29,35])
# print(temps * 9/5 + 32)
# print(temps[temps > 35])

import pandas as pd
df = pd.DataFrame({
    "name": ["Ali", "Bilal", "Cyzen"],
    "score": [100, 89, 92],
    "city": ["karachi", "lahore", "islamabad"]
})

# print(df.loc[0, "score"])
# print(df.iloc[1,2])

# print(df.groupby("city"))

print(df[df["city"] == "karachi"])
print(df["score"].mean())
print(df.loc[df["score"].idxmax(), "name"])