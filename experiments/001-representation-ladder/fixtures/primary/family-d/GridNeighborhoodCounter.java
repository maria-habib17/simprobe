import java.util.Scanner;

public class GridNeighborhoodCounter {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int rows = scanner.nextInt();
        int columns = scanner.nextInt();
        String[] grid = new String[rows];

        for (int row = 0; row < rows; row++) {
            grid[row] = scanner.next();
        }

        int ones = 0;
        int links = 0;

        for (int row = 0; row < rows; row++) {
            for (int column = 0; column < columns; column++) {
                if (grid[row].charAt(column) == '1') {
                    ones++;

                    if (column + 1 < columns &&
                        grid[row].charAt(column + 1) == '1') {
                        links++;
                    }

                    if (row + 1 < rows &&
                        grid[row + 1].charAt(column) == '1') {
                        links++;
                    }
                }
            }
        }

        System.out.println("ones=" + ones);
        System.out.println("links=" + links);
    }
}
