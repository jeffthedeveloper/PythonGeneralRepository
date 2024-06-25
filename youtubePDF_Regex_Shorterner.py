import re

def extract_youtube_video_id(url):
  """Extracts the YouTube video ID from a given URL.

  Args:
    url: A string containing the URL to a YouTube video.

  Returns:
    A string containing the extracted YouTube video ID, or None if the URL is not
    a valid YouTube video URL.
  """

  regex = r'(?P<id>[a-zA-Z0-9-_]{11})'
  match = re.search(regex, url)
  if match:
    return match.group('id')
  else:
    return None


link = input()

print(extract_youtube_video_id(link))
