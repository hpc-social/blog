---
author: Mark Nelson's Blog
author_tag: markhpc
blog_subtitle: I like to make distributed systems go fast.
blog_title: Mark Nelson’s Blog
blog_url: https://markhpc.github.io/
category: markhpc
date: '2022-04-13 01:00:00'
layout: post
original_url: https://markhpc.github.io/2022/04/13/Spooky-Allocator.html
slug: spooky-allocator-issues-and-fixes
title: Spooky Allocator Issues and Fixes
---

<p>Recently we started noticing performance issues in the main branch of Ceph that ultimately were traced back to a commit last summer that changed parts of our AVL and hybrid disk allocator implementations in bluestore.  Strangly, the issue only affected some of the NVMe drives in our test lab but not others.  The quick <a href="https://github.com/ceph/ceph/pull/45884">fix</a> was to always update and save the allocator’s cursor position so that we don’t search (and fail) over and over in fast-fit mode for every allocation request.  Another interesting offshoot of this though is that it may be much <a href="https://github.com/ceph/ceph/pull/45771">nicer</a> to limit fast-fit searches based on time rather than byte distance or the number of iterations.</p>