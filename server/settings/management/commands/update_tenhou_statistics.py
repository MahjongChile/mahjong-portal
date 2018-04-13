import re

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils import timezone

from player.models import TenhouNickname, TenhouStatistics


def get_date_string():
    return timezone.now().strftime('%H:%M:%S')


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('{0}: Start'.format(get_date_string()))

        tenhou_objects = TenhouNickname.objects.all()

        for tenhou_object in tenhou_objects:
            url = 'http://arcturus.su/tenhou/ranking/ranking.pl?name={}&d1={}'.format(
                tenhou_object.tenhou_username,
                tenhou_object.username_created_at.strftime('%Y%m%d'),
            )

            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser', from_encoding='utf-8')

            tags = soup.find_all('p')

            rank = ''
            for tag in tags:
                if '4man' in tag.text:
                    rank = re.search(r"\s+(\w+)\s+", tag.text.strip()).group(0).strip()

            places_dict = {
                '1位': 1,
                '2位': 2,
                '3位': 3,
                '4位': 4,
            }

            lobbies_dict = {
                '般': TenhouStatistics.KYU_LOBBY,
                '上': TenhouStatistics.DAN_LOBBY,
                '特': TenhouStatistics.UPPERDAN_LOBBY,
                '鳳': TenhouStatistics.PHOENIX_LOBBY,
            }

            lobbies_data = {
                TenhouStatistics.KYU_LOBBY: {'played_games': 0, 1: 0, 2: 0, 3: 0, 4: 0},
                TenhouStatistics.DAN_LOBBY: {'played_games': 0, 1: 0, 2: 0, 3: 0, 4: 0},
                TenhouStatistics.UPPERDAN_LOBBY: {'played_games': 0, 1: 0, 2: 0, 3: 0, 4: 0},
                TenhouStatistics.PHOENIX_LOBBY: {'played_games': 0, 1: 0, 2: 0, 3: 0, 4: 0},
            }

            records = soup.find('div', {'id': 'records'}).text.split('\n')
            for record in records:
                if not record:
                    continue

                temp_array = record.strip().split('|')
                game_settings = temp_array[5].strip()

                place = places_dict[temp_array[0].strip()]
                lobby_number = temp_array[1].strip()
                lobby_name = lobbies_dict[game_settings[1]]

                # for now let's collect stat only from usual games for 4 players
                if lobby_number == 'L0000' and game_settings[0] == u'四':
                    lobbies_data[lobby_name]['played_games'] += 1
                    lobbies_data[lobby_name][place] += 1

            total_played_games = 0
            total_first_place = 0
            total_second_place = 0
            total_third_place = 0
            total_fourth_place = 0
            for lobby_key, lobby_data in lobbies_data.items():
                if lobby_data['played_games']:
                    stat_object, _ = TenhouStatistics.objects.get_or_create(
                        lobby=lobby_key,
                        tenhou_object=tenhou_object
                    )

                    games_count = lobby_data['played_games']
                    first_place = lobby_data[1]
                    second_place = lobby_data[2]
                    third_place = lobby_data[3]
                    fourth_place = lobby_data[4]

                    total_played_games += games_count
                    total_first_place += first_place
                    total_second_place += second_place
                    total_third_place += third_place
                    total_fourth_place += fourth_place

                    average_place = (first_place + second_place * 2 + third_place * 3 + fourth_place * 4) / games_count

                    first_place = (first_place / games_count) * 100
                    second_place = (second_place / games_count) * 100
                    third_place = (third_place / games_count) * 100
                    fourth_place = (fourth_place / games_count) * 100

                    stat_object.played_games = games_count
                    stat_object.average_place = average_place
                    stat_object.first_place = first_place
                    stat_object.second_place = second_place
                    stat_object.third_place = third_place
                    stat_object.fourth_place = fourth_place
                    stat_object.save()

            total_average_place = (total_first_place + total_second_place * 2 + total_third_place * 3 + total_fourth_place * 4) / total_played_games

            tenhou_object.rank = [x[0] for x in TenhouNickname.RANKS if x[1] == rank][0]
            tenhou_object.played_games = total_played_games
            tenhou_object.average_place = total_average_place
            tenhou_object.save()

        print('{0}: End'.format(get_date_string()))