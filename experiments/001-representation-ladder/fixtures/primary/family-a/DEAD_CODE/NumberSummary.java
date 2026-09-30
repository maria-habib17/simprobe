import java.util.Scanner;

public class NumberSummary {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] values = readValues(scanner, n);

        System.out.println("sum=" + sum(values));
        System.out.println("min=" + min(values));
        System.out.println("max=" + max(values));
        System.out.println("even=" + countEven(values));
    }

    private static int[] readValues(Scanner scanner, int n) {
        int[] values = new int[n];
        for (int i = 0; i < n; i++) {
            values[i] = scanner.nextInt();
        }
        return values;
    }

    private static int sum(int[] values) {
        int result = 0;
        for (int value : values) {
            result += value;
        }
        return result;
    }

    private static int min(int[] values) {
        int result = values[0];
        for (int value : values) {
            if (value < result) {
                result = value;
            }
        }
        return result;
    }

    private static int max(int[] values) {
        int result = values[0];
        for (int value : values) {
            if (value > result) {
                result = value;
            }
        }
        return result;
    }

    private static int countEven(int[] values) {
        int result = 0;
        for (int value : values) {
            if (value % 2 == 0) {
                result++;
            }
        }
        return result;
    }
    private static int unusedDifference(int left, int right) {
        return left - right;
    }
}
