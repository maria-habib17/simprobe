class DivisibilityProfileSupport {
    static int divisibleBy2(int n) {
        int count = 0;
        for (int value = 1; value <= n; value++) {
            if (value % 2 == 0) count++;
        }
        return count;
    }

    static int divisibleBy3(int n) {
        int count = 0;
        for (int value = 1; value <= n; value++) {
            if (value % 3 == 0) count++;
        }
        return count;
    }
}
