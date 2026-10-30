/**
 * The Class Main.
 * 
 * @author giordii.dev
 */

public class Main {

	/**
	 * The main method.
	 *
	 * @param args the arguments
	 */
	public static void main(String[] args) {

		Prodotto acqua = new Prodotto("acqua", 100, 0.70);
		Prodotto spritz = new Prodotto("spritz", 100, 1.2);
		Prodotto snack = new Prodotto("snack", 100, 2.50);
		Prodotto croccantelle = new Prodotto("croccantelle", 100, 0.50);
		Prodotto brioche = new Prodotto("brioche", 100, 0.70);

		MacchinaDistributrice Argenta = new MacchinaDistributrice();
		Argenta.aggingiProdotto(acqua);
		Argenta.aggingiProdotto(brioche);
		Argenta.aggingiProdotto(spritz);
		Argenta.aggingiProdotto(croccantelle);
		Argenta.aggingiProdotto(snack);
		System.out.println("\n\n\t Benvenuto!\n  Macchina Distributrice 1.0.0\n------------------------------------\n");
		System.out.println(Argenta.toString());
		System.out.println("\n\nAcquistiamo alcuni prodotti....\nmhhh....\nVoglio uno snack!\nControlliamo ci sia!");
		System.out.println(snack.toString());
		Argenta.acquistaProdotto("snack");
		System.out.println("\nBene!\nSono sicuro che sarà delizioso!\n\n\nManca qualcosa da bere!\nPrendiamo uno sprits!");
		Argenta.acquistaProdotto("spritz");
		System.out.println("\n OH LA!\nAdesso sono a posto");
		System.out.println("\n\n\n\t A FEW MOMENTS LATER...\n");
		System.out.println("Admin: Voglio controllare alcuni dati. Facciamo una query!\n");
		System.out.println(Argenta.toString());
		System.out.println("Il totale dei prodotti rimanenti è: " + Argenta.totale() + " €");

	}
}