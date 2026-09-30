import java.util.Scanner;

public class GridNeighborhoodCounter {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int rows = scanner.nextInt();
        int columns = scanner.nextInt();
        String[] grid = readGrid(scanner, rows);

        System.out.println("ones=" + countOnes(grid, rows, columns));
        System.out.println("links=" + countLinks(grid, rows, columns));
    }

    private static String[] readGrid(Scanner scanner, int rows) {
        String[] grid = new String[rows];
        for (int row = 0; row < rows; row++) {
            grid[row] = scanner.next();
        }
        return grid;
    }

    private static int countOnes(String[] grid, int rows, int columns) {
        int count = 0;
        for (int row = 0; row < rows; row++) {
            for (int column = 0; column < columns; column++) {
                if (grid[row].charAt(column) == '1') {
                    count++;
                }
            }
        }
        return count;
    }

    private static int countLinks(String[] grid, int rows, int columns) {
        int links = 0;
        for (int row = 0; row < rows; row++) {
            for (int column = 0; column < columns; column++) {
                if (grid[row].charAt(column) != '1') {
                    continue;
                }

                if (hasRightNeighbor(grid, row, column, columns)) {
                    links++;
                }

                if (hasBelowNeighbor(grid, row, column, rows)) {
                    links++;
                }
            }
        }
        return links;
    }

    private static boolean hasRightNeighbor(
            String[] grid, int row, int column, int columns) {
        return column + 1 < columns
                && grid[row].charAt(column + 1) == '1';
    }

    private static boolean hasBelowNeighbor(
            String[] grid, int row, int column, int rows) {
        return row + 1 < rows
                && grid[row + 1].charAt(column) == '1';
    }
}
