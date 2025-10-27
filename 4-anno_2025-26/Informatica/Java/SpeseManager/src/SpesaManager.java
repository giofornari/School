import java.util.ArrayList;

public class SpesaManager {
	private final ArrayList<Spese> spese;

	public SpesaManager() {
		spese = new ArrayList<>();
	}

	public void addSpesa(Spese spesa) {
		spese.add(spesa);
	}

	public ArrayList<Spese> getSpese() {
		return spese;
	}

	public double spesaTotale() {
		double totale = 0;
		for (Spese spesa : spese) {
			totale += spesa.getMoneyyy();
		}
		return totale;
	}

	public double spesaMedia() {
		return spese.isEmpty() ? 0 : spesaTotale() / spese.size();
	}

	public double spesaMax() {
		if (spese.isEmpty()) {
			return 0;
		}
		double max = spese.get(0).getMoneyyy();
		for (Spese spesa : spese) {
			if (spesa.getMoneyyy() > max) {
				max = spesa.getMoneyyy();
			}
		}
		return max;
	}

	public double spesaMin() {
		if (spese.isEmpty()) {
			return 0;
		}
		double min = spese.get(0).getMoneyyy();
		for (Spese spesa : spese) {
			if (spesa.getMoneyyy() < min) {
				min = spesa.getMoneyyy();
			}
		}
		return min;
	}

	private ArrayList<String> getCategory() {
		ArrayList<String> categories = new ArrayList<>();
		for (Spese spesa : spese) {
			String category = spesa.getCategory();
			if (!categories.contains(category)) {
				categories.add(category);
			}
		}
		return categories;
	}

	private ArrayList<String> getPayMethod() {
		ArrayList<String> methods = new ArrayList<>();
		for (Spese spesa : spese) {
			String method = spesa.getPayMethod();
			if (!methods.contains(method)) {
				methods.add(method);
			}
		}
		return methods;
	}

	private double spesaMediaPerCategoria(String categoria) {
		double totale = 0;
		int count = 0;
		for (Spese spesa : spese) {
			if (spesa.getCategory().equals(categoria)) {
				totale += spesa.getMoneyyy();
				count++;
			}
		}
		return count == 0 ? 0 : totale / count;
	}

	private double spesaTotPerPayMethod(String method) {
		double totale = 0;
		for (Spese spesa : spese) {
			if (spesa.getPayMethod().equals(method)) {
				totale += spesa.getMoneyyy();
			}
		}
		return totale;
	}

	public String calcolaPayMethodMaggiore() {
		ArrayList<String> methods = this.getPayMethod();
		if (methods.isEmpty()) {
			return "";
		}
		String migliore = methods.get(0);
		double totaleMigliore = this.spesaTotPerPayMethod(migliore);
		for (String metodo : methods) {
			double totaleMetodo = this.spesaTotPerPayMethod(metodo);
			if (totaleMetodo > totaleMigliore) {
				migliore = metodo;
				totaleMigliore = totaleMetodo;
			}
		}
		return migliore;
	}

	public String calcolaPayMethodMinore() {
		ArrayList<String> methods = this.getPayMethod();
		if (methods.isEmpty()) {
			return "";
		}
		String peggiore = methods.get(0);
		double totalePeggiore = this.spesaTotPerPayMethod(peggiore);
		for (String metodo : methods) {
			double totaleMetodo = this.spesaTotPerPayMethod(metodo);
			if (totaleMetodo < totalePeggiore) {
				peggiore = metodo;
				totalePeggiore = totaleMetodo;
			}
		}
		return peggiore;
	}

	public String calcolaCategoriaMaggiore() {
		ArrayList<String> categorie = this.getCategory();
		if (categorie.isEmpty()) {
			return "";
		}
		String migliore = categorie.get(0);
		double mediaMigliore = this.spesaMediaPerCategoria(migliore);
		for (String categoria : categorie) {
			double mediaCategoria = this.spesaMediaPerCategoria(categoria);
			if (mediaCategoria > mediaMigliore) {
				migliore = categoria;
				mediaMigliore = mediaCategoria;
			}
		}
		return migliore;
	}

	public String calcolaCategoriaMinore() {
		ArrayList<String> categorie = this.getCategory();
		if (categorie.isEmpty()) {
			return "";
		}
		String peggiore = categorie.get(0);
		double mediaPeggiore = this.spesaMediaPerCategoria(peggiore);
		for (String categoria : categorie) {
			double mediaCategoria = this.spesaMediaPerCategoria(categoria);
			if (mediaCategoria < mediaPeggiore) {
				peggiore = categoria;
				mediaPeggiore = mediaCategoria;
			}
		}
		return peggiore;
	}
}
