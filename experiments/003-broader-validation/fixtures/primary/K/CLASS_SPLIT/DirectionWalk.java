import java.util.Scanner;

public class DirectionWalk {
    static int distance(String moves) {
        return Math.abs(DirectionWalkSupport.finalX(moves)) + Math.abs(DirectionWalkSupport.finalY(moves));
    }

    static int returnCount(String moves) {
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
        System.out.println("x=" + DirectionWalkSupport.finalX(moves));
        System.out.println("y=" + DirectionWalkSupport.finalY(moves));
        System.out.println("distance=" + distance(moves));
        System.out.println("returns=" + returnCount(moves));
    }
}
