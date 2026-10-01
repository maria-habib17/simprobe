import java.util.Scanner;

public class ProgramF {
    static boolean operation1(char value) {
        return value == 'a' || value == 'e' || value == 'i' || value == 'o' || value == 'u';
    }

    static int operation2(String word) {
        int count = 0;
        for (int i = 0; i < word.length(); i++) {
            if (operation1(word.charAt(i))) count++;
        }
        return count;
    }

    static int operation3(String word) {
        int runs = 0;
        boolean previousVowel = false;
        for (int i = 0; i < word.length(); i++) {
            boolean currentVowel = operation1(word.charAt(i));
            if (currentVowel && !previousVowel) runs++;
            previousVowel = currentVowel;
        }
        return runs;
    }

    static int operation4(String word) {
        return operation1(word.charAt(0)) ? 1 : 0;
    }

    static int operation5(String word) {
        return word.length();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String word = scanner.nextLine();
        System.out.println("length=" + operation5(word));
        System.out.println("vowels=" + operation2(word));
        System.out.println("runs=" + operation3(word));
        System.out.println("startsVowel=" + operation4(word));
    }
}
