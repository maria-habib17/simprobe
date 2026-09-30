import java.util.Scanner;

public class SentenceShape {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String line = scanner.nextLine();
        String[] words = splitWords(line);

        int wordCount = countWords(words);
        int characters = countCharacters(words);
        int longest = findLongest(words);
        int sameStart = countSameStarts(words);

        System.out.println("words=" + wordCount);
        System.out.println("characters=" + characters);
        System.out.println("longest=" + longest);
        System.out.println("sameStart=" + sameStart);
    }

    private static String[] splitWords(String line) {
        return line.split(" ");
    }

    private static int countWords(String[] words) {
        return words.length;
    }

    private static int countCharacters(String[] words) {
        int total = 0;
        for (String word : words) {
            total += word.length();
        }
        return total;
    }

    private static int findLongest(String[] words) {
        int longest = 0;
        for (String word : words) {
            if (word.length() > longest) {
                longest = word.length();
            }
        }
        return longest;
    }

    private static int countSameStarts(String[] words) {
        int matches = 0;

        for (int i = 1; i < words.length; i++) {
            char previous = Character.toLowerCase(words[i - 1].charAt(0));
            char current = Character.toLowerCase(words[i].charAt(0));

            if (previous == current) {
                matches++;
            }
        }

        return matches;
    }
}
