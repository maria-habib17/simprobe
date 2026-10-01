import java.util.Scanner;

public class DigitBalance {
    static int oddCount(String digits) {
        return digits.length() - DigitBalanceSupport.evenCount(digits);
    }

    static int digitSum(String digits, boolean wantEven) {
        int sum = 0;
        for (int i = 0; i < digits.length(); i++) {
            int digit = digits.charAt(i) - '0';
            if (DigitBalanceSupport.isEven(digit) == wantEven) sum += digit;
        }
        return sum;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String digits = scanner.nextLine();
        System.out.println("even=" + DigitBalanceSupport.evenCount(digits));
        System.out.println("odd=" + oddCount(digits));
        System.out.println("evenSum=" + digitSum(digits, true));
        System.out.println("oddSum=" + digitSum(digits, false));
    }
}
