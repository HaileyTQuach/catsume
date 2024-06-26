#!/usr/bin/env python3

import argparse
import json
import logging
import time
import xml.etree.ElementTree as ET

from datetime import datetime, timedelta

from .spca_scraper import SpcaScraper

class Server:

    def __init__(self, scraper, args, rss_file_path):
        """ `Server` initializer. """

        self.scraper = scraper
        self.args = args
        self.rss_file_path = rss_file_path

    def create_rss_feed(self, output, language="en"):
        """Creates an RSS feed from the output of scraped data."""
        # Define the namespace for media
        ET.register_namespace('media', 'http://search.yahoo.com/mrss/')
        ns_media = {'media': 'http://search.yahoo.com/mrss/'}

        rss = ET.Element("rss", version="2.0", attrib={"xmlns:media": "http://search.yahoo.com/mrss/"})
        channel = ET.SubElement(rss, "channel")
        ET.SubElement(channel, "title").text = "Montreal SPCA Adoptions"
        ET.SubElement(channel, "link").text = "http://spca.com"
        ET.SubElement(channel, "description").text = "Latest animals available for adoption at the Montreal SPCA"

        for category, animals in output.items():
            for animal in animals:
                item = ET.SubElement(channel, "item")
                ET.SubElement(item, "title").text = animal.get('name', 'No Name Available')
                ET.SubElement(item, "link").text = animal.get('url', 'No URL Available')
                details = animal.get('details', {})
                description_text = f"Species: {details.get('species', 'Unknown')}, Age: {details.get('age', 'Unknown')}, Sex: {details.get('sex', 'Unknown')}, Size: {details.get('size', 'Unknown')}"
                ET.SubElement(item, "description").text = description_text

                if 'image_url' in animal:
                    media_content = ET.SubElement(item, "media:content", attrib={
                        "url": animal['image_url'],
                        "type": "image/jpeg"
                    })

        xml_string = ET.tostring(rss, encoding='utf8', method='xml').decode('utf8')
        # print(xml_string)  # Debugging print of the final XML
        return xml_string
    
    def schedule_task(self, interval_hours=0, interval_minutes=0):
        """ ... """
        next_run_time = datetime.now() + timedelta(hours=interval_hours, minutes=interval_minutes)

        while True:
            now = datetime.now()
            if now >= next_run_time:
                self.run_task()

                next_run_time = now + timedelta(hours=interval_hours, minutes=interval_minutes)
            time.sleep(60)

    def run_task(self):
        """ ... """

        print("Task running...", datetime.now())
        self.write_rss_file(self.scraper, self.args, self.rss_file_path)
    
    def write_rss_file(self, scraper, args, file_path):
        """ ... """

        if args.all or args.birds:
            keys = {
                'en': 'birds',
                'fr': 'oiseaux'
            }

            key = keys.get(args.language)
            output[key] = scraper.get_birds()

        if args.all or args.cats:
            keys = {
                'en': 'cats',
                'fr': 'chats'
            }

            key = keys.get(args.language)
            output[key] = scraper.get_cats()

        if args.all or args.dogs:
            keys = {
                'en': 'dogs',
                'fr': 'chiens'
            }

            key = keys.get(args.language)
            output[key] = scraper.get_dogs()

        if args.all or args.rabbits:
            keys = {
                'en': 'rabbits',
                'fr': 'lapins'
            }

            key = keys.get(args.language)
            output[key] = scraper.get_rabbits()

        if args.all or args.small_animals:
            keys = {
                'en': 'small-animals',
                'fr': 'petits-animaux'
            }

            key = keys.get(args.language)
            output[key] = scraper.get_small_animals()
            
        rss_feed = self.create_rss_feed(output)
        with open(file_path, 'w', encoding='utf8') as file:
            file.write(rss_feed)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        prog='catsume',
        description='Web scraper for Montreal SPCA (spca.com) adoption pages.')

    arg_parser.add_argument(
        '-a',
        '--all',
        help='include all animals available for adoption',
        action='store_true')

    arg_parser.add_argument(
        '-b',
        '--birds',
        help='include all birds available for adoption',
        action='store_true')

    arg_parser.add_argument(
        '-c',
        '--cats',
        help='include all cats available for adoption',
        action='store_true')

    arg_parser.add_argument(
        '-d',
        '--dogs',
        help='include all dogs available for adoption',
        action='store_true')

    arg_parser.add_argument(
		'-L',
		'--language',
		default='en',
		help='the desired language (i.e., "en" or "fr")',
        nargs='?',
		type=str)

    arg_parser.add_argument(
		'-l',
		'--log-level',
		default=logging.INFO,
		help='the desired log level',
		type=lambda x: getattr(logging, x))

    arg_parser.add_argument(
        '-r',
        '--rabbits',
        help='include all rabbits available for adoption',
        action='store_true')

    arg_parser.add_argument(
        '-s',
        '--small-animals',
        help='include all small animals available for adoption',
        action='store_true')
    
    arg_parser.add_argument(
        '-x',
        '--server',
        help='run as RSS feed server',
        action='store_true')

    # Initialize to store json file content.
    output = {}

    args = arg_parser.parse_args()
    scraper = SpcaScraper(language=args.language)

    if args.server:
        server = Server(scraper, args, r'C:\Users\VanHalesing\Desktop\catsume\libcatsume\feed.xml')
        server.schedule_task(interval_hours=12, interval_minutes=0)
    
    else:

        if args.all or args.birds:
            keys = {
                'en': 'birds',
                'fr': 'oiseaux'
            }

            key = keys.get(args.language)
            output[key] = scraper.get_birds()

        if args.all or args.cats:
            keys = {
                'en': 'cats',
                'fr': 'chats'
            }

            key = keys.get(args.language)
            output[key] = scraper.get_cats()

        if args.all or args.dogs:
            keys = {
                'en': 'dogs',
                'fr': 'chiens'
            }

            key = keys.get(args.language)
            output[key] = scraper.get_dogs()

        if args.all or args.rabbits:
            keys = {
                'en': 'rabbits',
                'fr': 'lapins'
            }

            key = keys.get(args.language)
            output[key] = scraper.get_rabbits()

        if args.all or args.small_animals:
            keys = {
                'en': 'small-animals',
                'fr': 'petits-animaux'
            }

            key = keys.get(args.language)
            output[key] = scraper.get_small_animals()

        print(json.dumps(output))