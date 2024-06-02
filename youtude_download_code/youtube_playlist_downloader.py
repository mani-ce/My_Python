from pytube import YouTube, Playlist
import os

def DownloadVideo(link, path):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download(output_path=path)
        print(f"Download completed successfully: {link}")
    except Exception as e:
        print(f"An error occurred while downloading {link}: {e}")

def Download(link, path):
    if 'playlist' in link:
        try:
            playlist = Playlist(link)
            print(f"Downloading playlist: {playlist.title}")
            for video_url in playlist.video_urls:
                DownloadVideo(video_url, path)
            print("All videos in the playlist have been downloaded successfully.")
        except Exception as e:
            print(f"An error occurred with the playlist: {e}")
    else:
        try:
            DownloadVideo(link, path)
        except Exception as e:
            print(f"An error occurred: {e}")

link = input("Enter the YouTube video or playlist URL: ")
# path = input("Enter the path where to store the video(s): ")
path ="C:\\Users\\vijay\\Downloads\\YouTubePlaylist\\New folder"
# Ensure the path exists
if not os.path.exists(path):
    os.makedirs(path)

Download(link, path)