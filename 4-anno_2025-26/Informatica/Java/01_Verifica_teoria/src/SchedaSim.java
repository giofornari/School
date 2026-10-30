/**
 * Classe per la gestione della scheda sim
 * @author giordii.dev
 */
public class SchedaSim {
	private String num_tel; // numero personale
	private double credit; // credito a disposizione
	private final double PRICEPERMIN = 0.45; // costo al minuto
	private double tot_min_in; // totale dei minuti in entrata
	private double tot_min_out; // totale minuti in uscita
	private String lastCall;
	
	/**
	 * Costruttore per la sim
	 * @param num_tel numero di telefono personale
	 * @param credit credito iniziale
	 */
	public SchedaSim(String num_tel, double credit) {
		this.num_tel = num_tel;
		this.credit = credit;
	}
		
	/**
	 * @return il proprio numero di telefono
	 */
	public String getNum_tel() {
		return num_tel;
	}
	/**
	 * @return il credito rimanente
	 */
	public double getCredit() {
		return credit;
	}

	/**
	 * @param credit il credito da aggiungere
	 */
	public void addCredit(double credit) {
		this.credit += credit;
	}
	/**
	 * @return totale minuti in entrata
	 */
	public double getTot_min_in() {
		return tot_min_in;
	}
	/**
	 * @return totale minuti in uscita
	 */
	public double getTot_min_out() {
		return tot_min_out;
	}
	/**
	 * @return il costo fisso al minuto
	 */
	public double getPRICEPERMIN() {
		return PRICEPERMIN;
	}
	
	/**
	 * @return l'ultima chiamata
	 */
	public String getLastCall() {
		return lastCall;
	}

	@Override
	public String toString() {
		return "\n\t SchedaSim \n --------------------------- \n - num_tel= +39 " + num_tel + "\n - credit=" + credit + "$\n - PRICEPERMIN=" + PRICEPERMIN + "$\n - tot_min_in="
				+ tot_min_in + " minutes \n - tot_min_out=" + tot_min_out + "minutes \n---------------------------\n\n";
	}

	/**
	 * Aggiorna i dati della scheda sim in base alle caratteristiche della telefonata
	 * @param telefonata l'oggetto telefonata (contenente il numero chiamato)
	 */
	public void addTelefonata(Telefonata telefonata) {
		this.lastCall = telefonata.getNum_called();
		if (telefonata.isIn_or_out()) {
			this.tot_min_out += telefonata.getDuration();
			this.credit -= telefonata.getDuration() * PRICEPERMIN;
		} else {
			this.tot_min_in += telefonata.getDuration();
		}
	}

}
