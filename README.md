# first-agent

Progetto didattico per capire come funziona un agente AI costruendolo **da zero in Python**, senza framework, prima di passare a LangChain.

L'agente usa un modello linguistico tramite [OpenRouter](https://openrouter.ai) e può chiamare degli strumenti (tool) per ottenere informazioni che il modello da solo non conosce.

## Cosa dimostra

- **Tool calling**: il modello decide quando usare uno strumento e con quali argomenti
- **Ciclo agentico**: l'agente continua a chiamare tool finché non ha tutto ciò che gli serve per rispondere
- **Composizione di tool**: alla domanda *"Quanti giorni mancano a Natale?"* l'agente recupera prima la data di oggi e poi calcola la differenza, in tre iterazioni, senza che la sequenza sia scritta nel codice
- **Conversazione come lista di messaggi** con i ruoli `system`, `user`, `assistant` e `tool`

## Struttura

| File | Contenuto |
|---|---|
| `main.py` | La chiamata base al modello, senza tool |
| `agent.py` | L'agente completo con ciclo e tool |

## Tool disponibili

- `get_current_datetime`: restituisce giorno della settimana, data e ora correnti
- `days_between_dates`: calcola i giorni tra due date

## Requisiti

- Python 3.10 o superiore
- Una chiave API di OpenRouter

## Installazione

```bash
git clone https://github.com/FontaMatte/first-agent.git
cd first-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copia `.env.example` in `.env` e inserisci la tua chiave:

```
OPENROUTER_API_KEY=la-tua-chiave
```

## Utilizzo

```bash
python agent.py
```

La domanda dell'utente si modifica nella lista `messages` in `agent.py`.

## Roadmap

- [x] Fase 0: chiamata base al modello
- [x] Fase 1: agente costruito a mano, con ciclo e tool
- [ ] Fase 2: lo stesso agente con LangChain
- [ ] Fase 3: memoria della conversazione
- [ ] Fase 4: RAG su documenti
- [ ] Fase 5: agente su database MySQL
- [ ] Fase 6: interfaccia web