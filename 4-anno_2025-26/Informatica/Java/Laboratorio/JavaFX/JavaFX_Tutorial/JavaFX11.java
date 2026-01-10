import javafx.application.Application;
import javafx.geometry.*;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Stage;

/* Cosa insegna questo esempio:
    Container	Ruolo
    BorderPane	Struttura principale
    ToolBar	    Barra strumenti
    VBox	    Menu verticale
    GridPane	Form a righe/colonne
    HBox	    Pulsanti orizzontali
    StackPane	Sovrapposizione

    Struttura ad albero dei nodi:
    StackPane
    └── BorderPane
        ├── Top    → ToolBar
        ├── Left   → VBox (menu)
        ├── Center → GridPane (form)
        └── Bottom → HBox (pulsanti)
     
     StackPane è il livello più esterno per sovrapporre il messaggio di benvenuto
*/
public class JavaFX11 extends Application {

    @Override
    public void start(Stage stage) {

        // =========================
        // ROOT: BorderPane
        // =========================
        BorderPane root = new BorderPane();

        // =========================
        // TOP: ToolBar (HBox-like)
        // =========================
        ToolBar toolBar = new ToolBar(
                new Button("Nuovo"),
                new Button("Apri"),
                new Separator(),
                new Button("Salva")
        );
        root.setTop(toolBar);

        // =========================
        // LEFT: VBox (menu laterale)
        // =========================
        VBox menu = new VBox(10);
        menu.setPadding(new Insets(10));
        menu.getChildren().addAll(
                new Button("Home"),
                new Button("Clienti"),
                new Button("Ordini")
        );
        root.setLeft(menu);

        // =========================
        // CENTER: GridPane (form)
        // =========================
        GridPane form = new GridPane();
        form.setPadding(new Insets(15));
        form.setHgap(10);
        form.setVgap(10);

        form.add(new Label("Nome:"), 0, 0);
        form.add(new TextField(), 1, 0);

        form.add(new Label("Email:"), 0, 1);
        form.add(new TextField(), 1, 1);

        form.add(new Label("Ruolo:"), 0, 2);
        form.add(new ComboBox<>(), 1, 2);

        root.setCenter(form);

        // =========================
        // BOTTOM: HBox (pulsanti)
        // =========================
        HBox actions = new HBox(10);
        actions.setPadding(new Insets(10));
        actions.setAlignment(Pos.CENTER_RIGHT);
        actions.getChildren().addAll(
                new Button("Annulla"),
                new Button("Salva")
        );
        root.setBottom(actions);

        // =========================
        // OVERLAY: StackPane
        // =========================
        Label message = new Label("Benvenuto nell'app!");
        message.setStyle("-fx-font-size: 26px;");

        StackPane overlay = new StackPane(message);
        overlay.setAlignment(Pos.CENTER);

        // StackPane contiene BorderPane + messaggio
        StackPane main = new StackPane(root, overlay);

        // =========================
        // SCENE & STAGE
        // =========================
        Scene scene = new Scene(main, 600, 400);
        stage.setTitle("Demo Container JavaFX");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
