import java.util.Scanner;

public class WordProfile {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String line = scanner.nextLine();
        String[] words = WordAnalysis.splitWords(line);

        System.out.println("words=" + words.length);
        System.out.println("vowels=" + WordAnalysis.countVowels(words));
        System.out.println("longest=" + WordAnalysis.longestLength(words));
    }
}
