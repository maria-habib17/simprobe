import java.util.Scanner;

public class NumberSummary {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] values = readValues(scanner, n);

        System.out.println("sum=" + NumberOperations.sum(values));
        System.out.println("min=" + NumberOperations.min(values));
        System.out.println("max=" + NumberOperations.max(values));
        System.out.println("even=" + NumberOperations.countEven(values));
    }

    private static int[] readValues(Scanner scanner, int n) {
        int[] values = new int[n];
        for (int i = 0; i < n; i++) {
            values[i] = scanner.nextInt();
        }
        return values;
    }
}
