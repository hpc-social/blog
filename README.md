# hpc.social Blogs

Welcome to the hpc.social blogs! This is a portal for our family of blogs:

 - [Community Blog](https://hpc.social/community-blog/) served from [this repository](https://github.com/hpc-social/community-blog)
 - [Personal Blog](https://hpc.social/personal-blog/) served from [this repository](https://github.com/hpc-social/personal-blog)
 - [Commercial Blog](https://hpc.social/commercial-blog/) served from [this repository](https://github.com/hpc-social/commercial-blog)
 
This central point serves to provide shared instructions for contributing to each, along with 
how to decide which blog your feed is scoped to. 

## Which blog should I add my feed to?

This comes down to a simple question - are you writing from a personal blog about your work and ideas, or do you represent some kind of entity or project?
In more detailed terms:

- **The Personal blogs aggregator** is the "soul" of the HPC community - HPCers who are personally invested in the minutiae of the work they are doing, the projects they are working on with some content about their culture, life, and thoughts. 

- **The Community content aggregator**: is content from people who represent projects, ecosystems, or governance boards that talk about specific community interested content around the work they represent. The content range from release notes, tricks and tips, discussion around tooling and infrastructure, and other things that are neutrally branded. Discussion of branded topics like CUDA, SYCL, and oneAPI are ok - discussions about hardware are ok. Product announcements are not ok especially.

- **The Commercial blogs aggregator** includes content for vendor and company voices that don't fit in the personal or community spaces. We advocate for learning resources, tutorials, and related content,  and discourage advertising or similar.

We generally try to be inclusive, and thus have created these two spaces to support different kinds of feeds!
However, if moderators of the hpc.social community receive a complaint or themselves feel that a piece of content crosses the line between "Here's a cool thing we're doing" and "Here is a product we want to sell you" that feels like a breach of trust, you will be contacted first to have discussion about how to mediate the situation, and in the worst of cases that remediation is not possible, the blog or individual post may be removed.

Once you choose a blog, move on to the next steps in the instructions below! 

> ⚠️ **important** The blog you chose from the links above should be the one that you clone, and not the central portal repository where you are reading the instructions now.

## How do I contribute my blog?

Each blog mentioned above serves it's own set of feeds (e.g., if people only are interested in a subset
of content) and a master aggregated feed (that hits both syndicated blogs) is served from here.
Thus, you can add an rss/xml feed to share stories and experiences to be presented in either feed,
and it will show up in the feed for the respective repository and the [aggregated blogs feed](https://hpc.social/blog/)
here. Here is how to get started, for either of the above!

1. Fork the repository that you've chosen in the step above (**you should not be forking this repository where you are reading!**), checkout a new branch, and clone it to your machine.
1. Add your entry to the [_data/authors.yml](_data/authors.yml) file
1. Generate your set of posts (instructions below)
1. Push your change to GitHub
1. Open a pull request to the main repository!

> ⚠️ **important** The blog you chose from the links above should be the one that you clone, and not the central portal repository where you are reading the instructions now.

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

#### Blogger

Blogger is Google's blogging platform and also provides a main feed at 
`https://<yourblog>.blogspot.com/feeds/posts/default`.
Like Wordpress, you can also create a feed for a specific [label or
tag](https://support.google.com/blogger/answer/97933) which can be accessed via
`https://<yourblog>.blogspot.com/feeds/posts/default/-/<label>`.  The page
linked above also describes options if you want to publish only the first part
of each post to your feed.

A known limitation with Blogger is that images embedded in blog posts won't
appear in the Community Syndicated Blog version.  This happens because
[Blogger disallows directly linking blog images from external
sources](https://support.google.com/blogger/thread/133238986/image-url-from-blogger-googleusercontent-com-is-not-accepted-by-other-websites-if-i-want-to-insert-m?hl=en).

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

And then generate posts:

```bash
$ python scripts/generate_posts.py _data/authors.yml --output _posts/ --test
```

It will show you any new folders and files generated without actually doing it.
Here is how to do it "for realsies":

```bash
$ python scripts/generate_posts.py _data/authors.yml --output _posts/
```

## Blog Site Development

To develop the site, clone the repository and then build with jekyll:

```bash
$ bundle exec jekyll serve
```

You can also run the script to generate posts locally, if you choose.

```bash
cd scripts

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

## How is the feed generated here?

We have plans to aggregate the feeds, and for now we are pulling the 
personal blog feed (to ensure the current functionality with the previous
blog site is consistent). If you would like to contribute automation
to merge the two feeds, please open a pull request!


## 🎨️ Thank You! 🎨️

This is a modified version of [Ephesus](https://github.com/onepase/Ephesus). We
maintain the original [LICENSE](.github/LICENSE-Ephesus) and preserve it [here](LICENSE).
