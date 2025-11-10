// TODO: Auto-generated Javadoc
/**
 * The Class Prodotto.
 */

public class Prodotto {
	
	/** The nome. */
	private String nome;
	
	/** The quantita. */
	private int quantita;
	
	/** The prezzo. */
	private double prezzo;

	/**
	 * Instanzia un nuovo prodotto.
	 *
	 * @param nome the nome
	 * @param quantita the quantita
	 * @param prezzo the prezzo
	 */
	public Prodotto(String nome, int quantita, double prezzo) {
		this.nome = nome;
		this.quantita = quantita;
		this.prezzo = prezzo;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public int getQuantita() {
		return quantita;
	}

	/**
	 * Sets the quantita.
	 *
	 * @param quantita the new quantita
	 */
	public void setQuantita(int quantita) {
		this.quantita = quantita;
	}

	/**
	 * Riduce la quantita.
	 *
	 * @return true, if successful
	 */
	public boolean reduceQuantita() {
		if (this.quantita == 0) {
			return false;
		}
		this.quantita--;
		return true;
	}

	public double getPrezzo() {
		return prezzo;
	}

	public void setPrezzo(double prezzo) {
		this.prezzo = prezzo;
	}
	/**
	 * Ritorna tutte le informazioni sul prodotto
	 * 
	 * @return a fancy overview
	 */
	@Override
	public String toString() {
		return "[ "+ nome.toUpperCase() + " - " + prezzo +  "€" + " - " + quantita +" rimanenti ]";
	}
	
}
