import java.util.Scanner;

public class RunLengthEncoder {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String input = scanner.nextLine();

        StringBuilder result = new StringBuilder();
        char current = input.charAt(0);
        int count = 1;

        for (int i = 1; i < input.length(); i++) {
            char ch = input.charAt(i);

            if (ch == current) {
                count++;
            } else {
                result.append(current).append(count);
                current = ch;
                count = 1;
            }
        }

        result.append(current).append(count);
        System.out.println(result);
    }
}
