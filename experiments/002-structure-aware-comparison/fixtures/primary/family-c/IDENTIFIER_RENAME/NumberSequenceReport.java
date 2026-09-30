import java.util.Scanner;

public class NumberSequenceReport {
    public static void main(String[] arguments) {
        Scanner input = new Scanner(System.in);
        String sequence = input.nextLine();

        int groups = measureGroups(sequence);
        int maximum = maximumGroup(sequence);
        int transitions = measureTransitions(sequence);
        int positional = positionalTotal(sequence);

        System.out.println("runs=" + groups);
        System.out.println("longest=" + maximum);
        System.out.println("changes=" + transitions);
        System.out.println("weighted=" + positional);
    }

    private static int measureGroups(String sequence) {
        int groups = 1;

        for (int position = 1; position < sequence.length(); position++) {
            if (sequence.charAt(position) != sequence.charAt(position - 1)) {
                groups++;
            }
        }

        return groups;
    }

    private static int maximumGroup(String sequence) {
        int maximum = 1;
        int active = 1;

        for (int position = 1; position < sequence.length(); position++) {
            if (sequence.charAt(position) == sequence.charAt(position - 1)) {
                active++;
                if (active > maximum) {
                    maximum = active;
                }
            } else {
                active = 1;
            }
        }

        return maximum;
    }

    private static int measureTransitions(String sequence) {
        int transitions = 0;

        for (int position = 1; position < sequence.length(); position++) {
            if (sequence.charAt(position) != sequence.charAt(position - 1)) {
                transitions++;
            }
        }

        return transitions;
    }

    private static int positionalTotal(String sequence) {
        int result = 0;

        for (int position = 0; position < sequence.length(); position++) {
            int digit = sequence.charAt(position) - '0';
            result += digit * (position + 1);
        }

        return result;
    }
}
