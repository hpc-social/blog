---
author: Jonathan Dursi's Blog
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2017-02-15 00:00:00'
layout: post
original_url: http://www.dursi.ca/post/beyond-single-core-R.html
title: Beyond Single Core R- Parallel Data Analysis
---

<p>I was asked recently to do short presentation for the <a href="https://www.meetup.com/Greater-Toronto-Area-GTA-R-Users-Group">Greater Toronto R Users Group</a>
on parallel computing in R; My slides can be seen below or on <a href="https://ljdursi.github.io/beyond-single-core-R">github</a>, where <a href="https://github.com/ljdursi/beyond-single-core-R">the complete materials can be found</a>.</p>

<p>I covered some similar things I had covered in a half-day workshop
a couple of years earlier (though, obviously, without the hands-on
component):</p>
<ul>
  <li>How to think about parallelism and scalability in data analysis</li>
  <li>The standard parallel package, including what was the snow and multicore facilities, using airline data as an example</li>
  <li>The foreach package, using airline data and simple stock data;</li>
  <li>A summary of best practices,</li>
</ul>

<p>with some bonus material tacked on the end touching on a couple advanced topics.</p>

<p>I was quite surprised at how little had changed since late 2014, other than 
further development of <a href="http://spark.apache.org/docs/latest/sparkr.html">SparkR</a> (which
I didn’t cover), and the interesting but seemingly not very much used <a href="https://cran.r-project.org/web/packages/future/index.html">future</a>
package.   I was also struck by how hard it is to find similar materials
online, covering a range of parallel computing topics in R - it’s rare enough
that even this simple effort made it to the <a href="https://cran.r-project.org/web/views/HighPerformanceComputing.html">HPC project view on CRAN</a> 
(under “related links”).  R <a href="http://spectrum.ieee.org/computing/software/the-2016-top-programming-languages">continues to grow in popularity</a> for data analysis; 
is this all desktop computing?  Is Spark siphoning off the clustered-dataframe
usage?</p>

<p>(This was also my first time with <a href="https://support.rstudio.com/hc/en-us/articles/200486468-Authoring-R-Presentations">RPres</a> in RStudio;
wow, not a fan, RPres was <em>not</em> ready for general release.  And I’m a big fan of RMarkdown.)</p>