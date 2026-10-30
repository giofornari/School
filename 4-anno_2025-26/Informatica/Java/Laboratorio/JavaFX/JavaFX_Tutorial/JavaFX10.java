import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

public class JavaFX10 extends Application {
    @Override
    public void start(Stage stage) {
        Canvas canvas = new Canvas(400, 300);
        GraphicsContext g = canvas.getGraphicsContext2D();

        g.setFill(Color.LIGHTGRAY);
        g.fillRect(0, 0, 400, 300);

        g.setStroke(Color.BLUE);
        g.setLineWidth(3);
        g.strokeOval(100, 80, 200, 150);

        StackPane root = new StackPane(canvas);
        stage.setScene(new Scene(root));
        stage.show();
    }
    public static void main(String[] args) { launch(); }
}
