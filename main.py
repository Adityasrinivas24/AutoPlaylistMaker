import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


api_key = os.getenv('YT_API_KEY')
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


#api and credentials
def build_youtube_client():
    api_service_name = "youtube"
    api_version = "v3"

    credentials = None
    if os.path.exists("token.pickle"):
        print("Loading Credentials From File....")
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
            # credentials = Credentials.from_authorized_user_file("token.json")

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing Access Token....")
            credentials.refresh(Request())
        else:
            print("Fetching New Tokens....")
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json",scopes=SCOPES)
            flow.run_local_server(port=8080, prompt = "consent")
            credentials = flow.credentials

        with open("token.pickle","wb") as f:
            print("Saving Credentials for Future Use.....")
            pickle.dump(credentials, f)
    return build(api_service_name, api_version, credentials=credentials)



# Function to get playlist id from url
def get_playlist_id(playlist_url):
    client = build('youtube', 'v3', developerKey=api_key)

    playlist_id = None
    if 'list=' in playlist_url:
        index = playlist_url.index('list=')
        playlist_id = playlist_url[index + 5:]

        if '&' in playlist_id:
            playlist_id = playlist_id[:playlist_id.index('&')]

    if playlist_id:

        playlist_response = client.playlists().list(part='snippet',id=playlist_id).execute()

        if 'items' in playlist_response and len(playlist_response['items']) > 0:
            playlist_title = playlist_response['items'][0]['snippet']['title']
            print(f"Playlist Title: {playlist_title}")
            print(f"Playlist ID: {playlist_id}")
        else:
            print("Playlist not found or no data available.")

    else:
        print("Invalid playlist URL. Please provide a valid YouTube playlist URL.")

    return playlist_id



#Function to match playlist with keywords
def get_matching_videos(playlist_id, keywords):
    youtube = build_youtube_client()
    video_data = []

    try:
        next_page_token = None
        while True:
            request = youtube.playlistItems().list(part="snippet,contentDetails",
                                                   maxResults=30, #change accordingly
                                                   playlistId=playlist_id,
                                                   pageToken=next_page_token)

            response = request.execute()

            for item in response["items"]:
                video_title = item["snippet"]["title"]
                video_id = item["snippet"]["resourceId"]["videoId"]
                video_desc = item["snippet"]["description"]
                

                if any(keyword in video_title for keyword in keywords) or any(keyword in video_desc for keyword in keywords):
                    formatted_video = {"title": video_title, "id": video_id, "description": video_desc}
                    video_data.append(formatted_video)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

    except HttpError as e:
        print("An HTTP error occurred:", e)

    # with open("test.txt","w") as file:
    #     for video in video_data:
    #         file.write(str(video) + "\n")

    return video_data


#Function that checks if video already exists in the playlist
def video_exists(youtube,your_playlist_id,video_id):
    try:
        playlist_items = youtube.playlistItems().list(
            part="snippet",
            playlistId=your_playlist_id,
            videoId=video_id
        ).execute()
        return "items" in playlist_items and len(playlist_items["items"]) > 0
    except HttpError as e:
        print("An Http error occured: ",e)
        return False
    


# # Function to add videos to a new personal playlist
def add_videos_to_playlist(your_playlist_id, video_data):
    youtube = build_youtube_client()
    try:
        count = 0 
        for video in video_data:
            if not video_exists(youtube,your_playlist_id,video["id"]):
                request = youtube.playlistItems().insert(
                    part="snippet",
                    body={
                    "snippet": {
                        "playlistId": your_playlist_id,
                        # "position": 0,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video["id"] # change
                        }
                    }
                })

                request.execute()
                count +=1
                print(f"Video {video['id']} added to the playlist.")

            else:
                print("Video already exists in the playlist.")

        print(f"{count} Videos added to the new playlist successfully!")

    except HttpError as e:
        print("An HTTP error occurred:", e)



def main():

    playlist_url = input("Enter the YouTube playlist URL: ")
    channel_playlist_id = get_playlist_id(playlist_url=playlist_url)

    your_playlist_url = input("Enter Your private YouTube playlist URL: ")
    personal_playlist_id = get_playlist_id(playlist_url=your_playlist_url)

    keyword = list(input("Enter the keyword you want to search for in the video titles and descriptions: ")) 

    videos = get_matching_videos(channel_playlist_id, keywords=keyword)
    add_videos_to_playlist(your_playlist_id=personal_playlist_id,video_data=videos)


if __name__ == "__main__":
    main()
