import os
import asyncio
from pytube import YouTube, Playlist
from concurrent.futures import ThreadPoolExecutor

def download_video(link, path):
    youtube_object = YouTube(link)
    youtube_object = youtube_object.streams.get_highest_resolution()
    try:
        youtube_object.download(output_path=path)
        print(f"Download completed successfully: {link}")
    except Exception as e:
        print(f"An error occurred while downloading {link}: {e}")

async def async_download_video(link, path, executor):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, download_video, link, path)

async def download_playlist(playlist_link, path):
    playlist = Playlist(playlist_link)
    print(f"Downloading playlist: {playlist.title}")
    executor = ThreadPoolExecutor(max_workers=10) # Increased number of workers from 10 to 20 it lead speedup the process
    tasks = [async_download_video(video_url, path, executor) for video_url in playlist.video_urls]
    await asyncio.gather(*tasks)
    executor.shutdown(wait=True)  # Ensure all threads have completed
    print("All videos in the playlist have been downloaded successfully.")

link = input("Enter the YouTube video or playlist URL: ")
path = "C:\\Users\\vijay\\Downloads\\YouTubePlaylist\\New folder"# here you can change your local location path to store the files

if not os.path.exists(path):
    os.makedirs(path)

if 'playlist' in link:
    asyncio.run(download_playlist(link, path))
else:
    download_video(link, path)