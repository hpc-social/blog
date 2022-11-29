---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2014-09-04 01:00:00'
layout: post
original_url: http://www.dursi.ca/post/hadoop-for-hpcers.html
slug: hadoop-for-hpcers
title: Hadoop For HPCers
---

<p>I and my colleague Mike Nolta have put together <a href="https://github.com/ljdursi/hadoop-for-hpcers-tutorial">a half-day tutorial on Hadoop</a> - briefly covering HDFS, Map Reduce, <a href="http://pig.apache.org">Pig</a>, and Spark - for an HPC audience, and put the materials on <a href="https://github.com/ljdursi/hadoop-for-hpcers-tutorial">github</a>.</p>


<p>The <a href="https://hadoop.apache.org">Hadoop</a> ecosystem of tools continues to rapidly grow, and now includes tools like <a href="https://spark.apache.org">Spark</a> and <a href="http://flink.incubator.apache.org">Flink</a> that are very good for iterative numerical computation - either simulation or data analysis.   These tools, and the underlying technologies, are (or should be) of real interest to the HPC community, but most materials are written for audiences with web application or maybe machine-learning backgrounds, which makes it harder for an HPC audience to see how they can be useful to them and how they might be applied.</p>


<p>Most of the source code is Python.  Included on git hub are all sources for the examples, a vagrantfile for a VM to run the software on your laptop, and the presentation in <a href="https://github.com/ljdursi/hadoop-for-hpcers-tutorial/blob/master/presentation/presentation.md">Markdown</a> and <a href="https://github.com/ljdursi/hadoop-for-hpcers-tutorial/blob/master/presentation/keynote-presentation.pdf?raw=true">PDF</a>.  Feel free to fork, send pull requests, or use the materials as you see fit.</p>