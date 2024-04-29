#!/usr/bin/env python3

import re

from bs4 import BeautifulSoup
from curl_cffi import requests
from typing import Any, Dict, List


class SpcaScraper:
	""" Web scraper for spca.com. """

	_details_pattern = re.compile('(.+) ● (.+) ● (.+) ● (.+)')

	@staticmethod
	def _get_items(base_url: str, fingerprint: str) -> List[Dict[str, Any]]:
		""" Returns all animals of `species` available for adoption. """

		if not isinstance(base_url, str):
			raise TypeError(f'base_url (expected: str, received: {type(base_url)})')

		if not isinstance(fingerprint, str):
			raise TypeError(f'fingerprint (expected: str, received: {type(fingerprint)})')

		output = []

		has_next = True
		page_index = 0

		while has_next:
			page_index += 1
			url = f'{base_url}/{page_index}/'

			response = requests.get(url, impersonate=fingerprint)
			items, has_next = SpcaScraper._parse_items(response.text)
			output += items

		return output

	@staticmethod
	def _parse_items(html_content: str) -> List[Dict[str, Any]]:
		""" Parses items from `html_content`. """

		if not isinstance(html_content, str):
			raise TypeError(f'html_content (expected: str, received: {type(html_content)})')

		soup = BeautifulSoup(html_content, 'lxml')

		cards = soup.find_all('a', class_='card--link')
		arrow_right = soup.find_all('i', class_='icon-arrow-right')
		has_next = len(arrow_right) > 1

		output = []

		for card in cards:
			title = card.find('h5', class_='card--title').text.strip()
			image_url = card.find('img')['src']
			url = card['href']

			details = {}
			details_text = card.find('div', class_='pet--infos').text.strip()
			details_match = SpcaScraper._details_pattern.match(details_text)

			if details_match:
				details['species'] = details_match.group(1)
				details['age'] = details_match.group(2)
				details['sex'] = details_match.group(3)
				details['size'] = details_match.group(4)

			for key in details:
				details[key] = details[key].strip()

			card_info = {
				'details': details,
				'name': title,
				'image_url': image_url,
				'url': url
			}

			output.append(card_info)

		return output, has_next
	
	def __init__(self, language: str = 'en', fingerprint: str = 'chrome110') -> None:
		""" `SpcaScraper` initializer. """

		if not isinstance(language, str):
			raise TypeError(f'language (expected: str, received: {type(language)})')

		if not isinstance(fingerprint, str):
			raise TypeError(f'fingerprint (expected: str, received: {type(fingerprint)})')

		self._fingerprint = fingerprint
		self._language = language

	def get_birds(self) -> List[Dict[str, Any]]:
		""" Returns all birds available for adoption. """

		urls = {
			'en': 'https://www.spca.com/en/adoption/birds-for-adoption/page',
			'fr': 'https://www.spca.com/adoption/oiseaux-en-adoption/page'
		}

		url = urls.get(self._language)

		return self._get_items(url, self._fingerprint) if url else []

	def get_cats(self) -> List[Dict[str, Any]]:
		""" Returns all cats available for adoption. """

		urls = {
			'en': 'https://www.spca.com/en/adoption/cats-for-adoption/page',
			'fr': 'https://www.spca.com/adoption/chats-en-adoption/page'
		}

		url = urls.get(self._language)

		return self._get_items(url, self._fingerprint) if url else []

	def get_dogs(self) -> List[Dict[str, Any]]:
		""" Returns all dogs available for adoption. """

		urls = {
			'en': 'https://www.spca.com/en/adoption/dogs-for-adoption/page',
			'fr': 'https://www.spca.com/adoption/chiens-en-adoption/page'
		}

		url = urls.get(self._language)

		return self._get_items(url, self._fingerprint) if url else []

	def get_rabbits(self) -> List[Dict[str, Any]]:
		""" Returns all rabbits available for adoption. """

		urls = {
			'en': 'https://www.spca.com/en/adoption/rabbits-for-adoption/page',
			'fr': 'https://www.spca.com/adoption/lapins-en-adoption/page'
		}

		url = urls.get(self._language)

		return self._get_items(url, self._fingerprint) if url else []

	def get_small_animals(self) -> List[Dict[str, Any]]:
		""" Returns all small animals available for adoption. """

		urls = {
			'en': 'https://www.spca.com/en/adoption/small-animals-for-adoption/page',
			'fr': 'https://www.spca.com/adoption/petits-animaux-en-adoption/page'
		}

		url = urls.get(self._language)

		return self._get_items(url, self._fingerprint) if url else []
