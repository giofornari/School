
// test polimorfismo
public class NotificationManager {

    public static void main(String[] args) {
        System.out.println("-- test polimorfismo --\n");

        Notification notification;
        String message = "Test message";

        // Testa ogni tipo di notifica con polimorfismo
        notification = new EmailNotification();
        notification.send(message);

        notification = new SmsNotification();
        notification.send(message);

        notification = new PushNotification();
        notification.send(message);

        notification = new WhatsAppNotification();
        notification.send(message);
    }
}
