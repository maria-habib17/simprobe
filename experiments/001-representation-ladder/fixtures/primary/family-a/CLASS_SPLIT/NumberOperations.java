public class NumberOperations {
    public static int sum(int[] values) {
        int result = 0;
        for (int value : values) {
            result += value;
        }
        return result;
    }

    public static int min(int[] values) {
        int result = values[0];
        for (int value : values) {
            if (value < result) {
                result = value;
            }
        }
        return result;
    }

    public static int max(int[] values) {
        int result = values[0];
        for (int value : values) {
            if (value > result) {
                result = value;
            }
        }
        return result;
    }

    public static int countEven(int[] values) {
        int result = 0;
        for (int value : values) {
            if (value % 2 == 0) {
                result++;
            }
        }
        return result;
    }
}
