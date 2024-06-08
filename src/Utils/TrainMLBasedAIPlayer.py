import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

os.makedirs('src/Data', exist_ok=True)
os.makedirs('src/Model', exist_ok=True)

# Définir les chemins pour les données et le modèle
data_path = os.path.join('src', 'Data', 'data.csv')
model_path = os.path.join('src', 'Model', 'trained_model.pkl')

# Supposons que vous avez un fichier CSV 'game_data.csv' avec les données de jeu
# Les colonnes devraient inclure les caractéristiques de l'état du jeu et les actions correspondantes
data = pd.read_csv('../Data/data.csv')

# Séparation des caractéristiques (X) et de l'étiquette (y)
X = data.drop('action', axis=1)
y = data['action']

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraînement du modèle Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Évaluation du modèle
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')

# Sauvegarde du modèle entraîné
joblib.dump(model, model_path)
