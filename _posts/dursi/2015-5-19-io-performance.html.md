---
author: Jonathan Dursi's Blog
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2015-05-19 00:00:00'
layout: post
original_url: http://www.dursi.ca/post/io-performance.html
title: On Random vs. Streaming I/O Performance; Or seek(), and You Shall Find ---
  Eventually.
---

<p>At the <a href="http://simpsonlab.github.io/blog/">Simpson Lab blog</a>, I’ve written a post
<a href="http://simpsonlab.github.io/2015/05/19/io-performance/">on streaming vs random access I/O performance</a>,
an important topic in bioinformatics. Using a very simple problem (randomly choosing lines in a 
non-indexed text file) I give a quick overview of the file system stack and what it means for
streaming performance, and reservoir sampling for uniform random online sampling.</p>