# hpc.social Community Syndicated Blog

This is a syndicated blog to provide content for the hpc.social community!
Here you can add an rss/xml feed to share stories and experiences. This
repository is based on the [US-RSE community blog](https://github.com/USRSE/blog), 
which was also imagined, designed, and implemented by author [@vsoch](https://github.com/vsoch).

## How does it work?

### 1. Add Metadata

An center, group, or individual that has a blog, podcast, or similar feed can add their
metadata to the [authors.yml](_data/authors.yml) file. Here is an example
of the required fields that we collect:

```yaml
- name: "hpc.social"
  tag: "hpc-social"
  url: https://hpc.social/
  feed: https://hpc.social/feed.xml
```

The tag must be unique (and this is tested), and the feed should be a format
parseable by [feedparser](https://pythonhosted.org/feedparser/) (most are).

#### Wordpress

WordPress is a common blogging platform, and so we include notes here for how
to find a feed for your wordpress blog. If you want to include all content,
you can usually find a main feed at `https://<yourblog>/feed/`. However, it's
recommended to create a [tag or category](https://wordpress.org/support/article/wordpress-feeds/#categories-and-tags)
feed, in which case you could find the feed at `https://<yourblog>/category/<category>/feed/`. See the linked
page for more ways that you can generate custom feeds based on tags and categories.
Once you've added your feed, it's recommended to test generate posts to ensure
that it's parsed correctly. This is done during the continuous integration,
but you can also do it locally (see below).

### 2. Generate Posts

The posts are generated automatically - we do this by way of a cron job (scheduled
job). During the run, each feed is read, and any new posts are generated
as markdown files, with the author tag corresponding to the folder name in [_posts](_posts).
If the post is already included, it is skipped over. This is a reasonable task to do,
because typically feeds only provide the 10 (or a small number) of latest posts.

If you look at the [.github/workflows](.github/workflows) you'll notice that
this workflow runs by way of a nightly job, and you can reproduce it locally!
Here is how:

First install python dependencies:

```bash
$ pip install -r .github/requirements.txt
```

```bash
$ python scripts/generate_posts.py _data/authors.yml --output _posts/ --test
```

It will show you any new folders and files generated without actually doing it.

```bash
$ python scripts/generate_posts.py _data/authors.yml --output _posts/ --test
```

## Development

To develop the site, clone the repository and then build with jekyll:

```bash
$ bundle exec jekyll serve
```

You can also run the script to generate posts locally, if you choose.

```bash
cd script

python generate_posts.py
usage: generate_posts.py [-o OUTPUT] authors

Authors Parser

positional arguments:
  authors               the authors.yml file.

optional arguments:
  -o OUTPUT, --output OUTPUT
                        The output folder to write posts.
```

This is how the posts are generated in the continuous integration setup:

```bash
python generate_posts.py ../_data/authors.yml --output ../_posts/
```

### Important Notes

The "posts" page under the [posts](posts) folder is intentionally separate from
the other pages in [pages](pages) because the pagination plugin needs to find an
index.html to parse. Please don't rename or change the location of this file.
