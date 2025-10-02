# Dictionnaire Personnel - Guide d'Utilisation

## Vue d'ensemble

La fonctionnalité de dictionnaire personnel vous permet de créer et gérer vos propres remplacements de mots et expressions qui seront automatiquement appliqués lors de la transcription vocale.

## Accès à la fonctionnalité

Dans la fenêtre principale de dictée vocale, cliquez sur le bouton **⚙️ Dictionnaire** pour ouvrir l'interface de gestion du dictionnaire personnel.

## Utilisation

### Ajouter un nouveau remplacement

1. Dans la fenêtre "Paramètres - Dictionnaire personnel"
2. Entrez le texte source dans le champ "De:" (par exemple : "Maya")
3. Entrez le texte de remplacement dans le champ "Vers:" (par exemple : "Maïa")
4. Cliquez sur le bouton **➕ Ajouter**
5. Le remplacement est immédiatement actif pour toutes les futures transcriptions

### Supprimer un remplacement

1. Dans la table "Vos remplacements personnalisés"
2. Trouvez le remplacement que vous souhaitez supprimer
3. Cliquez sur le bouton **🗑️ Supprimer** correspondant
4. Confirmez la suppression dans la boîte de dialogue

### Modifier un remplacement existant

Pour modifier un remplacement :
1. Supprimez l'ancien remplacement
2. Ajoutez un nouveau remplacement avec les valeurs mises à jour

Ou bien :
1. Ajoutez un nouveau remplacement avec le même texte source
2. Le système vous demandera si vous voulez remplacer l'existant

## Exemples d'utilisation

### Correction de noms propres
- **De:** "Maya" → **Vers:** "Maïa"
- **De:** "Jean francois" → **Vers:** "Jean-François"

### Correction de ponctuation
- **De:** "estce que" → **Vers:** "est-ce que"
- **De:** "Estce" → **Vers:** "Est-ce"

### Acronymes et abréviations
- **De:** "chaque GPT" → **Vers:** "ChatGPT"
- **De:** "API" → **Vers:** "interface de programmation"

### Suppression de textes parasites
- **De:** "Sous-titrage Société Radio-Canada" → **Vers:** "" (vide)
- **De:** "euh" → **Vers:** ""

### Expressions complètes
- **De:** "1000000" → **Vers:** "un million"
- **De:** "comment allez vous" → **Vers:** "comment allez-vous"

## Priorité des remplacements

- **Les remplacements personnalisés ont la priorité** sur les remplacements par défaut du système
- Si un mot apparaît dans votre dictionnaire personnel ET dans les remplacements par défaut, votre version sera utilisée

## Stockage

Vos remplacements personnalisés sont sauvegardés dans le fichier :
```
~/.vorkvoice/user_mappings.json
```

Ce fichier est automatiquement créé lors de l'ajout de votre premier remplacement.

## Format du fichier

Le fichier JSON contient une liste de paires [source, remplacement] :

```json
[
  ["Maya", "Maïa"],
  ["chaque GPT", "ChatGPT"],
  ["estce que", "est-ce que"]
]
```

Vous pouvez éditer ce fichier directement si nécessaire, mais il est recommandé d'utiliser l'interface graphique.

## Conseils d'utilisation

1. **Testez vos remplacements** : Faites quelques tests de transcription après avoir ajouté des remplacements
2. **Soyez spécifique** : Plus votre texte source est spécifique, moins il y a de risque de remplacements non désirés
3. **Ordre des remplacements** : Les remplacements utilisateur sont appliqués avant les remplacements par défaut
4. **Sensibilité à la casse** : Les remplacements sont sensibles à la casse (majuscules/minuscules)

## Dépannage

### Les remplacements ne s'appliquent pas

- Vérifiez que le texte source correspond exactement au texte transcrit (casse, espaces, ponctuation)
- Relancez le serveur de transcription pour s'assurer qu'il charge les nouveaux mappings
- Vérifiez que le fichier `~/.vorkvoice/user_mappings.json` existe et contient vos remplacements

### Impossible d'ajouter un remplacement

- Assurez-vous que les champs "De" et "Vers" ne sont pas vides
- Vérifiez qu'il n'y a pas d'erreurs dans les permissions du dossier `~/.vorkvoice/`

### Le fichier de configuration est corrompu

Si le fichier JSON est corrompu :
1. Supprimez le fichier `~/.vorkvoice/user_mappings.json`
2. Relancez l'application
3. Ajoutez à nouveau vos remplacements

## Support

Pour plus d'aide ou pour signaler des problèmes, veuillez ouvrir une issue sur le dépôt GitHub du projet.
