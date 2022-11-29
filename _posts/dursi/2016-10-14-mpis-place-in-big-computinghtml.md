---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2016-10-14 01:00:00'
layout: post
original_url: http://www.dursi.ca/post/mpis-place-in-big-computing.html
slug: mpi-s-place-in-big-computing
title: MPI's Place in Big Computing
---

<p>The organizers of <a href="http://www.eurompi2016.ed.ac.uk">EuroMPI 2016</a> were kind enough to invite me to give a keynote and participate in a panel at their meeting, which was held at the end of September in beautiful Edinburgh.  The event was terrific, with lots of very interesting work going on in MPI implementations and with MPI.</p>


<p>The topic of my talk was “MPI’s Place in Big Computing”; the materials from the talk can be found <a href="http://github.com/ljdursi/EuroMPI2016">on github</a>. The talk, as you might expect, included discussion of high-productivity big data frameworks, but also — and missing from the discussion in my “HPC is dying” blog post — the “data layer” frameworks that underpin them.</p>


<p>I think a lot of people have taken, quite reasonably, my that blog post to suggest that <a href="http://spark.apache.org">Spark</a> for example is a competitor to MPI; the point I wanted to make is a little more nuanced that that.</p>


<p>I’m actually skeptical of Spark’s utility for (<em>e.g.</em>) large-scale simulations. However attractive the model is from a variety of points of view, absent some huge breakthrough I don’t think that functional models with immutable data can support the performance, memory requirements, or performance predictability we require.  (But who knows; maybe that’ll be one of the compromises we find we have to make on the road to exascale).</p>


<p>But whatever you might think of Spark’s efficacy for your particular use case,</p>


<ul>
  <li>A lot of people manifestly find it to be extremely useful for <em>their</em> use case; and</li>
  <li>Performance is quite important to those communities.</li>
</ul>

<p>So given that, why isn’t Spark built atop of MPI for network communications?  And why isn’t <a href="http://tensorflow.org">TensorFlow</a>, or <a href="http://dask.pydata.org">Dask</a>, or <a href="http://www.seastar-project.org">SeaStar</a>?</p>


<p>The past five years have seen a huge number of high-productivity tools for large-scale number crunching gain extremely rapid adoption.  Even if you don’t like those particular tools for your problems, surely you’d like for there to exist some tools like that for the traditional HPC community; why do other communications frameworks support this flourishing ecosystem of platforms, and MPI doesn’t?</p>


<p>There’s another argument there, too - simply from a self-preservation point of view, it would be in MPI’s interest to be adopted by a high-profile big data platform to ensure continued success and support.  But none are; why?  It’s not because the developers of Spark or at Google are just too dumb to figure out MPI’s syntax.</p>


<p>Going through what does get used for these packages and what doesn’t — which is what I do in this talk — I think the issues become fairly clear.  MPI wants to be both a low-level communications framework and a higher-level programming model, and ends up tripping over it’s own feet trying to dance both dances.  As a communications “data plane” it imposes too many high-level decisions on applications — no fault tolerance, restrictive communications semantics (in-order and arrival guarantees), and provides too few services (<em>e.g.</em> a performant active message/RPC layer).  And as a high-level programming model it is too low level and is missing different services (communications-aware scheduling came up in several guises at the meeting).</p>


<p>I don’t think that’s insurmountable; I think inside MPI implementations there is a performant, network-agnostic low-level communications layer trying to get out.  Exposing more MPI runtime services is a move in the right direction.  I was surprised at how open the meeting participants were to making judicious changes — even perhaps breaking some backwards compatability — in the right directions.</p>


<p>Thanks again to the organizers for extending the opportunity to participate; it was great.</p>


<p>My slides can be seen below or on <a href="http://ljdursi.github.io/EuroMPI2016/#1">github</a>, where <a href="http://github.com/ljdursi/EuroMPI2016">the complete materials can be found</a>.</p>