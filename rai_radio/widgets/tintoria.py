import xml.etree.ElementTree as ET
import requests
import yt_dlp


def tintoria_episodes():
    rss_feed_url = 'https://www.spreaker.com/show/2830173/episodes/feed'
    response = requests.get(rss_feed_url)

    root = ET.fromstring(response.content)

    enclosure_urls = []
    for item in root.findall(".//item"):
        enclosure = item.find("enclosure")
        if enclosure is not None and 'url' in enclosure.attrib:
            enclosure_urls.append(enclosure.attrib['url'])

    titles = []
    for item in root.findall(".//item"):
        title = item.find("title")
        if title is not None:
            titles.append(title.text)

    # for title in titles:
    #     print(title)
    

    tintoria_list = {}

    for episode,url in zip(titles, enclosure_urls):

        tintoria_list[episode.strip().lower().replace("#", "").replace(" ", "")] = {
                
                "url": url,
        }

        break
    print(tintoria_list)


tintoria_episodes()

def extract_audio_url():
    ydl_opts = {'quiet': True, 'force_generic_extractor': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info("https://dts.podtrac.com/redirect.mp3/api.spreaker.com/download/episode/62372275/tintoria_226_giorgio_montanini_spreaker.mp3", download=False)
        if 'url' in info:
            return info['url']
        else:
            print("Unable to extract audio URL.")
            return None

print(extract_audio_url())
