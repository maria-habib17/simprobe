import java.util.Scanner;

public class ProgramL {
    static int operation1(int n) {
        int count = 0;
        for (int value = 1; value <= n; value++) {
            if (value % 2 == 0) count++;
        }
        return count;
    }

    static int operation2(int n) {
        int count = 0;
        for (int value = 1; value <= n; value++) {
            if (value % 3 == 0) count++;
        }
        return count;
    }

    static int operation3(int n) {
        int count = 0;
        for (int value = 1; value <= n; value++) {
            if (value % 2 == 0 && value % 3 == 0) count++;
        }
        return count;
    }

    static int operation4(int n) {
        int count = 0;
        for (int value = 1; value <= n; value++) {
            if (value % 2 != 0 && value % 3 != 0) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        System.out.println("div2=" + operation1(n));
        System.out.println("div3=" + operation2(n));
        System.out.println("divBoth=" + operation3(n));
        System.out.println("neither=" + operation4(n));
    }
}
