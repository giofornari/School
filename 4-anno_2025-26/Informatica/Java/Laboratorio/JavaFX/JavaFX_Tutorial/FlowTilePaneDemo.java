import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Orientation;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.FlowPane;
import javafx.scene.layout.TilePane;
import javafx.stage.Stage;
/*
    FlowPane e TilePane sembrano simili, ma servono a cose diverse.

        FlowPane = flusso libero (come testo)
        TilePane = griglia di “piastrelle” tutte uguali

🔹 FlowPane
    dispone i nodi in sequenza, va a capo automaticamente, ogni nodo mantiene la sua dimensione

    Esempio visivo
        [ Btn1 ][ BottoneLungo ][ B3 ][ B4 ]
        [ B5 ][ B6 ][ B7 ]
    
    Quando usarlo:
        tag / categorie
        pulsanti dinamici
        elenchi che cambiano dimensione
        layout “a flusso”

🔹 TilePane
    dispone i nodi in celle tutte uguali, dimensione fissa o calcolata, allineamento ordinato

    Esempio visivo
        [ Btn1 ] [ Btn2 ] [ Btn3 ]
        [ Btn4 ] [ Btn5 ] [ Btn6 ]

    Quando usarlo:
        tastiere
        griglie di icone
        menu “a piastrelle”
        dashboard
 */

public class FlowTilePaneDemo extends Application {

    @Override
    public void start(Stage stage) {

        // PROVA ALTERNATIVAMENTE FlowPane o TilePane
        //FlowPane flow = new FlowPane();
        TilePane flow = new TilePane();

        // orientamento (HORIZONTAL è default)
        flow.setOrientation(Orientation.HORIZONTAL);

        // spazio tra i nodi
        flow.setHgap(10);
        flow.setVgap(10);

        // padding interno
        flow.setPadding(new Insets(10));

        // aggiungiamo molti pulsanti
        for (int i = 1; i <= 20; i++) {
            flow.getChildren().add(new Button("Btn " + i));
        }
        // Aggiungi un pulsante più lungo per vedere la differenza
        //flow.getChildren().add(new Button("Bottone Lungo"));

        Scene scene = new Scene(flow, 300, 200);
        stage.setTitle("Esempio FlowPane");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
