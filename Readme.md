## ghost ide theme



### Create your own theme online
- [click](https://hanzodev1375.github.io/ghosttheme/themecreatemodern.html)
#### You can add your own themes to this repository, but there are a number of conditions that must be met.

- The rule is that a theme name must be valid.
- The second rule is that the theme logo must be in webp format, or the preview.
- Rule 3: You have no restrictions. Please test the theme and then publish it. Thank you.
- The fourth rule, which is the most important, is if you can add the theme and preview image to the json file. If you don't know json, it's no problem. I'll add it myself. We also provide you with a Java code that you can implement to automatically add themes to json.

***Welcome to the Ghostide family***




```java

package ir.ninjacoder.ghostide.prograssdialog;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONException;
import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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
    new Thread(
            () -> {
              try {
                String apiUrl = convertToApiUrl(repoUrl);
                Map<String, Theme> themes = new HashMap<>();
                List<Background> backgrounds = new ArrayList<>();

                // Step 1: Scan repository
                scanRepository(apiUrl, themes, backgrounds);

                // Step 2: Match backgrounds with themes
                matchBackgrounds(themes, backgrounds);

                // Step 3: Generate JSON
                JSONArray jsonArray = generateJson(themes.values());

                // Step 4: Save to file
                saveToFile(jsonArray.toString(), savePath);

                callback.onSuccess(savePath, themes.size());
              } catch (Exception e) {
                callback.onFailure(e.getMessage());
              }
            })
        .start();
  }

  private void scanRepository(
      String apiUrl, Map<String, Theme> themes, List<Background> backgrounds) throws Exception {
    Request request =
        new Request.Builder().url(apiUrl).header("Authorization", "token " + authToken).build();

    Response response = client.newCall(request).execute();
    JSONArray items = new JSONArray(response.body().string());
    String repoPath = extractRepoPath(apiUrl);
    String branch = extractBranchFromApiUrl(apiUrl);

    for (int i = 0; i < items.length(); i++) {
      JSONObject item = items.getJSONObject(i);
      String type = item.getString("type");
      String path = item.getString("path");
      String name = path.substring(path.lastIndexOf('/') + 1);
      String rawUrl = GITHUB_RAW_BASE + "/" + repoPath + "/" + branch + "/" + path;

      if (type.equals("file")) {
        processFile(themes, backgrounds, path, name, rawUrl);
      } else if (type.equals("dir")) {
        scanRepository(item.getString("url"), themes, backgrounds);
      }
    }
  }

  private void processFile(
      Map<String, Theme> themes,
      List<Background> backgrounds,
      String path,
      String name,
      String rawUrl) {

    String dirName = path.contains("/") ? path.substring(0, path.lastIndexOf('/')) : "";
    String extension =
        name.contains(".") ? name.substring(name.lastIndexOf('.') + 1).toLowerCase() : "";

    // پردازش فایل‌های تم (.ghost)
    if (extension.equals("ghost")) {
      Theme theme = themes.getOrDefault(dirName, new Theme());
      theme.themeUrl = rawUrl;
      theme.name = name.replace(".ghost", "");
      themes.put(dirName, theme);
    }
    // پردازش فایل‌های JSON (ذخیره فقط مسیر)
    else if (extension.equals("json")) {
      Theme theme = themes.getOrDefault(dirName, new Theme());
      theme.themeJson = rawUrl; // فقط URL فایل JSON را ذخیره می‌کنیم
      themes.put(dirName, theme);
    }
    // پردازش تصاویر پیش‌نمایش
    else if (isPreviewImage(name)) {
      Theme theme = themes.getOrDefault(dirName, new Theme());
      theme.imageUrl = rawUrl;
      themes.put(dirName, theme);
    }
    // پردازش تصاویر پس‌زمینه
    else if (isBackgroundImage(name)) {
      backgrounds.add(new Background(dirName, rawUrl));
    }
  }

  private void matchBackgrounds(Map<String, Theme> themes, List<Background> backgrounds) {
    for (Background bg : backgrounds) {
      // Try to match by directory name first
      if (themes.containsKey(bg.directory)) {
        themes.get(bg.directory).backgroundUrl = bg.url;
        continue;
      }

      // Try to match by common patterns
      for (Theme theme : themes.values()) {
        if (bg.directory.contains(theme.name.toLowerCase())
            || theme.name.toLowerCase().contains(bg.directory.toLowerCase())) {
          theme.backgroundUrl = bg.url;
          break;
        }
      }
    }
  }

  private JSONArray generateJson(Iterable<Theme> themes) {
    JSONArray jsonArray = new JSONArray();

    for (Theme theme : themes) {
      try {
        JSONObject obj = new JSONObject();
        obj.put("theme", theme.themeUrl != null ? theme.themeUrl : JSONObject.NULL);
        obj.put("image", theme.imageUrl != null ? theme.imageUrl : JSONObject.NULL);
        obj.put("themeObject", theme.themeJson != null ? theme.themeJson : JSONObject.NULL);

        boolean hasBackground = theme.backgroundUrl != null;
        obj.put("background", hasBackground ? theme.backgroundUrl : JSONObject.NULL);
        obj.put("hasbackground", hasBackground);

        jsonArray.put(obj);
      } catch (JSONException e) {
        e.printStackTrace();
      }
    }

    return jsonArray;
  }

  private boolean isPreviewImage(String filename) {
    String lower = filename.toLowerCase();
    return lower.endsWith(".png") || lower.endsWith(".webp");
  }

  private boolean isBackgroundImage(String filename) {
    String lower = filename.toLowerCase();
    return lower.endsWith(".jpeg");
  }

  private void saveToFile(String json, String path) throws Exception {
    File file = new File(path);
    file.getParentFile().mkdirs();
    try (FileWriter writer = new FileWriter(file)) {
      writer.write(json);
    }
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

  private static class Theme {
    String name;
    String themeUrl;
    String imageUrl;
    String backgroundUrl;
    String themeJson;
  }

  private static class Background {
    String directory;
    String url;

    Background(String directory, String url) {
      this.directory = directory;
      this.url = url;
    }
  }

  public interface CrawlCallback {
    void onSuccess(String savedPath, int themeCount);

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
## java is hard? using `python code`

``` python
import requests
import json
import os
from threading import Thread
from typing import List, Callable, Optional
#tnks for deepseek to fix bug
class GitHubDownloader:
    GITHUB_API_BASE = "https://api.github.com"
    GITHUB_RAW_BASE = "https://raw.githubusercontent.com"

    def __init__(self, auth_token: str = None):
        """
        Initialize the GitHub downloader with an optional auth token.
        
        Args:
            auth_token: GitHub personal access token (optional but recommended)
        """
        self.auth_token = auth_token
        self.session = requests.Session()
        if auth_token:
            self.session.headers.update({
                "Authorization": f"token {auth_token}",
                "Accept": "application/vnd.github.v3+json"
            })

    def crawl_and_save(self, repo_url: str, save_path: str, callback: Callable = None) -> None:
        """
        Crawl a GitHub repository and save found images and themes to a JSON file.
        
        Args:
            repo_url: URL of the GitHub repository (e.g., "https://github.com/user/repo")
            save_path: Path to save the JSON file
            callback: Optional callback function with signature (success: bool, result: dict)
        """
        def run():
            try:
                api_url = self._convert_to_api_url(repo_url)
                image_urls = []
                theme_urls = []
                
                self._crawl_directory(api_url, image_urls, theme_urls)
                
                # Prepare the JSON data
                result = []
                max_length = max(len(image_urls), len(theme_urls))
                
                for i in range(max_length):
                    item = {
                        "image": image_urls[i] if i < len(image_urls) else None,
                        "theme": theme_urls[i] if i < len(theme_urls) else None
                    }
                    result.append(item)
                
                # Save to file
                self._save_json_to_file(result, save_path)
                
                if callback:
                    callback(True, {
                        "saved_path": save_path,
                        "image_count": len(image_urls),
                        "theme_count": len(theme_urls)
                    })
            except Exception as e:
                if callback:
                    callback(False, {"error": str(e)})

        Thread(target=run).start()

    def _crawl_directory(self, api_url: str, image_urls: List[str], theme_urls: List[str]) -> None:
        """
        Recursively crawl a GitHub directory to find image and theme files.
        """
        response = self.session.get(api_url)
        response.raise_for_status()
        
        repo_path = self._extract_repo_path(api_url)
        branch = self._extract_branch_from_api_url(api_url)
        
        for item in response.json():
            item_type = item.get("type")
            path = item.get("path")
            
            if item_type == "file":
                lower_path = path.lower()
                raw_url = f"{self.GITHUB_RAW_BASE}/{repo_path}/{branch}/{path}"
                
                if self._is_image_file(lower_path):
                    image_urls.append(raw_url)
                elif lower_path.endswith(".ghost"):
                    theme_urls.append(raw_url)
                    
            elif item_type == "dir":
                self._crawl_directory(item["url"], image_urls, theme_urls)

    @staticmethod
    def _is_image_file(filename: str) -> bool:
        """Check if the file is an image based on its extension."""
        return filename.endswith(".webp") or filename.endswith(".png") or filename.endswith(".gif")

    @staticmethod
    def _extract_branch_from_api_url(api_url: str) -> str:
        """Extract branch name from API URL."""
        return api_url.split("?ref=")[1] if "?ref=" in api_url else "main"

    def _convert_to_api_url(self, repo_url: str) -> str:
        """Convert a GitHub repository URL to API URL."""
        return f"{self.GITHUB_API_BASE}/repos/{self._extract_repo_path(repo_url)}/contents"

    @staticmethod
    def _extract_repo_path(url: str) -> str:
        """Extract repository path from URL."""
        if url.startswith(GitHubDownloader.GITHUB_API_BASE):
            path = url.replace(f"{GitHubDownloader.GITHUB_API_BASE}/repos/", "")
            return path.split("/contents")[0].split("?")[0]
        return url.replace("https://github.com/", "").replace(".git", "")

    @staticmethod
    def _save_json_to_file(data: dict, path: str) -> None:
        """Save JSON data to a file."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# Example usage
if __name__ == "__main__":
    # Create a callback function to handle results
    def callback(success, result):
        if success:
            print(f"Success! Saved to {result['saved_path']}")
            print(f"Found {result['image_count']} images and {result['theme_count']} themes")
        else:
            print(f"Error: {result['error']}")

    # Initialize the downloader (token is optional but recommended)
    downloader = GitHubDownloader(auth_token="yourtoken")
    
    # Start crawling (this will run in the background)
    downloader.crawl_and_save(
        repo_url="https://github.com/HanzoDev1375/ghosttheme",
        save_path="/sdcard/output/result.json",
        callback=callback
    )
    
    print("Crawling started in the background...")

```