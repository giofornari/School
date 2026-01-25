// Veicolo che può sia volare che nuotare
// Implementa due interfacce diverse (ereditarietà multipla)
public class VeicoloAnfibio implements Volante, Nuotante {
    private String nome;
    
    public VeicoloAnfibio(String nome) {
        this.nome = nome;
    }
    
    // Metodo dell'interfaccia Volante
    @Override
    public void vola() {
        System.out.println(nome + " sta volando in aria");
    }
    
    // Metodo dell'interfaccia Nuotante
    @Override
    public void nuota() {
        System.out.println(nome + " sta nuotando nell'acqua");
    }
    
    public String getNome() {
        return nome;
    }
}
