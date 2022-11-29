#!/usr/bin/env python

# Read in the data.yml file to describe authors and feeds
# to generate post content for the site. The posts are named based on
# the author tag and date from the feed, as to not generate repeated
# posts.

import argparse
import os
import re
import sys
from datetime import datetime
from time import mktime

import feedparser
import frontmatter
import yaml
from bs4 import BeautifulSoup


def get_parser():

    parser = argparse.ArgumentParser(
        description="Authors Parser",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )

    parser.add_argument("authors", nargs=1, help="the authors.yml file.", type=str)

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        dest="output",
        help="The output folder to write posts.",
    )

    parser.add_argument(
        "--test",
        default=False,
        dest="test",
        action="store_true",
        help="Test generation only (show files to be created)",
    )
    return parser


def validate_authors(authors):
    """validate the list of authors, meaning that:

    1. every author has required fields name, url, tag
    2. there are no repeated tags
    """
    valid = True

    required_fields = ["feed", "url", "name", "tag"]
    tags = set()

    for author in authors:

        # Ensure all required fields
        for field in required_fields:
            if field not in author:
                print("Author is missing %s", field)
                print(author)
                valid = False

        tag = author.get("tag")
        if tag != None and tag in tags:
            print("Found repeat tag %s, not valid" % tag)
            valid = False

    return valid


def slugify(text):
    """
    slugify text!
    """
    return re.sub(r"[\W_]+", "-", text.lower())


def clean_post(post):
    """
    Clean post content:

    1. links that are known to not embed
    2. add extra spacing for sanity and rendering!
    """
    # Add some extra white space for formatting
    for div in ["</div>", "</p>"]:
        post.content = post.content.replace(div, f"{div}\n")

    post.content = post.content.replace('<a name="more"></a>', "")

    # Blogger google images don't embed - thanks Google!
    soup = BeautifulSoup(post.content, "html.parser")

    # These will not embed. We would need to get and save locally
    for image in soup.find_all("img"):
        if image.get("src") and "https://blogger.googleusercontent.com" in image.get(
            "src"
        ):
            image.parent.decompose()
    post.content = soup.renderContents
    return post


def parse_feeds(authors, output_dir, test=False):
    """read in the list of authors, parse feeds and save results to a
    specified output directory.

    Parameters
    ==========
    authors: a list of authors, read in from an authors.yml
    output_dir: the output directory to write markdown posts to.
    test: don't write any files, only test generate
    """
    if output_dir == None:
        print("Output directory must be defined.")
        sys.exit(1)

    output_dir = os.path.abspath(output_dir)
    if not os.path.exists(output_dir):
        print("Output directory %s does not exist." % output_dir)
        sys.exit(1)

    for author in authors:

        # Create output folder
        author_folder = os.path.join(output_dir, author["tag"])
        if not os.path.exists(author_folder):
            if test is False:
                print("Creating new author folder %s" % author_folder)
                os.mkdir(author_folder)
            else:
                print("[TEST] new author folder %s" % author_folder)

        # Parse the feed, each entry is written to file based on title
        feed = feedparser.parse(author["feed"])
        for entry in feed["entries"]:

            markdown = get_markdown_file(author_folder, entry)

            # Write the file if it doesn't exist
            if not os.path.exists(markdown):

                print("Preparing new post: %s" % markdown)
                post = generate_post(entry, author, feed)

                # Custom parsing for blogger
                post = clean_post(post)

                if test is False:

                    # Write to file
                    with open(markdown, "w") as filey:
                        filey.write(frontmatter.dumps(post))


def generate_post(entry, author, feed):
    """
    Generate a post, including content and front end matter, from an entry.
    """
    post = frontmatter.Post(entry["summary"])
    post.metadata["original_url"] = entry.get("link", "")
    post.metadata["title"] = entry.get("title", "")
    post.metadata["author_tag"] = author["tag"]
    post.metadata["layout"] = "post"
    post.metadata["author"] = author.get("name", author["tag"])
    post.metadata["blog_title"] = feed["feed"].get("title", "")
    post.metadata["blog_subtitle"] = feed["feed"].get("subtitle", "")
    post.metadata["blog_url"] = feed["feed"].get("link", "")
    post.metadata["category"] = author["tag"]

    # If we have a title, slugify
    if post.metadata["title"]:
        post.metadata["slug"] = slugify(post.metadata["title"])

    # Remove :
    for key in ["title", "blog_subtitle", "author"]:
        value = post.metadata[key]
        if ":" in value:
            post.metadata[key] = post.metadata[key].replace(":", "-")

    # Convert the time.struct into a datetime object
    # 2017-10-26 23:45:13 -0400
    dt = datetime.fromtimestamp(mktime(entry["published_parsed"]))
    post["date"] = dt.strftime("%Y-%m-%d %H:%M:%S")
    return post


def get_markdown_file(author_folder, entry):
    """return the path to a markdown file in an author folder, where the
    format should be: YYYY-MM-DD-title.md. If the file exists, we won't
    write it again.

    Parameters
    ==========
    author_folder: the author's base folder
    entry: the dict of metadata for the post from feedparser
    """
    year = entry["published_parsed"].tm_year
    month = entry["published_parsed"].tm_mon
    day = entry["published_parsed"].tm_mday

    # The id is the last part of the url, lowercase
    title = [x for x in entry["id"].split("/") if x][-1].lower()

    # Replace any variable names (blogger, wordpress) with -
    for char in ["?", ":", ",", "."]:
        title = title.replace(char, "")
    filename = "%s-%s-%s-%s.md" % (year, month, day, title)

    # The output markdown name is consistent
    return os.path.join(author_folder, filename)


def read_authors(authors_file):
    """
    Read the authors.yml file, exit with retval 1 on error

    Parameters
    ==========
    authors_file: the authors.yml file to read.

    Returns
    =======
    List of authors:

        [{'name': 'Dinosaur',
          'tag': 'dinosaur',
          'url': 'https://dinosaur.org/feed.xml'}, .. ]

    """
    # The authors file must exist
    if not os.path.exists(authors_file):
        print("%s does not exist." % authors_file)
        sys.exit(1)

    with open(authors_file, "r") as stream:
        try:
            authors = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    return authors


def main():

    parser = get_parser()

    def help(return_code=0):
        parser.print_help()
        sys.exit(return_code)

    if len(sys.argv) == 1:
        help()
    try:
        args, options = parser.parse_known_args()
    except:
        sys.exit(0)

    # Read in the authors file, a list of authors and metadata
    authors = read_authors(args.authors[0])

    # Ensure data file is valid
    if not validate_authors(authors):
        print("Authors file %s is not valid." % authors)

    # Generate outputs based on authors
    parse_feeds(authors, args.output, args.test)


if __name__ == "__main__":
    main()
