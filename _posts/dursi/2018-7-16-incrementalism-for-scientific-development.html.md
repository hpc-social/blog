---
author: Jonathan Dursi's Blog
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2018-07-16 00:00:00'
layout: post
original_url: http://www.dursi.ca/post/incrementalism-for-scientific-development.html
title: A Killer Feature for Scientific Development Frameworks- An Incremental Path
  To Maturity
---

<p>( <strong>Note</strong>: This is a bit of a work in progress; even more so than usual, comments/criticisms/additions welcome )</p>

<h3 id="the-stages-of-research-software-development">The Stages of Research Software Development</h3>

<p>Research software development covers a lot of ground — it’s the development of software for research,
and research is a broad endeavour that covers a lot of use cases.</p>

<p>The part of research software development that I find the most interesting is the part that 
<em>is a research effort itself</em>; the creation of new simulation methods, new data analysis techniques,
new ways to combining different sorts of approaches.  Like any new tools, this work
can enable people to ask entirely new questions, or answer old questions in new ways, pushing
scholarship forward along previously unexplored paths.</p>

<p>But for new methods to live up to their potential and have that impact, they have to be developed
and disseminated.  As a community, we’re still developing the training and tool chains that 
make this routine; without them, there are still too many bottlenecks in the method development
pipeline that mean good ideas for new tools get delayed, sometimes indefinitely, before adoption.</p>

<p>Computational tools for science and scholarship go through stages of development like any experimental technique:</p>

<ol>
  <li><strong>Will this even work?</strong>  Testing the core ideas out, usually interactively</li>
  <li><strong>Will this answer my question?</strong>  Developing a very early prototype on your own data set/conditions</li>
  <li><strong>Is this an interesting question to others?</strong>  Sharing a more robust prototype with friendly collaborators who think it might be useful</li>
  <li><strong>Becoming Research Infrastructure</strong> The robust, usable, automatable tool becomes something strangers start to use routinely in their own research</li>
</ol>

<p>These steps can be thought of as a sort of an internal-to-the-research-endeavour version of 
the <a href="https://en.wikipedia.org/wiki/Technology_readiness_level">Technology Readiness Levels</a> 
that are used to describe the maturity of technologies and tools, now often used when talking
about commercialization.</p>

<p>Not every idea has to go through all four stages to be successful; sometimes a tool will be a ‘one-off’
or nearly so, used for one or two projects and that’s it.  This isn’t at all a bad thing, 
if it served its one purpose well.</p>

<p>But each transition between stages represents a potential barrier for ideas becoming new tools,
a jump in level of development skills and effort required.  Every tool that stalls at between 
stages solely because there isn’t training or tooling to allow incremental progress along 
the pipeline is a tool that is unnecessarily lost to researchers who might have made use of it.</p>

<h3 id="training-research-software-developers-to-tackle-all-stages">Training Research Software Developers To Tackle all Stages</h3>

<p>The set of techniques that we mean when we talk about “Software
Engineering” is most useful at step 4 — these techniques
largely assume that there already exists a well-posed problem and
an understood, implementable solution.  I’ve argued in the past
that it’s not only unnecessary but actually irresponsible to build
“well-engineered” software for tools at stage 1 or 2,
where the answers will often turn out to be “No”.</p>

<p>It was understood fairly early that the lifecycle for scientific
projects differed a great deal from scientific software development.
Realizing that something correspondingly different training was needed, in the late 90s 
<a href="https://software-carpentry.org">Software Carpentry</a>, and later <a href="https://carpentries.org">The Carpentries</a>,
started teaching more research trainees enough modern programming skills to ask their own 
questions — to navigate the biggest transition from nothing to stage 1, when existing tools
won’t work for their questions; and to get started on the journey of the next transition, to
stage 2, building an entire early prototype.  That training may or may not get students
all the way to the end of stage 2, with issues like speed or advanced functionality remaining,
but those issues will vary from research project to research project, and the goal is to
get the students to the point where they can learn additional material themselves.</p>

<p>There still isn’t a lot of training for researchers to make the next big jump, from
prototype-for-self to tool-some-others-can-use.  However, authors are beginning to write
resources for students wanting to learn how to proceed<sup id="fnref:1"><a class="footnote" href="https://www.dursi.ca/feed.xml#fn:1" rel="footnote">1</a></sup><sup>,</sup><sup id="fnref:2"><a class="footnote" href="https://www.dursi.ca/feed.xml#fn:2" rel="footnote">2</a></sup><sup>,</sup><sup id="fnref:3"><a class="footnote" href="https://www.dursi.ca/feed.xml#fn:3" rel="footnote">3</a></sup><sup>,</sup><sup id="fnref:4"><a class="footnote" href="https://www.dursi.ca/feed.xml#fn:4" rel="footnote">4</a></sup>.</p>

<p>The second-biggest transition in that list, that from 3 to 4, is the one I worry the least
about.  It’s at that stage that existing software engineering teaching, tooling,
and resources become the most helpful.  And while the effort to learn those techniques
and apply them can be significant, at this point the ideas and the tool have proven themselves
useful enough that it is much easier to find the time, people, and resources to complete a 
“research infrastructure”-grade implementation.</p>

<p>Of course, once the set of ideas is implemented as research infrastructure, it’s
much harder for most practicing researchers to get under the hood and start 
tinkering with by making changes or incorporating additional ideas.  And so the cycle starts again.</p>

<h3 id="the-best-scientific-development-frameworks-will-allow-an-incremental-path-towards-maturity">The Best Scientific Development Frameworks will Allow an Incremental Path Towards Maturity</h3>

<p>While the research computing community has made great progress in creating development training
specific to their needs, there’s been much less success with programming languages, tools, or
frameworks which reflect the path of research programs.</p>

<p>Arguably the best programming language for science, and certainly one of the most successful, 
has been a general purpose programming language, Python.  I think the reasons for this include
the relatively smooth path scientific software development can take towards maturity in the
Python ecosystem:</p>

<ul>
  <li>One can easily and rapidly test out ideas at the REPL and in a notebook. (Stage 1)</li>
  <li>The large standard library and even larger ecosystem lets you quickly implement a lot of functionality (Stages 1/2)</li>
  <li>Great tooling exists, including <a href="https://code.visualstudio.com">VSCode</a> which makes much IDE functionality available for free (Stages 2/3)</li>
  <li>Compared to languages more commonly used earlier like C and FORTRAN, the exception system lets
you implement a number of things and still understand what’s happening before you have to start
implementing boilerplate error handling, making it something that can be added incrementally at later stages. (Stages 2/3/4)</li>
  <li>Tools like <a href="http://numba.pydata.org">Numba</a>, <a href="https://www.pypy.org">PyPy</a>, or <a href="http://cython.org">Cython</a> allow 
substantial but incremental performance improvement for many kinds of computation (Stages 2/3/4)</li>
  <li>Tools like <a href="https://www.pypy.org">Dask</a> offer an incremental path to scale (Stages 3/4)</li>
</ul>

<p>It’s useful to consider incrementalism-as-a-feature in the context
of existing programming environments, each of which have some ideas useful to
scientific computing.  <a href="http://www.ada2012.org">Ada</a>, a highish-level programming
language with an emphasis on correctness, has a reputation of being
a somewhat authoritarian programming environment; however, many of its correctness
features are things you can incrementally add on (things like pre- and post-conditions).
On the other hand, <a href="https://www.rust-lang.org/en-US/">Rust</a>, a lower level
language aimed at systems programming where reliability and security in an environment
where memory bugs continue to cause problems, enables very low-level concurrency
features but one very quickly has to wrestle with Rust’s powerful 
<a href="https://doc.rust-lang.org/1.8.0/book/references-and-borrowing.html">borrow checker</a>;
adding non-trivial sharing semantics to code in Rust results in a
dramatically non-incremental development effort, which is arguably
the right choice for a low-level systems programming language.</p>

<p>While Python and other general programming languages have flourished,
other frameworks, aimed more directly at solving needs particular
to research or branches of research, have struggled.  Much of this,
of course, has to do with the simple math of adoption; but most
have not made much effort to make tools which ease the development
of increasingly mature research software.</p>

<p>To their credit, the <a href="https://julialang.org">Julia</a> community has
come closest, but they are focussed on a narrow piece of the issue;
the need for a framework for incremental adoption becomes “one
language for everything” with tools like Numba or PyPy as,
essentially, cheating; and the only maturity metric focused on is
performance.  It’s better to have fast code than not, of course, but it is by no means
the primary development problem of most researchers.</p>

<p>Having said that, most other programming languages aimed for
scientific communities have not made nearly as much progress on key
usability issues for researchers.  I’ll certainly be watching the
progress of their 1.x releases with some interest.</p>

<h3 id="the-developing-field-of-research-software-engineering">The Developing Field of Research Software Engineering</h3>

<p>It’s been fascinating to watch from the sidelines over the past two decades
as research software engineering and RSE as a profession has gone from
basically nothing to <a href="https://rse.ac.uk/conf2018/">conferences</a>, 
<a href="https://carpentries.org">organizations</a>, and research.  I’m enormously
heartened by the fact that training now exists to tackle the specific 
challenges of developing software that itself is research into methods
development.</p>

<p>I’m still somewhat pessimistic, however, on the state of development frameworks
for research computing.  My current work with web services development
just drives home the point of how scarce the tooling is for building
research software.</p>

<p>The history of research computing since Fortran’s dominance has
been that research software engineering has grafted itself on to
a set of existing general purpose programming languages like C++
or Python, each of which has advantages but also gaps for research
computing.  There are exciting experiments here and there with new
languages, but none are yet particularly compelling.</p>

<p>As Data Science/Data Engineering becomes more and more common in
commercial enterprises and as a computing use case, we may yet end
up finding frameworks which, if not actually designed for science,
are made for similar purposes.  The good news is that people problems
are hard, while technology problems are (comparatively) tractable.
If one or more promising development frameworks appear in the coming
years, ones that allow a path from “basic methods science”
to “methods commercialization”, other people’s hard
work has led to a generation of research software developers who are ready
to take the plunge.</p>

<div class="footnotes">
  <ol>
    <li id="fn:1">
      <p><a href="http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005412"><em>Ten simple rules for making research software more robust</em>, Taschuk &amp; Wilson</a> <a class="reversefootnote" href="https://www.dursi.ca/feed.xml#fnref:1">&#8617;</a></p>
    </li>
    <li id="fn:2">
      <p><a href="http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005265"><em>Ten Simple Rules for Developing Usable Software in Computational Biology</em>, List, Ebert, &amp; Albrecht</a> <a class="reversefootnote" href="https://www.dursi.ca/feed.xml#fnref:2">&#8617;</a></p>
    </li>
    <li id="fn:3">
      <p><a href="http://katyhuff.github.io/python-testing"><em>Testing and Continuous Integration with Python</em>, Huff</a> <a class="reversefootnote" href="https://www.dursi.ca/feed.xml#fnref:3">&#8617;</a></p>
    </li>
    <li id="fn:4">
      <p><a href="https://arxiv.org/pdf/1609.00037.pdf"><em>Good Enough Practices in Scientific Computing</em>, Wilson et al.</a> <a class="reversefootnote" href="https://www.dursi.ca/feed.xml#fnref:4">&#8617;</a></p>
    </li>
  </ol>
</div>