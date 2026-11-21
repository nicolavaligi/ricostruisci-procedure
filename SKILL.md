---
name: ricostruisci-procedure
description: Ricostruisce e documenta workflow funzionali di siti e app da osservazioni autorizzate, manuali, registrazioni o codice disponibile. Usa quando l'utente vuole capire, ripetere o migrare una procedura esistente.
---

Leggi [il prompt operativo](references/prompt.md) e applicalo allo scenario richiesto. Parti dalle fonti fornite e, se necessario, osserva il flusso tramite gli strumenti autorizzati. Per app desktop senza accesso diretto usa registrazioni, schermate o manuali. Registra anche il ruolo, la versione se nota e il punto fino al quale hai verificato direttamente il flusso.

Descrivi le alternative come passi applicabili alla relativa condizione o inseriscile tra i punti aperti. Fermati prima di effetti esterni privi di autorizzazione e registra l'ultimo stato osservabile.

Per una consegna Markdown ripetibile, prepara un JSON con questa struttura. Usa identificativi brevi e indica il punto preciso dell'evidenza nel valore di ogni fonte.

```json
{
  "titolo": "Esportazione ordini",
  "contesto": "Demo, ruolo operatore",
  "prerequisiti": ["Almeno un ordine di prova"],
  "fonti": {"V1": "Registrazione demo, 00:12"},
  "passi": [
    {"azione": "Seleziona Esporta", "esito": "Compare il formato CSV", "stato": "osservato", "fonti": ["V1"]}
  ],
  "punti_aperti": ["Comportamento senza ordini"],
  "verifica": "Esaminata la registrazione demo"
}
```

Gli stati ammessi sono `osservato`, `inferito` e `da verificare`. Le osservazioni e le inferenze richiedono almeno una fonte. Esegui `python3 scripts/render_procedura.py osservazioni.json` dalla cartella della skill e salva l'output dove richiesto. Controlla la coerenza dei passi con le evidenze prima della consegna.
