import pandas as pd
import numpy as np

np.random.seed(88)
df = pd.DataFrame({"A": np.linspace(1, 10, 10)})
df = pd.concat([df, pd.DataFrame(np.random.randn(10, 4), columns=list("BCDE"))], axis=1)
df.iloc[3, 3] = np.nan
df.iloc[0, 2] = np.nan
df.style.highlight_min()
print(df)
