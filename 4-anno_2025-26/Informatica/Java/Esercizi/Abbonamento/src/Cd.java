
public class Cd {
	private String titolo;
	private String autore;
	private int n_brani;
	private double durata;
	/**
	 * @param titolo
	 * @param autore
	 * @param n_brani
	 * @param durata
	 */
	public Cd(String titolo, String autore, int n_brani, double durata) {
		super();
		this.titolo = titolo;
		this.autore = autore;
		this.n_brani = n_brani;
		this.durata = durata;
	}
	/**
	 * @return the titolo
	 */
	public String getTitolo() {
		return titolo;
	}
	/**
	 * @param titolo the titolo to set
	 */
	public void setTitolo(String titolo) {
		this.titolo = titolo;
	}
	/**
	 * @return the autore
	 */
	public String getAutore() {
		return autore;
	}
	/**
	 * @param autore the autore to set
	 */
	public void setAutore(String autore) {
		this.autore = autore;
	}
	/**
	 * @return the n_brani
	 */
	public int getN_brani() {
		return n_brani;
	}
	/**
	 * @param n_brani the n_brani to set
	 */
	public void setN_brani(int n_brani) {
		this.n_brani = n_brani;
	}
	/**
	 * @return the durata
	 */
	public double getDurata() {
		return durata;
	}
	/**
	 * @param durata the durata to set
	 */
	public void setDurata(double durata) {
		this.durata = durata;
	}
	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("╭╶╶╶╶╶╶╶╶ Cd ╶╶╶╶╶╶╶╶╶╶╶╶┒\n┆ - titolo --> ");
		builder.append(titolo);
		builder.append(" \n┆ - autore --> ");
		builder.append(autore);
		builder.append(" \n┆ - n_brani --> ");
		builder.append(n_brani);
		builder.append(" \n┆ - durata --> ");
		builder.append(durata);
		builder.append("\n╰╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶╶┚");
		return builder.toString();
	}

}
