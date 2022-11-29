---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2015-04-19 01:00:00'
layout: post
original_url: http://www.dursi.ca/post/in-praise-of-mpi-collectives-and-mpi-io.html
title: In Praise of MPI Collectives and MPI-IO
---

<p>While I have a number of posts I want to write on other topics and technologies, there is one last followup I want to make to <a href="http://www.dursi.ca/hpc-is-dying-and-mpi-is-killing-it/">my MPI post</a>.</p>

<p>Having said what I think is wrong about MPI (the standard, not the implementations, which are of very high quality), it’s only fair to say something about what I think is very good about it.  And <em>why</em> I like these parts gives lie to one of the most common pro-MPI arguments I’ve been hearing for years; that application programmers coding at low levels is somehow essential - or even just a good idea - for performance.</p>

<h2 id="two-great-things-about-mpi">Two great things about MPI</h2>

<h3 id="collective-operations">Collective Operations</h3>
<p>Since the very beginning, MPI has defined a suite of <a href="https://computing.llnl.gov/tutorials/mpi/#Collective_Communication_Routines">collective communications</a> that include operations like scatter, gather, <a href="http://en.wikipedia.org/wiki/Prefix_sum">prefix scan</a>, and reduce.  While these weren’t invented by MPI – many were already implemented as “global communications” routines in the <a href="http://en.wikipedia.org/wiki/Connection_Machine">CM-2’s</a> <a href="http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=365582">Connection Machine Scientific Software Library</a>, for instance, and there is lots of literature on implementing those operations on other architectures like the iPSC/860-based hypercube systems – it’s certainly fair to say that it was MPI that popularized them to the point that they’ve started getting <a href="http://www.mellanox.com/page/products_dyn?product_family=104&amp;menu_section=73">hardware support in network cards</a>. The popularization stems partly from how widely taught MPI is, but also from useful generalizations that the MPI Forum made, like user-defined reduction operations, or being able to perform these operations on user-defined subsets of tasks.</p>

<p>A classic use of MPI collective operations would be using a reduce to find a global sum (or max, or min, or a user defined operation) of local values:</p>

<pre><code class="language-python">from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

local = random.random()

globalsum = comm.reduce(local, op=MPI.SUM, root=0)
globalmin = comm.reduce(local, op=MPI.MIN, root=0)
globalmax = comm.reduce(local, op=MPI.MAX, root=0)

if rank == 0:
    print "Min, mean, max = ", globalmin, globalsum/nprocs, globalmax
</code></pre>

<h3 id="mpi-io">MPI-IO</h3>

<p><a href="http://beige.ucs.indiana.edu/I590/node86.html">MPI-IO</a> is the foundational middleware for HPC parallel I/O.  <a href="https://hdfgroup.org/HDF5/PHDF5/">Parallel HDF5</a> (and thus <a href="http://www.unidata.ucar.edu/software/netcdf/docs_rc/parallel_io.html">Parallel NetCDF4</a>), <a href="https://www.olcf.ornl.gov/center-projects/adios/">ADIOS</a>, and others are built on top of it.  As a result, even application software that doesn’t explicitly use MPI sometimes relies on MPI-IO for reading and writing large files in parallel.</p>

<p>The key concept in MPI-IO is a “file view”, which describes (in terms of MPI data layouts) where in the file a process will be writing.  Once that’s done, writing data to the file just looks like sending a message to the file.  A trivial example follows below; more complex data layouts like (as often happens in scientific computing) non-contiguous slices of large multidimensional arrays being read and written would look exactly the same:</p>

<pre><code class="language-python">from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

myString = 'Hello ' if rank % 2 == 0 else 'World!'
stringSize = 6

subarray = MPI.CHAR.Create_subarray( (stringSize*nprocs,), (stringSize,), (stringSize*rank,))
subarray.Commit()

filehandle = MPI.File.Open(comm, 'ioexample.txt', MPI.MODE_CREATE | MPI.MODE_WRONLY)
filehandle.Set_view(0, MPI.CHAR, subarray)
filehandle.Write_all(myString)

filehandle.Close()
</code></pre>

<h2 id="why-theyre-great">Why they’re great</h2>

<p>These two very different parts of the MPI standard have three important features in common for this discussion.</p>

<ul>
  <li>They’re at much higher levels of abstraction than most of the API</li>
  <li>Application programmers would get worse performance, not better, if they tried to implement their own at lower levels.</li>
  <li>Original implementations of these APIs didn’t perform nearly as well as current implementations.  But algorithmic and implementation work done by software engineers greatly sped the low level implementations up without applications programmers needing to rewrite their code.</li>
</ul>

<h3 id="collectives-and-mpi-io-are-higher-levels-of-abstraction">Collectives and MPI-IO are higher levels of abstraction</h3>

<p>Calls to MPI collective operations or MPI-IO describe what should be done, not how to do it, and at a much higher level than <code>MPI_Send()/MPI_Put()</code>.</p>

<p>Operations like “All processes sum their results and distribute the result to all processes”, or “Each process writes to their slice of the file” are enormously broader than “Send this message to process X”.  There’s a large number of ways they could be implemented, and in fact there’s a huge literature on both <a href="https://scholar.google.ca/scholar?q=mpi+collectives">collectives</a> and <a href="https://scholar.google.ca/scholar?q=mpi-io">MPI-IO</a> on various approaches to doing so.</p>

<h3 id="application-programmers-reimplementing-them-would-be-worse-for-performance">Application programmers reimplementing them would be worse for performance</h3>

<p>If the “low-level application programming is essential for high performance” argument was true, then of course we would be actively dissuading researchers from using these high-level tools.  But we don’t, and we’re right not to.</p>

<p>Most of us who have worked with enough researchers writing their own HPC codes have had the experience of someone coming into our office who was broadcasting data with a loop over <code>MPI_Send()</code>s, or trying to write to a shared file using <code>fseek()</code> or the like, and we’ve directed them to collective operations or MPI-IO instead.  We do the same, of course, when someone is trying to type in some Gaussian Elimination code from Numerical Recipes (no link; that book has done enough damage) and we guide them to our local <a href="http://en.wikipedia.org/wiki/LAPACK">LAPACK</a> implementation instead.</p>

<p>And we do this because even we don’t believe that scientists implementing these things at low level will give better performance.  It’s not about it being “too hard”; it’s something else entirely.  We know that it would be a huge amount of wasted effort for a <em>worse</em>, <em>slower</em>, result.</p>

<p>MPI collective operation implementations make run-time decisions behind the researchers back, based on the size of the data, and the structure of the communicator being used, to decide whether to use k-ary trees, or hyper-cubes, or split-ring approaches, and in one, two, or multiple phases of communications, to perform the operation.  MPI-IO implementations uses approaches like data-sieving or two-phase I/O to trade off network communication for disk I/O, and use close integration with the filesystem to inform that tradeoff.</p>

<p>Somebody had to do all that challenging low-level work, yes.  But the idea that those optimizations and algorithmic work is properly the job of the researcher/application programmer is absurd.</p>

<h3 id="implementations-got-faster-and-faster">Implementations got faster and faster</h3>

<p>These highly optimized implementations of these high-level abstractions did not, of course, spring fully formed from somewhere, any more than the <a href="http://www.netlib.org/lapack/">reference implementation of LAPACK/BLAS</a> was blazingly fast.  The abstractions were created with an understanding of both what application programmers needed and what was implementable, and then years and years of work went into developing the algorithms and implementations that we make use of today.</p>

<p>Initial implementations of MPI-1 collectives were (naturally!) not super optimized, and there were certainly developers who scoffed at the performance and who pointed out they could do better writing low-level network code on their own.  They were, in that snapshot in time, narrowly correct; but more broadly and in the longer term, they were flat-out wrong.  The most useful and productive approach to a researcher finding out that early versions of those collective operations (say) were slow in some situations was not to break down and re-implement it themselves at low level; it was to file an issue with the library provider, and help them fix it so that it would be faster for everyone.</p>

<h2 id="these-points-generalize">These points generalize</h2>

<p>I don’t think anything I’ve said above is particuarly controversial. Performance, as well as productivity, for researchers and applications programmers has clearly improved as a result of MPI’s collectives and MPI-IO.</p>

<p>But for some reason, the idea that this generalizes — that performance as well as productivity of scientific software development would improve if applications developers spent their time using other, newer higher-level constructs while more tool-builders implemented those constructs in efficient ways — is anathaema to a section of our HPC community.</p>

<p>I’ve yet to hear compelling reasons why operations on distributed multidimensional arrays, or hash tables, or trees, are completely different from collectives or IO; why application programmers have to implement them directly or indirectly in a low-level tool like MPI sends and receives or gets and puts rather than having them implemented by experts in higher-level environments like Chapel, or Spark, or Ignite, or any of a zillion other projects from within or outside of the HPC community.</p>