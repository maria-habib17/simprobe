public class WordAnalysis {
    public static String[] splitWords(String line) {
        return line.trim().split(" +");
    }

    public static int countVowels(String[] words) {
        int count = 0;
        for (String word : words) {
            for (int i = 0; i < word.length(); i++) {
                if (isVowel(word.charAt(i))) {
                    count++;
                }
            }
        }
        return count;
    }

    private static boolean isVowel(char value) {
        char ch = Character.toLowerCase(value);
        return ch == 'a' || ch == 'e' || ch == 'i'
                || ch == 'o' || ch == 'u';
    }

    public static int longestLength(String[] words) {
        int longest = 0;
        for (String word : words) {
            if (word.length() > longest) {
                longest = word.length();
            }
        }
        return longest;
    }
}
