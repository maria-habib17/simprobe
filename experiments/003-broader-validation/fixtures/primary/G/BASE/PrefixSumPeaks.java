import java.util.Scanner;

public class PrefixSumPeaks {
    static int finalSum(int[] values) {
        int sum = 0;
        for (int value : values) sum += value;
        return sum;
    }

    static int maximumPrefix(int[] values) {
        int sum = 0;
        int maximum = Integer.MIN_VALUE;
        for (int value : values) {
            sum += value;
            if (sum > maximum) maximum = sum;
        }
        return maximum;
    }

    static int minimumPrefix(int[] values) {
        int sum = 0;
        int minimum = Integer.MAX_VALUE;
        for (int value : values) {
            sum += value;
            if (sum < minimum) minimum = sum;
        }
        return minimum;
    }

    static int positivePrefixes(int[] values) {
        int sum = 0;
        int count = 0;
        for (int value : values) {
            sum += value;
            if (sum > 0) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] values = new int[n];
        for (int i = 0; i < n; i++) values[i] = scanner.nextInt();
        System.out.println("final=" + finalSum(values));
        System.out.println("maxPrefix=" + maximumPrefix(values));
        System.out.println("minPrefix=" + minimumPrefix(values));
        System.out.println("positivePrefixes=" + positivePrefixes(values));
    }
}
