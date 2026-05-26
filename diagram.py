import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load JSONL file (Train-Sent (1).jsonl)
jsonl_file_path = r"C:\Users\raji\Downloads\garbage_ml\Train-Sent (1).jsonl"
data = []
with open(jsonl_file_path, "r", encoding="utf-8") as f:
    for line in f:
        data.append(json.loads(line))
df_jsonl = pd.DataFrame(data)

# Load JSON file (ipc.json)
ipc_file_path = r"C:\Users\raji\Downloads\garbage_ml\ipc.json"
with open(ipc_file_path, "r", encoding="utf-8") as f:
    ipc_data = json.load(f)
df_ipc = pd.DataFrame(ipc_data)

# Ensure proper column names
df_ipc.rename(columns={"Section": "ipc_section"}, inplace=True)

# 📊 Bar Chart: IPC Section Frequency
if "ipc_section" in df_jsonl.columns:
    plt.figure(figsize=(12, 6))
    df_jsonl["ipc_section"].value_counts().plot(kind="bar", color="teal")
    plt.xlabel("IPC Section")
    plt.ylabel("Frequency")
    plt.title("Frequency of IPC Sections in Complaints")
    plt.xticks(rotation=90)
    plt.savefig("ipc_section_frequency.png")  # Save the plot
    plt.show()

# 📉 Histogram: Distribution of Similarity Scores
if "similarity_score" in df_jsonl.columns:
    plt.figure(figsize=(8, 6))
    sns.histplot(df_jsonl["similarity_score"], bins=30, kde=True, color="purple")
    plt.xlabel("Similarity Score")
    plt.ylabel("Density")
    plt.title("Distribution of Similarity Scores")
    plt.savefig("similarity_score_distribution.png")
    plt.show()

# 🥧 Pie Chart: IPC Sections Distribution
if "ipc_section" in df_jsonl.columns:
    plt.figure(figsize=(8, 8))
    df_jsonl["ipc_section"].value_counts().nlargest(10).plot(kind="pie", autopct="%1.1f%%", cmap="coolwarm")
    plt.title("Top 10 IPC Sections in Complaints")
    plt.ylabel("")  # Remove y-axis label for clarity
    plt.savefig("ipc_section_pie_chart.png")
    plt.show()

# ☁️ Word Cloud: Common IPC Section Titles (from ipc.json)
if "Title" in df_ipc.columns:
    text = " ".join(df_ipc["Title"].dropna())  # Concatenate all section titles
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud of IPC Section Titles")
    plt.savefig(r"C:\Users\raji\Downloads\garbage_ml\wordcloud.png")

    plt.show()
