---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2020-04-18 01:00:00'
layout: post
original_url: http://www.dursi.ca/post/cobol-imperial-college-and-sustained-scientific-softare.html
slug: cobol-imperial-college-bursty-maintenance-and-sustained-scientific-software
title: COBOL, Imperial College, Bursty Maintenance, and Sustained Scientific Software
---

<p>We’ve all read about the huge rise in unemployment claims causing
unprecedented loads on US state software systems, with the situation
so dire that the governor of New Jersey put out <a href="https://qz.com/1832988/covid-19-results-in-new-jersey-desperately-needing-cobol-coders/">an urgent call
for COBOL programmers</a>.
It’s worth looking at this from the point of view of research
software, where we need software to be sustainable and reproducible
for long periods of time.</p>


<p>The systems that need suddenly need COBOL developers have often
been chugging away with maintenance and tweaks for 40–50
years.  This is an almost unfathomable success in the world of
software. So the current issue clearly isn’t with the quality of
the software itself <em>per se</em>.</p>


<p>Is COBOL being “obsolete” the problem?  I mean, look
at that record of success again.  COBOL is a proven, <a href="https://hackernoon.com/i-took-a-cobol-course-and-it-wasnt-the-worst-z1ba3yrp">perfectly
serviceable</a>,
domain-specific language for these sorts of batch tasks. There’s
ways to connect to tools and services written in other languages,
so it can coexist with other systems.  The lack of (say) a vibrant and
rapidly-evolving ecosystem of third-party packages isn’t necessarily
a bad thing here. (How innovative and cutting-edge do you want the
system that sends out your pension cheques to be, exactly, when the
time comes? Do you really want someone to accidentally
<a href="https://qz.com/646467/how-one-programmer-broke-the-internet-by-deleting-a-tiny-piece-of-code/">leftpad</a>
your bank account?)</p>


<p>Yes, people coming in to maintain the software for the first time
will have to familiarize themselves with a new, old, language.  But
people in research or open-source software learn an unfamiliar language to
contribute to a code base every day. Even if they knew the language,
they would still have to learn the codebase itself, the idioms, and
the problem domain. All of those things can be quickly learned by
new developers if there is documentation and tests, and especially
if there are people who have recently been maintaining the code
base to help.  And that’s the issue here.</p>


<p>These COBOL systems weren’t poorly designed, or obsolete, or a bad
match to their requirements.  Easily handling 100x the previously
expected maximum rate of applications isn’t a feature, it’s a symptom
of giddy overengineering.  The requirements just changed suddenly.
And when that happened, the people, procedures, and resources weren’t
in place to do the necessary maintenance.</p>


<p>There is no such thing as infrastructure which does not require
maintenance, and the need for that maintenance is often quite bursty.
This is just as true in research software as it is in governmental
systems.  Research software which goes into production needs to be
written in a maintainable fashion, but that’s not enough.  There
has to be funding support to keep in place the people, procedures,
and resources necessary to maintain that software, likely in bursts.
And those resources have to remain in place between bursts.</p>


<p>The bursty nature of necessary maintenance has also come up in
research software, in the saga of the <a href="https://twitter.com/neil_ferguson/status/1241835454707699713">Imperial College epidemic
modelling
software</a>.
When COVID-19 arrived, this tool suddenly moved from a mildly
interesting research code to a key input into UK domestic policy.
Transparency and flexibility leapt from being nice-to-haves to key
requirements, and the people, procedures, documentation, tests, and
resources weren’t in place to add them.</p>


<p>The importance and urgency of epidemic modelling meant that expertise
and resources from many places were made available to extend and
eventually rewrite the code. But this isn’t a sustainable model for
research computing software, any more than it is for unemployment
application processing systems.</p>


<p>We still genuinely don’t know how to reliably provide maintenance, bursty
or otherwise, for software, shared databases, or systems in
our research communities.  Our funding models are all built around
supporting experiments, observations, or theoretical works —
short-term projects which start, proceed, result in publications
and other research outputs, and are then done.  Mechanisms for ongoing support of evolving
research <em>inputs</em> isn’t even a work in progress — it’s absent.</p>


<p>If experimental methods work develops new kinds of equipment or
reagents which are useful to other researchers, then a vendor starts
manufacturing and selling those items to researchers, with money
that comes out of their grants — and that’s the sustainability
model.  We don’t have that for ongoing efforts in software, databases,
or even reliably for hardware shared at a larger scale than a single
organization yet.</p>


<p>For software undergoing active development, there are at least
plausible approaches proposed.  Some of them look,
reasonably enough, like the research equipment model above.  Add a
modest amount of money to grants earmarked for distribution to
software, databases, or systems that the research group relies on.
Maybe that would work!  But it would almost certainly preferentially
fund projects that are being actively worked on, taking feature
requests and bug reports for software or new submissions for
databases.</p>


<p>For mature, quiescent resources that “just work” and
so fade into the background, the tools that don’t need development
until they suddenly do, we need other solutions.  Likely we need
centres of expertise in research computing, populated by professionals
as advocated by <a href="https://society-rse.org">RSE societies</a> <a href="https://us-rse.org">around
the world</a>, with named maintainers even for
research tools actively used but not actively developed.</p>


<p>People —
<a href="https://bssw.io/blog_posts/maintainers-drive-software-sustainability">maintainers</a>,
with the tools to do their job — are what drive software
sustainability, not language choices or technologies.  As a research
community we need to find and retain funding to retain, develop,
and empower those people to do their work.  Otherwise we’re going
to waste time and effort urgently re-learning and re-creating tools
when individually unforeseeable but collectively predictable bursts
in maintenance are needed.</p>