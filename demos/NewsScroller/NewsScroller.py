import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

from matrix_library import LEDWall, Canvas, Controller, shapes

RSS_FEED_URL = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
MAX_TITLES = 3
SCROLL_SPEED = 2
TEXT_COLOR = (255, 255, 255)
HEADER_COLOR = (255, 215, 0)
HEADER_POSITION = [4, 8]
DATE_POSITION = [4, 20]


class NewsScroller(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        self.titles = []
        self.current_index = 0
        self.current_phrase = None
        self.completed = False
        self.header_phrase = None
        self.date_phrase = None
        super().__init__(canvas, controller, trackFPS=False, fps=20)

    def preLoop(self):
        headlines, pulled_date = self._fetch_titles()
        self.titles = headlines or ["No headlines available"]
        self._prepare_header(pulled_date)
        self.current_index = 0
        self.completed = False
        self._prepare_phrase()

    def __draw__(self):
        if self.completed:
            self.quit()
            return

        self.canvas.clear()

        if self.header_phrase:
            self.canvas.add(self.header_phrase)
        if self.date_phrase:
            self.canvas.add(self.date_phrase)

        if self.current_phrase is not None:
            self.canvas.add(self.current_phrase)
            self.current_phrase.translate(-SCROLL_SPEED, 0)

            if self.current_phrase.position[0] + self.current_phrase.get_width() < 0:
                self.current_index += 1
                self._prepare_phrase()
        else:
            message = shapes.Phrase("No news to show", [20, 60], TEXT_COLOR)
            self.canvas.add(message)
            self.completed = True

    def __bind_controls__(self):
        self.controller.add_function("SELECT", self.quit)

    def postLoop(self):
        self.canvas.clear()
        self.canvas.draw()
        time.sleep(0.5)

    def _prepare_phrase(self):
        if self.current_index >= len(self.titles):
            self.completed = True
            return

        text = self.titles[self.current_index]
        self.current_phrase = shapes.Phrase(text, [128, 58], TEXT_COLOR)

    def _fetch_titles(self):
        try:
            with urllib.request.urlopen(RSS_FEED_URL, timeout=10) as response:
                data = response.read()
        except Exception as exc:
            print(f"Failed to fetch RSS feed: {exc}")
            return None, None

        try:
            root = ET.fromstring(data)
        except ET.ParseError as exc:
            print(f"Failed to parse RSS feed: {exc}")
            return None, None

        items = root.findall(".//item")
        titles = []
        for item in items:
            title = item.findtext("title")
            if title:
                titles.append(title.strip())
            if len(titles) >= MAX_TITLES:
                break

        pub_date = root.findtext(".//channel/pubDate")
        formatted_date = self._format_date(pub_date)

        return titles, formatted_date

    def _prepare_header(self, pulled_date):
        self.header_phrase = shapes.Phrase("NYT News", HEADER_POSITION, HEADER_COLOR, size=1.2)
        if pulled_date:
            self.date_phrase = shapes.Phrase(pulled_date, DATE_POSITION, TEXT_COLOR, size=1)
        else:
            self.date_phrase = None

    def _format_date(self, date_str):
        if not date_str:
            return None

        try:
            dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return date_str


if __name__ == "__main__":
    NewsScroller(Canvas(), Controller())
