import java.util.Scanner;

public class CharacterFrequencyExtremes {
    static int repeatedCount(int[] counts) {
        int repeated = 0;
        for (int count : counts) {
            if (count > 1) repeated++;
        }
        return repeated;
    }

    static int minimumPositiveFrequency(int[] counts) {
        int minimum = Integer.MAX_VALUE;
        for (int count : counts) {
            if (count > 0 && count < minimum) minimum = count;
        }
        return minimum;
    }

    static int maximumFrequency(int[] counts) {
        int maximum = 0;
        for (int count : counts) {
            if (count > maximum) maximum = count;
        }
        return maximum;
    }

    static int distinctCount(int[] counts) {
        int distinct = 0;
        for (int count : counts) {
            if (count > 0) distinct++;
        }
        return distinct;
    }

    static int[] frequencies(String word) {
        int[] counts = new int[26];
        for (int i = 0; i < word.length(); i++) {
            counts[word.charAt(i) - 'a']++;
        }
        return counts;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String word = scanner.nextLine();
        int[] counts = frequencies(word);
        System.out.println("distinct=" + distinctCount(counts));
        System.out.println("maxFreq=" + maximumFrequency(counts));
        System.out.println("minFreq=" + minimumPositiveFrequency(counts));
        System.out.println("repeated=" + repeatedCount(counts));
    }
}
