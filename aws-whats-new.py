import tempfile, webbrowser, feedparser, yaml

RSS_FEED = 'https://aws.amazon.com/new/feed/'

with open('profiles.yml') as profiles_file:
    PROFILES = yaml.load(profiles_file.read(), Loader=yaml.FullLoader)
    print(PROFILES)

blog_posts_by_profile = {profile : [] for profile in PROFILES}

html_file = tempfile.mktemp(suffix='.html')
with open(html_file, 'w') as file:
    file.write('<ul>\n')

    for entry in feedparser.parse(RSS_FEED).entries:
        title = entry['title']
        for profile in PROFILES:
            for service in PROFILES[profile]:
                if service.lower() in title.lower():
                    blog_posts_by_profile[profile].append((
                        entry['link'], profile, title
                    ))
                    print(f'[{profile}]', title)

    # Ensure bullet points are sorted by profile
    for profile in blog_posts_by_profile:
        for post in blog_posts_by_profile[profile]:
            file.write('<li><a href="{}">[{}] {}</a></li>\n'.format(*post))

    file.write('</ul>\n')

webbrowser.open(f'file://{html_file}')
