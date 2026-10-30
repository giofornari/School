
// notifica sms (con errori 30%)
public class SmsNotification implements Notification {

    private String phoneNumber;

    // num default
    public SmsNotification() {
        this.phoneNumber = "+1 234567890";
    }

    // num custom
    public SmsNotification(String phoneNumber) {
        if (phoneNumber == null || phoneNumber.isEmpty()) {
            throw new IllegalArgumentException("Numero vuoto");
        }
        this.phoneNumber = phoneNumber;
    }

    @Override
    public boolean send(String message) {
        if (message == null || message.isEmpty()) {
            System.out.println("[SMS] ERROR: Messaggio vuoto");
            return false;
        }

        // Simula errore casuale (30%)
        if (Math.random() < 0.3) {
            System.out.println("[SMS] ERROR: Failed to send to number: " + phoneNumber);
            return false;
        }

        System.out.println("[SMS] Sending to number: " + phoneNumber + " - Message: " + message);
        return true;
    }
}
