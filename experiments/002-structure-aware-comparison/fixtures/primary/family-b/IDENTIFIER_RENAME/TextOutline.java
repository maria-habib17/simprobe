import java.util.Scanner;

public class TextOutline {
    public static void main(String[] arguments) {
        Scanner input = new Scanner(System.in);
        String text = input.nextLine();
        String[] parts = separateTerms(text);

        int terms = measureTerms(parts);
        int letters = measureLetters(parts);
        int maximum = maximumLength(parts);
        int matching = matchingInitials(parts);

        System.out.println("words=" + terms);
        System.out.println("characters=" + letters);
        System.out.println("longest=" + maximum);
        System.out.println("sameStart=" + matching);
    }

    private static String[] separateTerms(String text) {
        return text.split(" ");
    }

    private static int measureTerms(String[] parts) {
        return parts.length;
    }

    private static int measureLetters(String[] parts) {
        int amount = 0;
        for (String part : parts) {
            amount += part.length();
        }
        return amount;
    }

    private static int maximumLength(String[] parts) {
        int maximum = 0;
        for (String part : parts) {
            if (part.length() > maximum) {
                maximum = part.length();
            }
        }
        return maximum;
    }

    private static int matchingInitials(String[] parts) {
        int matching = 0;

        for (int position = 1; position < parts.length; position++) {
            char left = Character.toLowerCase(parts[position - 1].charAt(0));
            char right = Character.toLowerCase(parts[position].charAt(0));

            if (left == right) {
                matching++;
            }
        }

        return matching;
    }
}
