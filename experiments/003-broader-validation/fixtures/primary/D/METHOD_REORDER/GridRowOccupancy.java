import java.util.Scanner;

public class GridRowOccupancy {
    static int maxRow(String[] rows) {
        int maximum = 0;
        for (String row : rows) {
            maximum = Math.max(maximum, rowOnes(row));
        }
        return maximum;
    }

    static int fullRows(String[] rows) {
        int count = 0;
        for (String row : rows) {
            if (rowOnes(row) == row.length()) count++;
        }
        return count;
    }

    static int nonemptyRows(String[] rows) {
        int count = 0;
        for (String row : rows) {
            if (rowOnes(row) > 0) count++;
        }
        return count;
    }

    static int totalOnes(String[] rows) {
        int total = 0;
        for (String row : rows) total += rowOnes(row);
        return total;
    }

    static int rowOnes(String row) {
        int count = 0;
        for (int i = 0; i < row.length(); i++) {
            if (row.charAt(i) == '1') count++;
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int r = scanner.nextInt();
        int c = scanner.nextInt();
        String[] rows = new String[r];
        for (int i = 0; i < r; i++) rows[i] = scanner.next();
        System.out.println("ones=" + totalOnes(rows));
        System.out.println("nonemptyRows=" + nonemptyRows(rows));
        System.out.println("fullRows=" + fullRows(rows));
        System.out.println("maxRow=" + maxRow(rows));
    }
}
