import zzz_enums as enum
import zzz_tools as t
import classes.log as log
# print(t.is_enum_value("Polsat", enum.Supplier))
log.log_header("test")
log.print_log()

import pandas as pd
import numpy as np

# Load your dataframe (replace this with your actual dataframe loading code)
data = {'cpp': [np.inf, np.inf, np.inf, np.inf, 25, 30]}
df = pd.DataFrame(data)

max_index = df[df['cpp'] != np.inf]['cpp'].idxmax()
print(max_index)