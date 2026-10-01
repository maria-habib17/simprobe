class TemperatureSummarySupport {
    static int minimum(int[] values) {
        int result = values[0];
        for (int value : values) {
            if (value < result) result = value;
        }
        return result;
    }

    static int maximum(int[] values) {
        int result = values[0];
        for (int value : values) {
            if (value > result) result = value;
        }
        return result;
    }
}
