import requests

def extract_youtube_video_id(url):
  """Extracts the YouTube video ID from a given URL.

  Args:
    url: A string containing the URL to a YouTube video.

  Returns:
    A string containing the extracted YouTube video ID, or None if the URL is not
    a valid YouTube video URL.
  """

  response = requests.get(url)
  video_id = response.headers['X-Goog-Cid']
  return video_id


link = input()

print(extract_youtube_video_id(link))
