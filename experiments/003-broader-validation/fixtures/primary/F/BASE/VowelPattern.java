import java.util.Scanner;

public class VowelPattern {
    static boolean isVowel(char value) {
        return value == 'a' || value == 'e' || value == 'i' || value == 'o' || value == 'u';
    }

    static int vowelCount(String word) {
        int count = 0;
        for (int i = 0; i < word.length(); i++) {
            if (isVowel(word.charAt(i))) count++;
        }
        return count;
    }

    static int vowelRuns(String word) {
        int runs = 0;
        boolean previousVowel = false;
        for (int i = 0; i < word.length(); i++) {
            boolean currentVowel = isVowel(word.charAt(i));
            if (currentVowel && !previousVowel) runs++;
            previousVowel = currentVowel;
        }
        return runs;
    }

    static int startsWithVowel(String word) {
        return isVowel(word.charAt(0)) ? 1 : 0;
    }

    static int wordLength(String word) {
        return word.length();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String word = scanner.nextLine();
        System.out.println("length=" + wordLength(word));
        System.out.println("vowels=" + vowelCount(word));
        System.out.println("runs=" + vowelRuns(word));
        System.out.println("startsVowel=" + startsWithVowel(word));
    }
}
