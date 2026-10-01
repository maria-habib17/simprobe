import java.util.Scanner;

public class VowelPattern {
    static int vowelRuns(String word) {
        int runs = 0;
        boolean previousVowel = false;
        for (int i = 0; i < word.length(); i++) {
            boolean currentVowel = VowelPatternSupport.isVowel(word.charAt(i));
            if (currentVowel && !previousVowel) runs++;
            previousVowel = currentVowel;
        }
        return runs;
    }

    static int startsWithVowel(String word) {
        return VowelPatternSupport.isVowel(word.charAt(0)) ? 1 : 0;
    }

    static int wordLength(String word) {
        return word.length();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String word = scanner.nextLine();
        System.out.println("length=" + wordLength(word));
        System.out.println("vowels=" + VowelPatternSupport.vowelCount(word));
        System.out.println("runs=" + vowelRuns(word));
        System.out.println("startsVowel=" + startsWithVowel(word));
    }
}
