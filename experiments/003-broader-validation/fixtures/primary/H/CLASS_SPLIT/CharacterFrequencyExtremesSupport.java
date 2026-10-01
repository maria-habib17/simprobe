class CharacterFrequencyExtremesSupport {
    static int[] frequencies(String word) {
        int[] counts = new int[26];
        for (int i = 0; i < word.length(); i++) {
            counts[word.charAt(i) - 'a']++;
        }
        return counts;
    }

    static int distinctCount(int[] counts) {
        int distinct = 0;
        for (int count : counts) {
            if (count > 0) distinct++;
        }
        return distinct;
    }
}
