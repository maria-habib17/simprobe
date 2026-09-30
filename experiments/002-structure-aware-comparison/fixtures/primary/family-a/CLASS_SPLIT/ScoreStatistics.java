import java.util.Scanner;

public class ScoreStatistics {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int count = scanner.nextInt();
        int[] scores = readScores(scanner, count);

        int total = ScoreOperations.calculateTotal(scores);
        int average = ScoreOperations.calculateAverage(total, count);
        int above = countAbove(scores, average);
        int range = calculateRange(scores);

        System.out.println("total=" + total);
        System.out.println("average=" + average);
        System.out.println("above=" + above);
        System.out.println("range=" + range);
    }

    private static int[] readScores(Scanner scanner, int count) {
        int[] scores = new int[count];
        for (int i = 0; i < count; i++) {
            scores[i] = scanner.nextInt();
        }
        return scores;
    }

    private static int countAbove(int[] scores, int average) {
        int above = 0;
        for (int score : scores) {
            if (score > average) {
                above++;
            }
        }
        return above;
    }

    private static int calculateRange(int[] scores) {
        int minimum = scores[0];
        int maximum = scores[0];

        for (int score : scores) {
            if (score < minimum) {
                minimum = score;
            }
            if (score > maximum) {
                maximum = score;
            }
        }

        return maximum - minimum;
    }
}
