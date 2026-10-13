import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

raw = {
    "Date": ["2026-03-01", "2026-03-02", "2026-03-03", "2026-03-04", "2026-03-05",
             "2026-03-06", "2026-03-07", "2026-03-08", "2026-03-09", "2026-03-10",
             "2026-03-11", "2026-03-12", "2026-03-13", "2026-03-14", "2026-03-15",
             "2026-03-09"],
    "City": ["Lahore", "lahore", "LAHORE", " Lahore", "Lahore ", "lahore", "Lahore",
             " LAHORE ", "Lahore", "lahore", "Lahore", "LAHORE", "Lahore", " lahore",
             "Lahore", "Lahore"],
    "Temperature": ["32C", "24C", "27C", "34C", "28C", "35C", "22C", "33C", "26C",
                    "36C", "23C", "34C", "29C", "31C", "27C", "26C"],
    "Humidity": [40, 82, np.nan, 38, 60, np.nan, 88, 42, 65, 35, np.nan, 40, 55, 48,
                 62, 65],
    "Condition": ["sunny", " Rainy", "Cloudy", "SUNNY", "CLOUDY", "Sunny", "rainy ",
                  " sunny", "cloudy", "Sunny", "RAINY", "sunny ", "CLOUDY ", "Sunny",
                  "Cloudy", "cloudy"],
}
df = pd.DataFrame(raw)

# (a) Cleaning
df["City"] = df["City"].str.strip().str.title()
df["Condition"] = df["Condition"].str.strip().str.title()
df["Temperature"] = pd.to_numeric(df["Temperature"].str.replace("C", "", regex=False), errors="coerce")
df["Date"] = pd.to_datetime(df["Date"])
df = df.drop_duplicates()
print("Rows after dropping duplicates:", len(df))

median_hum = df["Humidity"].median()
df["Humidity"] = df["Humidity"].fillna(median_hum)
print("Missing Humidity filled with median:", median_hum)

# (b) One-hot encoding
encoded = pd.get_dummies(df, columns=["Condition"], dtype=int)
print(encoded.filter(like="Condition_").head())

# (d) Correlation
corr = df["Temperature"].corr(df["Humidity"])
print("Correlation (Temperature, Humidity):", round(corr, 2))

counts = df["Condition"].value_counts()
print("Condition counts:")
print(counts)

# (c, e, f) 2 x 2 dashboard
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].plot(df["Date"], df["Temperature"], marker="o", color="steelblue")
axes[0, 0].set_title("Temperature over Date")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Temperature (C)")
axes[0, 0].tick_params(axis="x", rotation=45)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].scatter(df["Temperature"], df["Humidity"], color="darkorange", s=60)
axes[0, 1].set_title("Temperature vs. Humidity")
axes[0, 1].set_xlabel("Temperature (C)")
axes[0, 1].set_ylabel("Humidity (%)")
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90,
               colors=["#F58518", "#4C78A8", "#54A24B"])
axes[1, 0].set_title("Days per Condition")

axes[1, 1].hist(df["Temperature"], bins=5, color="seagreen", edgecolor="white")
axes[1, 1].set_title("Temperature Distribution")
axes[1, 1].set_xlabel("Temperature (C)")
axes[1, 1].set_ylabel("Number of Days")

fig.suptitle("Weather Overview", fontsize=16)
plt.tight_layout()
plt.savefig("weather_dashboard.png")
plt.show()