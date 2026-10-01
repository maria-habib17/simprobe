import java.util.Scanner;

public class ProgramE {
    static boolean operation1(int value) {
        return value > 0;
    }

    static int operation2(int[] values) {
        int count = 0;
        for (int value : values) {
            if (operation1(value)) count++;
        }
        return count;
    }

    static int operation3(int[] values) {
        return values.length - operation2(values);
    }

    static int operation4(int[] values) {
        int count = 0;
        for (int i = 1; i < values.length; i++) {
            if (operation1(values[i]) != operation1(values[i - 1])) count++;
        }
        return count;
    }

    static int operation5(int[] values) {
        int sum = 0;
        for (int value : values) sum += Math.abs(value);
        return sum;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] values = new int[n];
        for (int i = 0; i < n; i++) values[i] = scanner.nextInt();
        System.out.println("positive=" + operation2(values));
        System.out.println("negative=" + operation3(values));
        System.out.println("changes=" + operation4(values));
        System.out.println("absSum=" + operation5(values));
    }
}
