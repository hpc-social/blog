---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2015-04-26 01:00:00'
layout: post
original_url: http://www.dursi.ca/post/coarray-fortran-goes-mainstream-gcc-5-1.html
title: Coarray Fortran Goes Mainstream- GCC 5.1
---

<p>This past week’s release of <a href="https://gcc.gnu.org/gcc-5/">GCC 5.1</a> contains at least <a href="https://gcc.gnu.org/gcc-5/changes.html">two new features</a> that are important to the big technical computing community: <a href="https://gcc.gnu.org/wiki/Offloading">OpenMP4/OpenACC offloading</a> to Intel Phi/NVIDIA accellerators, and compiler support for <a href="https://gcc.gnu.org/wiki/Coarray">Coarray Fortran</a>, with the communications layer provided by the <a href="http://opencoarrays.org">OpenCoarrays Project</a>.</p>

<p>While I don’t want to downplay the importance or technical accomplishment of the OpenMP 4 offloading now being available, I think it’s important to highlight the widespread availability for the first time of a tried-and-tested post-MPI programming model for HPC; and one that, since it is now part of the Fortran standard, is largely immune to fears that it might go away due to lack of interest. Here I’ll give a quick history of Coarray Fortran (CAF), some examples, and the pros and cons of CAF versus other approaches.</p>

<h2 id="a-quick-history-of-coarray-fortran">A quick history of Coarray Fortran</h2>

<p>Coarray Fortran first became widely known as Co-array Fortran, described in a <a href="https://scholar.google.ca/scholar?cluster=8719640223898917361&amp;hl=en&amp;as_sdt=0,5">1998 paper</a> which described an implementation on Cray systems (T3Es and X1s) of a minimal extension to Fortran 95 which included distributed memory computing of enough complexity to allow real applications.</p>

<p>The basic idea is simple enough from a developer’s point of view.  As with most MPI programs, a single program is launched across many processors.  Each “image” has its own local variables, as usual.  However, variables can also be defined to have a “co-dimension”; that is, a dimension which indexes that variable across all images.</p>

<pre><code class="language-fortran">program coarray1
  implicit none
  integer :: me, right, i
  integer, dimension(3), codimension[*] :: a

  me = this_image()

  right = me + 1
  if (right &gt; num_images()) right = 1

  a(:) = [ (me**i, i=1, 3) ]

  sync all

  print *, "Image ", me, " has a(2) = ", a(2)[me], "; neighbour has ", a(2)[right]
end program coarray1
</code></pre>
<p>where square brackets refer to the co-index across images; recall that Fortran, somewhat unfortunately, uses parenthesis both for array indexing and for function arguments.  Note also that, in Fortran fashion, image numbers begin at 1.</p>

<p>Running this on 4 images gives:</p>

<pre><code class="language-bash">$ ./coarray1
Image            2  has a(2) =            4 ; neighbour has            9
Image            3  has a(2) =            9 ; neighbour has           16
Image            4  has a(2) =           16 ; neighbour has            1
Image            1  has a(2) =            1 ; neighbour has            4
</code></pre>

<p>While it’s often the case that coarrays are also arrays – as is the case here with <code>a</code> – that needn’t be true.  Scalar variables - variables with out array dimensions - can nonetheless have codimensions and thus be coarrays.</p>

<p>Co-indexes needn’t be linear; one can also define co-dimensions of co-rank 2 or higher, to impose a grid-like pattern over the ranks.</p>

<p>Co-array Fortran continued to be used on Cray systems, and was submitted as a proposal for inclusion into Fortran 2008.  A stripped-down version of the original proposal (losing such things as image “teams”, and the hyphen in Co-array) made it through, with some minor syntax changes.  The Cray Fortran compiler quickly adopted the standard, and <a href="https://software.intel.com/en-us/articles/distributed-memory-coarray-fortran-with-the-intel-fortran-compiler-for-linux-essential">Intel’s fFortran compiler</a> has since version 12 supported SMP coarrays, and distributed-memory coarrays as part of the “Cluster suite” that includes Intel MPI.  IBM and PGI are said to be working on Coarray support. In less widely-used compilers, <a href="http://web.cs.uh.edu/~openuh/">OpenUH</a> supported Coarrays quite early on, as did the now-defunct <a href="http://www.g95.org">G95</a>.</p>

<p>A <a href="http://isotc.iso.org/livelink/livelink?func=ll&amp;objId=17064344&amp;objAction=Open">technical specification</a> which is expected to make it into a future Fortran standard largely unscathed re-instates support for teams (giving overlapping functionality with MPI communicators for coordinating subsets of processes), and adds some collective operations, some atomic operations, and Events, which are something like <a href="http://en.wikipedia.org/wiki/Monitor_(synchronization)">condition variables</a>.  GCC 5.1 supports many of these features already.</p>

<h2 id="examples">Examples</h2>

<p>Let’s take a look at a couple of simple examples to see how Coarray Fortran works in some familiar cases, and how the code complexity compares to MPI.</p>

<p>We’ll see in part that, unlike with (say) Spark or Chapel examples from earlier in the month, in Coarray Fortran the developer is still responsible for explicitly decomposing the problem.  That means a lot that part of the boilerplate of the MPI versions of the code remains.  However, as communication patterns become more complex, the code can still simplify quite a bit.</p>

<p>However, having the communications built into the language has another completely different advantage, one we’ve gotten used to not thinking about as we’re more used to using external libraries.  Communication being part of the language means that the compiler itself can perform high-level optimization on commuincations, just as it would with memory access.</p>

<h3 id="1d-diffusion-equation">1D diffusion equation</h3>

<p>Let’s take a look at a simple example I’ve used before, <a href="https://github.com/ljdursi/coarray-examples/tree/master/diffusion">1d diffusion</a>.  Here, we have a 1D domain broken up across images, or MPI ranks, exchanging data just with nearest neighbours.</p>

<p>Taking a look at the <a href="https://github.com/ljdursi/coarray-examples/blob/bc356ec1dce3493c59800f1845c93bf18a6e7403/diffusion/diffusion-coarray.f90#L108">CAF code</a>, we have the data exchange part:</p>

<pre><code class="language-fortran">!
! exchange boundary information
!

   sync images(neighbours(1:nneighbours))
   if (this_image() /= 1) then
       temperature(1,old) = temperature(locnpoints+1,old)[left]
   endif
   if (this_image() /= num_images()) then
      temperature(locnpoints+2,old) = temperature(2,old)[right]
   endif

!
! update solution
!
   forall (i=2:locnpoints+1)
       temperature(i,new) = temperature(i,old) + &amp;
             dt*kappa/(dx**2) * (                &amp;
                  temperature(i+1,old) -         &amp;
                2*temperature(i,  old) +         &amp;
                  temperature(i-1,old)           &amp;                           )
   end forall
</code></pre>

<p>There’s a synchronize statement at the beginning, to make sure we don’t get ahead of any of our neighbours (or vice versa), and then we pluck the necessary data for our guardcells out of the coarray of temperature.</p>

<p>This seems familiar, and indeed it’s not that different than the obvious <a href="https://github.com/ljdursi/coarray-examples/blob/bc356ec1dce3493c59800f1845c93bf18a6e7403/diffusion/diffusion-mpi.f90#L107">MPI implementation</a>:</p>

<pre><code class="language-fortran">   !...

   call MPI_Sendrecv(temperature(locnpoints+1,old), 1, MPI_REAL, right, righttag,  &amp;
             temperature(1,old), 1, MPI_REAL, left,  righttag, MPI_COMM_WORLD, rstatus, ierr)

   call MPI_Sendrecv(temperature(2,old), 1, MPI_REAL, left, lefttag,  &amp;
             temperature(locnpoints+2,old), 1, MPI_REAL, right,  lefttag, MPI_COMM_WORLD, rstatus, ierr)

   !...
</code></pre>

<p>(and the update is exactly same).</p>

<p>But having the exchange done in facilities built into the language has another benefit.  Let’s look back to the coarray version.  There’s a synchronization point, communications, computation, and (although we don’t see it here), a loop back to the synchronization point, as part of the iteration.</p>

<p>The compiler will, as it does, perform reorderings that it can prove to itself don’t change the meaning of the code but will likely improve performance.  With memory increasingly a bottleneck, compilers frequently perform some sort of prefetch optimization to move requests for data from slow main memory forward, perform computations on data already cache for the ~200 cycles that access will take, and only then work on the data that hopefully has loaded.</p>

<p>This optimization is familiar in the MPI world, of course; it’s overlapping communication with computation, and is performed using non-blocking Sends and Receives.  But because the communication is explicit to the compiler, it’s a difference of degree, not of kind, that the data is coming from over the network rather than from main memory.  Thus, this optimization is straightforwardly performed automatically by the compiler.</p>

<p>On the other hand, it is much less automatic for a developer to rewrite <a href="https://github.com/ljdursi/coarray-examples/blob/1acda1378398f3973a0066e09d89498a36769839/diffusion/diffusion-mpi-nonblocking.f90#L105">the MPI code</a>:</p>

<pre><code class="language-fortran">!
! begin exchange of boundary information
!

           call MPI_Isend(temperature(locnpoints+1,old), 1, MPI_REAL, &amp;
                          right, righttag, MPI_COMM_WORLD, requests(1), ierr)
           call MPI_Isend(temperature(2,old), 1, MPI_REAL, &amp;
                          left, lefttag,  MPI_COMM_WORLD, requests(2), ierr)
           call MPI_Irecv(temperature(1,old), 1, MPI_REAL, &amp;
                          left,  righttag, MPI_COMM_WORLD, requests(3), ierr)
           call MPI_Irecv(temperature(locnpoints+2,old), 1, MPI_REAL, &amp;
                          right, lefttag, MPI_COMM_WORLD, requests(4), ierr)

!
! update solution
!
           forall (i=3:locnpoints)
               temperature(i,new) = temperature(i,old) + &amp;
                     dt*kappa/(dx**2) * (                &amp;
                          temperature(i+1,old) -         &amp;
                        2*temperature(i,  old) +         &amp;
                          temperature(i-1,old)           &amp;
                     )
           end forall
           time = time + dt

!
! wait for communications to complete
!
           call MPI_Waitall(4, requests, statuses, ierr)
!
! update solution
!
           temperature(2,new) = temperature(2,old) + dt*kappa/(dx**2) *  &amp;
                        ( temperature(1,old) - 2*temperature(2, old) + temperature(3,old) )
           temperature(locnpoints+1,new) = temperature(locnpoints+1,old) + dt*kappa/(dx**2) *  &amp;
                        ( temperature(locnpoints,old) - 2*temperature(locnpoints+1, old) + &amp;
                          temperature(locnpoints+2,old) )
</code></pre>

<h3 id="block-matrix-multiplication">Block matrix multiplication</h3>

<p>Let’s take a look at another example, a simple <a href="https://github.com/ljdursi/coarray-examples/tree/master/blockmatrixmult">block matrix multiplication</a> where each image/task has one block of the A and B matrices, and we’re calculating \(C = A \times B\).</p>

<p>In the <a href="https://github.com/ljdursi/coarray-examples/blob/bc356ec1dce3493c59800f1845c93bf18a6e7403/blockmatrixmult/blockmatrix-coarray.f90#L38">CAF version</a>, this is almost embarrasingly easy:</p>

<pre><code class="language-fortran">    sync all
    c = 0.
    do k=1,ncols
        c = c + matmul(a[myrow,k],b[k,mycol])
    enddo
    sync all
</code></pre>

<p>and the exchange not that bad in <a href="https://github.com/ljdursi/coarray-examples/blob/bc356ec1dce3493c59800f1845c93bf18a6e7403/blockmatrixmult/blockmatrix-mpi.f90#L53">the MPI version, either</a>, using the SUMMA algorithm (Cannon’s, which can be better for small $P$, would have been messier):</p>

<pre><code class="language-fortran">    do k=0,ncols-1
        aremote = a
        bremote = b
        call MPI_Bcast(aremote, blockrows*blockcols, MPI_INTEGER, k, rowcomm, ierr)
        call MPI_Bcast(bremote, blockrows*blockcols, MPI_INTEGER, k, colcomm, ierr)
        c = c + matmul(aremote, bremote)
    enddo
</code></pre>

<p>although it did take us a lot more boilerplate to get there; three communicators, explicit temporary arrays, etc:</p>

<pre><code class="language-fortran">    call MPI_Init(ierr)
    call MPI_Comm_size(MPI_COMM_WORLD, comsize, ierr)

	!...

    allocate(aremote(blockrows,blockcols))
    allocate(bremote(blockcols,blockrows))

	!...

    call MPI_Cart_create(MPI_COMM_WORLD, 2, dims, [1,1], 1, cartcomm, ierr)
    call MPI_Comm_rank(cartcomm, rank, ierr)
    call MPI_Cart_coords(cartcomm, rank, 2, coords, ierr)

    ! create row, column communicators
    call MPI_Comm_split( cartcomm, myrow, mycol, rowcomm, ierr )
    call MPI_Comm_split( cartcomm, mycol, myrow, colcomm, ierr )
</code></pre>

<p>and this is still a fairly straightforward communications pattern.  As communications become more complex, the advantage of it being performed implicitly becomes more clear.</p>

<h3 id="coarray-pros">Coarray Pros</h3>

<p>We’ve only looked at two examples, but that’s enough to get some feelings about the strengths and weaknesses of CAF vs other options:</p>

<h4 id="part-of-the-language">Part of the Language</h4>

<p>Compilers are enormously more sophisticated than they were twenty+ years ago, and using those optimization engines to our advantage in generating fast communications code is an enormous advantage.  Having the communications be explicit in the language enables the compiler to perform entire suites of automatic optimizations (prefetching, batching, memory/time tradeoffs) that can’t easily done with library-based approaches.</p>

<h4 id="stable">Stable</h4>

<p>One concern in the HPC community about trying new approaches is lingering doubt about whether a given new tool or language will be around five or ten years later; a concern that can become self-fulfilling.</p>

<p>As part of the Fortran standard, Coarray Fortran is quite definitely here to stay; there are now several competing implementations, and competition will only improve them.</p>

<h4 id="incremental">Incremental</h4>

<p>Because Coarray Fortran uses a familiar model — Single Program, Multiple Data, with data manually decomposed — and only changes how the communications are expressed, there is very modest learning curve for developers already familiar with MPI, and very modest porting effort required.</p>

<p>The familiarity extends in another dimension, as well; Coarray fortran is about as “authentically HPC” as it’s possible to get (Cray!  T3Es!  Fortran!) for a community that is sometimes skeptical of ideas from the outside.</p>

<p>In addition, this incremental approach also makes interoperability with MPI relatively straightforward, for those requiring MPI-based library support.</p>

<h4 id="already-quite-fast">Already Quite Fast</h4>

<p>OpenCoarrays, which provides the communications support for gfortran’s coarray implementation, is <a href="http://opencoarrays.org/yahoo_site_admin/assets/docs/pgas14_submission_7.30712505.pdf">already comparable to and sometimes faster than</a> typical MPI code and even faster in some cases the very-well tested Cray coarray implementation(!).  While this is still the first major release of gfortran coarrays, and performance improvements and doubtless bug fixes remain to be made, this is already a fairly solid and fast piece of software.</p>

<h3 id="coarray-cons">Coarray Cons</h3>

<p>On the other side of the ledger are primarily points we’ve already considered as Pros, but viewed from the glass-half-empty side:</p>

<h4 id="part-of-a-language">Part of <em>A</em> Language</h4>

<p>Being built into a language means that it necessarily isn’t available to users of other languages.  I think this is largely inevitable for next-gen HPC approaches, to take full advantage of the compilers and runtimes that are now available, but it certainly will affect adoption; I can’t imagine too many C++ programmers will migrate to Fortran for their next project.  (Although it does start looking intriguing for Matlab or Python/Numpy users).</p>

<h4 id="stable-1">Stable</h4>

<p>As I’ve mentioned in the context of MPI, too much stability can be a bad thing, and the Fortran committee makes the MPI Forum look like a squirrel on cocaine.  I’m less concerned about that here in the short term, since the Coarrays that went into the standard were based on a model that had been used for years successfully, and new features are already in the works; but any additional new features that are seen to be needed may well be a long time coming.</p>

<h4 id="incremental-1">Incremental</h4>

<p>That Coarrays are incremental certainly makes it easier to port existing code, but it means that many of my concerns about MPI as a development environment remain unaddressed.  A researcher or application developer still has to perform the manual decomposition of a problem.  This requires an enormous amount of eminently automatable boilerplate and zillions of opportunities for meaningless bugs like off-by-one errors.  (That sort of bookkeeping is precisely what computers are better at than developers!)  That burden also means that substantial amounts of code must be rewritten if the decomposition changes.</p>

<h4 id="already-quite-fast-1">Already Quite Fast</h4>

<p>…Ok, it’s hard to see much of a downside here.</p>

<h3 id="conclusion">Conclusion</h3>

<p>The release of gcc-5.1 with coarray support is going to be the first time a huge number of HPC developers have ready access to coarrays.  From my point of view, it’s notably less ambitious than a large number of projects out there, but that may well make it easier to adopt for a sizable community.  Certainly anyone planning to start a new project in Fortran should give it very serious consideration.</p>

<p>My own hope is that Coarray Fortran will have a large number of delighted users, some of whose appetite then becomes whetted for other still more productive languages and environments for large-scale technical computing.  In the next few posts, I’ll take a closer look at some of those.</p>