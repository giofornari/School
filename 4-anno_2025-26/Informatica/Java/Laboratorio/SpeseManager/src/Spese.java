
import java.time.LocalDate;

/**
 * La classe {@code Spese} rappresenta una singola spesa con attributi relativi alla data,
 * importo, categoria e metodo di pagamento.
 * @author giordii.dev
 */
public class Spese {
    private LocalDate date;
    private double Moneyyy;
    private String Category;
    private String PayMethod;

    /**
     * Costruttore completo per l'inizializzazione completa degli oggetti.
     * @param date data della spesa
     */

    public Spese(String Category, LocalDate date, double Moneyyy, String PayMethod) {
        this.Category = Category;
        this.date = date;
        this.Moneyyy = Moneyyy;
        this.PayMethod = PayMethod;
    }


    /**
     * Costruttore senza Date per spese incognite
     * @hidden per i soldi in nero :|
     */

    public Spese(double moneyyy, String category, String payMethod) {
		this.Moneyyy = moneyyy;
		this.Category = category;
		this.PayMethod = payMethod;
	}


	// getter e setter
    public void setDate(LocalDate date) {
        this.date = date;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setMoneyyy(double Moneyyy) {
        this.Moneyyy = Moneyyy;
    }

    public void setCategory(String Category) {
        this.Category = Category;
    }

    public void setPayMethod(String PayMethod) {
        this.PayMethod = PayMethod;
    }

    public double getMoneyyy() {
        return Moneyyy;
    }

    public String getCategory() {
        return Category;
    }

    public String getPayMethod() {
        return PayMethod;
    }

    @Override
	public String toString() {
		return "Spese [date=" + date + ", Moneyyy=" + Moneyyy + ", Category=" + Category + ", PayMethod=" + PayMethod
				+ "]";
	}

    /**
     * Metodo per applcare l'iva alle spese con scontrino
     * @return Spesa+iva 22%
     */
    public double applicaIva() {
        return this.Moneyyy * 1.22;
    }
}