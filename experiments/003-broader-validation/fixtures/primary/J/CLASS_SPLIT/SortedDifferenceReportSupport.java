class SortedDifferenceReportSupport {
    static int duplicateCount(int[] values) {
        int count = 0;
        for (int i = 1; i < values.length; i++) {
            if (values[i] == values[i - 1]) count++;
        }
        return count;
    }

    static int positiveGapCount(int[] values) {
        int count = 0;
        for (int i = 1; i < values.length; i++) {
            if (values[i] > values[i - 1]) count++;
        }
        return count;
    }
}
