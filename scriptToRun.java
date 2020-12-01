import java.io.File;
//import pritDP;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class scriptToRun {
    public static void main(String[] args) {
        //args should be: inputs, outputs, [name], [start_filenum_range], [end_filenum_range]
        File input_dir = new File(args[0]);
        File output_dir = new File(args[1]);
        int startRange = Integer.parseInt(args[2]);
        int endRange = Integer.parseInt(args[3]);
//        System.out.println(input_dir.toPath());
//        System.out.println(output_dir);
//        System.out.println(username);
        File[] directoryListing = input_dir.listFiles();
        if (directoryListing != null) {
            for (File child : directoryListing) {



                String filename = child.toString();
                //System.out.println("here");


                String pattern = "(.*)\\/(.*)";
                Pattern r = Pattern.compile(pattern);
                Matcher m = r.matcher(filename);
                if (m.find()) {
                    filename = m.group(2);
                }
                //System.out.println("here1");

                if (!filename.substring(filename.length()-3).equals(".in")) {
                    //System.out.println(filename);
                    continue;
                }
                //System.out.println("here1.5");
                filename = filename.substring(0, filename.length()-3);
                String[] pritArgs = new String[2];

                pattern = "(.*)-(.*)";
                r = Pattern.compile(pattern);
                m = r.matcher(filename);
                String str = "";
                if (m.find()) {
                    str = m.group(2);
                }
                int filenum = Integer.parseInt(str);

                if ((filenum <= endRange) && (filenum >= startRange)) {
                    //System.out.println("here2");
                    pritArgs[0] = child.toString();
                    pritArgs[1] = output_dir.toString() + "/" + filename + ".out";
//                    System.out.println();
//                    System.out.println(pritArgs[0]);
//                    System.out.println(pritArgs[1]);
//                    System.out.println();
                    pritDP.main(pritArgs);
//                    System.out.println("made it");
//                    System.out.println("here3");
                }


                // Do something with child
            }
        } else {
            // Handle the case where dir is not really a directory.
            // Checking dir.isDirectory() above would not be sufficient
            // to avoid race conditions with another process that deletes
            // directories.
            return;
        }



    }
}
