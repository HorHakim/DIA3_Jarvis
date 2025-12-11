# DIA3_Jarvis

Assistant conversationnel "Jarvis" (persona mafieuse) accessible en terminal, via une interface web Streamlit ou en bot Discord. S'appuie sur l'API Groq pour interroger différents modèles de langage (liste dans `config.py`).

## Prérequis
- Python 3.10+ recommandé
- Compte Groq avec clé API (`GROQ_KEY`)
- (Optionnel) Token Discord bot (`DISCORD_TOKEN`) si vous utilisez le bot

## Installation
1) Cloner le dépôt et se placer dedans  
2) Créer un environnement virtuel et l'activer :
   - macOS/Linux : `python3 -m venv .venv && source .venv/bin/activate`
   - Windows (PowerShell) : `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
3) Installer les dépendances : `pip install -r requirements.txt`
4) Copier le fichier `env.example` en `.env` et renseigner vos clés.

## Configuration
Variables à définir dans `.env` :
- `GROQ_KEY` : clé API Groq (obligatoire)
- `DISCORD_TOKEN` : token du bot Discord (optionnel si vous n'utilisez pas Discord)

Les modèles disponibles pour l'UI Streamlit sont listés dans `config.py` (`LLM_MODELS`). Vous pouvez les adapter selon vos accès Groq.

## Utilisation
### 1) Mode terminal
```
python conversation_agent.py
```
Entrez vos messages. Tapez `exit` pour quitter.

### 2) Interface web (Streamlit)
```
streamlit run frontend.py
```
Ouvre une interface chat avec historique et sélection du modèle.

### 3) Bot Discord
```
python discord_bot.py
```
- Le bot enregistre une commande slash `/ask`.
- Si les commandes n'apparaissent pas, redémarrez Discord (Ctrl+R) côté client.

## Notes
- Les réponses Discord sont tronquées à 2000 caractères pour respecter la limite.
- L'historique de conversation est conservé en mémoire pendant l'exécution (non persistant).
- Le prompt système (persona Jarvis) est défini dans `context.txt`.