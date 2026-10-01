class PrefixSumPeaksSupport {
    static int finalSum(int[] values) {
        int sum = 0;
        for (int value : values) sum += value;
        return sum;
    }

    static int maximumPrefix(int[] values) {
        int sum = 0;
        int maximum = Integer.MIN_VALUE;
        for (int value : values) {
            sum += value;
            if (sum > maximum) maximum = sum;
        }
        return maximum;
    }
}
