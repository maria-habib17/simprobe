import java.util.Scanner;

public class MatrixDiagonalReport {
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

    static int equalPositions(int[][] matrix) {
        int count = 0;
        int n = matrix.length;
        for (int i = 0; i < n; i++) {
            if (matrix[i][i] == matrix[i][n - 1 - i]) count++;
        }
        return count;
    }

    static int centerValue(int[][] matrix) {
        int n = matrix.length;
        return n % 2 == 1 ? matrix[n / 2][n / 2] : 0;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[][] matrix = new int[n][n];
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) matrix[r][c] = scanner.nextInt();
        }
        System.out.println("main=" + mainDiagonal(matrix));
        System.out.println("anti=" + antiDiagonal(matrix));
        System.out.println("equalPositions=" + equalPositions(matrix));
        System.out.println("center=" + centerValue(matrix));
    }
}
