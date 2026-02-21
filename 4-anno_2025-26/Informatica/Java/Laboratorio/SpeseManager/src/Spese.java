
import java.time.LocalDate;

/**
 * La classe {@code Spese} rappresenta una singola spesa con attributi relativi alla data,
 * importo, categoria e metodo di pagamento.
 * @author giordii.dev
 */
public class Spese {
    private LocalDate date;
    private double amount;
    private String category;
    private String payMethod;

    /**
     * Costruttore completo per l'inizializzazione completa degli oggetti.
     * @param category categoria della spesa
     * @param date data della spesa
     * @param amount importo della spesa
     * @param payMethod metodo di pagamento
     */
    public Spese(String category, LocalDate date, double amount, String payMethod) {
        this.category = category;
        this.date = date;
        this.amount = amount;
        this.payMethod = payMethod;
    }

    /**
     * Costruttore senza Date per spese incognite
     * @param amount importo della spesa
     * @param category categoria della spesa
     * @param payMethod metodo di pagamento
     */
    public Spese(double amount, String category, String payMethod) {
		this.amount = amount;
		this.category = category;
		this.payMethod = payMethod;
	}

	// getter e setter
    public void setDate(LocalDate date) {
        this.date = date;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public void setPayMethod(String payMethod) {
        this.payMethod = payMethod;
    }

    public double getAmount() {
        return amount;
    }

    public String getCategory() {
        return category;
    }

    public String getPayMethod() {
        return payMethod;
    }

    @Override
	public String toString() {
		return "Spese [date=" + date + ", amount=" + amount + ", category=" + category + ", payMethod=" + payMethod
				+ "]";
	}

    /**
     * Metodo per applicare l'iva alle spese con scontrino
     * @return Spesa+iva 22%
     */
    public double applicaIva() {
        return this.amount * 1.22;
    }
}
