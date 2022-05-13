import requests
from input_source_reader import get_output_format, get_source_list
from web_extractor import get_pattern_url, get_teams_url_list
from web_extractor import get_players_info, get_team_stats
import pandas as pd


def create_template(xls_name, xls_sheetname_format, set_range):
    columns_list = get_output_format(xls_name, xls_sheetname_format)
    output_dataframe = pd.DataFrame(
        columns=columns_list,
        index=range(set_range)
    )
    return output_dataframe


def prepare_source_list(xls_name, xls_sheetname_sources):
    source_list = get_source_list(xls_name, xls_sheetname_sources)
    for source in source_list:
        response_code = requests.get(
            source[0],
            headers={"User-Agent": "Firefox/67.0.4"}
        ).status_code
        print(
            'source url: ',
            source[0],
            'response status code (200 - OK): ',
            response_code
        )
    return source_list


def data_extractor(team_url):
    response_code = requests.get(
        team_url,
        headers={"User-Agent": "Firefox/67.0.4"}
    ).status_code
    if response_code == 200:
        players_list = get_players_info(team_url)
        all_players = get_team_stats(players_list, team_url)
    return all_players


def data_transformer(xls_name, xls_sheetname_format, source_list):
    output_frame = create_template(xls_name, xls_sheetname_format, 0)
    for source in source_list:
        response_code = requests.get(
            source[0],
            headers={"User-Agent": "Firefox/67.0.4"}
        ).status_code
        if response_code == 200:
            tournament_url = get_pattern_url(source[0], pattern='Турнир')
            teams_info = get_teams_url_list(source[0], pattern='teams')
            for idx in range(len(teams_info)):
                all_players = data_extractor(teams_info['team_url'][idx])
                output_format = create_template(
                    xls_name,
                    xls_sheetname_format,
                    len(all_players)
                )
                for row in range(len(all_players)):
                    output_format['ссылка на страницу турнира'][
                        row
                    ] = tournament_url
                    output_format['сслыка на страницу команды'][
                        row
                    ] = teams_info['team_url'][idx]
                    output_format['название команды'][
                        row
                    ] = teams_info['team_name'][idx]
                    output_format['ссылка на страницу игрока'][
                        row
                    ] = all_players['url'][row]
                    output_format['имя игрока'][
                        row
                    ] = all_players['name'][row]
                    output_format['гражданство'][
                        row
                    ] = all_players['country'][row]
                    output_format['дата рождения'][
                        row
                    ] = all_players['birthday'][row]
                    output_format['количество игр в которых участвовал игрок'][
                        row
                    ] = all_players['games_count'][row]
                    output_format['количество минут, проведенных на поле'][
                        row
                    ] = all_players['minutes_amount'][row]
                output_frame = output_frame.append(output_format)
                print(
                    'processed rows : ',
                    len(output_frame)
                )
        else:
            print('check connection status')
    return output_frame
