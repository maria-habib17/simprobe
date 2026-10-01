import java.util.Scanner;

public class PrefixSumPeaks {
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
        System.out.println("final=" + PrefixSumPeaksSupport.finalSum(values));
        System.out.println("maxPrefix=" + PrefixSumPeaksSupport.maximumPrefix(values));
        System.out.println("minPrefix=" + minimumPrefix(values));
        System.out.println("positivePrefixes=" + positivePrefixes(values));
    }
}
