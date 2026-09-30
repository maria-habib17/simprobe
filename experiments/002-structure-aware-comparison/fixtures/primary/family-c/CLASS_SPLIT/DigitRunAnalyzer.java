import java.util.Scanner;

public class DigitRunAnalyzer {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String digits = scanner.nextLine();

        int runs = countRuns(digits);
        int longest = longestRun(digits);
        int changes = DigitMetrics.countChanges(digits);
        int weighted = DigitMetrics.weightedSum(digits);

        System.out.println("runs=" + runs);
        System.out.println("longest=" + longest);
        System.out.println("changes=" + changes);
        System.out.println("weighted=" + weighted);
    }

    private static int countRuns(String digits) {
        int runs = 1;

        for (int i = 1; i < digits.length(); i++) {
            if (digits.charAt(i) != digits.charAt(i - 1)) {
                runs++;
            }
        }

        return runs;
    }

    private static int longestRun(String digits) {
        int longest = 1;
        int current = 1;

        for (int i = 1; i < digits.length(); i++) {
            if (digits.charAt(i) == digits.charAt(i - 1)) {
                current++;
                if (current > longest) {
                    longest = current;
                }
            } else {
                current = 1;
            }
        }

        return longest;
    }
}
