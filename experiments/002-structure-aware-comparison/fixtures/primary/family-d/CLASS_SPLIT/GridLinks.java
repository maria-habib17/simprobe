class GridLinks {
    static int countHorizontal(
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

    static int countVertical(
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
}
