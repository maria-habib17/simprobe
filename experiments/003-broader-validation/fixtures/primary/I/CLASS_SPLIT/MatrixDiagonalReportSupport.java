class MatrixDiagonalReportSupport {
    static int mainDiagonal(int[][] matrix) {
        int sum = 0;
        for (int i = 0; i < matrix.length; i++) sum += matrix[i][i];
        return sum;
    }

    static int antiDiagonal(int[][] matrix) {
        int sum = 0;
        int n = matrix.length;
        for (int i = 0; i < n; i++) sum += matrix[i][n - 1 - i];
        return sum;
    }
}
