# Ricostruisci procedure

Una skill Codex e una CLI Python per descrivere un workflow di un sito o di un'app e verificare se una tua implementazione riproduce gli esiti osservati.

1. **Studia** il flusso con schermate, registrazioni, manuali o codice che puoi consultare. Annota azione, esito e fonte in un file JSON.
2. **Genera la specifica** e usala come brief per costruire il tuo workflow. [Schema delle osservazioni](SKILL.md)
3. **Verifica** la nuova implementazione con gli stessi scenari e registra gli esiti in un secondo JSON. Riusa gli ID dei passi e cita le fonti della nuova prova.

## Prova locale

Servono Python 3.9 o superiore e il contenuto del repository.

```bash
python3 scripts/workflow.py specifica examples/ordini.json > specifica.md
python3 scripts/workflow.py confronta examples/ordini.json examples/ordini.json
```

Il secondo comando confronta il campione fittizio con sé stesso. Stampa due esiti conformi. Per provare una differenza, copia il JSON in un altro file, cambia un campo `esito` e passa la copia come secondo argomento.

Il confronto usa gli esiti osservati con lo stesso `id` e normalizza gli spazi. Usa lo stesso vocabolario nei due file, per esempio `Il menu include CSV`. Gli esiti diversi o senza una corrispondente osservazione producono codice di uscita 1. Gli ID aggiuntivi sono informativi. Gli input non validi producono codice 2.

L'osservazione e l'implementazione si svolgono fuori dalla CLI. I comandi lavorano sui JSON locali e scrivono i report su standard output. Il [prompt operativo](references/prompt.md) guida il lavoro con Codex.
