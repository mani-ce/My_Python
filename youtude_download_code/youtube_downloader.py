import os
import asyncio
from pytube import YouTube, Playlist
from concurrent.futures import ThreadPoolExecutor
import streamlit as st

def download_video(link, path, progress_bar):
    youtube_object = YouTube(link, on_progress_callback=lambda stream, chunk, bytes_remaining: progress_bar.progress((1 - bytes_remaining / stream.filesize) * 100))
    youtube_object = youtube_object.streams.get_highest_resolution()
    try:
        youtube_object.download(output_path=path)
        st.write(f"Download completed successfully: {link}")
    except Exception as e:
        st.write(f"An error occurred while downloading {link}: {e}")

async def async_download_video(link, path, executor, progress_bar):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, download_video, link, path, progress_bar)

async def download_playlist(playlist_link, path):
    playlist = Playlist(playlist_link)
    st.write(f"Downloading playlist: {playlist.title}")
    executor = ThreadPoolExecutor(max_workers=20)
    progress_bar = st.progress(0)
    tasks = [async_download_video(video_url, path, executor, progress_bar) for video_url in playlist.video_urls]
    await asyncio.gather(*tasks)
    executor.shutdown(wait=True)
    st.write("All videos in the playlist have been downloaded successfully.")

def main():
    st.set_page_config(page_title="YouTube Downloader", page_icon="🎥", layout="wide")
    st.title("🎥 YouTube Video/Playlist Downloader")
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main'>", unsafe_allow_html=True)

    link = st.text_input("Enter the YouTube video or playlist URL:")
    os_option = st.selectbox("Select your Operating System:", ["Windows", "Linux", "MacOS"])
    
    default_path = ""
    if os_option == "Windows":
        default_path = "C:\\Users\\<YourUserName>\\Downloads\\YouTubeDownloads"
    elif os_option == "Linux":
        default_path = "/home/<YourUserName>/Downloads/YouTubeDownloads"
    elif os_option == "MacOS":
        default_path = "/Users/<YourUserName>/Downloads/YouTubeDownloads"
    
    path = st.text_input("Enter the path where files need to be stored:", value=default_path)
    
    if st.button("Download"):
        if not os.path.exists(path):
            os.makedirs(path)
        
        if 'playlist' in link:
            asyncio.run(download_playlist(link, path))
        else:
            progress_bar = st.progress(0)
            download_video(link, path, progress_bar)

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
