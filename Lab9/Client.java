import java.io.*;
import java.net.*;

public class Client {

        protected String serverName;
        protected int serverPort;
        protected String message;
        protected String path = "/home/quanghuy25899/Desktop/";
        protected int buf_size = 1024;

        public Client(String serverName, int serverPort, String message) {
                this.serverName = serverName;
                this.serverPort = serverPort;
                this.message = message;
        }

        public void connect() throws Exception {
                // Concat the file name with file path
                String file_name = path + this.message;
                
                try (
                        Socket socket = new Socket(serverName, serverPort);
                        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                        BufferedInputStream in = new BufferedInputStream(socket.getInputStream());
                ) {
                        // Send data to server
                        out.println(this.message);
                        int count=0;
                        // Create a byte type array to store file data
                        byte[] b = new byte[buf_size];
                        //Open a file to write data
                        BufferedOutputStream fileOut = new BufferedOutputStream(new FileOutputStream(file_name));
                        // System.out.println(in.read(b));
                        while ((count = in.read(b, 0, buf_size)) > 0) {
                                System.out.println(count);
                                // Write data from b array to a file
                                fileOut.write(b, 0, count);
                        }
                        // Flush all old data
                        fileOut.flush();
                        System.out.println("here");
                        // Close the file
                        fileOut.close();
                } catch (UnknownHostException e) {
                        System.err.println(e);
                        System.exit(-1);
                } catch (IOException e) {
                        System.err.println(e);
                        System.exit(-2);
                } catch (SecurityException e) {
                        System.err.println(e);
                        System.exit(-3);
                } catch (IllegalArgumentException e) {
                        System.err.println(e);
                        System.exit(-4);
                }
        }

        public static void main(String[] args) throws Exception {
		if (args.length != 3) {
			System.err.println("Need <host> <port> <message>");
			System.exit(-2);
		}
                Client c = new Client(args[0], Integer.valueOf(args[1]), args[2]);
                c.connect();
        }
}