class WordMetrics {
    static int countCharacters(String[] words) {
        int total = 0;
        for (String word : words) {
            total += word.length();
        }
        return total;
    }

    static int findLongest(String[] words) {
        int longest = 0;
        for (String word : words) {
            if (word.length() > longest) {
                longest = word.length();
            }
        }
        return longest;
    }
}
