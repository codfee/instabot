"""
    instabot example

    Workflow:
    1) Repost photo to your account
"""

import os
import sys

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot
from instabot.bot.bot_support import read_list_from_file


def exists_in_posted_medias(new_media_id, path='posted_medias.txt'):
    medias = read_list_from_file(path)
    return new_media_id in medias


def update_posted_medias(new_media_id, path='posted_medias.txt'):
    medias = read_list_from_file(path)
    medias.append(str(new_media_id))
    with open(path, 'w') as file:
        file.writelines('\n'.join(medias))
    return True


def repost_photo(my_bot, new_media_id, path='posted_medias.txt'):
    if exists_in_posted_medias(new_media_id, path):
        my_bot.logger.warning("Media {0} was uploaded earlier".format(new_media_id))
        return False
    photo_path = my_bot.download_photo(new_media_id, description=True)
    if not photo_path:
        return False
    with open(photo_path[:-3] + 'txt', 'r') as f:
        text = ''.join(f.readlines())
    if my_bot.upload_photo(photo_path, text):
        update_posted_medias(new_media_id, path)
        my_bot.logger.info('Media_id {0} is saved in {1}'.format(new_media_id, path))


media_id = ''

if not media_id:
    print('Media id is empty!')
    exit(1)

bot = Bot()
bot.login()

repost_photo(bot, media_id)
