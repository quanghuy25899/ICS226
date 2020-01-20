import java.io.*;
import java.net.*;
import java.net.http.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;
import java.util.regex.*;


public class Crawl {
	public static ArrayList<String> totalURL = new ArrayList<String>();
	public static Map<Integer, String> visitedURL = new HashMap<Integer, String>();
	private static int MAX_LEVELS = 2;
	private static int key = 0;

	public static void connect(String url) {
		synchronized(totalURL) {
			// Specify the URL's pattern
			Pattern pattern = Pattern.compile("href=\"([^\"]*)\"", Pattern.CASE_INSENSITIVE);
			// Search for the match URL in the string url
			Matcher matcher = pattern.matcher(url);

			while(matcher.find()) {
				// Store the found link
				String value = String.valueOf(matcher.group(1));
				// System.out.println("Found value: " + value);
				if (visitedURL.size() == 0) {
					// Add the link the visitedURL dictionary
					visitedURL.put(key, value);
					key++;
					// System.out.println("key: " + key);

					// Add the link to totalURL array
					totalURL.add(value);
					// System.out.println("here if");
					// System.out.println("totalURL:" + totalURL);
					// System.out.println("visitedURL:" + totalURL);
				}
				else {
					// Create a counter
					int count = 0;

					// For each key in visietedURL dictionary
					for (int i : visitedURL.keySet()) {
						// System.out.println("here else");
						// System.out.println("i: " + i);
						// System.out.println("Link to compare: " + value);
						// System.out.println("Visited Link: " + visitedURL.get(i));

						// Check the value in the dictionary with the found link
						if((visitedURL.get(i)).equals(value)) {
							// Check if the link is not in visitedURL, increment the counter
							// If it in the visitedURL, break the loop
							break;
						}
						count++;
						// System.out.println("Count: " + count);
					}
					// System.out.println("visitedURL size: " + visitedURL.size());

					// Check if counter is equal with the visitedURL length,
					// which means the link is not in visitedURL
					// so add the new link
					if(count == (visitedURL.size())) {
						visitedURL.put(key, value);
						key++;
						// System.out.println("key: " + key);
						totalURL.add(value);
						// System.out.println("totalURL: " + totalURL);
						// System.out.println("visitedURL: " + totalURL);
					}
				}
			}
		}
	}
	public static void main(String[]args) {
		ArrayList<URI> urlList = new ArrayList<URI>(); 
		for(String url : args) {
			urlList.add(URI.create("http://" + url));
		}

		System.out.println("totalURL:" + totalURL);

		while (MAX_LEVELS > 0) {
			List<HttpRequest> requests = urlList
				.stream()
				.map(url -> HttpRequest.newBuilder(url))
				.map(reqBuilder -> reqBuilder.build())
				.collect(Collectors.toList());

			HttpClient client = HttpClient.newHttpClient();
			CompletableFuture<?>[] asyncs = requests
				.stream()
				.map(request -> client
					.sendAsync(request, HttpResponse.BodyHandlers.ofString())
					.thenApply(HttpResponse::body)
					.thenAccept(Crawl::connect))
				.toArray(CompletableFuture<?>[]::new);
			CompletableFuture.allOf(asyncs).join();

			urlList.clear();
			for (int j = 0; j<totalURL.size(); j++) {
				// System.out.println("http://" + args[0] + totalURL.get(j));
				urlList.add(URI.create("http://" + args[0] + totalURL.get(j)));
			}

			// Print the total URL
			System.out.println("totalURL:" + totalURL);
			// System.out.println("visitedURL:" + totalURL);
			MAX_LEVELS-=1;
		}
	}
}