import java.util.Scanner;

public class OccupiedCellBoundary {
    public static void main(String[] arguments) {
        Scanner input = new Scanner(System.in);
        int height = input.nextInt();
        int width = input.nextInt();
        String[] cells = loadCells(input, height);

        int occupied = measureOccupied(cells);
        int across = measureAcross(cells, height, width);
        int down = measureDown(cells, height, width);
        int boundary = computeBoundary(occupied, across, down);

        System.out.println("ones=" + occupied);
        System.out.println("horizontal=" + across);
        System.out.println("vertical=" + down);
        System.out.println("perimeter=" + boundary);
    }

    private static String[] loadCells(Scanner input, int height) {
        String[] cells = new String[height];
        for (int y = 0; y < height; y++) {
            cells[y] = input.next();
        }
        return cells;
    }

    private static int measureOccupied(String[] cells) {
        int occupied = 0;

        for (String line : cells) {
            for (int x = 0; x < line.length(); x++) {
                if (line.charAt(x) == '1') {
                    occupied++;
                }
            }
        }

        return occupied;
    }

    private static int measureAcross(
        String[] cells,
        int height,
        int width
    ) {
        int links = 0;

        for (int y = 0; y < height; y++) {
            for (int x = 1; x < width; x++) {
                if (
                    cells[y].charAt(x) == '1'
                    && cells[y].charAt(x - 1) == '1'
                ) {
                    links++;
                }
            }
        }

        return links;
    }

    private static int measureDown(
        String[] cells,
        int height,
        int width
    ) {
        int links = 0;

        for (int y = 1; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if (
                    cells[y].charAt(x) == '1'
                    && cells[y - 1].charAt(x) == '1'
                ) {
                    links++;
                }
            }
        }

        return links;
    }

    private static int computeBoundary(
        int occupied,
        int across,
        int down
    ) {
        return 4 * occupied - 2 * across - 2 * down;
    }
}
