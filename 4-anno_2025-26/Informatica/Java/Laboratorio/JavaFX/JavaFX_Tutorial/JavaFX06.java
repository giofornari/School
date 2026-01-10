import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;

// 6) Layout BorderPane con Toolbar e TextArea
/*   TooolBar: 
     è un contenitore simile a HBox, ma con stile e comportamento specifici (azioni) per le barre degli strumenti.
     HBox è un contenitore generico, ToolBar è un controllo con un significato preciso
     Non fanno la stessa cosa, anche se visivamente possono sembrare uguali.
     ToolBar gestisce automaticamente l'aspetto e il comportamento dei suoi elementi figli in modo coerente con le convenzioni delle barre degli strumenti.
     Il vantaggio di usare ToolBar è che fornisce funzionalità aggiuntive come il supporto per la riduzione a icona, il trascinamento e il ridimensionamento 
     automatico degli elementi in base allo spazio disponibile.
     ToolBar migliora l'usabilità e l'aspetto dell'interfaccia utente rispetto a un semplice HBox.
 */
public class JavaFX06 extends Application{
    @Override
        public void start(Stage stage) {
        BorderPane root = new BorderPane();

        ToolBar toolbar = new ToolBar(new Button("Nuovo"), new Button("Apri"));
        toolbar.getItems().add(new Button("Salva"));  // Aggiunta postuma
        TextArea area = new TextArea();

        root.setTop(toolbar);
        root.setCenter(area);

        stage.setScene(new Scene(root, 400, 300));
        stage.show();
    }
    public static void main(String[] args) { launch(); }
}