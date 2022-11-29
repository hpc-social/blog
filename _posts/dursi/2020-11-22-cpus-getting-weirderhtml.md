---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2020-11-22 00:00:00'
layout: post
original_url: http://www.dursi.ca/post/cpus-getting-weirder.html
slug: buckle-up-cpus-are-going-to-get-weirder
title: Buckle up, CPUs are going to get weirder
---

<h2 id="the-m1-is-a-good-test-run-lets-get-ready">The M1 is a good test run, let’s get ready</h2>

<p>(Note: This post is adapted from last week’s <a href="https://newsletter.researchcomputingteams.org/archive/5246c80f-2211-470c-94cb-d25496e8d5e8">issue 51</a> 
of the <a href="https://www.researchcomputingteams.org">resarch computing teams newsletter</a>)</p>


<p>The big news of the past month has been Apple’s new <a href="https://www.anandtech.com/show/16252/mac-mini-apple-m1-tested/7">M1
CPU</a>.
The M1’s specs in and of themselves kind of interesting, but more
important to us in research computing is that the M1 is an example
of how CPUs are going to get more different as time goes on, and
that will have impacts on our teams.  The M1 going to be a trial run for
a future of more diverse computing architectures that we’d do well
to get ready for.</p>


<p>Large-scale research computing systems have all been about “co-design”
for ages, but the truth is that in the mainstream, big-picture CPU
design choices have been pretty fixed, with most of co-design
being about choice of accelerators or mix and match between CPU,
memory. and acceleration.  Now that the market has accepted ARM as
a platform — and with <a href="https://riscv.org">RISC-V</a> on its way — we
can expect to start seeing bolder choices for CPU design being
shipped, with vendors making very different tradeoffs than have
been made in the past.  So whether or not you see yourself using
Apple hardware in the future, M1’s choices and their consequences
are interesting.</p>


<p>M1 makes two substantially different trade-offs.  The first is
having DRAM on socket.  This sacrifices extensibility — you can’t
just add memory — for significantly better memory performance and
lower power consumption.  Accurately moving bits back and forth
between chips takes a surprising amount of energy, and doing it
fast takes a lot of power!   The results are striking:</p>


<blockquote class="twitter-tweet"><p dir="ltr" lang="ja">M1 MacBook AirでLINPACK動かして電力測定をしてみた。USB PD電力計＋iOS用Linpackという謎アプリのため参考値だが34.01 GFlops/W。まともに測るべきだしスケールしないやり方なので比べられる値ではないが、点灯したLCD込みでGreen 500の1位は超えていることに… うーん、正しいのか？ <a href="https://t.co/ldEroByfxt">pic.twitter.com/ldEroByfxt</a></p>
&mdash; Ohtsuji (@ohtsuji) <a href="https://twitter.com/ohtsuji/status/1328768907461623808?ref_src=twsrc%5Etfw">November 17, 2020</a></blockquote>


<p>LINPACK - solving a set of linear equations - is a pretty flawed
benchmark, but it’s widely understood.  The performance numbers
here are pretty healthy for a chip with four big cores, but the
<em>efficiency</em> numbers are startling.  They’re not unprecedented
except for the context; these wouldn’t be surprising numbers for a
GPU, which also have DRAM-on-socket, and are similarly non-extensible.
But they are absurdly high for something more general-purpose like
a CPU.</p>


<p>Having unified on-socket memory between CPU and integrated GPU also
makes possible some <a href="https://blog.tensorflow.org/2020/11/accelerating-tensorflow-performance-on-mac.html">great Tensorflow
performance</a>,
simultaneously speeds up and lowers power consumption for <a href="https://www.macrumors.com/2020/11/17/apple-silicon-m1-compiles-code-as-fast-as-mac-pro/">compiling
code</a>,
and does weirdly well at running
<a href="https://info.crunchydata.com/blog/postgresql-benchmarks-apple-arm-m1-macbook-pro-2020">postgreSQL</a>.</p>


<p>The second tradeoff has some more immediate effects for research
computing teams. Apple, as is its wont, didn’t worry too much about
backwards-looking compatibility, happily sacrificing that for
future-looking capabilities.  The new Rosetta (x86 emulation) seems
to work seamlessly and is <a href="https://twitter.com/pmelsted/status/1329934691944816640">surprisingly
performant</a>.  But
if you want to take full advantage of the architecture of course
you have to compile natively.  And on the day of release, a lot of
key tools and libraries didn’t just “automatically” work the way
they seemed to when most people first started using other ARM chips.
(Though that wasn’t magic either; the ecosystem had spent years
slowly getting ready for adoption by the mainstream.)</p>


<p>“Freaking out” wouldn’t be too strong a way to describe
the reaction in some corners; one user claimed that GATK would
<a href="https://twitter.com/biocrusoe/status/1328704001039339521">“never
work”</a> on
Apple silicon (because a build script mistakenly assumed that an
optional library that had Intel-specific optimizations would be
present - they’re on it), and the absence of a free fortran compiler
on the day of hardware release worried other people (there’s already
<a href="https://github.com/fxcoudert/gfortran-for-macOS/releases/tag/11-arm-alpha1">experimental gfortran
builds</a>).
Having come of computational science age in the 90s when new chips
took months to get good tooling for, the depth of concern seemed a
bit overwrought.</p>


<p>This isn’t to dismiss the amount of work that’s needed to get
software stacks working on new systems.  Between other ARM systems
and M1, a lot of research software teams are going to have to put
in a lot of time porting new low-level libraries and tools to the
new architectures.  Many teams that haven’t had to worry about this
sort of thing before are going to have to refactor architecture-specific
optimizations out and into libraries.  Some code will simply have
to be rewritten - some R code has depended on <a href="https://developer.r-project.org/Blog/public/2020/11/02/will-r-work-on-apple-silicon/">Intel-specific NaN
handling</a>
to implement NA semantics (which are <a href="https://blog.revolutionanalytics.com/2016/07/understanding-na-in-r.html">similar to but different
from</a>
NaN) that M1 does not honour, so natively compiled R needs extra
checks on M1.</p>


<p>It’s also not to dismiss the complexity that people designing and
running computing systems will have to face.  Fifteen years ago,
the constraints on a big computing system made things pretty clear — 
you’d choose a whackload of x86 with some suitably fast (for your application)
network. The main question were how fat are the nodes, what’s
the mix of low, medium, and high-memory nodes, and what your storage
system is like.  It’s been more
complex for a while with accelerators, and now with entirely different
processor architectures in the mix, it will get harder.  Increasingly,
there is no “best” system; a system has to be tuned to favour some
specific workloads.  And that necessarily means disfavouring others,
which centres have been loathe to do.</p>


<p>So the point here isn’t M1.  Is M1 a good choice for your research
computing support needs?  Almost certainly not if you run on clusters.
And if you’re good with your laptop or desktop, well, then lots of
processors will work well enough.</p>


<p>But even so, a lot of software is going to now have to support these
new chips. And this is just the start of “weird” CPUs 
coming for research computing.</p>


<p>CPUs will keep coming that will make radically different tradeoffs
than choices than seemed obvious before.  That’s going to make
things harder for research software and research computing systems
teams for a while.  A lot of “<a href="https://encyclopedia2.thefreedictionary.com/vaxocentrism">all the world’s an
x86</a>”
assumptions - some that are so ingrained they are currently hard
to see - are going to get upended, and setting things back right
is going to take work.  The end result will be more flexible and
capable code, build systems, and better-targeted systems, but it’ll
take a lot of work to get there.   If you haven’t already started
using build and deployment workflows and processes that can handle
supporting multiple architectures, now is a good time to start.</p>


<p>But the new architectures, wider range of capabilities, and different
tradeoff frontiers are also going to expand the realm of what’s
possible for research computing.  And isn’t that why we got into
this field?</p>