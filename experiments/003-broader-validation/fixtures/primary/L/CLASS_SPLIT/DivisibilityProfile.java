import java.util.Scanner;

public class DivisibilityProfile {
    static int divisibleByBoth(int n) {
        int count = 0;
        for (int value = 1; value <= n; value++) {
            if (value % 2 == 0 && value % 3 == 0) count++;
        }
        return count;
    }

    static int divisibleByNeither(int n) {
        int count = 0;
        for (int value = 1; value <= n; value++) {
            if (value % 2 != 0 && value % 3 != 0) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        System.out.println("div2=" + DivisibilityProfileSupport.divisibleBy2(n));
        System.out.println("div3=" + DivisibilityProfileSupport.divisibleBy3(n));
        System.out.println("divBoth=" + divisibleByBoth(n));
        System.out.println("neither=" + divisibleByNeither(n));
    }
}
