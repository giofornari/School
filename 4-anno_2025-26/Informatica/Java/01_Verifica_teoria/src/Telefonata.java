/**
 * Classe per la gestione dellle caratterisitche di ogni telefonata
 * @author giordii.dev
 */

public class Telefonata {
	private double duration;
	private String num_called;
	private boolean in_or_out;
	/**
	 * @param duration
	 * @param num_called
	 * @param in_or_out
	 */
	public Telefonata(double duration, String num_called, String in_or_out) {
		this.duration = duration;
		this.num_called = num_called;
		this.in_or_out = "out".equals(in_or_out) ? true : false;
	}
	
	/**
	 * @return la durata della chiamata effettuata
	 */
	public double getDuration() {
		return duration;
	}
	/**
	 * Setter per modificare la durata della chiamata
	 * @param duration nuova durata
	 */
	public void setDuration(double duration) {
		this.duration = duration;
	}
	/**
	 * Getter per ottenere il numero chiamato
	 * @return the num_called
	 */
	public String getNum_called() {
		return num_called;
	}
	/**
	 * Setter per modificare la durata della chiamata
	 * @param num_called nuovo numero chiamato
	 */
	public void setNum_called(String num_called) {
		this.num_called = num_called;
	}
	/**
	 * Getter booleano per vedere se è in entrata o in uscita
	 * @return un valore booleano
	 */
	public boolean isIn_or_out() {
		return in_or_out;
	}
	/**
	 * Setter per scegliere se è in entrata o in uscita
	 * @param in_or_out "in" oppure "out"
	 */
	public void setIn_or_out(String in_or_out) {
		this.in_or_out = "out".equals(in_or_out) ? true : false;
	}
	
}