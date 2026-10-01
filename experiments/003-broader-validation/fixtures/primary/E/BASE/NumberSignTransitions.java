import java.util.Scanner;

public class NumberSignTransitions {
    static boolean isPositive(int value) {
        return value > 0;
    }

    static int positiveCount(int[] values) {
        int count = 0;
        for (int value : values) {
            if (isPositive(value)) count++;
        }
        return count;
    }

    static int negativeCount(int[] values) {
        return values.length - positiveCount(values);
    }

    static int signChanges(int[] values) {
        int count = 0;
        for (int i = 1; i < values.length; i++) {
            if (isPositive(values[i]) != isPositive(values[i - 1])) count++;
        }
        return count;
    }

    static int absoluteSum(int[] values) {
        int sum = 0;
        for (int value : values) sum += Math.abs(value);
        return sum;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] values = new int[n];
        for (int i = 0; i < n; i++) values[i] = scanner.nextInt();
        System.out.println("positive=" + positiveCount(values));
        System.out.println("negative=" + negativeCount(values));
        System.out.println("changes=" + signChanges(values));
        System.out.println("absSum=" + absoluteSum(values));
    }
}
