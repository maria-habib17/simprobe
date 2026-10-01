import java.util.Scanner;

public class WordLengthProfile {
    static int evenLengthCount(String[] words) {
        int count = 0;
        for (String word : words) {
            if (word.length() % 2 == 0) count++;
        }
        return count;
    }

    static String[] splitWords(String line) {
        return line.split(" ");
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String[] words = splitWords(scanner.nextLine());
        System.out.println("words=" + words.length);
        System.out.println("shortest=" + WordLengthProfileSupport.shortest(words));
        System.out.println("longest=" + WordLengthProfileSupport.longest(words));
        System.out.println("even=" + evenLengthCount(words));
    }
}
