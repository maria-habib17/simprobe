import java.util.Scanner;

public class TemperatureSummary {
    static int spread(int[] values) {
        return TemperatureSummarySupport.maximum(values) - TemperatureSummarySupport.minimum(values);
    }

    static int countNonnegative(int[] values) {
        int count = 0;
        for (int value : values) {
            if (value >= 0) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] values = new int[n];
        for (int i = 0; i < n; i++) values[i] = scanner.nextInt();
        System.out.println("min=" + TemperatureSummarySupport.minimum(values));
        System.out.println("max=" + TemperatureSummarySupport.maximum(values));
        System.out.println("spread=" + spread(values));
        System.out.println("nonnegative=" + countNonnegative(values));
    }
}
