import java.util.Scanner;

public class NumberSummary {
    public static void main(String[] args) {
        Scanner inputReader = new Scanner(System.in);
        int quantity = inputReader.nextInt();
        int[] numbers = loadNumbers(inputReader, quantity);

        System.out.println("sum=" + calculateTotal(numbers));
        System.out.println("min=" + findMinimum(numbers));
        System.out.println("max=" + findMaximum(numbers));
        System.out.println("even=" + calculateEvenCount(numbers));
    }

    private static int[] loadNumbers(Scanner inputReader, int quantity) {
        int[] numbers = new int[quantity];
        for (int position = 0; position < quantity; position++) {
            numbers[position] = inputReader.nextInt();
        }
        return numbers;
    }

    private static int calculateTotal(int[] numbers) {
        int aggregate = 0;
        for (int element : numbers) {
            aggregate += element;
        }
        return aggregate;
    }

    private static int findMinimum(int[] numbers) {
        int aggregate = numbers[0];
        for (int element : numbers) {
            if (element < aggregate) {
                aggregate = element;
            }
        }
        return aggregate;
    }

    private static int findMaximum(int[] numbers) {
        int aggregate = numbers[0];
        for (int element : numbers) {
            if (element > aggregate) {
                aggregate = element;
            }
        }
        return aggregate;
    }

    private static int calculateEvenCount(int[] numbers) {
        int aggregate = 0;
        for (int element : numbers) {
            if (element % 2 == 0) {
                aggregate++;
            }
        }
        return aggregate;
    }
}
