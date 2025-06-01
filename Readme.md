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