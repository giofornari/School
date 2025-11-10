import java.util.ArrayList;

// TODO: Auto-generated Javadoc
/**
 * MacchinaDistributrice.
 * 
 * @author giordii.dev
 */

public class MacchinaDistributrice {

	/** i prodotti. */
	private ArrayList<Prodotto> prodotti;

	/**
	 * Crea una nuova macchina distributrice e inizialiazza l'arraylist.
	 *
	 */
	public MacchinaDistributrice() {
		this.prodotti = new ArrayList<Prodotto>();
	}

	/**
	 * Aggingi prodotto.
	 *
	 * @param p il p
	 */
	public void aggingiProdotto(Prodotto p) {
		this.prodotti.add(p);
	}

	/**
	 * Cerca il prodotto in base al nome.
	 *
	 * @param nomeProdotto il nome prodotto
	 * @return il prodotto
	 */
	public Prodotto cercaProdotto(String nomeProdotto) {
		for (Prodotto p : prodotti) {
			if (p.getNome().equals(nomeProdotto)) {
				return p;
			}
		}
		return null;
	}

	/**
	 * Rimuovi prodotto.
	 *
	 * @param nomeProdotto il nome del prodotto
	 */
	public void rimuoviProdotto(String nomeProdotto) {
		if (this.cercaProdotto(nomeProdotto) != null) {
			this.prodotti.remove(this.cercaProdotto(nomeProdotto));
		}
	}

	/**
	 * Acquista prodotto.
	 *
	 * @param nomeProdotto nome del prodotto
	 * @return true, if successful
	 */
	public boolean acquistaProdotto(String nomeProdotto) {
		return this.cercaProdotto(nomeProdotto).reduceQuantita();

	}

	/**
	 * Totale.
	 *
	 * @return il totale degli elementi per il loro prezzo.
	 */
	public double totale() {
		double totaleP = 0;
		for (Prodotto p : prodotti) {
			totaleP += p.getPrezzo() * p.getQuantita();
		}
		return totaleP;
	}

	/**
	 * To string.
	 *
	 * @return il string
	 */
	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("---- Prodotti rimanenti -------\n");
		for (int i = 0; i < prodotti.size(); i++) {
			Prodotto p = prodotti.get(i);
			builder.append(i + ") " + p.getNome() + ": " + p.getQuantita() + "\n");
		}
		builder.append("-------------------------------");
		return builder.toString();
	}

}