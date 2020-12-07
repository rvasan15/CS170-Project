import java.util.*;
import java.io.*;


//3 lines that u mess w/ stress max that should be < not <=

public class pritDP {
    static float[][] h, s, dp;
    static float[] totalStress, totalHappiness;
    static float stressThreshold;
    static int bestRooms, n;
    static float S_max;
    static ArrayList<Room> r;
    static int iterations = 0;
    static String outputPath;

    public static void main(String[] args) {
        n = 50;
        parse(args[0]);
        outputPath = args[1];
        Room.totalRooms = 0;

        // Storing happiness and stress values for all possible rooms
        totalHappiness = new float[1 << n];
        totalStress = new float[1 << n];

        // Get the initial time when we start running the code
        long time = System.currentTimeMillis();

        // Go through all possible room possibilities and set the happiness/stress values of that room
        for (int i = 0; i < (1 << n); i++) {
            // Don't need to worry about rooms with one value
            if (Integer.bitCount(i) < 2) continue;

            // Create the room based on the bits in i
            ArrayList<Integer> set = new ArrayList<>();
            for (int j = 0; j < n; j++) {
                if (((i >> j) & 1) == 1) {
                    set.add(j);
                }
            }

            // Set the happiness of that bit mask based on the values in the room
            // Check every student with every other student
            for (int a = 0; a < set.size(); a++) {
                for (int b = a + 1; b < set.size(); b++) {
                    totalHappiness[i] += h[set.get(a)][set.get(b)];
                    totalStress[i] += s[set.get(a)][set.get(b)];
                }
            }
        }

        // Arraylist which represents our room
        r = new ArrayList<>();
        float res = -1;
        bestRooms = n;

        // Traverse through max room sizes 1 - 5
        for (int rooms = 1; rooms <= n; rooms++) {
            // Create an array for max happiness given the rooms
            dp = new float[1 << n][rooms + 1];
            for (int i = 0; i < (1 << n); i++) {
                Arrays.fill(dp[i], -1);
            }

            System.out.println("Here!");

            // Max stress for this room configuration
            stressThreshold = S_max / rooms;

            // Default case is 0
            dp[0][0] = 0;

            float maxHappiness = dfs((1 << n) - 1, rooms);

            // Check if the happiness improved
            System.out.println("Rooms: " + rooms + " MaxHappiness: " + maxHappiness);
            if (maxHappiness > res) {
                res = maxHappiness;
                bestRooms = rooms;
            }
        }

        // Print out the best happiness that we found
        System.out.println("Maximum Happiness Attainable: " + res);

        // Create the best room combination from what we found
        dp = new float[1 << n][bestRooms + 1];
        for (float[] arr : dp) Arrays.fill(arr, -1);
        stressThreshold = S_max / bestRooms;
        dp[0][0] = 0;
        for (int i = 0; i < (1 << n) - 1; i++) {
            if (Integer.bitCount(i) == 1) dp[i][1] = 0;
        }

        // Run dfs on the best number of rooms we had
        dfs((1 << n) - 1, bestRooms);
        generateRooms((1 << n) - 1, bestRooms);

        // Print the room configurations that we found and write it to the file
        writeAndPrintRooms();
        System.out.println("Time: " + (System.currentTimeMillis() - time));
        System.out.println("Num dfs calls: " + iterations);
    }

    private static void writeAndPrintRooms() {
        // Print the room configurations to the term
        for (Room room : r) {
            System.out.print("Room " + room.index + ": ");
            for (Integer i : room.members) {
                System.out.print(i + " ");
            }
            System.out.println();
        }

        // Write to a file
        try {
            // Create a printwriter which can be used to print outputs to files
            PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter(outputPath)));
            for (Room room : r) {
                for (Integer i : room.members) {
                    // Print in the format -> <node> <room>
                    pw.println(i + " " + room.index);
                }
            }
            pw.close();

            // Catching an IOE exception
        } catch (Exception e) {
            System.out.println(e);
        }
    }

    private static void parse(String filepath) {
        // Create the file and scanner we will be using
        File input = new File(filepath);
        Scanner scan;
        try {
            scan = new Scanner(input);
        } catch (Exception e) {
            System.out.println("File Read Error!");
            return;
        }

        // Declare our static class variables
        n = scan.nextInt();
        S_max = (float) scan.nextDouble();

        h = new float[n][n];
        s = new float[n][n];

        // Scan in the everything from the file
        while (scan.hasNextInt()) {
            // Scan in the pair of students
            int i = scan.nextInt();
            int j = scan.nextInt();

            // Scan in happiness and stress values and store them
            float hap = (float) scan.nextDouble();
            float stress = (float) scan.nextDouble();
            h[i][j] = hap;
            s[i][j] = stress;
            h[j][i] = hap;
            s[j][i] = stress;
        }

        // Close the scanner
        scan.close();
    }


    // assume we use k rooms.
    //dp[mask][r] = maximum happiness we can get using the
    //subset of people in mask using r rooms s.t. stress is under S_max / k
    // 0011100011 - the subset we are considering is 7, 6, 5, 0, 1

    static float dfs(int mask, int rooms) {
        iterations += 1;
        if (rooms == 0) {
            if (Integer.bitCount(mask) == 0) return dp[mask][rooms] = 0;
            else return dp[mask][rooms] = Integer.MIN_VALUE;
        } else if (rooms == 1) {
            if (totalStress[mask] <= stressThreshold) return dp[mask][rooms] = totalHappiness[mask];
            else return dp[mask][rooms] = Integer.MIN_VALUE;
        }

        if (rooms > Integer.bitCount(mask)) return Integer.MIN_VALUE;
        if (dp[mask][rooms] != -1) return dp[mask][rooms];

        float res = Integer.MIN_VALUE;
        for (int i = mask; i > 0; i = (i - 1) & mask) {
            if (totalStress[i] <= stressThreshold) {
                res = Math.max(res, totalHappiness[i] + dfs(mask ^ i, rooms - 1));
            }
        }

        return dp[mask][rooms] = res;
    }

    static void generateRooms(int mask, int rooms) {
        if (Integer.bitCount(mask) == 0) return;
        for (int i = mask; i > 0; i = (i - 1) & mask) {
            if (dp[mask][rooms] == dp[mask ^ i][rooms - 1] + totalHappiness[i] && totalStress[i] <= S_max / bestRooms) {
                r.add(Room.createRoom(i));
                generateRooms(mask ^ i, rooms - 1);
                return;
            }
        }
    }

    static class Room {
        static int totalRooms;
        int index;
        ArrayList<Integer> members;

        Room(int index) {
            this.index = index;
            members = new ArrayList<>();
        }

        static Room createRoom(int mask) {
            Room newRoom = new Room(totalRooms++);
            for (int i = 0; i < n; i++) {
                if (((mask >> i) & 1) == 1) {
                    newRoom.members.add(i);
                }
            }
            return newRoom;
        }
    }
}
