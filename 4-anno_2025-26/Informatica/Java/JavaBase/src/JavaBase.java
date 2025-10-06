import java.util.Scanner;

public class JavaBase {
	public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);
		System.out.print("Enter input: ");
		String input = scanner.nextLine();
		System.out.println("You entered: " + input);
		scanner.close();
	}
}
