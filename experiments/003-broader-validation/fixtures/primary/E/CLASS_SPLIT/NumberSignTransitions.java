import java.util.Scanner;

public class NumberSignTransitions {
    static int negativeCount(int[] values) {
        return values.length - NumberSignTransitionsSupport.positiveCount(values);
    }

    static int signChanges(int[] values) {
        int count = 0;
        for (int i = 1; i < values.length; i++) {
            if (NumberSignTransitionsSupport.isPositive(values[i]) != NumberSignTransitionsSupport.isPositive(values[i - 1])) count++;
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
        System.out.println("positive=" + NumberSignTransitionsSupport.positiveCount(values));
        System.out.println("negative=" + negativeCount(values));
        System.out.println("changes=" + signChanges(values));
        System.out.println("absSum=" + absoluteSum(values));
    }
}
