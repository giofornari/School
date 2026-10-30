Classe quarta informatica – Itis Leonardo da Vinci PR
Verifica di Programmazione Orientata agli Oggetti (Java) – Ereditarietà e polimorfismo
Si intende modellare un sistema di gestione delle transazioni finanziarie che lega i metodi di pagamento agli utenti che li possiedono.
Parte A: Gerarchia dei Metodi di Pagamento (Ereditarietà & Override)
Tutti i metodi di pagamento sono caratterizzati da un identificativo univoco e un importo da pagare.
MetodoPagamento: Classe base che definisce le proprietà comuni. Deve includere un metodo per autorizzare la transazione e uno per calcolare la commissione sulla transazione.
CartaDiCredito: È un MetodoPagamento caratterizzato dal numero di carta (String) e dalla data di scadenza (String).
La commissione standard è fissa, pari al 2.0% dell'importo.
BonificoBancario: È un MetodoPagamento caratterizzato dall'IBAN del beneficiario (String).
La commissione è fissa, pari a 2.50 €, indipendentemente dall'importo.
CartaPremium: È un particolare tipo di CartaDiCredito che offre commissioni ridotte.
Deve ereditare da CartaDiCredito.
La commissione è ridotta all'1.5% dell'importo.
Compiti di Implementazione (Parte A)
Definire le classi in modo da sfruttare una classe astratta per MetodoPagamento.
Implementare in ogni classe il metodo autorizzaTransazione() (restituendo true se importo > 0 e stampando l'avviso di autorizzazione).
Implementare il metodo calcolaCommissione() in ogni classe risolvendo il calcolo con metodi in override, specializzando la logica (2.0%, 2.50 € fisso, 1.5%).
Sovrascrivere il metodo toString() per mostrare tutti i dettagli (incluso l'importo totale addebitato, che è importo + commissione.
Parte B: La Classe Utente (Composizione)
Definire la classe Utente che rappresenta un cliente del sistema.
Attributi: nome (String), idUtente (int).
Composizione: La classe Utente deve contenere un riferimento a un MetodoPagamento preferito.
Compiti di Implementazione (Parte B)
Costruttore: La classe Utente deve essere inizializzata con nome e idUtente. Il metodo di pagamento può essere impostato successivamente.
Metodo di Aggiornamento: Creare un metodo setMetodoPagamentoPreferito(MetodoPagamento mp) per assegnare il metodo.
Metodo di Pagamento: Creare un metodo effettuaPagamento(double importo, MetodoPagamento  mp  oppure null):
Se viene passato un MetodoPagamento come parametro, il pagamento viene effettuato con quello.
Se il parametro è null, il pagamento viene effettuato usando il MetodoPagamento preferito salvato nell'attributo dell'Utente.
Il metodo deve aggiornare l'importo del MetodoPagamento e chiamare il suo autorizzaTransazione().
Classe di Test (Main)
Codificare una classe Main che:
Istanzi due diversi metodi di pagamento (es. una CartaDiCredito e una CartaPremium).
Istanzi un oggetto Utente (es. "Marco Verdi").
Assegni la CartaDiCredito all'Utente come metodo preferito.
Esegua un pagamento di 500 € chiamando effettuaPagamento() senza specificare un metodo (usa il preferito).
Esegua un secondo pagamento di 100 € chiamando effettuaPagamento() specificando la CartaPremium come metodo temporaneo.
Stampi il risultato di tutte le transazioni.
Implementare una classe Transazioni dove memorizzare più utenti con relativo metodo per invocare il metodo effettuaPagamento() per tutti.