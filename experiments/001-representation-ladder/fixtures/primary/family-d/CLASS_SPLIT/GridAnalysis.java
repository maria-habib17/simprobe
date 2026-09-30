public class GridAnalysis {
    public static int countOnes(String[] grid, int rows, int columns) {
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

    public static int countLinks(String[] grid, int rows, int columns) {
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
