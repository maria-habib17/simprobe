import java.util.Scanner;

public class TemperatureSummary {
    static int countNonnegative(int[] values) {
        int count = 0;
        for (int value : values) {
            if (value >= 0) count++;
        }
        return count;
    }

    static int spread(int[] values) {
        return maximum(values) - minimum(values);
    }

    static int maximum(int[] values) {
        int result = values[0];
        for (int value : values) {
            if (value > result) result = value;
        }
        return result;
    }

    static int minimum(int[] values) {
        int result = values[0];
        for (int value : values) {
            if (value < result) result = value;
        }
        return result;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] values = new int[n];
        for (int i = 0; i < n; i++) values[i] = scanner.nextInt();
        System.out.println("min=" + minimum(values));
        System.out.println("max=" + maximum(values));
        System.out.println("spread=" + spread(values));
        System.out.println("nonnegative=" + countNonnegative(values));
    }
}
