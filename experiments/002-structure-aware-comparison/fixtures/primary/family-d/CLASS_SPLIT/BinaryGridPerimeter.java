import java.util.Scanner;

public class BinaryGridPerimeter {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int rows = scanner.nextInt();
        int columns = scanner.nextInt();
        String[] grid = readGrid(scanner, rows);

        int ones = countOnes(grid);
        int horizontal = GridLinks.countHorizontal(grid, rows, columns);
        int vertical = GridLinks.countVertical(grid, rows, columns);
        int perimeter = calculatePerimeter(ones, horizontal, vertical);

        System.out.println("ones=" + ones);
        System.out.println("horizontal=" + horizontal);
        System.out.println("vertical=" + vertical);
        System.out.println("perimeter=" + perimeter);
    }

    private static String[] readGrid(Scanner scanner, int rows) {
        String[] grid = new String[rows];
        for (int row = 0; row < rows; row++) {
            grid[row] = scanner.next();
        }
        return grid;
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

    private static int calculatePerimeter(
        int ones,
        int horizontal,
        int vertical
    ) {
        return 4 * ones - 2 * horizontal - 2 * vertical;
    }
}
