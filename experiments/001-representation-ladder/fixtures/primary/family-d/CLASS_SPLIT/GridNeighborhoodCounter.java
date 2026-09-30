import java.util.Scanner;

public class GridNeighborhoodCounter {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int rows = scanner.nextInt();
        int columns = scanner.nextInt();
        String[] grid = readGrid(scanner, rows);

        System.out.println(
                "ones=" + GridAnalysis.countOnes(grid, rows, columns));
        System.out.println(
                "links=" + GridAnalysis.countLinks(grid, rows, columns));
    }

    private static String[] readGrid(Scanner scanner, int rows) {
        String[] grid = new String[rows];
        for (int row = 0; row < rows; row++) {
            grid[row] = scanner.next();
        }
        return grid;
    }
}
