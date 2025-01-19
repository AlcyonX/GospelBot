# Author: AlcyonX
#
# Author YouTube channel link: https://www.youtube.com/@AlcyonX
# Official GospelBot YouTube channel : https://www.youtube.com/@GospelBot
#
# Copyright (c) 2025 AlcyonX. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# PRAISE THE LORD JESUS CHIRST ✝

import requests
import json
import random

def get_book(bible_id, book_id):

    url = f"https://bible.helloao.org/api/{bible_id}/books.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        books = response.json().get("books", [])

        dicts = {}
        
        for book in books:
            dicts[book['id']] = book['name']

        return dicts[book_id]
    
    except requests.exceptions.RequestException as e:
        raise ValueError(e)

def get_verse(bible_id, reference):

    reference = reference.split()
    book_id = reference[0]
    chapter = reference[1]
    verse = int(reference[2])
    
    book = get_book(bible_id, book_id)

    url = f"https://bible.helloao.org/api/{bible_id}/{book.replace(' ', '_')}/{chapter}.json"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    for item in data['chapter']['content']:
        if item['type'] == 'verse':
            if item['number'] == verse:
                verse_text = item['content'][0]
                if type(verse_text) == dict:
                    verse_text = verse_text["text"]
                return f"{book} {chapter}:{verse}", verse_text

def get_random_edit_content(num_entries, edit_content, bible_id):

    with open(edit_content) as file:
        refs_list = json.load(file)
        
    title, refs_list = random.choice(list(refs_list.items()))
    selected_refs = random.sample(refs_list, min(num_entries, len(refs_list)))
    
    refs_dict = {entry['text']: get_verse(bible_id, entry['reference'])[0] for entry in selected_refs}
    
    return title, refs_dict
