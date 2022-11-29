---
author: Mark Nelson's Blog
author_tag: markhpc
blog_subtitle: I like to make distributed systems go fast.
blog_title: Mark Nelson’s Blog
blog_url: https://markhpc.github.io/
category: markhpc
date: '2022-01-12 00:00:00'
layout: post
original_url: https://markhpc.github.io/2022/01/12/Age-Binning.html
slug: cache-age-binning-pr-finally-merged-
title: Cache Age Binning PR Finally Merged!
---

<p>I’ve had this PR hanging around in various forms for years.  It’s basically the last peice of the OSD memory target code.  We can now get a “binned” view of the relative ages of items in different LRU caches and dynamically adjust target sizes for different caches.  PR is <a href="https://github.com/ceph/ceph/pull/43299">here</a> and memory usage behavior charts are <a href="https://docs.google.com/spreadsheets/d/1lSp2cLzYmRfPILDCyLMXciIfdf0OvSFngwXukQFXIqQ/edit?usp=sharing">here</a>.</p>