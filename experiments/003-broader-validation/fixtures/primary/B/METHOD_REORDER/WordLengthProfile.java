import java.util.Scanner;

public class WordLengthProfile {
    static String[] splitWords(String line) {
        return line.split(" ");
    }

    static int evenLengthCount(String[] words) {
        int count = 0;
        for (String word : words) {
            if (word.length() % 2 == 0) count++;
        }
        return count;
    }

    static int longest(String[] words) {
        int result = words[0].length();
        for (String word : words) {
            if (word.length() > result) result = word.length();
        }
        return result;
    }

    static int shortest(String[] words) {
        int result = words[0].length();
        for (String word : words) {
            if (word.length() < result) result = word.length();
        }
        return result;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String[] words = splitWords(scanner.nextLine());
        System.out.println("words=" + words.length);
        System.out.println("shortest=" + shortest(words));
        System.out.println("longest=" + longest(words));
        System.out.println("even=" + evenLengthCount(words));
    }
}
