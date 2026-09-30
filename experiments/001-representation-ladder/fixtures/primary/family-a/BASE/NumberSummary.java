import java.util.Scanner;

public class NumberSummary {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        int first = scanner.nextInt();

        int sum = first;
        int min = first;
        int max = first;
        int even = first % 2 == 0 ? 1 : 0;

        for (int i = 1; i < n; i++) {
            int value = scanner.nextInt();

            sum += value;

            if (value < min) {
                min = value;
            }

            if (value > max) {
                max = value;
            }

            if (value % 2 == 0) {
                even++;
            }
        }

        System.out.println("sum=" + sum);
        System.out.println("min=" + min);
        System.out.println("max=" + max);
        System.out.println("even=" + even);
    }
}
