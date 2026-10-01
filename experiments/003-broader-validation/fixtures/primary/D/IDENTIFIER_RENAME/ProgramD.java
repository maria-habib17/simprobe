import java.util.Scanner;

public class ProgramD {
    static int operation1(String row) {
        int count = 0;
        for (int i = 0; i < row.length(); i++) {
            if (row.charAt(i) == '1') count++;
        }
        return count;
    }

    static int operation2(String[] rows) {
        int total = 0;
        for (String row : rows) total += operation1(row);
        return total;
    }

    static int operation3(String[] rows) {
        int count = 0;
        for (String row : rows) {
            if (operation1(row) > 0) count++;
        }
        return count;
    }

    static int operation4(String[] rows) {
        int count = 0;
        for (String row : rows) {
            if (operation1(row) == row.length()) count++;
        }
        return count;
    }

    static int operation5(String[] rows) {
        int maximum = 0;
        for (String row : rows) {
            maximum = Math.max(maximum, operation1(row));
        }
        return maximum;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int r = scanner.nextInt();
        int c = scanner.nextInt();
        String[] rows = new String[r];
        for (int i = 0; i < r; i++) rows[i] = scanner.next();
        System.out.println("ones=" + operation2(rows));
        System.out.println("nonemptyRows=" + operation3(rows));
        System.out.println("fullRows=" + operation4(rows));
        System.out.println("maxRow=" + operation5(rows));
    }
}
