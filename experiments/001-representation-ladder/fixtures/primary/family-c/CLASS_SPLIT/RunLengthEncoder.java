import java.util.Scanner;

public class RunLengthEncoder {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String input = scanner.nextLine();
        System.out.println(RunEncoder.encode(input));
    }
}
