import java.util.Scanner;

public class DigitBalance {
    static int digitSum(String digits, boolean wantEven) {
        int sum = 0;
        for (int i = 0; i < digits.length(); i++) {
            int digit = digits.charAt(i) - '0';
            if (isEven(digit) == wantEven) sum += digit;
        }
        return sum;
    }

    static int oddCount(String digits) {
        return digits.length() - evenCount(digits);
    }

    static int evenCount(String digits) {
        int count = 0;
        for (int i = 0; i < digits.length(); i++) {
            if (isEven(digits.charAt(i) - '0')) count++;
        }
        return count;
    }

    static boolean isEven(int digit) {
        return digit % 2 == 0;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String digits = scanner.nextLine();
        System.out.println("even=" + evenCount(digits));
        System.out.println("odd=" + oddCount(digits));
        System.out.println("evenSum=" + digitSum(digits, true));
        System.out.println("oddSum=" + digitSum(digits, false));
    }
}
