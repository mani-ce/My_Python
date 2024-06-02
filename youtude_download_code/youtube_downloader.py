import os
import asyncio
from pytube import YouTube, Playlist
from concurrent.futures import ThreadPoolExecutor
import streamlit as st

def download_video(link, path):
    youtube_object = YouTube(link)
    youtube_object = youtube_object.streams.get_highest_resolution()
    try:
        youtube_object.download(output_path=path)
        st.write(f"Download completed successfully: {link}")
    except Exception as e:
        st.write(f"An error occurred while downloading {link}: {e}")

async def async_download_video(link, path, executor):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, download_video, link, path)

async def download_playlist(playlist_link, path):
    playlist = Playlist(playlist_link)
    st.write(f"Downloading playlist: {playlist.title}")
    executor = ThreadPoolExecutor(max_workers=20)  # Increased number of workers
    tasks = [async_download_video(video_url, path, executor) for video_url in playlist.video_urls]
    await asyncio.gather(*tasks)
    executor.shutdown(wait=True)  # Ensure all threads have completed
    st.write("All videos in the playlist have been downloaded successfully.")

def main():
    st.title("YouTube Video/Playlist Downloader")

    link = st.text_input("Enter the YouTube video or playlist URL:")
    path = st.text_input("Enter the path where files need to be stored:", value="C:\\Users\\vijay\\Downloads\\YouTubePlaylist\\New folder")
    
    if st.button("Download"):
        if not os.path.exists(path):
            os.makedirs(path)
        
        if 'playlist' in link:
            asyncio.run(download_playlist(link, path))
        else:
            download_video(link, path)

if __name__ == "__main__":
    main()
