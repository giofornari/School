/**
 * 
 */

/**
 * Classe main di test per la verifica delle corrette funzionalità
 * @param args
 * @author giordii.dev
 */
public class Main {

	/**
	 * Entry point del programma
	 * @param args
	 */
	public static void main(String[] args) {
		SchedaSim mySim = new SchedaSim("3348330252", 24.35);
		System.out.println(mySim.toString());
		Telefonata call1 = new Telefonata(12.0, "3534356163", "in");
		mySim.addTelefonata(call1);
		Telefonata call2 = new Telefonata(4.0, "3534356163", "out");
		mySim.addTelefonata(call2);
		Telefonata call3 = new Telefonata(5.0, "3534356467", "out");
		mySim.addTelefonata(call3);
		System.out.println("Credito = " + mySim.getCredit());
		mySim.addCredit(-1.0);
		System.out.println("Credito = " + mySim.getCredit());
		System.out.println("Last Call = " + mySim.getLastCall());
		System.out.println("In = " + mySim.getTot_min_in() + " minuti \nOut = " + mySim.getTot_min_out() + " minuti");
		
		
	}

}
