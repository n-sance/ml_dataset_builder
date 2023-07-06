import argparse
from pathlib import Path

from src.parsers.similarweb import similarweb_get
from src.parsers.ssl_checker import check_ssl_certificate
from src.parsers.domain_age import get_domain_age
from src.parsers.content_analysis.analyzer import analyze_page_content
from src.common.url_management import parse_url
from src.common.files_management import write_csv, read_urls


def process_arguments():
    parser = argparse.ArgumentParser(description='Process URLs')
    parser.add_argument('-i', '--input_path', type=Path, help='Path to input file with URLs')
    parser.add_argument('-o', '--output_path', type=Path, help='Path to output CSV file')
    parser.add_argument('-m', '--mode', choices=['online', 'offline'], default='online', help='Processing mode '
                                                                                              '(online or offline)')
    parser.add_argument('-s', '--stored_websites_folder', type=Path, help='Path to folder containing stored websites')

    return parser.parse_args()


def process_url(url: str, mode: str = 'online', storage: Path = None) -> dict:
    result = {'url': url}

    scheme, netloc, path_n_params = parse_url(url)

    result['name'] = netloc
    result['country'], \
    result['rank_local'], \
    result['rank_global'], \
    result['average_time_on_site_sec'], \
    result['visits'] = similarweb_get(netloc)
    result['has_ssl'], \
    result['has_ssl_self_signed'], \
    result['ssl_date'] = check_ssl_certificate(netloc, scheme)
    result['whois_age_days'] = get_domain_age(netloc)

    result['has_http_links'], \
    result['has_inputs'], \
    result['has_pwds'], \
    result['has_textareas'] = analyze_page_content(scheme, netloc, path_n_params, mode, storage, store_text=True)

    print(f'|{netloc}| processed')
    return result


def main():
    args = process_arguments()

    urls = read_urls(args.input_path)
    print(f'Provided {len(urls)} urls')
    print(f'Mode {args.mode}')
    if args.mode == 'offline':
        print(f'Storage folder: {args.stored_websites_folder}')

    results = []
    for i, url in enumerate(urls):
        print(f'{i + 1}/{len(urls)}')
        result = process_url(url, args.mode, args.stored_websites_folder)
        results.append(result)

    write_csv(args.output_path, results)


if __name__ == '__main__':
    main()
