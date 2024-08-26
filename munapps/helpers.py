import numpy as np

# Helpers
def get_rows_table(rows):
    n_row = np.quantile(np.arange(1, rows), [.25, .5, .75, ])
    return np.append(np.unique(np.rint(n_row).astype(int)).astype(str), ['All'])