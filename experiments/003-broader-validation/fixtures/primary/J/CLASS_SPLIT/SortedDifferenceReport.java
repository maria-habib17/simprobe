import java.util.Scanner;

public class SortedDifferenceReport {
    static int maximumGap(int[] values) {
        int maximum = 0;
        for (int i = 1; i < values.length; i++) {
            int gap = values[i] - values[i - 1];
            if (gap > maximum) maximum = gap;
        }
        return maximum;
    }

    static int span(int[] values) {
        return values[values.length - 1] - values[0];
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] values = new int[n];
        for (int i = 0; i < n; i++) values[i] = scanner.nextInt();
        System.out.println("duplicates=" + SortedDifferenceReportSupport.duplicateCount(values));
        System.out.println("positiveGaps=" + SortedDifferenceReportSupport.positiveGapCount(values));
        System.out.println("maxGap=" + maximumGap(values));
        System.out.println("span=" + span(values));
    }
}
