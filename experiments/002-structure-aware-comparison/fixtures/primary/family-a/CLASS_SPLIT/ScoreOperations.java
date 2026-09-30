class ScoreOperations {
    static int calculateTotal(int[] scores) {
        int total = 0;
        for (int score : scores) {
            total += score;
        }
        return total;
    }

    static int calculateAverage(int total, int count) {
        return total / count;
    }
}
