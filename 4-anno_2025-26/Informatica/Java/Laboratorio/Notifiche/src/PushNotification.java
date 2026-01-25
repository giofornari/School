
// notifica push
public class PushNotification implements Notification {

    private String deviceId;

    // device default
    public PushNotification() {
        this.deviceId = "device";
    }

    // device custom
    public PushNotification(String deviceId) {
        if (deviceId == null || deviceId.isEmpty()) {
            throw new IllegalArgumentException("Device ID vuoto");
        }
        this.deviceId = deviceId;
    }

    @Override
    public boolean send(String message) {
        if (message == null || message.isEmpty()) {
            System.out.println("[PUSH] ERROR: Messaggio vuoto");
            return false;
        }
        System.out.println("[PUSH] Notification sent to " + deviceId + " - Message: " + message);
        return true;
    }
}
