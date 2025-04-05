## ghost ide theme

#### You can add your own themes to this repository, but there are a number of conditions that must be met.

- The rule is that a theme name must be valid.
- The second rule is that the theme logo must be in webp format, or the preview.
- Rule 3: You have no restrictions. Please test the theme and then publish it. Thank you.
- The fourth rule, which is the most important, is if you can add the theme and preview image to the json file. If you don't know json, it's no problem. I'll add it myself. We also provide you with a Java code that you can implement to automatically add themes to json.

***Welcome to the Ghostide family***




```java

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.List;

public class GitHubDownloder {

    private static final String GITHUB_API_BASE = "https://api.github.com";
    private static final String GITHUB_RAW_BASE = "https://raw.githubusercontent.com";

    private final String authToken;
    private final OkHttpClient client;

    public GitHubDownloder(String authToken) {
        this.authToken = authToken;
        this.client = new OkHttpClient();
    }

    public void crawlAndSave(String repoUrl, String savePath, CrawlCallback callback) {
        new Thread(() -> {
            try {
                String apiUrl = convertToApiUrl(repoUrl);
                List<String> imageUrls = new ArrayList<>();
                List<String> themeUrls = new ArrayList<>();
                crawlDirectory(apiUrl, imageUrls, themeUrls);
                
                JSONArray jsonArray = new JSONArray();
                int maxLength = Math.max(imageUrls.size(), themeUrls.size());
                
                for (int i = 0; i < maxLength; i++) {
                    JSONObject obj = new JSONObject();
                    obj.put("image", i < imageUrls.size() ? imageUrls.get(i) : JSONObject.NULL);
                    obj.put("theme", i < themeUrls.size() ? themeUrls.get(i) : JSONObject.NULL);
                    jsonArray.put(obj);
                }
                
                saveJsonToFile(jsonArray.toString(), savePath);
                callback.onSuccess(savePath, imageUrls.size(), themeUrls.size());
            } catch (Exception e) {
                callback.onFailure(e.getMessage());
            }
        }).start();
    }

    private void crawlDirectory(String apiUrl, List<String> imageUrls, List<String> themeUrls) throws Exception {
        Request request = new Request.Builder()
                .url(apiUrl)
                .header("Authorization", "token " + authToken)
                .build();

        Response response = client.newCall(request).execute();
        String jsonData = response.body().string();
        JSONArray files = new JSONArray(jsonData);
        String repoPath = extractRepoPath(apiUrl);
        String branch = extractBranchFromApiUrl(apiUrl);

        for (int i = 0; i < files.length(); i++) {
            JSONObject item = files.getJSONObject(i);
            String type = item.getString("type");
            String path = item.getString("path");

            if (type.equals("file")) {
                String lowerPath = path.toLowerCase();
                String rawUrl = GITHUB_RAW_BASE + "/" + repoPath + "/" + branch + "/" + path;
                
                if (isImageFile(lowerPath)) {
                    imageUrls.add(rawUrl);
                } else if (lowerPath.endsWith(".ghost")) {
                    themeUrls.add(rawUrl);
                }
            } else if (type.equals("dir")) {
                crawlDirectory(item.getString("url"), imageUrls, themeUrls);
            }
        }
    }

    private boolean isImageFile(String filename) {
        return filename.endsWith(".webp");
    }

    private String extractBranchFromApiUrl(String apiUrl) {
        return apiUrl.contains("?ref=") ? apiUrl.split("\\?ref=")[1] : "main";
    }

    private String convertToApiUrl(String repoUrl) {
        return GITHUB_API_BASE + "/repos/" + extractRepoPath(repoUrl) + "/contents";
    }

    private String extractRepoPath(String url) {
        if (url.startsWith(GITHUB_API_BASE)) {
            String path = url.replace(GITHUB_API_BASE + "/repos/", "");
            return path.split("/contents")[0].split("\\?")[0];
        }
        return url.replace("https://github.com/", "").replace(".git", "");
    }

    private void saveJsonToFile(String json, String path) throws Exception {
        File file = new File(path);
        file.getParentFile().mkdirs();
        try (FileWriter writer = new FileWriter(file)) {
            writer.write(json);
        }
    }

    public interface CrawlCallback {
        void onSuccess(String savedPath, int imageCount, int themeCount);
        void onFailure(String error);
    }
}
```


how to using java code?? 

```java

    String token =
                  "yourtoken github"; //adding token
              // استفاده کنید
              String repoUrl = "https://github.com/HanzoDev1375/ghosttheme";
              String savePath = "/sdcard/github_theme.json";
    
              new GitHubDownloder(token)
                  .crawlAndSave(
                      repoUrl,
                      savePath,
                      new GitHubDownloder.CrawlCallback() {
                        @Override
                        public void onSuccess(String savedPath, int imageCount,int i) {
                          runOnUiThread(
                              () -> {
                                Toast.makeText(
                                        MainActivity.this,
                                        "Found " + imageCount + " images",
                                        Toast.LENGTH_SHORT)
                                    .show();
                                // پردازش فایل ذخیره شده
                              });
                        }
    
                        @Override
                        public void onFailure(String error) {
                          runOnUiThread(
                              () -> {
                                Toast.makeText(MainActivity.this, error, Toast.LENGTH_LONG).show();
                              });
                        }
                      });
```