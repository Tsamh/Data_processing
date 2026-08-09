# Rapport d'analyse - Données COVID-19
**Notebook :** `covid_19_data_country_comparison.ipynb` | **Données :** `covid_19_data.csv`
**Periode couverte :** 22 janvier 2020 - 8 mars 2020 | **111 pays ou régions**

---

## 1. Inspection initiale du jeu de données

### 1.1 Structure générale

Le dataset contient **4 247 lignes et 8 colonnes** :

| Colonne | Description |
|---|---|
| `SNo` | Identifiant de ligne, sans valeur analytique |
| `ObservationDate` | Date d'observation (format `MM/DD/YYYY`) |
| `Province/State` | Province ou état, souvent absent |
| `Country/Region` | Pays ou région |
| `Last Update` | Horodatage de la dernière mise à jour |
| `Confirmed` | Nombre cumulé de cas confirmés |
| `Deaths` | Nombre cumulé de décès |
| `Recovered` | Nombre cumulé de guérisons |

Chaque ligne représente une observation pour une province ou un pays à une date donnée. Les données sont donc **cumulatives**, pas journalières brutes - ce point est fondamental pour l'interprétation des graphiques temporels.

### 1.2 Statistiques descriptives (avant nettoyage)

Les trois variables numériques utiles ont les caractéristiques suivantes :

| Statistique | Confirmed | Deaths | Recovered |
|---|---|---|---|
| Moyenne | 586.9 | 17.5 | 187.9 |
| Médiane | 9 | 0 | 1 |
| Max | 67 707 | 2 986 | 45 235 |
| 75e percentile | 99.5 | 1 | 16 |

**Interpretation :** L'écart très important entre la moyenne et la médiane (ex. 586 vs 9 pour les cas confirmés) révèle une distribution fortement asymétrique à droite. Quelques pays - principalement la Chine continentale - concentrent l'essentiel des cas, ce qui tire la moyenne vers le haut. Cette asymétrie justifie l'utilisation de graphiques à barres plutôt que de simples moyennes pour comparer les pays.

La valeur maximale de 67 707 cas confirmés pour une seule ligne correspond à une province chinoise à une date avancée de la pandémie. Ces valeurs ne sont pas des erreurs : elles reflètent la réalité épidémiologique de la Chine au moment de la collecte.

---

## 2. Nettoyage et préparation des données

### 2.1 Conversion des types numériques

```python
df["Confirmed"] = df["Confirmed"].astype(int)
df["Deaths"] = df["Deaths"].astype(int)
df["Recovered"] = df["Recovered"].astype(int)
```

**Justification :** Les colonnes `Confirmed`, `Deaths` et `Recovered` sont initialement en `float64` parce que pandas assigne ce type à toute colonne entière contenant des valeurs manquantes (les NaN ne sont pas représentables en `int` natif). Comme il n'y a aucune valeur manquante dans ces colonnes, la conversion en `int` est sans risque et améliore la lisibilité des valeurs affichées ainsi que la précision des agrégations.

### 2.2 Renommage de la colonne `Last Update`

```python
df.rename(columns={"Last Update": "LastUpdate"}, inplace=True)
```

**Justification :** Un espace dans un nom de colonne oblige à utiliser la notation entre guillemets (`df["Last Update"]`) plutôt que la notation pointée (`df.LastUpdate`). Le renommage améliore la compatibilité avec les outils qui ne tolèrent pas les espaces dans les identifiants (SQL, certaines bibliothèques de visualisation).

### 2.3 Conversion des dates en `datetime`

```python
df["ObservationDate"] = pd.to_datetime(df["ObservationDate"], format="%m/%d/%Y")
df["LastUpdate"] = pd.to_datetime(df["LastUpdate"], format="%m/%d/%Y %H:%M", errors="coerce")
```

**Justification :** Sans cette conversion, les dates sont des chaînes de caractères. Le tri chronologique, le groupement par date, et le calcul d'intervalles ne seraient pas possibles ou donneraient des résultats lexicographiques incorrects (ex. `"10/01/2020"` < `"02/01/2020"` en tri alphabétique). Le paramètre `errors="coerce"` sur `LastUpdate` permet de tolérer les quelques entrées dont le format diffère, en les convertissant en `NaT` plutôt qu'en levant une exception.

### 2.4 Traitement des valeurs manquantes

```python
df["Province/State"].fillna("Inconnue", inplace=True)
```

La colonne `Province/State` contient **1 501 valeurs manquantes sur 4 247 lignes**, soit environ 35 % du dataset. Cette absence n'est pas une erreur de saisie : de nombreux pays rapportent leurs données à l'échelle nationale sans décomposition provinciale. Remplacer ces NaN par `"Inconnue"` est une décision défendable pour :
- éviter que ces lignes soient exclues des groupements par province,
- préserver la traçabilité (on sait que la province n'est pas renseignée, et non pas qu'elle n'existe pas).

**Remarque technique :** L'utilisation de `fillna(..., inplace=True)` sur une colonne isolée peut déclencher un avertissement `ChainedAssignmentError` dans les versions récentes de pandas (Copy-on-Write). La syntaxe correcte et pérenne est :

```python
# Syntaxe recommandée (pandas >= 2.0)
df["Province/State"] = df["Province/State"].fillna("Inconnue")
```

---

## 3. Analyse par pays

### 3.1 Cas confirmés cumulés - Top 10

| Rang | Pays | Cas confirmés |
|---|---|---|
| 1 | Mainland China | 2 312 052 |
| 2 | South Korea | 58 078 |
| 3 | Italy | 35 041 |
| 4 | Iran | 30 003 |
| 5 | Others | 15 692 |
| 6 | Japan | 5 309 |
| 7 | France | 4 411 |
| 8 | Germany | 4 316 |
| 9 | Singapore | 2 817 |
| 10 | US | 2 660 |

**Interpretation :** La Chine continentale domine massivement avec plus de 2,3 millions de cas cumulés sur la période, ce qui représente plus de 95 % du total mondial à cette date. Ce chiffre élevé s'explique par deux facteurs : la Chine est le premier foyer de la pandémie (données démarrant en janvier 2020), et ses données sont agrégées sur l'ensemble de la période alors que les autres pays ont commencé à rapporter plus tard. La Corée du Sud, l'Italie et l'Iran apparaissent en rang 2, 3 et 4, témoignant des premières vagues significatives hors de Chine en février-mars 2020.

La catégorie `"Others"` (rang 5) correspond au navire de croisière Diamond Princess, en quarantaine au Japon, qui ne peut être rattaché à un pays.

### 3.2 Décès cumulés - Top 10

| Rang | Pays | Décès |
|---|---|---|
| 1 | Mainland China | 71 199 |
| 2 | Italy | 1 318 |
| 3 | Iran | 1 030 |
| 4 | South Korea | 362 |
| 5 | US | 90 |

**Interpretation :** La Chine représente l'écrasante majorité des décès sur la période. Cependant, le taux de létalité brut de la Corée du Sud (362 décès pour 58 078 cas, soit ~0,6 %) est nettement inférieur à celui de l'Italie (1 318 décès pour 35 041 cas, soit ~3,8 %). Cette différence reflète des réalités distinctes : capacité de dépistage, structure démographique, saturation des systèmes de santé.

### 3.3 Guérisons cumulées - Top 10

| Rang | Pays | Guérisons |
|---|---|---|
| 1 | Mainland China | 780 798 |
| 2 | Iran | 7 058 |
| 3 | Italy | 2 961 |
| 4 | Singapore | 1 324 |
| 5 | South Korea | 843 |

**Interpretation :** La Chine domine également les guérisons. L'Iran présente un nombre de guérisons relativement élevé par rapport à ses décès, ce qui peut refléter une définition différente du critère de "guérison" selon les pays, ou des délais de déclaration. Singapore et Vietnam affichent des taux de guérison remarquables rapportés à leur nombre de cas, ce qui traduit une gestion précoce et ciblée de la pandémie.

### 3.4 Analyse des boîtes à moustaches (boxplots)

Les boxplots sur les top 5 pays permettent de visualiser la **distribution des rapports journaliers** par pays, et non uniquement les totaux.

**Decisions methodologiques :**

1. **Pourquoi des boxplots ?** Les agrégations (sommes) masquent la variabilité interne. Un pays peut avoir un total élevé avec une progression régulière, ou avec un seul pic massif. Le boxplot révèle cette structure.

2. **Limitation identifiée :** Le code utilise `confirmed_by_country` (variable initialement définie sur les cas confirmés, puis réécrasée par les décès, puis par les guérisons) pour filtrer le top 5 dans chaque boxplot. Cela signifie que les trois boxplots utilisent en réalité le top 5 des pays par **guérisons** (dernière affectation), et non le top 5 cohérent avec la variable tracée. Ce bogue ne corrompt pas les données mais peut induire des comparaisons incohérentes.

**Correction recommandée :**

```python
# Calcul des tops une seule fois, chacun sur sa propre variable
top5_confirmed = df.groupby("Country/Region")["Confirmed"].sum().nlargest(5).index
top5_deaths = df.groupby("Country/Region")["Deaths"].sum().nlargest(5).index
top5_recovered = df.groupby("Country/Region")["Recovered"].sum().nlargest(5).index

# Puis utiliser la variable appropriée dans chaque boxplot
df[df["Country/Region"].isin(top5_confirmed)].boxplot(column="Confirmed", by="Country/Region")
df[df["Country/Region"].isin(top5_deaths)].boxplot(column="Deaths", by="Country/Region")
df[df["Country/Region"].isin(top5_recovered)].boxplot(column="Recovered", by="Country/Region")
```

---

## 4. Evolution temporelle

### 4.1 Courbes cumulatives

```
Date         Confirmés   Décès   Guéris
2020-02-28    84 124     2 872   36 711
2020-03-01    88 371     2 996   42 716
2020-03-04    95 124     3 254   51 171
2020-03-08   109 835     3 803   60 695
```

Le graphique temporel trace l'évolution **cumulée** des trois indicateurs. La courbe des confirmés est en croissance quasi-exponentielle à partir de fin février, ce qui correspond à la propagation de la pandémie hors de Chine. La courbe des guérisons rattrape progressivement les confirmés, signe que la Chine était en phase de récupération tandis que les nouveaux foyers s'installaient en Europe et en Iran.

**Limitation du graphique actuel :** Comme les données sont cumulatives, la courbe ne peut que croître ou stagner. Elle ne permet pas de détecter les accélérations ou ralentissements. L'ajout d'une courbe de **nouveaux cas quotidiens** (delta) est nécessaire pour une lecture épidémiologique correcte.

### 4.2 Nouveaux cas quotidiens (ajout recommandé)

| Date | Nouveaux cas | Nouveaux décès | Nouvelles guérisons |
|---|---|---|---|
| 04/03/2020 | 2 280 | 94 | 2 942 |
| 05/03/2020 | 2 762 | 94 | 2 626 |
| 06/03/2020 | 3 914 | 112 | 2 069 |
| 07/03/2020 | 4 036 | 98 | 2 493 |
| 08/03/2020 | 3 999 | 245 | 2 336 |

**Interpretation :** Entre le 4 et le 8 mars 2020, les nouveaux cas quotidiens oscillent entre 2 280 et 4 036, avec une nette accélération entre le 5 et le 7 mars. Le pic de 245 nouveaux décès le 8 mars est particulièrement notable et reflète l'aggravation de la situation en Italie et en Iran. Le fait que les nouvelles guérisons (2 336 le 8 mars) restent inférieures aux nouveaux cas (3 999) indique que la pandémie était encore en phase de croissance à la fin de la période couverte.

```python
# Calcul des nouveaux cas quotidiens (ajout recommandé au notebook)
cases_by_date = df.groupby("ObservationDate")[["Confirmed", "Deaths", "Recovered"]].sum()
daily = cases_by_date.diff().rename(columns={
    "Confirmed": "Nouveaux_cas",
    "Deaths": "Nouveaux_deces",
    "Recovered": "Nouvelles_guerisons"
})

plt.figure(figsize=(12, 6))
plt.bar(daily.index, daily["Nouveaux_cas"], label="Nouveaux cas", alpha=0.7)
plt.plot(daily.index, daily["Nouveaux_deces"], color="red", label="Nouveaux décès", linewidth=2)
plt.title("Nouveaux cas et décès quotidiens (niveau mondial)")
plt.xlabel("Date")
plt.ylabel("Nombre")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

---

## 5. Matrice de corrélation

| | Confirmed | Deaths | Recovered |
|---|---|---|---|
| **Confirmed** | 1.000 | **0.987** | 0.859 |
| **Deaths** | 0.987 | 1.000 | **0.918** |
| **Recovered** | 0.859 | 0.918 | 1.000 |

**Interpretation :** Les trois variables sont très fortement corrélées entre elles. La corrélation Confirmed-Deaths (0.987) est quasi-parfaite : les pays qui ont le plus de cas confirmés ont aussi le plus de décès, ce qui est attendu. La corrélation Deaths-Recovered (0.918) est également élevée.

**Nuance importante :** Ces corrélations sont en grande partie **spurieuses** (artificielles), car elles reflètent avant tout la taille de l'épidémie dans chaque pays. La Chine, avec ses valeurs très élevées dans les trois colonnes, tire mécaniquement toutes les corrélations vers 1. Une analyse plus informative consisterait à calculer les **taux** (létalité, taux de guérison) plutôt que les valeurs brutes, puis à les corréler.

**Complement recommandé :**

```python
# Taux de létalité et de guérison par pays
country_stats = df.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered"]].sum()
country_stats = country_stats[country_stats["Confirmed"] > 100]  # filtrer les petits pays
country_stats["lethality_rate"] = country_stats["Deaths"] / country_stats["Confirmed"]
country_stats["recovery_rate"] = country_stats["Recovered"] / country_stats["Confirmed"]

print(country_stats[["lethality_rate", "recovery_rate"]].sort_values("lethality_rate", ascending=False).head(10))
```

---

## 6. Indicateurs globaux au 8 mars 2020

| Indicateur | Valeur |
|---|---|
| Cas confirmés cumulés | 109 835 |
| Décès cumulés | 3 803 |
| Guérisons cumulées | 60 695 |
| **Taux de létalité brut** | **3.46 %** |
| **Taux de guérison brut** | **55.26 %** |
| Cas actifs (confirmés - décès - guéris) | 45 337 |

**Interpretation :** Au 8 mars 2020, environ 55 % des cas confirmés étaient considérés comme guéris, et 3,46 % avaient conduit à un décès. Ces chiffres doivent être interprétés avec prudence :

- Le taux de létalité de 3,46 % est un **taux de létalité des cas détectés** (*case fatality rate*, CFR), non un taux de mortalité sur l'ensemble de la population exposée. Il est biaisé vers le haut car les cas asymptomatiques ou bénins ne sont pas tous dépistés.
- Le taux de guérison dépend de la définition adoptée par chaque pays pour déclarer un patient "guéri" (test négatif, sortie d'hospitalisation, absence de symptômes, etc.).
- Ces chiffres sont fortement influencés par la Chine, qui représente la majorité des données.

---

## 7. Synthèse des forces et limites de l'analyse

### Forces

- La pipeline de nettoyage (conversion de types, dates, valeurs manquantes) est logique et documentée.
- L'analyse par pays (sommes, barres, boxplots) couvre bien les dimensions géographiques.
- La matrice de corrélation est incluse, ce qui est pertinent pour une exploration initiale.

### Limites identifiées et pistes d'amélioration

| Limitation | Impact | Correction proposée |
|---|---|---|
| Bogue de réaffectation de `confirmed_by_country` | Boxplots filtrés sur un mauvais top 5 | Calculer trois variables distinctes (`top5_confirmed`, `top5_deaths`, `top5_recovered`) |
| Graphique temporel uniquement cumulatif | Impossible de détecter les vagues | Ajouter un graphique de nouveaux cas quotidiens (`diff()`) |
| Corrélations sur valeurs brutes | Résultats triviaux, dominés par la Chine | Corréler les taux (létalité, guérison) après filtrage des petits pays |
| Aucun taux calculé dans le notebook | Comparaisons entre pays biaisées par la taille | Ajouter `lethality_rate` et `recovery_rate` par pays |
| `fillna(inplace=True)` sur colonne isolée | Avertissement pandas (Copy-on-Write) | Remplacer par `df["col"] = df["col"].fillna(...)` |
| `SNo` non exclu explicitement de `describe()` | Statistiques légèrement imprécises dans l'affichage | Le code le gère avec `df.loc[:, df.columns != "SNo"]`, c'est correct |
