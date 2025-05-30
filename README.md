# NGine Archipelago Tools

Une application tout-en-un pour accompagner vos sessions **Archipelago Async**.

Ce logiciel propose plusieurs outils réunis dans une seule interface graphique :

---

## 🧩 Fonctions intégrées

### 1. **Log Splitter**
- 📄 Importez un spoiler log et générez automatiquement un fichier pour chaque joueur.
- ✅ Affiche les checks envoyés et reçus.
- 📁 Export dans un dossier choisi.

### 2. **Hatsune Miku Tracker**
- 🎵 Compare les musiques disponibles à celles déjà cochées dans un tracker CSV.
- 📊 Trie par catégorie de titres pour aider à votre progression.
- 🔁 À terme : synchronisation automatique avec un tracker personnalisé en ligne.

### 3. **Hint Manager**
- 🔍 Charge un fichier de hints CSV.
- 🧹 Peut filtrer les hints déjà trouvés.
- 📤 Exporte un résumé textuel pour partage Discord.
- 🔗 Prochainement : récupération directe via API Archipelago (WebSocket).

---

## 🚀 Installation

```bash
git clone https://github.com/votre-utilisateur/ngine-archipelago-tools.git
cd ngine-archipelago-tools
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python main.py
```

---

## 📦 Dépendances

- `pandas`
- `websocket-client`
- `tkinter` (inclus dans Python ≥ 3.7)

---

## 👤 Auteurs
Développé par Christophe Bonnefoi pour la communauté NaruGame’s.

---

## 📜 Licence
Projet personnel. Libre d’usage non commercial.