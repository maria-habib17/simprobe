import java.util.Scanner;

public class ProgramC {
    static boolean operation1(int digit) {
        return digit % 2 == 0;
    }

    static int operation2(String digits) {
        int count = 0;
        for (int i = 0; i < digits.length(); i++) {
            if (operation1(digits.charAt(i) - '0')) count++;
        }
        return count;
    }

    static int operation3(String digits) {
        return digits.length() - operation2(digits);
    }

    static int operation4(String digits, boolean wantEven) {
        int sum = 0;
        for (int i = 0; i < digits.length(); i++) {
            int digit = digits.charAt(i) - '0';
            if (operation1(digit) == wantEven) sum += digit;
        }
        return sum;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String digits = scanner.nextLine();
        System.out.println("even=" + operation2(digits));
        System.out.println("odd=" + operation3(digits));
        System.out.println("evenSum=" + operation4(digits, true));
        System.out.println("oddSum=" + operation4(digits, false));
    }
}
