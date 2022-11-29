---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2020-12-04 00:00:00'
layout: post
original_url: http://www.dursi.ca/post/reseach-infrastructure.html
slug: when-research-infrastructure-is-and-isn-t-maintained
title: When Research Infrastructure Is and Isn't Maintained
---

<p>(Note: This post is adapted from <a href="https://www.researchcomputingteams.org/newsletter_issues/0053">#53</a> of the <a href="https://www.researchcomputingteams.org">Research Computing Teams Newsletter</a>)</p>


<p>There were two big stories in the news this week (as I write this, at the end of 2020) about what’s possible with sustained research infrastructure funding and what happens when research infrastructure isn’t sustained.</p>


<p>In the first, you’ve probably read about AlphaFold, Google Brain’s efforts to bring deep learning to protein folding. <a href="https://www.the-scientist.com/news-opinion/deepmind-ai-speeds-up-the-time-to-determine-proteins-structures-68221">It did very well</a> in the 14th annual Critical Assessment of (protein) Structure Prediction (CASP) contest. Predictably but unfortunately, Google’s press releases wildly overhyped the results - “Protein Folding Solved”.</p>


<p>Most proteins fold very robustly in the chaotic environment of the cell, and so it’s expected that there should be complex features that predict how the proteins folded configurations look. We still don’t know anything about the model AlphaFold used - other than it did very well on these 100 proteins - or how it was trained. There are a lot of questions of how it will work with more poorly behaved proteins - a wrong confident prediction could be much worse than no prediction. But it did get very good results, and with a very small amount of computational time to actually make the predictions. That raises a lot of hope for the scope of near-term future advances.</p>


<p>But as <a href="https://twitter.com/aledmedwards/status/1333754396530847745">Aled Edwards points out on twitter</a>, the real story here is one of long term, multi-decadal, investment in research infrastructure including research data infrastructure by the structural biology community. The <a href="https://www.wwpdb.org">protein data bank</a> was set up 50 years ago (!!); and a culture of data sharing of these laboriously solved protein structures was set up, with a norm of contributing to (and helping curate) the data bank. That databank has been continuously curated and maintained, new techniques developed, eventually leading to the massive database now on which methods can be trained and results compared.</p>


<p>It’s the sustained funding and support - monetarily but also in terms of aligning research incentives like credit - which built the PDB. The other big story we heard this week tells us that you can’t just fund a piece of infrastructure, walk away, and expect the result to be self-sustaining. On December 1st, the iconic <a href="https://www.the-scientist.com/news-opinion/famous-arecibo-radio-telescope-in-puerto-rico-collapses-68219">Arecibo Radio Telescope in Puerto Rico collapsed</a>. The telescope was considered important enough to keep running - there was no move to decommission it until late November - but not important enough to keep funding the maintenance to keep it functioning.</p>


<p><img alt="Overhead image of a broken Arecibo Telescope" src="https://www.dursi.ca/assets/imgs/arecibo-collapsed.jpg" /></p>


<p>Digital research infrastructure - software, data resources, computing systems - fall apart at least as quickly without ongoing funded effort to maintain them.  It’s not about whether these digital pieces of infrastructure are “sustainable”; it’s whether or not they are <em>sustained</em>. Too many critical pieces of our digital research infrastructure are not being sustained.</p>