import java.util.Scanner;

public class ProgramA {
    static int operation1(int[] values) {
        int result = values[0];
        for (int value : values) {
            if (value < result) result = value;
        }
        return result;
    }

    static int operation2(int[] values) {
        int result = values[0];
        for (int value : values) {
            if (value > result) result = value;
        }
        return result;
    }

    static int operation3(int[] values) {
        return operation2(values) - operation1(values);
    }

    static int operation4(int[] values) {
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
        System.out.println("min=" + operation1(values));
        System.out.println("max=" + operation2(values));
        System.out.println("spread=" + operation3(values));
        System.out.println("nonnegative=" + operation4(values));
    }
}
