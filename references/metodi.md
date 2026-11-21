# Metodi per ricostruire un workflow

## Software e interfaccia

Usa l'analisi statica per ricavare candidati da manuali, schermate, codice autorizzato e configurazioni di esempio. Usa l'analisi dinamica per verificare gli stati nell'interfaccia ordinaria con dati di prova. Registra versione, ruolo e punto di partenza. Prova una variazione alla volta e registra le condizioni che cambiano l'esito. Un ramo nel codice suggerisce un'ipotesi. Un esito visto nella configurazione di prova documenta quella configurazione. [Awesome Reversing · Software](https://github.com/ReversingID/Awesome-Reversing/blob/master/software-reversing.md)

## Formati di esportazione

Confronta due esportazioni autorizzate ottenute cambiando un solo campo in ingresso. Annota struttura, tipi, valori vuoti, ordinamento e differenze. Per JSON e CSV usa parser standard. Per un formato binario di cui è disponibile una specifica, consulta la struttura con un parser dichiarativo come Kaitai Struct, se già disponibile. Cita il campione e la posizione del campo. [Awesome Reversing · Format](https://github.com/ReversingID/Awesome-Reversing/blob/master/format-reversing.md)

## Dati e schema

Quando disponi di un dump o di una copia SQLite autorizzata, lavora sulla copia in sola lettura. Leggi prima lo schema. Usa chiavi e vincoli dichiarati per formulare ipotesi sulle relazioni e verifica il comportamento visibile con dati di prova. Cita tabella e colonna. [Awesome Reversing · Database](https://github.com/ReversingID/Awesome-Reversing/blob/master/database-reversing.md)

Per una regola importante cerca riscontro tra percorso osservato e artefatto risultante. Se le fonti divergono, registra versioni e condizioni e lascia aperta la regola finché la discrepanza non è spiegata.
