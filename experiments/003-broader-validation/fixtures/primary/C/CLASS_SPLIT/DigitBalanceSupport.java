class DigitBalanceSupport {
    static boolean isEven(int digit) {
        return digit % 2 == 0;
    }

    static int evenCount(String digits) {
        int count = 0;
        for (int i = 0; i < digits.length(); i++) {
            if (isEven(digits.charAt(i) - '0')) count++;
        }
        return count;
    }
}
