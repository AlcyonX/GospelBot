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

import edge_tts
import asyncio
import os
import time

async def text_to_speech(text, voice):

    output_file = f"media/audio/speech/{voice}-{int(time.time())}.mp3"

    communicate = edge_tts.Communicate(text, voice, rate="+20%", pitch="+20Hz", volume="+10%")
    await communicate.save(output_file)

    return output_file

async def random_voice(gender, language):
    
    voices = await edge_tts.VoicesManager.create()
    voice = voices.find(Gender="Male", Language=language)
    voice = voice[0]["Name"]

    return voice
