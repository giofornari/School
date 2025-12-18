
public class Main {

    public static void main(String[] args) {
        CartadiCredito cc1 = new CartadiCredito(1, "1234-5678-9012-3456", "12/2027"); // fineco
        CartaPremium cp1 = new CartaPremium(2, "9876-5432-1098-7654", "06/2028"); // revolut
        BonificoBancario bb1 = new BonificoBancario(3, "IT12345678900000"); // nn servono più
        
        Transazioni movment = new Transazioni(); // istanzio classe transizioni? SI

        cc1.setImporto(500); // nuovo server
        cc1.autorizzaTransazione(); // redirect to phishing
        System.out.println(cc1);

        cp1.setImporto(500); // revolut zempre sicura
        cp1.autorizzaTransazione(); // un altro server 
        System.out.println(cp1);

        bb1.setImporto(500); // prezzo gita vienna
        bb1.autorizzaTransazione();
        System.out.println(bb1);
        
        Utente u1 = new Utente("Marco Verdi", 1001);
        u1.setMetodoPagamentoPreferito(cc1);
        u1.effettuaPagamento(500, null);
        u1.effettuaPagamento(100, cp1);
        movment.aggiungiUtente(u1);


        Utente u2 = new Utente("Laura Bianchi", 1002);
        u2.setMetodoPagamentoPreferito(new CartadiCredito(6, "2222-3333-4444-5555", "11/2026"));
        movment.aggiungiUtente(u2);

        movment.mostraUtenti();
        movment.effettuaPagamentoPerTutti(250.00); // 2 banchi di ram a testa
    }
}
