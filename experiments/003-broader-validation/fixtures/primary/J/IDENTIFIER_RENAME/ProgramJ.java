import java.util.Scanner;

public class ProgramJ {
    static int operation1(int[] values) {
        int count = 0;
        for (int i = 1; i < values.length; i++) {
            if (values[i] == values[i - 1]) count++;
        }
        return count;
    }

    static int operation2(int[] values) {
        int count = 0;
        for (int i = 1; i < values.length; i++) {
            if (values[i] > values[i - 1]) count++;
        }
        return count;
    }

    static int operation3(int[] values) {
        int maximum = 0;
        for (int i = 1; i < values.length; i++) {
            int gap = values[i] - values[i - 1];
            if (gap > maximum) maximum = gap;
        }
        return maximum;
    }

    static int operation4(int[] values) {
        return values[values.length - 1] - values[0];
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] values = new int[n];
        for (int i = 0; i < n; i++) values[i] = scanner.nextInt();
        System.out.println("duplicates=" + operation1(values));
        System.out.println("positiveGaps=" + operation2(values));
        System.out.println("maxGap=" + operation3(values));
        System.out.println("span=" + operation4(values));
    }
}
