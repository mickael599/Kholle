# 🎓 Tuteur Socratique MPSI (Streamlit + Gemini)

Un assistant pédagogique IA conçu spécialement pour les élèves de classes préparatoires **MPSI (Maths Sup)**. Il applique rigoureusement la **méthode socratique** : il ne donne jamais la réponse ni le calcul rédigé, mais guide l'élève pas à pas à travers des questions d'orientation, des vérifications de rigueur et des rappels méthodologiques.

---

## ✨ Fonctionnalités clés

1. **Multimodal (Vision & PDF)** :
   - Prise de photo directe via smartphone/webcam de l'énoncé ou du tableau.
   - Importation d'images (PNG, JPG) ou de polycopiés de TD/DM en PDF.
2. **Support des brouillons & calculs manuscrits** :
   - En cours d'exercice, l'élève peut photographier ses calculs sur feuille pour que le colleur vérifie sa démarche et pointe l'erreur sans la corriger à sa place.
3. **Boutons tactiles d'action rapide** :
   - 💡 *Indice suivant* (distille une indication de niveau supérieur)
   - 📖 *Rappel de cours* (théorème ou définition précis)
   - 🔎 *Vérifie ma démarche* (analyse la rigueur formelle : quantificateurs, hypothèses)
   - ✅ *J'ai trouvé la solution !* (validation du résultat et fiche réflexe)
4. **Moteur Gemini 2.0 & 1.5** :
   - Utilise le nouveau SDK officiel `google-genai` avec streaming en direct.
   - Formules mathématiques rendues en LaTeX pur ($...$ et $$...$$).
5. **Ergonomie Mobile-First** :
   - Accessible sur smartphone via le Wi-Fi local.

---

## 🚀 Démarrage en 1 clic

### Option 1 : Double-cliquer sur le lanceur
Double-cliquez simplement sur le fichier **`lancer.bat`**.

### Option 2 : Ligne de commande
```bash
# Dans le dossier tuteur-mpsi :
.venv\Scripts\streamlit run tuteur_mpsi.py --server.address 0.0.0.0 --server.port 8501
```

---

## 🔑 Clé API Gemini

Pour utiliser l'application :
1. Obtenez une clé API gratuite sur [Google AI Studio](https://aistudio.google.com).
2. Deux façons de la renseigner :
   - Directement dans le **menu latéral gauche** de l'application Streamlit.
   - Ou dans le fichier `.streamlit/secrets.toml` :
     ```toml
     GEMINI_API_KEY = "votre_cle_ici"
     ```

---

## 📱 Utilisation sur Smartphone (même Wi-Fi)

1. Lancez l'application avec `lancer.bat`.
2. Sur votre smartphone connecté au même réseau Wi-Fi, ouvrez votre navigateur web à l'adresse indiquée par Streamlit (ex: `http://192.168.x.x:8501`).
3. Vous pouvez directement utiliser l'appareil photo du téléphone pour shooter vos feuilles d'exercices et vos brouillons !
