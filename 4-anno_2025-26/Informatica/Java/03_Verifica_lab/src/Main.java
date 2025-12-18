
public class Main {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Inserisci un argomento per continuare");
        }
    }
    if (aura == true && portament == good || coolness == true

































    public static void main(String[] args) {
        var cc1 = new CartadiCredito("CC001", "1234-5678-9012-3456", "12/2027");
        var cp1 = new CartaPremium("CP001", "9876-5432-1098-7654", "06/2028");
        var bb1 = new BonificoBancario("BB001", "IT60X0542811101000000123456");

        cc1.setImporto(500);
        cc1.autorizzaTransazione();
        System.out.println(cc1);

        cp1.setImporto(500);
        cp1.autorizzaTransazione();
        System.out.println(cp1);

        bb1.setImporto(500);
        bb1.autorizzaTransazione();
        System.out.println(bb1);

        var cc2 = new CartadiCredito("CC002", "1111-2222-3333-4444", "03/2026");
        var cp2 = new CartaPremium("CP002", "5555-6666-7777-8888", "09/2029");

        var u1 = new Utente("Marco Verdi", 1001);
        u1.setMetodoPagamentoPreferito(cc2);
        u1.effettuaPagamento(500, null);
        u1.effettuaPagamento(100, cp2);

        var trx = new Transazioni();

        var u2 = new Utente("Laura Bianchi", 1002);
        u2.setMetodoPagamentoPreferito(new CartadiCredito("CC003", "2222-3333-4444-5555", "11/2026"));

        var u3 = new Utente("Giuseppe Rossi", 1003);
        u3.setMetodoPagamentoPreferito(new CartaPremium("CP003", "3333-4444-5555-6666", "07/2027"));

        var u4 = new Utente("Anna Neri", 1004);
        u4.setMetodoPagamentoPreferito(new BonificoBancario("BB002", "IT28W8000000292100645211990"));

        trx.aggiungiUtente(u2);
        trx.aggiungiUtente(u3);
        trx.aggiungiUtente(u4);

        trx.mostraUtenti();
        trx.effettuaPagamentoPerTutti(250.00);
    }
}
