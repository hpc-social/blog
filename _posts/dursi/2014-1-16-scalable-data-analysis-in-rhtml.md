---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2014-01-16 00:00:00'
layout: post
original_url: http://www.dursi.ca/post/scalable-data-analysis-in-r.html
title: Scalable Data Analysis in R
---

<p>R is a great environment for interactive analysis on your desktop, but when your data needs outgrow your personal computer, it’s not clear what to do next.</p>

<p>I’ve put together material for a day-long tutorial on scalable data analysis in R.  It covers:</p>

<ul>
  <li>A brief introduction to R for those coming from a Python background;</li>
  <li>The <a href="http://cran.r-project.org/web/packages/bigmemory/index.html">bigmemory</a> package for out-of-core computation on large data matrices, with a simple physical sciences example;</li>
  <li>The standard parallel package, including what was the snow and multicore facilities, using <a href="http://stat-computing.org/dataexpo/2009/the-data.html">airline data</a> as an example</li>
  <li>The <a href="http://cran.r-project.org/web/packages/foreach/index.html">foreach</a> package, using airline data and simple stock data;</li>
  <li>The <a href="http://cran.r-project.org/web/packages/Rdsm/index.html">Rdsm</a> package for shared memory; and</li>
  <li>a brief introduction to the powerful <a href="http://r-pbd.org">pbdR</a> pacakges for extremely large-scale computation.</li>
</ul>

<p>The presentation for the material, in R markdown (so including the sourcecode) is in the presentation directory; you can read the resulting presentation <a href="https://github.com/ljdursi/scalable-analysis-R/blob/master/presentation/ScalableDataAnalysis-R.md">as markdown there</a>, or <a href="https://github.com/ljdursi/scalable-analysis-R/blob/master/presentation/ScalableDataAnalysisInR.pdf?raw=true">as a PDF</a>.</p>

<p>The R code from the slides can be found in the R directory.</p>

<p>Some data can be found in the data directory; but as you might expect in a workshop on scalable data analysis, the files are quite large!  Mostly you can just find scripts for downloading the data; running make in the main directory will pull almost everything down, but a little more work needs go to into automating some of the production of the data products used.</p>

<p>Suggestions, as always, greatly welcomed.</p>