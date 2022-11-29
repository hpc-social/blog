---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2021-11-23 00:00:00'
layout: post
original_url: http://www.dursi.ca/post/users-time-is-valuable.html
title: Researcher's Time Has Value, Too
---

<h2 id="and-researchers-value-their-time">..And Researchers Value Their Time</h2>

<p>(Note: This post is adapted from <a href="https://www.researchcomputingteams.org/newsletter_issues/0102">#102</a> of the <a href="https://www.researchcomputingteams.org">Research Computing Teams Newsletter</a>)</p>

<p>If you followed HPC twitter in late 2021 at all, you will have seen a <a href="https://twitter.com/vsoch/status/1461908217223528448">heartfelt thread</a> by a well-known research software developer, one who was a key contributor to the Singularity project among others, lamenting the frankly appalling state of developer productivity in HPC - both in what tools exist, and support for them (and other tools for developers) at academic centres.  A <strong>lot</strong> of people <a href="https://twitter.com/HPC_Guru/status/1462070286983983108">chimed into the discussion</a>, including <a href="https://twitter.com/five9a2/status/1462137427527675918">one of the leading developers of the PetSC project</a>, embedded software developers, some key people at big computing centres, all agreeing that there was a problem, but typically zooming in on one or another particular technical or procedural issue and not coming to any conclusion.</p>

<p>I think the issue is a lot bigger than HPC software development workflows - it comes up in too many contexts to be about specific technical issues of running CI/CD pipelines on fixed infrastructure.  The only people to identify the correct underlying issue, in my opinion, were people with experience of both academia and the private sector, such as Brendan Bouffler at AWS:</p>

<blockquote class="twitter-tweet"><p dir="ltr" lang="en">Too much reliance on “free” labour - postgrads and post docs who, invariably, decide that burning their time being mechanical turks for their “superiors” just sucks, so they come and work for us. And since we pay $$, we’re not gonna waste them on things that software can do.</p>&mdash; Brendan Bouffler☁️ 🏳️‍🌈 (@boofla) <a href="https://twitter.com/boofla/status/1462099372255203346?ref_src=twsrc%5Etfw">November 20, 2021</a></blockquote>


<p>The same argument got made by R&amp;D research staff in the private sector.  Their time actually has value; as a result, it gets valued.</p>

<p>In academic research computing, partly because of low salaries — especially for the endless stream of trainees — but also because we typically provide research computing systems for free, we tend to put zero value on people’s time.  Thus our “lowest-cost” approach definitely does not apply to researcher or trainee effort. If researchers have to jump through absurd hoops to get or renew their accounts, or have to distort their workflows to fit one-size-fits-all clusters and queueing systems, or postdocs have to spend hours of work by hand every month hand because tools to automate some of that work would cost $500, well, what do they expect, right?</p>

<p>It’s not that this is an indefensible position to take, but one can’t take this position <em>and</em> act surprised when researchers who can afford to are seriously investigating taking their projects into the commercial cloud even though it costs 2x as much.  It turns out that people’s time is worth quite a lot to them, and is certainly worth some money.  If we were to <a href="https://www.dursi.ca/post/research-computing-funding-to-researchers">let researchers spend their research computing and data money wherever they pleased</a>, I think we’d find that significantly less than 100% of researchers would use “lowest price possible” as their sole criterion for choosing providers.  Core facilities like animal facilities, sequencing centres, and microscopy centres compete on dimensions other than being the cheapest option available.</p>

<p>To be sure, there are process issues in academia which exacerbates the tendency to see people’s time as valueless - rules about capital vs operating costs, for instance - but those rules aren’t a law of nature.  If we were paying people in academia <a href="https://www.levels.fyi/">what they pay in tech</a>, administration would suddenly discover some additional flexibility in the thresholds and criteria for considering something a capital expense if it meant we could be a bit more parsimonious with people’s time.</p>

<p>Until then, one can’t be too surprised when the most talented and ambitious staff get routinely poached by the private sector, and when research groups start considering service providers that cost more but respect their time.</p>