import java.util.Scanner;

public class RunLengthEncoder {
    public static void main(String[] args) {
        Scanner inputReader = new Scanner(System.in);
        String sequence = inputReader.nextLine();
        System.out.println(compressSequence(sequence));
    }

    private static String compressSequence(String sequence) {
        StringBuilder encoded = new StringBuilder();
        char activeSymbol = sequence.charAt(0);
        int runSize = 1;

        for (int position = 1; position < sequence.length(); position++) {
            char nextSymbol = sequence.charAt(position);
            if (nextSymbol == activeSymbol) {
                runSize++;
            } else {
                writeRun(encoded, activeSymbol, runSize);
                activeSymbol = nextSymbol;
                runSize = 1;
            }
        }

        writeRun(encoded, activeSymbol, runSize);
        return encoded.toString();
    }

    private static void writeRun(
            StringBuilder encoded, char symbol, int runSize) {
        encoded.append(symbol).append(runSize);
    }
}
