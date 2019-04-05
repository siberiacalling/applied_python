# -*- encoding: utf-8 -*-
import collections
import datetime
import heapq
import re


def count_urls(urls):
    top_five_urls = []
    counter = collections.Counter(urls)
    for url, count in counter.most_common(5):
        top_five_urls.append(count)
    return top_five_urls


def update_url_to_statsionary(d, url, time, ignore_www):
    url = get_www_ignore(url, ignore_www)
    d[url]['time'] += time
    d[url]['amount'] += 1
    return d


def get_www_ignore(url, ignore_www):
    if ignore_www:
        url = url.replace('www.', '')
        return (url)
    else:
        return (url)


def get_n_max_time(url_to_stats, n=5):
    def get_time(url): return url_to_stats[url]['time'] / url_to_stats[url]['amount']

    return [int(get_time(url)) for url in heapq.nlargest(n, url_to_stats, key=get_time)]


def make_list_all_urls(ignore_www, url, urls):
    url = get_www_ignore(url, ignore_www)
    urls.append(url)
    return urls


def get_result(url_to_stats, urls):
    if len(url_to_stats) == 0:
        result = count_urls(urls)
    else:
        result = get_n_max_time(url_to_stats)
    return result


def check_parse_params(result, ignore_urls, start_at, stop_at, request_type, ignore_files):
    bool_ignore_urls = check_ignore_urls(result, ignore_urls)
    if not bool_ignore_urls:
        return False
    bool_date = check_date(result, start_at, stop_at)
    if not bool_date:
        return False
    bool_request_type = check_request_type(result, request_type)
    if not bool_request_type:
        return False
    bool_ignore_files = check_ignore_files(result, ignore_files)
    if not bool_ignore_files:
        return False
    return True


def check_ignore_files(result, ignore_files):
    if not ignore_files:
        return True
    else:
        search_file = re.search('\.(html|htm|png|jpeg|css|gif|js)$', result.group('url'))
        if search_file is not None:
            return False
        else:
            return True


def check_request_type(result, request_type):
    if request_type is None:
        return True
    else:
        if result.group('type') == request_type:
            return True
        else:
            return False


def check_ignore_urls(result, ignore_urls):
    if len(ignore_urls) == 0:
        return True
    else:
        if result.group('url') not in ignore_urls:
            return True
        else:
            return False


def check_date(result, start_at, stop_at):
    if start_at is None and stop_at is None:
        return True
    else:
        d1 = start_at
        d2 = stop_at
        date_str = result.group('year') + result.group('month') + result.group('day')
        d = datetime.datetime.strptime(date_str, '%Y%b%d')
        if d1 is not None and d2 is not None:
            if d1 <= d <= d2:
                return True
            else:
                return False
        elif d1 is None:
            if d <= d2:
                return True
            else:
                return False
        elif d2 is None:
            if d1 <= d:
                return True
            else:
                return False


def parse(
        ignore_files=True,
        ignore_urls=[],
        start_at=None,
        stop_at=None,
        request_type=None,
        ignore_www=False,
        slow_queries=False
):
    regexp = ('^\[(?P<day>(0[1-9]|[12][0-9]|3[01]))'
              '/(?P<month>(Jan|Feb|Mar|Apr|May|June|July|Aug|Sept|Oct|Nov|Dec))'
              '/(?P<year>(19|20)\d\d)'
              ' (?P<h>(2[0-3]|[0-1]\d))'
              ':(?P<min>([0-5]\d))'
              ':(?P<sec>([0-5]\d))\]'
              ' "(?P<type>(GET|POST|PUT))'
              ' (http|ftp|https)://(?P<url>(([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?))'
              ' (?P<protocol>((HTTP|HTTPS|FTP)/\d(.\d)?))'
              '" (?P<code>(\d\d\d))'
              ' (?P<time>([\d]+))')
    f = open('log.log')
    url_to_stats = collections.defaultdict(lambda: collections.defaultdict(int))
    urls = []
    for line in f:
        result = re.match(regexp, line)
        if result is not None and check_parse_params(result, ignore_urls, start_at, stop_at, request_type,
                                                     ignore_files):
            if slow_queries:
                url_to_stats = update_url_to_statsionary(url_to_stats, result.group('url'), int(result.group('time')),
                                                         ignore_www)
            else:
                urls = make_list_all_urls(ignore_www, result.group('url'), urls)
    result = get_result(url_to_stats, urls)
    return result
