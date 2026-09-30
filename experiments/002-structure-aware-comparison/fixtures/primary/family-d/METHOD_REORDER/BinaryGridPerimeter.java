import java.util.Scanner;

public class BinaryGridPerimeter {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int rows = scanner.nextInt();
        int columns = scanner.nextInt();
        String[] grid = readGrid(scanner, rows);

        int ones = countOnes(grid);
        int horizontal = countHorizontal(grid, rows, columns);
        int vertical = countVertical(grid, rows, columns);
        int perimeter = calculatePerimeter(ones, horizontal, vertical);

        System.out.println("ones=" + ones);
        System.out.println("horizontal=" + horizontal);
        System.out.println("vertical=" + vertical);
        System.out.println("perimeter=" + perimeter);
    }

    private static int calculatePerimeter(
        int ones,
        int horizontal,
        int vertical
    ) {
        return 4 * ones - 2 * horizontal - 2 * vertical;
    }

    private static int countVertical(
        String[] grid,
        int rows,
        int columns
    ) {
        int pairs = 0;

        for (int row = 1; row < rows; row++) {
            for (int column = 0; column < columns; column++) {
                if (
                    grid[row].charAt(column) == '1'
                    && grid[row - 1].charAt(column) == '1'
                ) {
                    pairs++;
                }
            }
        }

        return pairs;
    }

    private static int countHorizontal(
        String[] grid,
        int rows,
        int columns
    ) {
        int pairs = 0;

        for (int row = 0; row < rows; row++) {
            for (int column = 1; column < columns; column++) {
                if (
                    grid[row].charAt(column) == '1'
                    && grid[row].charAt(column - 1) == '1'
                ) {
                    pairs++;
                }
            }
        }

        return pairs;
    }

    private static int countOnes(String[] grid) {
        int ones = 0;

        for (String line : grid) {
            for (int column = 0; column < line.length(); column++) {
                if (line.charAt(column) == '1') {
                    ones++;
                }
            }
        }

        return ones;
    }

    private static String[] readGrid(Scanner scanner, int rows) {
        String[] grid = new String[rows];
        for (int row = 0; row < rows; row++) {
            grid[row] = scanner.next();
        }
        return grid;
    }
}
