import java.net.*;
import java.io.*;
import java.nio.channels.*;

public class Server {

        protected final String HOST = "";
        protected int port;
        protected String path = "/home/quanghuy25899/Desktop/226Lab9/";
        protected int buf_size = 1024;

        public Server(int port) {
                this.port = port;
        }

        void serve() {
                try (
                        ServerSocket serverSocket = new ServerSocket(port);
                        Socket clientSocket = serverSocket.accept();
                        BufferedOutputStream out = new BufferedOutputStream(clientSocket.getOutputStream(), buf_size);
                        BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                ) {
                        // Read in from Client
                        String inputLine = in.readLine();

                        // Concat the file name with file path
                        String file_name = path + inputLine;

                        // Open file then create a input stream
                        BufferedInputStream fileIn = new BufferedInputStream(new FileInputStream(file_name));

                        // Byte type array to store file data
                        byte[] buf = new byte[buf_size];
                        int count;
                        while ((count = fileIn.read(buf, 0, buf_size)) != -1) {
                                // Send data to client
                                out.write(buf, 0, count);
                                System.out.println(count);
                                // System.out.println(buf);
                        }
                        // Flush all old data
                        out.flush();
                        System.out.println("here");
                        // Close the file and the input stream
                        fileIn.close();

                } catch (IOException e) {
                        System.err.println(e);
                        System.exit(-2);
                } catch (SecurityException e) {
                        System.err.println(e);
                        System.exit(-3);
                } catch (IllegalArgumentException e) {
                        System.err.println(e);
                        System.exit(-4);
                } catch (IllegalBlockingModeException e) {
                        System.err.println(e);
                        System.exit(-6);
                }
        }

        public static void main(String[] args) {
		if (args.length != 1) {
			System.err.println("Need <port>");
			System.exit(-99);
		}
                Server s = new Server(Integer.valueOf(args[0]));
                s.serve();
        }
}