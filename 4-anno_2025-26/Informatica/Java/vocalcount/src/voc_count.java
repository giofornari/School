public class voc_count {
	public static void main(String[] args) {
		char[] chars = {'p', 'r', 'e', 'f', 'e', 'r', 'i', 's', 'c', 'o', ' ', 'p', 'y', 't', 'h', 'o', 'n'};
		int[] vowelCount = new int[5];
		char[] vowels = {'a', 'e', 'i', 'o', 'u'};

		for (char c : chars) {
			char lower = Character.toLowerCase(c);
			for (int i = 0; i < vowels.length; i++) {
				if (lower == vowels[i]) {
					vowelCount[i]++;
					break;
				}
			}
		}

		for (int i = 0; i < vowels.length; i++) {
			System.out.println(vowels[i] + ": " + vowelCount[i]);
		}

		int total = 0;
		for (int count : vowelCount) {
			total += count;
		}
		System.out.println("vowel num: " + total);
	}
}
