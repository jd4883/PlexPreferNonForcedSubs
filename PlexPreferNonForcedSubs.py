from plexapi.server import PlexServer
from plexapi.media import SubtitleStream
import os
import traceback
import time

def report_error(error_message):
    github_issue_url = "https://github.com/RileyXX/PlexPreferNonForcedSubs/issues/new?template=bug_report.yml"
    traceback_info = traceback.format_exc()

    print("\n--- ERROR ---")
    print(error_message)
    print("Please submit the error to GitHub with the following information:")
    print("-" * 50)
    print(traceback_info)
    print("-" * 50)
    print(f"Submit the error here: {github_issue_url}")
    print("-" * 50)

def create_plex_session():
    baseurl = os.getenv('PLEX_URL','http://localhost:32400')
    token = os.getenv('PLEX_TOKEN', 'UNSET')
    if token == 'UNSET':
        print(f'\nHow to get your Plex token: https://www.plexopedia.com/plex-media-server/general/plex-token/\n')
        token = os.environ["PLEX_TOKEN"] = input("Enter your Plex token: ")            
    return PlexServer(baseurl, token)

def retrieve_subtitle_stream(item):
    try:
        return item.subtitleStreams()
    except: # TODO: exact except would be better design
        print(f"Error looking up {item}, sleeping for 5 seconds and trying again")
        time.sleep(5)
        retrieve_subtitle_stream(item)
        


def parse_movies(plex):
    table_headers = ['Title', 'Year', 'Status', 'Changes']
    title_width = 70
    year_width = 5
    status_width = 20
    changes_width = 8

    print("\n" + "-" * 114 + "\nMovies\n" + "-" * 114)
    print(f'\033[1m\033[96m{" | ".join([h.ljust(title_width if i == 0 else year_width if i == 1 else status_width if i == 2 else changes_width) for i, h in enumerate(table_headers)])}\033[0m')

    for section in plex.library.sections():
        if section.type == 'movie':
            for movie in section.all():
                english_subs = retrieve_subtitle_stream(movie)
                if english_subs is not None:
                    english_subs = [stream for stream in english_subs if stream is not None and stream.languageCode == 'eng']
                    non_forced_english_subs = [stream for stream in english_subs if stream is not None and (not stream.forced or (hasattr(stream, 'title') and 'forced' not in (getattr(stream, 'title', '') or '').lower()))]
                    forced_english_subs = [stream for stream in english_subs if stream is not None and (stream.forced or (hasattr(stream, 'title') and 'forced' in (getattr(stream, 'title', '') or '').lower()))]
                    part = movie.media[0].parts[0]
                    partsid = part.id
                    if forced_english_subs and non_forced_english_subs:
                        non_forced_english_subs[0].setSelected()
                        #non_forced_english_subs[0].setDefault()
                        print(f'\033[92m{movie.title[:title_width].ljust(title_width)} | {str(movie.year).ljust(year_width)} | {"English (Non-Forced)".ljust(status_width)} | {"Y".ljust(changes_width)}\033[0m')
                    elif non_forced_english_subs and not forced_english_subs:
                        print(f'{movie.title[:title_width].ljust(title_width)} | {str(movie.year).ljust(year_width)} | {"English".ljust(status_width)} | {"N".ljust(changes_width)}')
                    elif not non_forced_english_subs and not forced_english_subs:
                        print(f'\033[91m{movie.title[:title_width].ljust(title_width)} | {str(movie.year).ljust(year_width)} | {"No Subtitles Found".ljust(status_width)} | {"N".ljust(changes_width)}\033[0m')
                    else:
                        print(f'\033[91m{movie.title[:title_width].ljust(title_width)} | {str(movie.year).ljust(year_width)} | {"English (Forced)".ljust(status_width)} | {"N (Error)".ljust(changes_width)}\033[0m')

def parse_shows(plex):
    table_headers = ['Title', 'Year', 'Season #', 'Episode #', 'Status', 'Changes']
    title_width = 42
    year_width = 5
    season_width = 11
    episode_width = 11
    status_width = 20
    changes_width = 8
    season_row_width = 4
    episode_row_width = 3

    print("\n" + "-" * 114 + "\nShows\n" + "-" * 114)
    print(f'\033[1m\033[96m{" | ".join([h.ljust(title_width if i == 0 else year_width if i == 1 else season_width if i == 2 else episode_width if i == 3 else status_width if i == 4 else changes_width) for i, h in enumerate(table_headers)])}\033[0m')

    for section in plex.library.sections():
        if section.type == 'show':
            for show in section.all():
                for episode in show.episodes():
                    english_subs = retrieve_subtitle_stream(episode)
                    if english_subs is not None:
                        english_subs = [stream for stream in english_subs if stream is not None and stream.languageCode == 'eng']
                        non_forced_english_subs = [stream for stream in english_subs if stream is not None and (not stream.forced or (hasattr(stream, 'title') and 'forced' not in (getattr(stream, 'title', '') or '').lower()))]
                        forced_english_subs = [stream for stream in english_subs if stream is not None and (stream.forced or (hasattr(stream, 'title') and 'forced' in (getattr(stream, 'title', '') or '').lower()))]
                        part = episode.media[0].parts[0]
                        partsid = part.id
                        if forced_english_subs and non_forced_english_subs:
                            non_forced_english_subs[0].setDefault()
                            print(f'\033[92m{show.title[:title_width].ljust(title_width)} | {str(show.year).ljust(year_width)} | {"Season " + str(episode.seasonNumber).ljust(season_row_width)} | {"Episode " + str(episode.index).ljust(episode_row_width)} | {"English (Non-Forced)".ljust(status_width)} | {"Y".ljust(changes_width)}\033[0m')
                        elif non_forced_english_subs and not forced_english_subs:
                            print(f'{show.title[:title_width].ljust(title_width)} | {str(show.year).ljust(year_width)} | {"Season " + str(episode.seasonNumber).ljust(season_row_width)} | {"Episode " + str(episode.index).ljust(episode_row_width)} | {"English".ljust(status_width)} | {"N".ljust(changes_width)}')
                        elif not non_forced_english_subs and not forced_english_subs:
                            print(f'\033[91m{show.title[:title_width].ljust(title_width)} | {str(show.year).ljust(year_width)} | {"Season " + str(episode.seasonNumber).ljust(season_row_width)} | {"Episode " + str(episode.index).ljust(episode_row_width)} | {"No Subtitles Found".ljust(status_width)} | {"N".ljust(changes_width)}\033[0m')
                        else:
                            print(f'\033[91m{show.title[:title_width].ljust(title_width)} | {str(show.year).ljust(year_width)} | {"Season " + str(episode.seasonNumber).ljust(season_row_width)} | {"Episode " + str(episode.index).ljust(episode_row_width)} | {"English (Forced)".ljust(status_width)} | {"N (Error)".ljust(changes_width)}\033[0m')

if __name__ == '__main__':
    try:
        plex = create_plex_session()
        parse_movies(plex)
        parse_shows(plex)
    except Exception as e:
        error_message = "An error occurred while running the script."
        report_error(error_message)
