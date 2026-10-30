import java.util.Arrays;

public class MergeArrays {
    public static void main(String[] args) {
        int[] first = {1, 4, 9};
        int[] secnd = {2, 3, 7, 11};
        int[] res = new int[first.length + secnd.length];
        int i = 0;
        int j = 0;
        int k = 0;
        while (i < first.length && j < secnd.length) {
            if (first[i] <= secnd[j]) {
                res[k++] = first[i++];
            } else {
                res[k++] = secnd[j++];
            }
        }
        while (i < first.length) {
            res[k++] = first[i++];
        }
        while (j < secnd.length) {
            res[k++] = secnd[j++];
        }
        System.out.println(Arrays.toString(res));
    }
}