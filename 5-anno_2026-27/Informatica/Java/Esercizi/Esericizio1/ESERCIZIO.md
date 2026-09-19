costo noleggio è dichiarato astratto perchè dipende strettamente dal tipo di strumento che si vuole noleggiare.
ogni sottoclasse deve quindi definire la logica di costo noleggio, propria per ogni tipo di strumento.
per info() non deve essere cosi perchè le informazioni su uno strumento generale possono e dovrebbero esistere. inoltre, in questo modo per ogni strumento possiamo ereditare i campi standard da fornire allo strumento e limitarci all'aggiunta dei attrb specifici per il tipo di strumento definito nella sottoclasse.
