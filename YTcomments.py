from googleapiclient.discovery import build
import pandas as pd

DevKey = input("API key: ")
vid = input("Video ID: ")

token = None
comments = []
youtube = build('youtube', 'v3', developerKey=DevKey)
for i in range(15):
    response = youtube.commentThreads().list(
        part="snippet",
        videoId= vid,
        textFormat="plainText",
        order="relevance",
        pageToken = token
    ).execute()

    for item in response['items']:
        # Extracting comments
        comment = item['snippet']['topLevelComment']['snippet']
        
        author = comment["authorDisplayName"]
        text = comment["textDisplay"]
        likes = comment["likeCount"]
        comments.append({
            'user_name': author,
            'comment': text,
            'likes': likes
        })

    token = response.get("nextPageToken")
    if not token:
        break

df = pd.DataFrame(comments)
# Save the DataFrame to a CSV file
df.to_csv(f"{vid}_comments.csv", index=False)