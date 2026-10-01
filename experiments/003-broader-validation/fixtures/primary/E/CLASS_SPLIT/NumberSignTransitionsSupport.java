class NumberSignTransitionsSupport {
    static boolean isPositive(int value) {
        return value > 0;
    }

    static int positiveCount(int[] values) {
        int count = 0;
        for (int value : values) {
            if (isPositive(value)) count++;
        }
        return count;
    }
}
