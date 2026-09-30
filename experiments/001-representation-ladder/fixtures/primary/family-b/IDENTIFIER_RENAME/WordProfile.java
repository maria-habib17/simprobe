import java.util.Scanner;

public class WordProfile {
    public static void main(String[] args) {
        Scanner inputReader = new Scanner(System.in);
        String text = inputReader.nextLine();
        String[] tokens = extractTokens(text);

        System.out.println("words=" + tokens.length);
        System.out.println("vowels=" + calculateVowels(tokens));
        System.out.println("longest=" + calculateMaximumLength(tokens));
    }

    private static String[] extractTokens(String text) {
        return text.trim().split(" +");
    }

    private static int calculateVowels(String[] tokens) {
        int total = 0;
        for (String token : tokens) {
            for (int position = 0; position < token.length(); position++) {
                if (matchesVowel(token.charAt(position))) {
                    total++;
                }
            }
        }
        return total;
    }

    private static boolean matchesVowel(char symbol) {
        char normalized = Character.toLowerCase(symbol);
        return normalized == 'a' || normalized == 'e' || normalized == 'i'
                || normalized == 'o' || normalized == 'u';
    }

    private static int calculateMaximumLength(String[] tokens) {
        int maximum = 0;
        for (String token : tokens) {
            if (token.length() > maximum) {
                maximum = token.length();
            }
        }
        return maximum;
    }
}
