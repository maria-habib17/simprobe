import java.util.Scanner;

public class WordProfile {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String line = scanner.nextLine();

        String[] words = line.trim().split(" +");
        int vowels = 0;
        int longest = 0;

        for (String word : words) {
            if (word.length() > longest) {
                longest = word.length();
            }

            for (int i = 0; i < word.length(); i++) {
                char ch = Character.toLowerCase(word.charAt(i));
                if (ch == 'a' || ch == 'e' || ch == 'i' ||
                    ch == 'o' || ch == 'u') {
                    vowels++;
                }
            }
        }

        System.out.println("words=" + words.length);
        System.out.println("vowels=" + vowels);
        System.out.println("longest=" + longest);
    }
}
