import java.util.Scanner;

public class ProgramK {
    static int operation1(String moves) {
        int x = 0;
        for (int i = 0; i < moves.length(); i++) {
            if (moves.charAt(i) == 'E') x++;
            if (moves.charAt(i) == 'W') x--;
        }
        return x;
    }

    static int operation2(String moves) {
        int y = 0;
        for (int i = 0; i < moves.length(); i++) {
            if (moves.charAt(i) == 'N') y++;
            if (moves.charAt(i) == 'S') y--;
        }
        return y;
    }

    static int operation3(String moves) {
        return Math.abs(operation1(moves)) + Math.abs(operation2(moves));
    }

    static int operation4(String moves) {
        int x = 0;
        int y = 0;
        int count = 0;
        for (int i = 0; i < moves.length(); i++) {
            char move = moves.charAt(i);
            if (move == 'N') y++;
            if (move == 'S') y--;
            if (move == 'E') x++;
            if (move == 'W') x--;
            if (x == 0 && y == 0) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String moves = scanner.nextLine();
        System.out.println("x=" + operation1(moves));
        System.out.println("y=" + operation2(moves));
        System.out.println("distance=" + operation3(moves));
        System.out.println("returns=" + operation4(moves));
    }
}
