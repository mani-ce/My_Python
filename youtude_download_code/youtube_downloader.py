import os
import asyncio
from pytube import YouTube, Playlist
from concurrent.futures import ThreadPoolExecutor
import streamlit as st
from tkinter import Tk, filedialog

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
    executor = ThreadPoolExecutor(max_workers=10)#to speedup you can increase  works from 10 to 20
    progress_bar = st.progress(0)
    tasks = [async_download_video(video_url, path, executor, progress_bar) for video_url in playlist.video_urls]
    await asyncio.gather(*tasks)
    executor.shutdown(wait=True)
    st.write("All videos in the playlist have been downloaded successfully.")

def select_folder():
    root = Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory()
    root.destroy()  # Destroy the root window after selection
    return folder_path

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
    .input-field {
        background-color: #e6f7ff;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main'>", unsafe_allow_html=True)

    link = st.text_input("Enter the YouTube video or playlist URL:", key="link", help="Paste the YouTube link here", placeholder="https://www.youtube.com/...")

    if 'path' not in st.session_state:
        st.session_state['path'] = ""

    if st.button("Browse"):
        selected_folder = select_folder()
        if selected_folder:
            st.session_state['path'] = selected_folder

    st.write(f"Selected Path: {st.session_state['path']}")

    st.markdown("**Note:** The popup will open after pressing the above button. To find it, press 'Alt+Tab' accordingly.")

    if st.button("Download"):
        path = st.session_state['path']
        if not os.path.exists(path):
            os.makedirs(path)
        
        if 'playlist' in link:
            asyncio.run(download_playlist(link, path))
        else:
            progress_bar = st.progress(0)
            download_video(link, path, progress_bar)

    st.markdown("</div>", unsafe_allow_html=True)
    
    # Developer Information
    st.sidebar.markdown("### Developer Information")
    st.sidebar.markdown("**Name:** CE MANIVANNAN")
    st.sidebar.markdown("**Email:** cemanivannan98@gmail.com")

if __name__ == "__main__":
    main()