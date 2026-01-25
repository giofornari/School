
import java.util.ArrayList;

// test notifiche
public class Main {

    public static void main(String[] args) {
        System.out.println("-- test notifiche --\n");

        // lista canali
        ArrayList<Notification> channels = new ArrayList<>();
        channels.add(new EmailNotification("admin@company.com"));
        channels.add(new SmsNotification("+39 333 1234567"));
        channels.add(new PushNotification("iPhone-12-Pro"));
        channels.add(new WhatsAppNotification("+39 333 7654321"));

        // broadcast msg
        String message = "System maintenance scheduled for tonight";
        int success = 0;

        for (Notification channel : channels) {
            if (channel.send(message)) {
                success++;
            }
        }

        // risultati
        System.out.println("\ntot: " + channels.size());
        System.out.println("ok: " + success);
        System.out.println("fail: " + (channels.size() - success));
    }
}
