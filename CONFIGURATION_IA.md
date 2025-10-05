# Configuration IA - Guide d'Utilisation

## Vue d'ensemble

VorkVoice intègre maintenant l'API Gemini de Google pour traiter vos transcriptions avec l'intelligence artificielle. Cette fonctionnalité vous permet d'envoyer votre texte transcrit à Gemini pour qu'il soit enrichi, reformulé, ou traité selon vos besoins.

## 🚀 Installation

### 1. Installer la bibliothèque Gemini

```bash
pip install google-generativeai
```

Ou installez toutes les dépendances avec :

```bash
pip install -r requirements.txt
```

### 2. Obtenir une clé API Gemini

1. Visitez [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Créez un nouveau projet ou sélectionnez-en un existant
3. Générez une clé API
4. Copiez votre clé API

## ⚙️ Configuration

### Ajouter une clé API

1. Ouvrez l'application VorkVoice
2. Cliquez sur le bouton **"⚙️ Dictionnaire"**
3. Sélectionnez l'onglet **"🤖 Configuration IA"**
4. Dans le champ "Clé API", collez votre clé API Gemini
5. (Optionnel) Donnez un nom à votre clé pour l'identifier
6. Cliquez sur **"➕ Ajouter"**

### Gérer plusieurs clés API

Vous pouvez ajouter plusieurs clés API. L'application choisira automatiquement la clé avec le meilleur taux de succès pour chaque requête.

### Sélectionner un modèle

Dans l'onglet "Configuration IA", utilisez le menu déroulant "Modèle Gemini" pour sélectionner le modèle à utiliser :

- **gemini-1.5-flash** : Rapide et efficace, idéal pour un usage quotidien
- **gemini-1.5-pro** : Plus puissant, pour des tâches complexes
- **gemini-1.0-pro** : Version stable

## 🎯 Utilisation

### Workflow standard

1. **Enregistrer** : Appuyez sur le raccourci clavier (par défaut `²`) pour démarrer l'enregistrement
2. **Parler** : Dictez votre texte
3. **Transcrire** : Cliquez sur **"🛑 Stop & Transcrire"**
4. **Traiter avec IA** : Cliquez sur **"🤖 Traiter avec IA"**
5. **Résultat** : Le texte traité par Gemini est copié dans votre presse-papiers

### Exemple d'utilisation

Vous pouvez dire :
> "Écris un email professionnel pour remercier mon client pour sa commande et lui confirmer la livraison dans 3 jours"

Après transcription, cliquez sur le bouton IA, et Gemini générera un email professionnel structuré basé sur votre demande.

## 📊 Monitoring de l'utilisation

L'application suit automatiquement :
- **Nombre total de requêtes** par clé API
- **Nombre de succès** pour évaluer la fiabilité
- **Erreurs récentes** pour diagnostiquer les problèmes

Ces statistiques sont visibles dans la table des clés API.

## ⚠️ Limites et Quotas

### Limites de l'API Gemini

- **Version gratuite** : Limites de requêtes par minute (RPM) et par jour
- **Taille des messages** : Maximum de tokens par requête (varie selon le modèle)
- **Quotas** : Peuvent être augmentés avec un compte payant

Consultez la [documentation officielle](https://ai.google.dev/gemini-api/docs/quotas) pour plus de détails.

### Gestion des erreurs

Si vous atteignez une limite :
- L'application affichera un message d'erreur
- L'erreur sera enregistrée dans les statistiques de la clé
- Vous pouvez ajouter une autre clé API pour contourner les limites

## 🔒 Sécurité et Confidentialité

- **Stockage local** : Les clés API sont stockées dans `~/.vorkvoice/ai_config.json`
- **Pas de partage** : Vos clés ne sont jamais envoyées à des services tiers
- **Chiffrement** : Les clés sont affichées masquées dans l'interface (ex: "AIzaSy...abc123")

⚠️ **Important** : Ne partagez jamais vos clés API publiquement.

## 🛠️ Dépannage

### La bibliothèque n'est pas installée

**Erreur** : `La bibliothèque google-generativeai n'est pas installée`

**Solution** :
```bash
pip install google-generativeai
```

### Aucune clé API configurée

**Erreur** : `Aucune clé API configurée`

**Solution** : Ajoutez une clé API dans les paramètres (voir "Configuration" ci-dessus)

### Erreur d'authentification

**Erreur** : `Invalid API key`

**Solution** :
1. Vérifiez que votre clé API est correcte
2. Assurez-vous que l'API Gemini est activée dans votre projet Google Cloud
3. Vérifiez que votre clé n'a pas expiré

### Dépassement de quota

**Erreur** : `Quota exceeded` ou `Rate limit`

**Solution** :
1. Attendez que votre quota se réinitialise
2. Ajoutez une autre clé API
3. Passez à un plan payant pour des quotas plus élevés

## 💡 Conseils d'utilisation

1. **Soyez précis** : Plus votre transcription est claire, meilleur sera le résultat de l'IA
2. **Testez différents modèles** : Chaque modèle a ses forces
3. **Surveillez vos quotas** : Gardez un œil sur vos statistiques d'utilisation
4. **Plusieurs clés** : Utilisez plusieurs clés pour éviter les limites

## 🔄 Fonctionnalités futures

- Raccourci clavier pour traitement IA automatique après transcription
- Personnalisation des prompts système
- Historique des traitements IA
- Templates de prompts prédéfinis

## 📚 Ressources

- [Documentation Gemini API](https://ai.google.dev/docs)
- [Obtenir une clé API](https://makersuite.google.com/app/apikey)
- [Limites et quotas](https://ai.google.dev/gemini-api/docs/quotas)
- [Modèles disponibles](https://ai.google.dev/models/gemini)
