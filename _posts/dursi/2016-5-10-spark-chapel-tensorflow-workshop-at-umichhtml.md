---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2016-05-10 01:00:00'
layout: post
original_url: http://www.dursi.ca/post/spark-chapel-tensorflow-workshop-at-umich.html
title: Spark, Chapel, TensorFlow- Workshop at UMich
---

<p>The kind folks at the University of Michigan’s <a href="http://micde.umich.edu">Center for Computational Discovery and Engineering (MICDE)</a>, which is just part of the very impressive <a href="http://arc.umich.edu">Advanced Research Computing</a> division, invited me to give a workshop there a couple of months ago about the rapidly-evolving large-scale numerical computing ecosystem.</p>

<p>There’s lots that I want to do to extend this to a half-day length, but the workshop materials — including a VM that can be used to play with <a href="http://spark.apache.org">Spark</a>, <a href="http://chapel.cray.com">Chapel</a> and <a href="https://www.tensorflow.org">TensorFlow</a>, along with Jupyter notebooks for each — can be found <a href="https://github.com/ljdursi/Spark-Chapel-TF-UMich-2016">on GitHub</a> and may be of some use to others as they stand.</p>

<p>The title and abstract follow.</p>

<blockquote>
  <h4 id="next-generation-hpc--what-spark-tensorflow-and-chapel-are-teaching-us-about-large-scale-numerical-computing">Next Generation HPC?  What Spark, TensorFlow, and Chapel are teaching us about large-scale numerical computing</h4>
</blockquote>

<blockquote>
  <p>For years, the academic science and engineering community was almost alone in pursuing very large-scale numerical computing, and MPI - the 1990s-era message passing library - was the lingua franca for such work.  But starting in the mid-2000s, others became interesting in large-scale computing on data.  First internet-scale companies like Google and Yahoo! started performing fairly basic analytics tasks at enormous scale, and now many others are tackling increasingly complex and data-heavy machine-learning computations, which involve very familiar scientific computing tasks such as linear algebra, unstructured mesh decomposition, and numerical optimization.  But these new communities have created programming environments which emphasize what we’ve learned about computer science and programmability since 1994 - with greater levels of abstraction and encapsulation, separating high-level computation from the low-level implementation details, and some in HPC are starting to notice.  This talk will give a brief introduction to Apache Spark environment and Google’s Tensor Flow machine-learning package for high-level numerical computation, as well as the HPC-focused Chapel language from Cray, to show where each can be used today and how they might be used in the future.   The slides for this talk, and examples for each package along with a virtual machine which can be used for running them, will be available at https://github.com/ljdursi/Spark-Chapel-TF-UMich-2016 .</p>
</blockquote>