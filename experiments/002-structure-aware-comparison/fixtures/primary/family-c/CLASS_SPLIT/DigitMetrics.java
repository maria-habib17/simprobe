class DigitMetrics {
    static int countChanges(String digits) {
        int changes = 0;

        for (int i = 1; i < digits.length(); i++) {
            if (digits.charAt(i) != digits.charAt(i - 1)) {
                changes++;
            }
        }

        return changes;
    }

    static int weightedSum(String digits) {
        int total = 0;

        for (int i = 0; i < digits.length(); i++) {
            int value = digits.charAt(i) - '0';
            total += value * (i + 1);
        }

        return total;
    }
}
