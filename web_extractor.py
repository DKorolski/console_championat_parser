import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def _get_html(url):
    response = requests.get(url, headers={"User-Agent": "Firefox/67.0.4"})
    return response.text


def get_pattern_url(url, pattern):
    soup = BeautifulSoup(_get_html(url), 'lxml')
    pattern_url_text = soup.find_all('a', text=pattern)
    pattern_short_url = str(
        pattern_url_text[0]
    ).split('href="', 1)[1].split('">', 1)[0]
    pattern_url = 'https://www.championat.com/'+pattern_short_url
    return pattern_url


def get_teams_url_list(url, pattern):
    teams_urls = []
    teams_names = []
    soup = BeautifulSoup(_get_html(url), 'lxml')
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if pattern in str(href):
            if len(str(href).split(pattern+'/', 1)[1]) > 0:
                teams_urls = teams_urls + ['https://www.championat.com' + href]
                team_name = str(
                    a_tag.contents
                ).split('" class=', 1)[0].split('alt="', 1)[1]
                teams_names = teams_names + [team_name]
    teams_info = pd.DataFrame(
        columns=[
            'url',
            'team_url',
            'team_name'
        ],
        index=range(len(teams_urls))
    )
    for idx in range(len(teams_info)):
        teams_info['url'][idx] = url
        teams_info['team_url'][idx] = teams_urls[idx]
        teams_info['team_name'][idx] = teams_names[idx]
    return teams_info


def get_players_info(url):
    table_num = 0
    url_players = url.replace('result/', '') + 'players/'
    soup = BeautifulSoup(_get_html(url_players), 'lxml')
    tables = pd.read_html(url_players)
    for table in tables:
        proper_format = 8
        poper_format_short = 7
        if table.shape[1] == proper_format and table_num == 0:
            active_players = pd.DataFrame(
                data=table.values,
                columns=[
                    'country',
                    'num',
                    'name',
                    'amplua',
                    'birthday',
                    'height',
                    'weight',
                    'value'
                ]
            )
            active_players['url'] = np.nan
            active_players['id'] = ''
            active_players['is_active'] = 'true'
            table_num += 1
        elif table.shape[1] == poper_format_short and table_num == 0:
            active_players = pd.DataFrame(
                data=table.values,
                columns=[
                    'country',
                    'num',
                    'name',
                    'amplua',
                    'birthday',
                    'height',
                    'weight'
                ]
            )
            active_players['value'] = np.nan
            active_players['url'] = np.nan
            active_players['id'] = ''
            active_players['is_active'] = 'true'
            table_num += 1
        elif table.shape[1] == proper_format and table_num == 1:
            not_active_players = pd.DataFrame(
                data=table.values,
                columns=[
                    'country',
                    'num',
                    'name',
                    'amplua',
                    'birthday',
                    'height',
                    'weight',
                    'value'
                ]
            )
            not_active_players['url'] = np.nan
            not_active_players['id'] = ''
            not_active_players['is_active'] = 'false'
        elif table.shape[1] == poper_format_short and table_num == 1:
            not_active_players = pd.DataFrame(
                data=table.values,
                columns=[
                    'country',
                    'num',
                    'name',
                    'amplua',
                    'birthday',
                    'height',
                    'weight'
                ]
            )
            not_active_players['value'] = np.nan
            not_active_players['url'] = np.nan
            not_active_players['id'] = ''
            not_active_players['is_active'] = 'false'
    active_players_table_row = 0
    not_active_players_table_row = 0
    table_num = 0
    for table_tag in soup.findAll('table'):
        try:
            table_attr = table_tag.attrs.get("class")
            if 'table-responsive' in table_attr and table_num == 0:
                for tr_tag in table_tag.findAll('tr'):
                    if active_players_table_row > 0:
                        country = tr_tag.attrs.get("data-country")
                        player_url_short = tr_tag.find_all(
                            'a'
                        )[0].attrs.get("href")
                        player_url = 'https://www.championat.com' + player_url_short
                        active_players[
                            'country'
                        ][active_players_table_row-1] = country
                        active_players[
                            'url'
                        ][active_players_table_row-1] = player_url
                        id = str(int(player_url_short.split(
                            '/players/',
                            1
                        )[1].replace('/', '')))
                        active_players[
                            'id'
                        ][active_players_table_row-1] = str(id)
                    active_players_table_row += 1
                table_num += 1
                all_players = active_players
            elif 'table-responsive' in table_attr and table_num == 1:
                for tr_tag in table_tag.findAll('tr'):
                    if not_active_players_table_row > 0:
                        country = tr_tag.attrs.get("data-country")
                        player_url_short = tr_tag.find_all(
                            'a'
                        )[0].attrs.get("href")
                        player_url = 'https://www.championat.com' + player_url_short
                        not_active_players[
                            'country'
                        ][not_active_players_table_row-1] = country
                        not_active_players[
                            'url'
                        ][not_active_players_table_row-1] = player_url
                        id = str(
                            int(
                                player_url_short.split(
                                    '/players/',
                                    1
                                )[1].replace('/', '')
                            )
                        )
                        not_active_players[
                            'id'
                        ][not_active_players_table_row - 1] = str(id)
                    not_active_players_table_row += 1
                all_players = active_players.append(
                    not_active_players,
                    ignore_index=True
                )
        except:
            continue
    return all_players


def get_country_info(url):
    soup = BeautifulSoup(_get_html(url), 'lxml')
    ul_tags = soup.find_all('ul')
    for ul_tag in ul_tags:
        try:
            if ul_tag.attrs.get("class")[0].split('-', 1)[0] == 'entity':
                div_tags = ul_tag.find_all('div')
                for div_tag in div_tags:
                    if div_tag.contents[0] == 'Гражданство:':
                        country = div_tag.next_sibling.replace(
                            '  ',
                            ''
                        ).replace('\n', '')
        except Exception as ex:
            print("there is a error of", ex)
            continue
    return str(country)


def get_team_stats(all_players, team_url):
    all_players['games_count'] = ''
    all_players['minutes_amount'] = ''
    stats_url = team_url.replace('result/', '') + 'pstat/'
    soup = BeautifulSoup(_get_html(stats_url), 'lxml')
    tbls = soup.findAll('table')
    for table_tag in tbls:
        try:
            table_attr = table_tag.attrs.get("class")
            if 'table-responsive' in table_attr:
                tr_tags = table_tag.findAll('tr')
                for tr_tag in tr_tags:
                    td_url = tr_tag.contents[3]
                    try:
                        player_href = td_url.contents[1].attrs.get("href")
                        player_id = player_href.split(
                            'players/',
                            1
                        )[1].replace('/', '')
                        player_games = tr_tag.contents[5].text.replace(
                            ' ',
                            ''
                        ).replace('\n', '')
                        player_time = tr_tag.contents[7].text.replace(
                            ' ',
                            ''
                        ).replace('\n', '')
                        for idx in range(len(all_players)):
                            if player_id == all_players['id'][idx]:
                                all_players[
                                    'games_count'
                                ][idx] = str(player_games)
                                all_players[
                                    'minutes_amount'
                                ][idx] = str(player_time)
                    except:
                        continue
        except:
            continue
    return all_players
