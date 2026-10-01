import java.util.Scanner;

public class ProgramB {
    static int operation1(String[] words) {
        int result = words[0].length();
        for (String word : words) {
            if (word.length() < result) result = word.length();
        }
        return result;
    }

    static int operation2(String[] words) {
        int result = words[0].length();
        for (String word : words) {
            if (word.length() > result) result = word.length();
        }
        return result;
    }

    static int operation3(String[] words) {
        int count = 0;
        for (String word : words) {
            if (word.length() % 2 == 0) count++;
        }
        return count;
    }

    static String[] operation4(String line) {
        return line.split(" ");
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String[] words = operation4(scanner.nextLine());
        System.out.println("words=" + words.length);
        System.out.println("shortest=" + operation1(words));
        System.out.println("longest=" + operation2(words));
        System.out.println("even=" + operation3(words));
    }
}
