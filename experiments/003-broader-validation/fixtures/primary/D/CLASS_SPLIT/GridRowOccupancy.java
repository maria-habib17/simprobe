import java.util.Scanner;

public class GridRowOccupancy {
    static int nonemptyRows(String[] rows) {
        int count = 0;
        for (String row : rows) {
            if (GridRowOccupancySupport.rowOnes(row) > 0) count++;
        }
        return count;
    }

    static int fullRows(String[] rows) {
        int count = 0;
        for (String row : rows) {
            if (GridRowOccupancySupport.rowOnes(row) == row.length()) count++;
        }
        return count;
    }

    static int maxRow(String[] rows) {
        int maximum = 0;
        for (String row : rows) {
            maximum = Math.max(maximum, GridRowOccupancySupport.rowOnes(row));
        }
        return maximum;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int r = scanner.nextInt();
        int c = scanner.nextInt();
        String[] rows = new String[r];
        for (int i = 0; i < r; i++) rows[i] = scanner.next();
        System.out.println("ones=" + GridRowOccupancySupport.totalOnes(rows));
        System.out.println("nonemptyRows=" + nonemptyRows(rows));
        System.out.println("fullRows=" + fullRows(rows));
        System.out.println("maxRow=" + maxRow(rows));
    }
}
