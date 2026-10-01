import java.util.Scanner;

public class ProgramI {
    static int operation1(int[][] matrix) {
        int sum = 0;
        for (int i = 0; i < matrix.length; i++) sum += matrix[i][i];
        return sum;
    }

    static int operation2(int[][] matrix) {
        int sum = 0;
        int n = matrix.length;
        for (int i = 0; i < n; i++) sum += matrix[i][n - 1 - i];
        return sum;
    }

    static int operation3(int[][] matrix) {
        int count = 0;
        int n = matrix.length;
        for (int i = 0; i < n; i++) {
            if (matrix[i][i] == matrix[i][n - 1 - i]) count++;
        }
        return count;
    }

    static int operation4(int[][] matrix) {
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
        System.out.println("main=" + operation1(matrix));
        System.out.println("anti=" + operation2(matrix));
        System.out.println("equalPositions=" + operation3(matrix));
        System.out.println("center=" + operation4(matrix));
    }
}
