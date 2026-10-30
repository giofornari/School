
// notifica email
public class EmailNotification implements Notification {

    private String destMail;

    // email default
    public EmailNotification() {
        this.destMail = "admin@giordii.dev";
    }

    // email custom
    public EmailNotification(String destMail) {
        if (destMail == null || destMail.isEmpty()) {
            throw new IllegalArgumentException("Email error");
        }
        this.destMail = destMail;
    }

    @Override
    public boolean send(String message) {
        if (message == null || message.isEmpty()) {
            System.out.println("[EMAIL] ERROR: No message fund");
            return false;
        }
        System.out.println("[EMAIL] Send to: " + destMail + " - alert(): " + message);
        return true;
    }
}
