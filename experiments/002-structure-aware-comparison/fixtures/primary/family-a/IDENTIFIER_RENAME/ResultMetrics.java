import java.util.Scanner;

public class ResultMetrics {
    public static void main(String[] arguments) {
        Scanner input = new Scanner(System.in);
        int quantity = input.nextInt();
        int[] values = loadValues(input, quantity);

        int sum = sumValues(values);
        int mean = computeMean(sum, quantity);
        int higher = countHigher(values, mean);
        int spread = findSpread(values);

        System.out.println("total=" + sum);
        System.out.println("average=" + mean);
        System.out.println("above=" + higher);
        System.out.println("range=" + spread);
    }

    private static int[] loadValues(Scanner input, int quantity) {
        int[] values = new int[quantity];
        for (int position = 0; position < quantity; position++) {
            values[position] = input.nextInt();
        }
        return values;
    }

    private static int sumValues(int[] values) {
        int sum = 0;
        for (int value : values) {
            sum += value;
        }
        return sum;
    }

    private static int computeMean(int sum, int quantity) {
        return sum / quantity;
    }

    private static int countHigher(int[] values, int mean) {
        int higher = 0;
        for (int value : values) {
            if (value > mean) {
                higher++;
            }
        }
        return higher;
    }

    private static int findSpread(int[] values) {
        int low = values[0];
        int high = values[0];

        for (int value : values) {
            if (value < low) {
                low = value;
            }
            if (value > high) {
                high = value;
            }
        }

        return high - low;
    }
}
