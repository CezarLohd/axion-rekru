import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

df = pd.read_csv("dataset.csv")

# Ucinamy dataset z innych genre
df = df[df["track_genre"].isin(["rock", "hip-hop"])]
# Usuwamy duplikaty - w spotify np często ta sama piosenka ma różne wydania, przez co będzie się dublowac
df = df.drop_duplicates(subset=["artists", "track_name"])
# W datasecie sa tez kawalki zespolow jak 

print("<<< Liczba utworow po oczyszczeniu >>>")
print(df["track_genre"].value_counts())

print("<<< Avg, mediana i maksymalne odchylenia w speechiness (rock a hiphop) >>>")
print(df.groupby("track_genre")["speechiness"].agg(["mean", "median", "min", "max"]).round(3))

print("<<< Avg, mediana i maksymalne odchylenia w explicit (rock a hiphop) (to boolean!!)>>>")
print(df.groupby("track_genre")["explicit"].agg(["mean", "median", "min", "max"]).round(3))


cechy = ["speechiness", "danceability", "energy", "acousticness", "valence", "explicit"]
print("<<< Avg dla pozostalych cech >>>")
print(df.groupby("track_genre")[cechy].mean().round(3))


kolumny_info = ["artists", "track_name", "speechiness", "danceability", "explicit"]

rap = df[df["track_genre"] == "hip-hop"]
rock = df[df["track_genre"] == "rock"]

print("<<< HIP-HOP: najwyzsze speechiness >>>")
print(rap.nlargest(5, "speechiness")[kolumny_info])

print("<<< HIP-HOP: najnizsze speechiness >>>")
print(rap.nsmallest(5, "speechiness")[kolumny_info])

print("<<< ROCK: najwyzsze speechiness >>>")
print(rock.nlargest(5, "speechiness")[kolumny_info])



