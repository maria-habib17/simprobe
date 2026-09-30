import java.util.Scanner;

class WordProfile {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String line = scanner.nextLine();
        String[] words = splitWords(line);

        System.out.println("words=" + words.length);
        System.out.println("vowels=" + countVowels(words));
        System.out.println("longest=" + longestLength(words));
    }

    private static String[] splitWords(String line) {
        return line.trim().split(" +");
    }

    private static int countVowels(String[] words) {
        int count = 0;
        for (String word : words) {
            for (int i = 0; i < word.length(); i++) {
                if (isVowel(word.charAt(i))) {
                    count++;
                }
            }
        }
        return count;
    }

    private static boolean isVowel(char value) {
        char ch = Character.toLowerCase(value);
        return ch == 'a' || ch == 'e' || ch == 'i'
                || ch == 'o' || ch == 'u';
    }

    private static int longestLength(String[] words) {
        int longest = 0;
        for (String word : words) {
            if (word.length() > longest) {
                longest = word.length();
            }
        }
        return longest;
    }
}
