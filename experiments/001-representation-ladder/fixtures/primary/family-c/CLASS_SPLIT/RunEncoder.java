public class RunEncoder {
    public static String encode(String input) {
        StringBuilder result = new StringBuilder();
        char current = input.charAt(0);
        int count = 1;

        for (int i = 1; i < input.length(); i++) {
            char ch = input.charAt(i);
            if (ch == current) {
                count++;
            } else {
                appendRun(result, current, count);
                current = ch;
                count = 1;
            }
        }

        appendRun(result, current, count);
        return result.toString();
    }

    private static void appendRun(StringBuilder result, char value, int count) {
        result.append(value).append(count);
    }
}
