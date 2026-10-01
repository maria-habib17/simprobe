class GridRowOccupancySupport {
    static int rowOnes(String row) {
        int count = 0;
        for (int i = 0; i < row.length(); i++) {
            if (row.charAt(i) == '1') count++;
        }
        return count;
    }

    static int totalOnes(String[] rows) {
        int total = 0;
        for (String row : rows) total += rowOnes(row);
        return total;
    }
}
