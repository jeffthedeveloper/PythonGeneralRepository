def extract_youtube_video_id(url):
  """Extracts the YouTube video ID from a given URL.

  Args:
    url: A string containing the URL to a YouTube video.

  Returns:
    A string containing the extracted YouTube video ID, or None if the URL is not
    a valid YouTube video URL.
  """

  if "=v" in url:
    parts = url.split('=v')
  else:
    parts = url.split("/")

  # Return the last part, which is the video ID.
  return parts[-1]


link = input()

print(extract_youtube_video_id(link))
