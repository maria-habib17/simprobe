class DirectionWalkSupport {
    static int finalX(String moves) {
        int x = 0;
        for (int i = 0; i < moves.length(); i++) {
            if (moves.charAt(i) == 'E') x++;
            if (moves.charAt(i) == 'W') x--;
        }
        return x;
    }

    static int finalY(String moves) {
        int y = 0;
        for (int i = 0; i < moves.length(); i++) {
            if (moves.charAt(i) == 'N') y++;
            if (moves.charAt(i) == 'S') y--;
        }
        return y;
    }
}
