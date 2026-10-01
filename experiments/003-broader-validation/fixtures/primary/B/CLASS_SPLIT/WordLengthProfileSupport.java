class WordLengthProfileSupport {
    static int shortest(String[] words) {
        int result = words[0].length();
        for (String word : words) {
            if (word.length() < result) result = word.length();
        }
        return result;
    }

    static int longest(String[] words) {
        int result = words[0].length();
        for (String word : words) {
            if (word.length() > result) result = word.length();
        }
        return result;
    }
}
