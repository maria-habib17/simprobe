import java.util.Scanner;

public class ProgramH {
    static int[] operation1(String word) {
        int[] counts = new int[26];
        for (int i = 0; i < word.length(); i++) {
            counts[word.charAt(i) - 'a']++;
        }
        return counts;
    }

    static int operation2(int[] counts) {
        int distinct = 0;
        for (int count : counts) {
            if (count > 0) distinct++;
        }
        return distinct;
    }

    static int operation3(int[] counts) {
        int maximum = 0;
        for (int count : counts) {
            if (count > maximum) maximum = count;
        }
        return maximum;
    }

    static int operation4(int[] counts) {
        int minimum = Integer.MAX_VALUE;
        for (int count : counts) {
            if (count > 0 && count < minimum) minimum = count;
        }
        return minimum;
    }

    static int operation5(int[] counts) {
        int repeated = 0;
        for (int count : counts) {
            if (count > 1) repeated++;
        }
        return repeated;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String word = scanner.nextLine();
        int[] counts = operation1(word);
        System.out.println("distinct=" + operation2(counts));
        System.out.println("maxFreq=" + operation3(counts));
        System.out.println("minFreq=" + operation4(counts));
        System.out.println("repeated=" + operation5(counts));
    }
}
