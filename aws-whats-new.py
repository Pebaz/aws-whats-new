import sys, time, argparse, tempfile, webbrowser, feedparser, yaml
from datetime import datetime, timedelta
from pathlib import Path

# Parse CLI arguments
parser = argparse.ArgumentParser(description='Scrape AWS RSS feed for updates.')
parser.add_argument('--html', action='store_true', required=False)
parser.add_argument('--outfile', required=False, type=Path)
settings = parser.parse_args(sys.argv[1:])

# Define RSS feed source and load profiles config file
RSS_FEED = 'https://aws.amazon.com/new/feed/'
PROFILES = yaml.load(Path('profiles.yml').read_text(), Loader=yaml.FullLoader)

# Fetch new articles from RSS
print('Fetching new articles from RSS...')
blog_posts_by_profile = {profile : [] for profile in PROFILES}
blog_posts_by_profile['uncategorized'] = []

for entry in feedparser.parse(RSS_FEED).entries:
    # Ignore posts older than 1 week old
    published = datetime.fromtimestamp(time.mktime(entry['published_parsed']))
    delta = datetime.now() - published
    if delta.days > 7:
        continue

    title = entry['title']
    for profile in PROFILES:
        for service in PROFILES[profile]:
            if service.lower() in title.lower():
                blog_posts_by_profile[profile].append((
                    entry['link'], profile, title
                ))
                print(f'[{profile}]', title)

    else:
        blog_posts_by_profile['uncategorized'].append((
            entry['link'], None, title
        ))

# Generate html file for easy copy and pasting
if settings.html:
    html_file = settings.outfile or tempfile.mktemp(suffix='.html')

    with open(html_file, 'w') as file:
        file.write('<ul>\n')

        # Ensure bullet points are sorted by profile
        for profile in blog_posts_by_profile:
            if profile == 'uncategorized':
                continue
            for post in blog_posts_by_profile[profile]:
                file.write('<li><a href="{}">[{}] {}</a></li>\n'.format(*post))

        file.write('</ul>\n')

        file.write('<h3>Uncategorized Posts</h3>')
        file.write('<ul>\n')
        for (url, _, title) in blog_posts_by_profile['uncategorized']:
            file.write('<li><a href="{}">{}</a></li>\n'.format(url, title))
        file.write('</ul>\n')


    webbrowser.open(f'file://{html_file}')

# Display skipped articles
print(blog_posts_by_profile['uncategorized'])
for (url, _, title) in blog_posts_by_profile['uncategorized']:
     print(title)

     aws = title.split('AWS')
     amazon = title.split('Amazon')
