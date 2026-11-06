# -----------------------------------
#   1. setdir and data import
# -----------------------------------
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

data_dir = Path("example/data")

train_file = data_dir/("PXD006109_Cerebellum_rt_add_mox_all_rt_range_3_train.tsv")

test_file = data_dir/("PXD006109_Cerebellum_rt_add_mox_all_rt_range_3_test.tsv")

train = pd.read_csv(train_file, sep="\t")
test = pd.read_csv(test_file, sep="\t")

# -----------------------------------
#   2. check dim
# -----------------------------------
print("Training data dimension:", train.shape)
print("Testing data dimension:", test.shape)

print("\nColumn names:")
print(train.columns.tolist())

print("\nTraining Data type:")
print(train.info())
print("\nTesting Data type:")
print(test.info())

# first 10 rows
print("\nDisplay head:")
print(train.head(10).to_string(index=False))

# Data quality check
print("\nMissing values in training data:")
print(train.isna().sum())
print("\nMissing values in testing data:")
print(test.isna().sum())
print("\nDuplicate sequences in training data:")
print(train["x"].duplicated().sum())
print("\nTrain/Test sequence overlap:")
print(len(set(train["x"]) & set(test["x"])))

# numeric retention time
rt = pd.to_numeric(train["y"], errors="coerce")

print("\nRetention time statistics:")
print(rt.describe())

# peptide sequence length
seq_length = train["x"].str.len()
print("\nPeptide length statistics:")
print(seq_length.describe())

# identify modified sequences (for those have numeric value in sequence)
modified_sequence = train["x"].str.contains(r"\d",na=False)
print("\nSequences containing modification tokens:")
print(modified_sequence.sum())
print("\nDisplay 10 modified sequence:")
print(train.loc[modified_sequence, "x"].head(10).to_string(index=False))

# RT plot
fig, axes = plt.subplots(1, 2, figsize=(11, 4))


axes[0].hist(rt.dropna(), bins=50, color= "steelblue", edgecolor="white", linewidth=0.8)
axes[0].set_xlabel("Retention Time (min)")
axes[0].set_ylabel("Count")
axes[0].set_title("Retention Time Distribution")

axes[1].hist(seq_length.dropna(), bins=40, color = "TEAL", edgecolor = "white", linewidth = 0.8)
axes[1].set_xlabel("Peptide Length")
axes[1].set_ylabel("Count")
axes[1].set_title("Peptide Length Distribution")

plt.tight_layout()
plt.savefig("EDA_RT_exploration.png", dpi=200)
plt.show()





