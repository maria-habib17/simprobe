import java.util.Scanner;

public class GridNeighborhoodCounter {
    public static void main(String[] args) {
        Scanner inputReader = new Scanner(System.in);
        int height = inputReader.nextInt();
        int width = inputReader.nextInt();
        String[] cells = loadCells(inputReader, height);

        System.out.println("ones=" + calculateOccupied(cells, height, width));
        System.out.println("links=" + calculateConnections(cells, height, width));
    }

    private static String[] loadCells(Scanner inputReader, int height) {
        String[] cells = new String[height];
        for (int y = 0; y < height; y++) {
            cells[y] = inputReader.next();
        }
        return cells;
    }

    private static int calculateOccupied(
            String[] cells, int height, int width) {
        int total = 0;
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if (cells[y].charAt(x) == '1') {
                    total++;
                }
            }
        }
        return total;
    }

    private static int calculateConnections(
            String[] cells, int height, int width) {
        int connections = 0;
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if (cells[y].charAt(x) != '1') {
                    continue;
                }

                if (rightIsOccupied(cells, y, x, width)) {
                    connections++;
                }

                if (belowIsOccupied(cells, y, x, height)) {
                    connections++;
                }
            }
        }
        return connections;
    }

    private static boolean rightIsOccupied(
            String[] cells, int y, int x, int width) {
        return x + 1 < width && cells[y].charAt(x + 1) == '1';
    }

    private static boolean belowIsOccupied(
            String[] cells, int y, int x, int height) {
        return y + 1 < height && cells[y + 1].charAt(x) == '1';
    }
}
