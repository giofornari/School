
// notifica whatsapp
public class WhatsAppNotification implements Notification {

    private String phoneNumber;

    // num default
    public WhatsAppNotification() {
        this.phoneNumber = "+1 234567890";
    }

    // num custom
    public WhatsAppNotification(String phoneNumber) {
        if (phoneNumber == null || phoneNumber.isEmpty()) {
            throw new IllegalArgumentException("Numero vuoto");
        }
        this.phoneNumber = phoneNumber;
    }

    @Override
    public boolean send(String message) {
        if (message == null || message.isEmpty()) {
            System.out.println("[WHATSAPP] ERROR: Messaggio vuoto");
            return false;
        }
        System.out.println("[WHATSAPP] Sending to: " + phoneNumber + " - Message: " + message);
        return true;
    }
}
