---
author: Jonathan Dursi's Blog
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2015-04-09 00:00:00'
layout: post
original_url: http://www.dursi.ca/post/objections-continued.html
title: Objections, Continued
---

<p>Thanks for all of the comments about <a href="http://dursi.ca/hpc-is-dying-and-mpi-is-killing-it/">my HPC and MPI post</a>, on the post itself, or on twitter, or via email.  While much of the comments and discussions were positive, it won’t surprise you to learn that there were objections, too; so I thought I’d keep updating the Objections section in a new post.  I’ve also posted <a href="http://www.dursi.ca/in-praise-of-mpi-collectives-and-mpi-io/">one (hopefully last) followup</a>.</p>

<p>But do keep sending in your objections!</p>

<h2 id="further-objections">Further Objections</h2>
<h3 id="youre-saying-wed-have-to-rewrite-all-our-code">You’re saying we’d have to rewrite all our code!</h3>

<p>If someone had suggested I add this objection to the original list before publishing, I would have rejected it as too straw-man to use; I’d be transparently putting this objection up just to demolish it. Clearly, no one would actually claim that “the HPC community should urgently start engaging with and using new technical computing technologies” means “you have to burn all your old stuff to the ground”.</p>

<p>But sure enough, it came up <em>frequently</em>, in private email, and most dramatically, <a href="https://twitter.com/KpDooty/status/585582597746622464">on twitter</a>.</p>

<p>Even though this is by far the most common reaction I got, I hope it’s clear to most readers these aren’t the same things.  Learning (say) C++ and using it in development of new codes doesn’t mean your old C and Fortran stuff stops working.  Or that you’re under an obligation to take the working code in other languages and re-write it all in the new language before ever using it again to maintain some kind of computational moral consistency.</p>

<p>Your MPI code won’t stop working for you in a fit of rage because you’re seeing other frameworks.  MPI will continue to work and be maintained, exactly because there is 20+ years worth of stuff using it.</p>

<p>But <strong>new</strong> software projects are being started every day, in every field, in every region.  This argument is about what we should use for those codes. “Because we’ve always done it that way” isn’t a great reason for a community that’s supposed to be on the cutting edge of computing to keep doing things in one particular framework.</p>

<h3 id="big-data-and-hpc-are-completely-different-and-its-ridiculous-to-compare-them">Big data and HPC are completely different, and its ridiculous to compare them</h3>

<p>This was a close second in popularity. And this one worries me quite a bit, because it means that there’s a lot of people in our community that are disturbingly unaware what’s going on in computing and data analysis outside of the confines of their office.</p>

<p>It’s absolutely true that there are Big-Data-y things that are mainly just I/O with a little bit of processing.  But by and large people want to <em>analyze</em> that large amount of data. And then you end up with absolutely classic big numerical computing problems. To take an early example, Page Rank is, after all, <a href="http://en.wikipedia.org/wiki/PageRank#History">an eigenvalue problem</a>.  The drive for next-generation big data platforms like Spark is no small part to make machine learning algorithms that would be very familiar to us run as efficiently as possible.  Let’s take some example machine learning approaches:</p>

<ul>
  <li><a href="http://en.wikipedia.org/wiki/Spectral_clustering">Spectral clustering</a> solves an <a href="https://charlesmartin14.wordpress.com/2012/10/09/spectral-clustering/">equation for the graph Laplacian</a> - which looks exactly like any other <a href="https://www.dursi.ca/spectral clustering heat equation">parabolic PDE on an unstructured mesh</a>.  (Thanks to Lorena Barba for <a href="https://twitter.com/LorenaABarba/status/586515529973764096">pointing out an embarrasing mistake</a> in an earlier version of that point.)</li>
  <li><a href="http://en.wikipedia.org/wiki/Support_vector_machine">Support Vector Machines</a> are kernel based methods which involve Green’s functions and 1st order integral equations.</li>
  <li>Much of machine learning involves fitting a model, which means that there are entire <a href="http://mitpress.mit.edu/books/optimization-machine-learning">books</a> written about large-scale efficient optimization solvers for machine learning, including physical science chestnuts like <a href="http://en.wikipedia.org/wiki/Stochastic_gradient_descent">gradient descent</a>.</li>
  <li>A common first step in data analysis is dimensional reduction involving (say) <a href="http://en.wikipedia.org/wiki/Principal_component_analysis">PCA</a>, requiring the SVD (or similar factorizations) of huge matricies.</li>
  <li>In fact, Linear Algebra is omnipresent in machine learning (as it has to be with so much, eg, model fitting), to the point that there are entire <a href="http://stanford.edu/~rezab/nips2013workshop/">conferences</a> on large-scale linear algebra for machine learning.</li>
  <li>A lot of the data analyses involve statstical bayesian inference, requiring <a href="http://link.springer.com/article/10.1023%2FA%3A1020281327116">MCMC</a> calculations.</li>
  <li>k-Nearest-Neighbour problems in clustering, kernel density methods, and many other techniques relying on something like a distance or similarity metric require classic N-body solutions like <a href="https://books.google.ca/books?id=6GvSBQAAQBAJ&amp;pg=PA162&amp;lpg=PA162&amp;dq=k-d+trees+machine+learning&amp;source=bl&amp;ots=GdA2RtbSvY&amp;sig=JStlVpNy5CB8cJewtFYPIb53QCI&amp;hl=en&amp;sa=X&amp;ei=cRknVeH9OIG5sAWMkoCgAQ&amp;ved=0CE4Q6AEwCDgK#v=onepage&amp;q=k-d%20trees%20machine%20learning&amp;f=false">k-D trees</a>; and if positions are being updated, they essentially become <a href="http://www.cs.cmu.edu/~agray/nips-final.pdf">N-body problems</a>.  And of course, an entire class of high-dimensional optimization problems often used in machine learning are essentially <a href="http://en.wikipedia.org/wiki/Particle_swarm_optimization">tracer particle methods</a>.</li>
  <li>As a result of all this high mathematical intensity, machine learning is of course becoming a rapidly growing user of <a href="https://registration.gputechconf.com/form/session-listing&amp;doSearch=true&amp;additional_parameter_selector=none&amp;queryInput=&amp;topic_selector=Machine+Learning+%26+Deep+Learning&amp;type_selector=none">GPUs for their numerical algorithms</a>.</li>
</ul>

<p>So let’s see; PDEs on unstructured meshes, optimization, gradient descent, large-scale linear algebra, particle methods, GPUs. And of course, time series data of any sort means FFTs. So sure, I don’t know what is running on <em>your</em> HPC cluster, but is it really that different than the above?</p>

<h3 id="mpi-is-great-for-physics-even-if-less-great-for-the-other-stuff">MPI is great for physics, even if less great for the other stuff</h3>

<p>I got this by email and on twitter several times.</p>

<p>Great compared to what? And based on what evidence?</p>

<p>Say a physics grad student walks in to your office who’s going to develop a small bespoke particle code for their dissertation.  Pointing them to MPI, rather than other technologies with unimpeachable HPC bona fides like UPC, Chapel, Co-array Fortran, or, (for a particle simulation especially) Charm++ seems like it’s the lazy, easy way for <em>us</em>, and less about what’s actually best for <em>them</em>.</p>

<p>In what sense is it “great for physics” to have the student increase the amount of code they have to write, and debug by a factor of 3x?  In what sense is it great for them to have to re-invent all of the low-level communications algorithms which have been implemented better, in other packages?  Maybe you could make an argument about stability or performance against UPC/Chapel (although I’d counter-argue you’d get immediate and helpful support from the developers) - what’s the argument against pointing the student to Charm++?  Or Intel’s CAF?</p>

<p>And this doesn’t even begin to cover things like Spark, Flink, or <a href="http://ignite.incubator.apache.org/index.html">Ignite</a> - for simulation, or experimental physics work (which is physics too, right?), which is necessarily heavy on data analysis.</p>

<h3 id="youre-just-saying-mpi-is-too-hard">You’re just saying MPI is too hard</h3>

<p>I’m really not. As a community, we don’t mind hard.  Solving complex equations is hard, that’s just how it is.  We eat hard for breakfast.  (And the genomics and big-data communities are the same way, because they’re also filled with top-notch people with big computational problems).</p>

<p>I’m saying something different: MPI is needlessly, pointlessly, and uselessly a huge sink of researcher and toolbuilder effort for little if any reward.</p>

<p>How many grad students have had to tediously decompose a 2d or 3d grid by hand, write halo exchange code, get it debugged and running, run in that crude fasion for a while, then tried moving to move to overlapped communication and computation, and spent days or weeks trying to get that to work efficiently - and then had to re-write chunks as they need a new variable laid out differently (or just implemented a really bad transposition?) and still gotten performance that an expert would consider poor?</p>

<p>And regular grid codes are the easy stuff; how many scientist-decades worth of efforts have gone into implementing and re-implementing tree codes or unstructured meshes; and by and large resulting in efficiencies ranging from “meh” to “ugh”?</p>

<p>Wouldn’t it be better to have experts working on the common lower level stuff, tuning it and optimizing it, so that the scientists can actually focus on the numerics and not the communications?</p>

<p>The stuff about levels of abstraction isn’t some aesthetic philosophical preference. And I’m not complaining MPI because it’s hard; I’m complaining about it because it’s resulted in an enormous waste of researcher time and compute resources.  Let the scientists focus on hard stuff that matters to their research, not the stuff that can be effectively outsourced to builders.</p>

<p>Now, we at centres could at least improve <em>this</em> dreadful state of affairs even with MPI just by doing a better job pointing researchers embarking on a code project to libraries and packages like Trillinos or what have you, and stop counseling them to write raw MPI code themselves.  But of course, we normally don’t, because we keep telling ourselves and the incoming grad students “MPI is great for physics”…</p>

<h3 id="its-important-for-students-to-know-whats-going-on-under-the-hood-even-if-theyre-using-other-frameworks">It’s important for students to know what’s going on under the hood, even if they’re using other frameworks</h3>

<p>I do have some sympathy for this point, I will admit.</p>

<p>But anyone who thinks teaching generation after generation of grad students how to manually decompose a 2d mesh and do halo exchange on it using <code>MPI_Sendrecv()</code> is a productive and rewarding use of time, is someone who doesn’t spend enough time doing it.</p>

<p>As with other pro-low-level arguments: why is MPI automatically the right level to stop at? If we want to teach students how things really work under the covers, why aren’t we going all the way down to Infiniband or TCP/IP, user mode and kernel mode, and the network stack?  Or, why don’t we stop a level or two above, draw some diagrams on a whiteboard, and move on to actually solving equations?  Why is MPI in particular the right “under the hood” thing to teach, as opposed to GASNet, Charm++, or just pseudo-network-code?</p>

<p>If the answer to the questions above is “because MPI is what we know and have slides for”, then we need to think about what that implies, and how well it’s serving the research community.</p>

<h3 id="but-my-new-code-will-need-libraries-based-on-mpi-that-arent-supported-by-chapelupcsparkother-stuff-yet">But my new code will need libraries based on MPI that aren’t supported by Chapel/UPC/Spark/other stuff yet!</h3>

<p>Fair enough. When you choose what you are going to use to write a program, library and tool support really matter.  It’s absolutely true that there are great packages that use MPI, and if your project is going to rely on them, then this isn’t an example of a good project to start expermenting with a new platform on.  This is why such a large fraction of numerical code was in FORTRAN77 for so long.</p>

<p>Co-array Fortran, Chapel, and others do have various degree of MPI interoperability, so do check that out; but yes, you need what you need.</p>

<h3 id="but-people-are-starting-to-build-things-based-on-mpi-3-rma">But people <em>are</em> starting to build things based on MPI-3 RMA!</h3>

<p>This <a href="http://dursi.ca/hpc-is-dying-and-mpi-is-killing-it/#comment-1952126251">coment by Jeff on the original post</a>, is by some measure the most interesting objection I’ve heard so far.</p>

<p>People are legitimately starting to use MPI-3 RMA in the underlying implementations of higher level tools. If that really took off, then my arguments about MPI not being the right level of abstraction for toolbuilders would clearly be wrong, and a huge part of my post would be rendered irrelevant.</p>

<p>In that case, I would be completely wrong – and it would be awesome!  A higher-level toolset for researchers could finally flourish, the lower level stuff could be handled by a completely separate group of experts, and MPI would have found its place.</p>

<p>I want to be clear that I think it would be fantastic - really, the best of all possible worlds - to be wrong in this way.</p>

<p>I’m going to describe why I really don’t think I am, and what the stumbling blocks are.  Then I’ll discuss an alternate future which sidesteps the worst of those problems, and how it really could be a path to a very productive and growing HPC future - but it will of course never, ever, happen.</p>

<p>So MPI-3 - useful RMA, being used.  Perfect!  To see the problem that concerns me here, consider two questions; (1) What are the benefits of using MPI for this, and (2) what are the downsides?</p>

<p>On the upside, it’s great that MPI is sufficient to implement these tools.  But is it necessary?  What is the advantage of using something like MPI over something else, and in particular something lower level?  Maybe it would be a little easier or a little harder, but would it make a big difference?  Particularly to the end-user of the tool being built?</p>

<p>I doubt it makes much difference either way; the reason I ask is the downside.</p>

<p>MPI-3 RMA doesn’t come on its own; it’s part of MPI.  And in this context, I’m concerned with two real downsides with using even great parts of MPI for low-level toolbuilding.  They’re related: the heavy-weight forum process, and the enormous baggage of backwards compatability.</p>

<p>Let’s take the forum process first.  Let’s say there’s two competing tools you could use to build your next lower-layer tool; MPI-3 RMA and some other low-level network abstraction layer.  (What I’m picturing is something like <a href="https://github.com/ofiwg/libfabric">OFWG Libfabric</a>, which you can probably tell I’m quite taken with, but that’s not really right here.  But something at roughly that level or a little higher).</p>

<p>You’re starting to build your new tool, which contains a number of really innovative ideas; but now you’ve discovered you need one additional feature in either package.</p>

<p>Which will get you there first?</p>

<p>The MPI forum was really able to innovate with MPI-3 RMA, because they were nearly starting afresh - or at least complementary with what had gone before.  But now that MPI-3 is out, and a number of projects have used it, the spec is essentially encased in carbonite; the API in its every last detail will outlive us all.  None of the existing APIs will change.</p>

<p>That’s ok, because the Forum has shown its willingness to add new functions to the spec when justified.  Your case sounds interesting; you should get your answer in a couple of years or so.</p>

<p>And that’s kind of crazy for a low-level network abstraction layer.  The other package - whatever it is - won’t have that sort of friction.</p>

<p>There’s another issue in terms of new features; that’s the backwards compatability legacy.</p>

<p>Let’s take something like fault tolerance, which is important at extreme scale - but will eventually get important for more moderate scales, as well.</p>

<p>For a really low-level network abstraction, dealing withfault tolerance isn’t an enormous difficulty.  For something higher level like MPI-3 RMA, it’s more challenging, but it’s still something where one could imagine how it might go.</p>

<p>But for MPI-3+ to develop a feature like fault tolerance, it will have to be created in such a way that it integrates seamlessly with every single MPI feature that has ever existed, without altering any of the semantics of a single one of those calls. The backwards compatability requirements are crushing.</p>

<p>So this is sort of the tragedy of MPI-3 RMA. It’s a great thing that may have just come too late in the lifecycle of a project to be able to have its full impact.</p>

<p>Let’s imagine a world where we could just shrug this stuff off.  Let’s imagine a new framework – MPING, MPI++, whatever; which is a substantially paired down version of MPI.  It’s an MPI that has decided what it wants to be; a low level layer for toolbuilders, never to be taught to grad students who are planning to write application software.</p>

<p>It contains only pared-to-the bone versions of MPI3 RMA, which are demonstrably being found useful; MPI collectives, which are fantastic; MPI-IO, which is also fantastic; and auxiliary stuff like the datatype creation routines, etc.  The communications semantics for everything are greatly relaxed, which would confuse the heck out of newbie end users, but toolbuilders can deal with it.  And there’s no decades of backwards compatability to fight with.</p>

<p>This vision actually discourages me a bit, because it would be terrific; there’d be an active, vendor-supported, high-performance, productive network abstraction layer for toolbuilders; and no confusion about who it was for.  We could build high-productivity tools for scientific application writing atop a stable, high performance foundation.</p>

<p>And of course, it will never, ever, happen.</p>