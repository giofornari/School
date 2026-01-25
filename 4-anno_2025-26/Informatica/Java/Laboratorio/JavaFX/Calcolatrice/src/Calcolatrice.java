
// roba di javafx
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

/*
 * Calcolatrice fatta con JavaFX
 * uso GridPane xke e' tipo una griglia e metto i btn nelle celle
 * molto + comodo che farsi i calcoli a mano con le posizioni
 */
public class Calcolatrice extends Application {

    // var globali per far funzionare sta roba
    private TextField display;
    private double numero1 = 0;      // primo num inserito
    private String operatore = "";   // +,-,*,/ 
    private boolean nuovoNumero = true;  // flag per capire se devo pulire il display

    @Override
    public void start(Stage stage) {

        // display dove si vedono i numeri
        display = new TextField("0");
        display.setEditable(false);  // nn si puo scrivere
        display.setAlignment(Pos.CENTER_RIGHT);
        display.setStyle("-fx-font-size: 24px;");  // font + grande

        // griglia x i bottoni
        GridPane grid = new GridPane();
        grid.setHgap(5);  // spazio tra colonne
        // spazio tra righe
        grid.setVgap(5);
        
        grid.setPadding(new Insets(10));  // margine esterno

        // bottoni numeri 0-9
        Button btn0 = BtnNum("0");
        Button btn1 = BtnNum("1");
        Button btn2 = BtnNum("2");
        Button btn3 = BtnNum("3");
        Button btn4 = BtnNum("4");
        Button btn5 = BtnNum("5");
        Button btn6 = BtnNum("6");
        Button btn7 = BtnNum("7");
        Button btn8 = BtnNum("8");
        Button btn9 = BtnNum("9");

        // bottoni operazioni
        Button btnPiu = BtnOp("+");
        Button btnMeno = BtnOp("-");
        Button btnPer = BtnOp("*");
        Button btnDiviso = BtnOp("/");

        // btn uguale - calcola tutto
        Button btnUguale = new Button("=");
        btnUguale.setPrefSize(50, 50);
        btnUguale.setOnAction(e -> result());

        // btn C - cancella tt
        Button btnCancella = new Button("C");
        btnCancella.setPrefSize(50, 50);
        btnCancella.setOnAction(e -> rmrf());  // lol come rm -rf

        // metto i btn nella griglia (col, riga)
        // riga 0
        grid.add(btn7, 0, 0);
        grid.add(btn8, 1, 0);
        grid.add(btn9, 2, 0);
        grid.add(btnDiviso, 3, 0);

        // riga 1
        grid.add(btn4, 0, 1);
        grid.add(btn5, 1, 1);
        grid.add(btn6, 2, 1);
        grid.add(btnPer, 3, 1);

        // riga 2
        grid.add(btn1, 0, 2);
        grid.add(btn2, 1, 2);
        grid.add(btn3, 2, 2);
        grid.add(btnMeno, 3, 2);

        // riga 3
        grid.add(btnCancella, 0, 3);
        grid.add(btn0, 1, 3);
        grid.add(btnUguale, 2, 3);
        grid.add(btnPiu, 3, 3);

        // metto tt insieme - display sopra, griglia sotto
        VBox root = new VBox(10, display, grid);
        root.setPadding(new Insets(10));

        // creo finestra
        Scene scene = new Scene(root);
        stage.setTitle("Calcolatrice");
        stage.setScene(scene);
        stage.setResizable(false);  // nn si ridimensiona
        stage.show();
    }

    // crea btn x i numeri
    private Button BtnNum(String numero) {
        Button btn = new Button(numero);
        btn.setPrefSize(50, 50);
        btn.setOnAction(e -> addNum(numero));
        return btn;
    }

    // crea btn x le operazioni
    private Button BtnOp(String op) {
        Button btn = new Button(op);
        btn.setPrefSize(50, 50);
        btn.setOnAction(e -> setOpt(op));
        return btn;
    }

    // aggiunge cifra al display
    private void addNum(String cifra) {
        if (nuovoNumero) {
            display.setText(cifra);
            nuovoNumero = false;
        } else {
            // se c'e' 0 lo sostituisco sennò aggiungo
            if (display.getText().equals("0")) {
                display.setText(cifra);
            } else {
                display.setText(display.getText() + cifra);
            }
        }
    }

    // salva operatore e primo num
    private void setOpt(String op) {
        numero1 = Double.parseDouble(display.getText());
        operatore = op;
        nuovoNumero = true;
    }

    // fa il calcolo
    private void result() {
        double numero2 = Double.parseDouble(display.getText());
        double risultato = 0;

        // switch case ma con if xke era + veloce da scrivere
        if (operatore.equals("+")) {
            risultato = numero1 + numero2;
        } else if (operatore.equals("-")) {
            risultato = numero1 - numero2;
        } else if (operatore.equals("*")) {
            risultato = numero1 * numero2;
        } else if (operatore.equals("/")) {
            if (numero2 != 0) {
                risultato = numero1 / numero2;
            } else {
                display.setText("Errore");  // div x 0 = male
                nuovoNumero = true;
                return;
            }
        }

        // se e' intero tolgo il .0
        if (risultato == (int) risultato) {
            display.setText(String.valueOf((int) risultato));
        } else {
            display.setText(String.valueOf(risultato));
        }
        nuovoNumero = true;
    }

    // resetta tt
    private void rmrf() {
        display.setText("0");
        numero1 = 0;
        operatore = "";
        nuovoNumero = true;
    }

    // main - lancia l'app
    public static void main(String[] args) {
        launch();
    }
}
