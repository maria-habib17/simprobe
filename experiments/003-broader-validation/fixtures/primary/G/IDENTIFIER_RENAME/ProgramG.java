import java.util.Scanner;

public class ProgramG {
    static int operation1(int[] values) {
        int sum = 0;
        for (int value : values) sum += value;
        return sum;
    }

    static int operation2(int[] values) {
        int sum = 0;
        int maximum = Integer.MIN_VALUE;
        for (int value : values) {
            sum += value;
            if (sum > maximum) maximum = sum;
        }
        return maximum;
    }

    static int operation3(int[] values) {
        int sum = 0;
        int minimum = Integer.MAX_VALUE;
        for (int value : values) {
            sum += value;
            if (sum < minimum) minimum = sum;
        }
        return minimum;
    }

    static int operation4(int[] values) {
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
        System.out.println("final=" + operation1(values));
        System.out.println("maxPrefix=" + operation2(values));
        System.out.println("minPrefix=" + operation3(values));
        System.out.println("positivePrefixes=" + operation4(values));
    }
}
