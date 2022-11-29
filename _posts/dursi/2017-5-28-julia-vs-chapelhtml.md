---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2017-05-28 01:00:00'
layout: post
original_url: http://www.dursi.ca/post/julia-vs-chapel.html
slug: should-i-use-chapel-or-julia-for-my-next-project-
title: Should I use Chapel or Julia for my next project?
---

<p><a href="https://julialang.org">Julia</a> and <a href="http://chapel.cray.com">Chapel</a>
are both newish languages aimed at productitive scientific computing,
with parallel computing capabilities baked in from the start.
There’s lots of information about both online, but not much comparing
the two.  If you are starting a new scientific computing project
and are willing to try something new, which should you choose?  What
are their strengths and weaknesses, and how do they compare?</p>


<p>Here we walk through a comparison, focusing on distributed-memory
parallelism of the sort one would want for HPC-style simulation.
Both have strengths in largely disjoint areas.  If you want matlib-like
interactivity and plotting, and need only coodinator-worker parallelism,
Julia is the clear winner; if you want MPI+OpenMPI type scability
on rectangular distributed arrays (dense or sparse), Chapel wins
handily.  Both languages and environments have clear untapped
potential and room to grow; we’ll talk about future prospects of
the two languages at the end.</p>


<p><strong>Update</strong>: I’ve updated the timings - I hadn’t been using <code>@inbounds</code>
in the Julia code, and I had misconfigured my Chapel install so
that the compiles weren’t optimized; this makes a huge difference on
the 2d advection problem.  All timings now are on an AWS c4.8x instance.</p>


<ul id="markdown-toc">
  <li><a href="https://www.dursi.ca/feed.xml#a-quick-overview-of-the-two-languages" id="markdown-toc-a-quick-overview-of-the-two-languages">A quick overview of the two languages</a>    <ul>
      <li><a href="https://www.dursi.ca/feed.xml#julia" id="markdown-toc-julia">Julia</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#chapel" id="markdown-toc-chapel">Chapel</a></li>
    </ul>
  </li>
  <li><a href="https://www.dursi.ca/feed.xml#similarities-and-differences" id="markdown-toc-similarities-and-differences">Similarities and differences</a>    <ul>
      <li><a href="https://www.dursi.ca/feed.xml#standard-library" id="markdown-toc-standard-library">Standard library</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#other-packages" id="markdown-toc-other-packages">Other packages</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#language-features" id="markdown-toc-language-features">Language features</a></li>
    </ul>
  </li>
  <li><a href="https://www.dursi.ca/feed.xml#simple-computational-tasks" id="markdown-toc-simple-computational-tasks">Simple computational tasks</a>    <ul>
      <li><a href="https://www.dursi.ca/feed.xml#linear-algebra" id="markdown-toc-linear-algebra">Linear algebra</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#stencil-calculation" id="markdown-toc-stencil-calculation">Stencil calculation</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#kmer-counting" id="markdown-toc-kmer-counting">Kmer counting</a></li>
    </ul>
  </li>
  <li><a href="https://www.dursi.ca/feed.xml#parallel-primitives" id="markdown-toc-parallel-primitives">Parallel primitives</a>    <ul>
      <li><a href="https://www.dursi.ca/feed.xml#remote-function-execution" id="markdown-toc-remote-function-execution">Remote function execution</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#futures-atomics-and-synchronization" id="markdown-toc-futures-atomics-and-synchronization">Futures, atomics and synchronization</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#parallel-loops-reductions-and-maps" id="markdown-toc-parallel-loops-reductions-and-maps">Parallel loops, reductions, and maps</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#threading" id="markdown-toc-threading">Threading</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#distributed-data" id="markdown-toc-distributed-data">Distributed data</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#communications" id="markdown-toc-communications">Communications</a></li>
    </ul>
  </li>
  <li><a href="https://www.dursi.ca/feed.xml#a-2d-advection-problem" id="markdown-toc-a-2d-advection-problem">A 2d advection problem</a></li>
  <li><a href="https://www.dursi.ca/feed.xml#strengths-weaknesses-and-future-prospects" id="markdown-toc-strengths-weaknesses-and-future-prospects">Strengths, Weaknesses, and Future Prospects</a>    <ul>
      <li><a href="https://www.dursi.ca/feed.xml#julia-1" id="markdown-toc-julia-1">Julia</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#chapel-1" id="markdown-toc-chapel-1">Chapel</a></li>
    </ul>
  </li>
  <li><a href="https://www.dursi.ca/feed.xml#my-conclusions" id="markdown-toc-my-conclusions">My conclusions</a>    <ul>
      <li><a href="https://www.dursi.ca/feed.xml#both-projects-are-strong-and-useable-right-now-at-different-things" id="markdown-toc-both-projects-are-strong-and-useable-right-now-at-different-things">Both projects are strong and useable, right now, at different things</a></li>
      <li><a href="https://www.dursi.ca/feed.xml#both-projects-have-as-yet-untapped-potential" id="markdown-toc-both-projects-have-as-yet-untapped-potential">Both projects have as-yet untapped potential</a></li>
    </ul>
  </li>
</ul>

<h2 id="a-quick-overview-of-the-two-languages">A quick overview of the two languages</h2>

<h3 id="julia">Julia</h3>

<p>The <a href="https://julialang.org">Julia project</a> describes Julia as “a
high-level, high-performance dynamic programming language for
numerical computing.”  It exploits type inference of rich types,
just-in-time compilation, and <a href="https://en.wikipedia.org/wiki/Multiple_dispatch">multiple
dispatch</a> (think
of R, with say <code>print()</code> defined to operate differently on scalars,
data frames, or linear regression fits) to provide a dynamic,
interactive, “scripting language”-type high level numerical programming
language that gives performance less than but competitive with
C or Fortran.</p>


<p>The project sees the language as more or less a matlab-killer, and
so focusses on that sort of interface; interactive, through a REPL
or Jupyter notebook (both available to try <a href="https://juliabox.com">online</a>),
with integrated plotting; also, indexing begins at one, as God
intended.<sup id="fnref:1"><a class="footnote" href="https://www.dursi.ca/feed.xml#fn:1" rel="footnote">1</a></sup></p>


<table style="border: 1px solid black;">
<tbody>
<tr>
<td>Example from <a href="https://github.com/dpsanders/scipy_2014_julia">David Sanders’ SciPy 2014 tutorial</a></td>
<td></td>
</tr>
<tr>
<td>

<figure class="highlight"><pre><code class="language-julia"><span class="k">using</span> <span class="n">PyPlot</span>

<span class="c"># julia set</span>
<span class="k">function</span><span class="nf"> julia</span><span class="x">(</span><span class="n">z</span><span class="x">,</span> <span class="n">c</span><span class="x">;</span> <span class="n">maxiter</span><span class="o">=</span><span class="mi">200</span><span class="x">)</span>
    <span class="k">for</span> <span class="n">n</span> <span class="o">=</span> <span class="mi">1</span><span class="o">:</span><span class="n">maxiter</span>
        <span class="k">if</span> <span class="n">abs2</span><span class="x">(</span><span class="n">z</span><span class="x">)</span> <span class="o">&gt;</span> <span class="mi">4</span>
            <span class="k">return</span> <span class="n">n</span><span class="o">-</span><span class="mi">1</span>
        <span class="k">end</span>
        <span class="n">z</span> <span class="o">=</span> <span class="n">z</span><span class="o">*</span><span class="n">z</span> <span class="o">+</span> <span class="n">c</span>
    <span class="k">end</span>
    <span class="k">return</span> <span class="n">maxiter</span>
<span class="k">end</span>

<span class="n">jset</span> <span class="o">=</span> <span class="x">[</span> <span class="kt">UInt8</span><span class="x">(</span><span class="n">julia</span><span class="x">(</span><span class="n">complex</span><span class="x">(</span><span class="n">r</span><span class="x">,</span><span class="n">i</span><span class="x">),</span> <span class="n">complex</span><span class="x">(</span><span class="o">-.</span><span class="mi">06</span><span class="x">,</span><span class="o">.</span><span class="mi">67</span><span class="x">)))</span>
             <span class="k">for</span> <span class="n">i</span><span class="o">=</span><span class="mi">1</span><span class="o">:-.</span><span class="mi">002</span><span class="o">:-</span><span class="mi">1</span><span class="x">,</span> <span class="n">r</span><span class="o">=-</span><span class="mf">1.5</span><span class="o">:.</span><span class="mi">002</span><span class="o">:</span><span class="mf">1.5</span> <span class="x">];</span>
<span class="n">get_cmap</span><span class="x">(</span><span class="s">"RdGy"</span><span class="x">)</span>
<span class="n">imshow</span><span class="x">(</span><span class="n">jset</span><span class="x">,</span> <span class="n">cmap</span><span class="o">=</span><span class="s">"RdGy"</span><span class="x">,</span> <span class="n">extent</span><span class="o">=</span><span class="x">[</span><span class="o">-</span><span class="mf">1.5</span><span class="x">,</span><span class="mf">1.5</span><span class="x">,</span><span class="o">-</span><span class="mi">1</span><span class="x">,</span><span class="mi">1</span><span class="x">])</span></code></pre></figure>

</td>
<td>
<img alt="Julia set plot" src="https://www.dursi.ca/assets/julia_v_chapel/juliaset_in_julia.png" />
</td></tr>
</tbody>
</table>

<p>Julia blurs the distinction between scientific users of Julia and
developers in two quite powerful ways.  The first is lisp-like
<a href="https://docs.julialang.org/en/stable/manual/metaprogramming/">metaprogramming</a>,
where julia code can be generated or modified from within Julia,
making it possible to build domain-specific langauges (DSLs) inside Julia
for problems; this allows simple APIs for broad problem sets which
nonetheless take full advantage of the structure of the particular
problems being solved; <a href="https://github.com/JuliaStats">JuliaStats</a>,
<a href="https://github.com/JuliaDiffEq/DifferentialEquations.jl">DifferentialEquations.jl</a>,
<a href="https://github.com/JuliaFEM/JuliaFEM.jl">JuliaFEM</a>, and
<a href="https://github.com/JuliaOpt/JuMP.jl">JuMP</a> offer hints of what
that could look like.  Another sort of functionality this enables
is <a href="https://julialang.org/blog/2016/03/parallelaccelerator">Parallel Accellerator</a>, an
intel package that can rewrite some regular array operations into
fast, vectorized native code.  This code-is-data aspect of Julia,
combined with the fact that much of Julia itself is written in Julia,
puts user-written code on an equal footing with much “official”
julia code.</p>


<p>The second way Julia blurs the line between user and developer is
the <a href="https://docs.julialang.org/en/stable/manual/packages/">package system</a>
which uses git and GitHub; this means that once you’ve installed
someone’s package, you’re very close to being able to file a pull
request if you find a bug, or to fork the package to specialize
it to your own needs; and it’s similarly very easy to
contribute a package if you’re already using GitHub to develop the
package.</p>


<p>Julia has support for remote function execution (“out of the box”
using SSH + TCP/IP, but other transports are available through
packages), and distributed rectangular arrays; thread support
is still experimental, as is shared-memory on-node arrays.</p>


<h3 id="chapel">Chapel</h3>

<p>While Julia is a scientific programming language with parallel
computing support, Chapel is a programming language for parallel
scientific computing. It is a <a href="https://en.wikipedia.org/wiki/Partitioned_global_address_space">PGAS</a>
language, with partitioned but globally-accessible variables, using
<a href="https://gasnet.lbl.gov">GASNet</a> for communications.  It takes PGAS
two steps further however than languages like <a href="https://www.dursi.ca/post/coarray-fortran-goes-mainstream-gcc-5-1.html">Coarray
Fortran</a>,
<a href="http://upc.lbl.gov">UPC</a>, or <a href="http://x10-lang.org">X10</a>.</p>


<p>The first extension is to define all large data structures (arrays,
associative arrays, graphs) as being defined over <em>domains</em>, and
then definining a library of <em>domain maps</em> for distributing these
domains over different locality regions (“locales”) (nodes, or NUMA
nodes, or KNL accellerators) and <em>layouts</em> for describing their layout
within a locale.  By far the best tested and optimized domain maps
are for the cases of dense (and to a lesser extent, CSR-layout
sparse) rectangular arrays, as below, although there support for
associative arrays (dictionaries) and unstructured meshes/graphs
as well.</p>


<p>The second is to couple those domain maps with parallel iterators
over the domains, meaning that one can loop over the data in parallel
in one loop (think OpenMP) with a “global view” rather than expressing
the parallelism explicitly as a SIMD-type program.  This decouples
the expression of the layout of the data from the expression of the
calculation over the data, which is essential for productive parallel 
computing; it means that tweaking the layouts (or the dimensionality of
the program, or…) doesn’t require rewriting the internals of the
computation.</p>


<p>The distributions and layouts are written in Chapel, so that users can
contribute new domain maps to the project.</p>


<table style="border: 1px solid black;">
<tbody>
<tr> <td>
Example from <a href="http://chapel.cray.com/tutorials/ACCU2017/06-DomainMaps.pdf">Chapel tutorial at ACCU 2017</a>
</td> </tr>
<tr> <td>

<figure class="highlight"><pre><code class="language-chapel">var Dom: {1..4, 1..8} dmapped Block({1..4, 1..8});</code></pre></figure>

</td> </tr>
<tr> <td>
<img alt="Block Distribution" src="https://www.dursi.ca/assets/julia_v_chapel/block-dist.png" />
</td> </tr>
<tr> <td>

<figure class="highlight"><pre><code class="language-chapel">var Dom: {1..4, 1..8} dmapped Cyclic(startIdx=(1,1));</code></pre></figure>

</td> </tr>
<tr> <td>
<img alt="Block Distribution" src="https://www.dursi.ca/assets/julia_v_chapel/cyclic-dist.png" />
</td> </tr>
<tr> <td>

<figure class="highlight"><pre><code class="language-chapel">// either case:

var Inner : subdomain(Dom) = {2..3, 2..7};
const north = (-1,0), south = (1,0), east = (0,1), west = (0,-1);

var data, data_new : [Dom] real;
var delta : real;

forall ij in Inner {
    data_new(ij) = (data(ij+north) + data(ij+south)
                    + data(ij+east) + data(ij+west)) / 4.0;
}
delta = max reduce abs(data_new[Dom] - data[Dom]);</code></pre></figure>

</td> </tr>
</tbody>
</table>

<p>Chapel also exposes its lower-level parallel computing functionality —
such as remote function execution, fork/join task parallelism — so
that one can write a MPI-like SIMD program by explicity launching 
a function on each core:</p>


<figure class="highlight"><pre><code class="language-chapel">coforall loc in Locales do 
    on loc do
        coforall tid in 0..#here.maxTaskPar do
            do_simd_program(loc, tid);</code></pre></figure>

<p>At roughly eight years old as a publically available project, Chapel
is a slightly older and more mature language than Julia. However,
the language continues to evolve and there are breaking changes
between versions; these are much smaller and more localized breaking
changes than with Julia, so that most recent example code online
works readily.  As its focus has always been on large-scale parallelism
rather than desktop computing, its potential market is smaller
so has attracted less interest and fewer users than Julia
— however, if you read this blog, Chapel’s niche is one you are
almost certainly very interested in.  The relative paucity of users
is reflected in the smaller number of contributed packages, although
an upcoming package manager will likely lower the bar to future
contributions.</p>


<p>Chapel also lacks a REPL, which makes experimentation and testing
somewhat harder — there’s no equivalent of <a href="https://juliabox.com">JuliaBox</a>
where one can play with the language at a console or in a notebook.
There is an effort in that direction now which may be made easier
by ongoing work on the underlying compiler architecture.</p>


<h2 id="similarities-and-differences">Similarities and differences</h2>

<h3 id="standard-library">Standard library</h3>

<p>Both <a href="https://docs.julialang.org/en/stable">Julia</a> and <a href="http://chapel.cray.com/docs/latest/">Chapel</a>
have good documentation, and the basic modules or capabilities one would expect from languages 
aimed at technical computing:</p>


<ul>
  <li>Complex numbers</li>
  <li>Mathematical function libraries</li>
  <li>Random numbers</li>
  <li>Linear algebra</li>
  <li>FFTs</li>
  <li>C, Python interoperability</li>
  <li>Multi-precision floats / BigInts</li>
  <li>MPI interoperability</li>
  <li>Profiling</li>
</ul>

<p>although there are differences - in Julia, Python interoperability
is much more complete (the Julia set example above used matplotlib
plotting, while <a href="https://pychapel.readthedocs.io">pychapel</a> focuses
on calling Chapel from within python).  Also, Julia’s linear algebra
support is much slicker, styled after Matlab syntax and with a rich
set of matrix types (symmetric, tridiagonal, <em>etc.</em>), so that for
linear solves, say, a sensible method is chosen automatically; the
consise syntax and “do the right thing” approach are particularly
helpful for interactive use<sup id="fnref:2"><a class="footnote" href="https://www.dursi.ca/feed.xml#fn:2" rel="footnote">2</a></sup>, which is a primary use-case of Julia.</p>


<p>On profiling, the Julia support is primariy for serial profiling
and text based; Chapel has a very nice tool called
<a href="http://chapel.cray.com/docs/1.14/tools/chplvis/chplvis.html">chplvis</a> 
for visualizing parallel performance.</p>


<h3 id="other-packages">Other packages</h3>

<p>Julia’s early adoption of a package management framework and very
large initial userbase has lead to a <a href="http://pkg.julialang.org">very large ecosystem</a>
of contributed packages.  As with all such package ecosystems, 
the packages themselves are a bit of a mixed bag – lots are broken or
abandoned, many are simply wrappers to other tools – but there
are also excellent, substantial packages taking full advantage of
Julia’s capabalities that are of immediate interest
to those doing scientific computing, such as 
<a href="https://github.com/JuliaDiffEq/DifferentialEquations.jl">DifferentialEquations.jl</a>
for ODEs, SDEs, and and FEM for some PDEs,
<a href="https://github.com/BioJulia">BioJulia</a> for bioinformatics,
<a href="http://www.juliadiff.org">JuliaDiff</a> for automatic differentiation,
and <a href="http://juliastats.github.io">JuliaStats</a> for R-like
statistical computing.  The julia project would benefit from
having a more curated view of the package listings easily available
so that these high-quality tools were more readily visible to
new users.</p>


<p>On the other hand, there are almost no packages available for Chapel
outside of the main project.  There are efforts to develop a package
manager inspired by cargo (Rust) and glide (Go); this would be an
important and needed development, almost certainly necessary
to grow the Chapel community.</p>


<h3 id="language-features">Language features</h3>

<p>The biggest language feature difference is undoubtedly Julia’s
JIT-powered lisp-metaprogramming capabilities; Chapel is a more
statically-compiled language, with generics and reflection but not
full lisp-like code-is-data.  A small downside of Julia’s JIT
approach is that functions are often slow the first time they are
called, as they must be compiled.  Relatedly, Julia is garbage-collected,
which can lead to pauses and memory pressure at unexpected times.
On the other hand, Chapel’s compile time, which is still quite long
even compared to other compilers, makes the development cycle much
slower than it would be with Julia or Python.</p>


<p>Beyond that, Julia and Chapel are both quite new and have functionality
one might expect in a modern language: first class functions, lambda
functions, comprehensions, keyword/optional parameters, type
inference, generics, reflection, iterators, ranges, coroutines and
green threads, futures, and JuliaDoc/chpldoc python packages for
generating online documentation from source code and embedded
comments.</p>


<p>More minor but something that quickly comes up: there’s difference
in command-line argument handling which reflects the use
cases each team finds important.  Both give access to an argv-like array of
strings passed to the command line; in base Julia with its interactive
nature, that’s it (although there’s a nice python-argparse inspired
<a href="http://carlobaldassi.github.io/ArgParse.jl/latest/">contributed package</a>),
while in Chapel, intended to make compiled long-running executables
one can define a constant (<code>const n = 10;</code>) and make it settable
on the command line by prefixing the <code>const</code> with <code>config</code> and running
the program with <code>--n 20</code>.</p>


<h2 id="simple-computational-tasks">Simple computational tasks</h2>

<p>Here we take a look at a couple common single-node scientific
computation primitives in each framework (with Python for comparison)
to compare the language features.  Full code for the examples are
available <a href="http://www.github.com/ljdursi/julia_v_chapel">on GitHub</a>.</p>


<h3 id="linear-algebra">Linear algebra</h3>

<p>For linear algebra operations, Julia’s matlab lineage and
interactive really shine:</p>


<table style="border: 1px solid black;">
<tbody>
<tr><td><strong>Julia</strong></td>
<td>

<figure class="highlight"><pre><code class="language-julia"><span class="c"># ...</span>
<span class="n">n</span> <span class="o">=</span> <span class="mi">500</span>
<span class="n">B</span> <span class="o">=</span> <span class="n">rand</span><span class="x">(</span><span class="n">n</span><span class="x">,</span> <span class="n">n</span><span class="x">)</span>
<span class="n">x</span> <span class="o">=</span> <span class="n">rand</span><span class="x">(</span><span class="n">n</span><span class="x">)</span>

<span class="n">A</span> <span class="o">=</span> <span class="n">x</span><span class="o">*</span><span class="n">x</span><span class="err">'</span>
<span class="n">y</span> <span class="o">=</span> <span class="n">B</span><span class="o">*</span><span class="n">x</span>

<span class="n">println</span><span class="x">(</span><span class="n">A</span><span class="x">[</span><span class="mi">1</span><span class="x">,</span><span class="mi">1</span><span class="x">])</span>

<span class="n">A</span> <span class="o">=</span> <span class="n">eye</span><span class="x">(</span><span class="n">n</span><span class="x">)</span>
<span class="n">y</span> <span class="o">=</span> <span class="n">A</span><span class="o">\</span><span class="n">x</span>

<span class="n">println</span><span class="x">(</span><span class="n">sum</span><span class="x">(</span><span class="n">abs</span><span class="o">.</span><span class="x">(</span><span class="n">x</span><span class="o">-</span><span class="n">y</span><span class="x">)))</span>
<span class="c"># ...</span></code></pre></figure>

</td></tr>
<tr><td><strong>Chapel</strong></td>
<td>

<figure class="highlight"><pre><code class="language-c"><span class="n">use</span> <span class="n">LinearAlgebra</span><span class="p">;</span>
<span class="n">use</span> <span class="n">LAPACK</span><span class="p">;</span>
<span class="n">use</span> <span class="n">Random</span><span class="p">;</span>

<span class="n">config</span> <span class="k">const</span> <span class="n">n</span><span class="o">=</span><span class="mi">500</span><span class="p">;</span>

<span class="n">var</span> <span class="n">A</span> <span class="o">=</span> <span class="n">Matrix</span><span class="p">(</span><span class="n">n</span><span class="p">,</span> <span class="n">n</span><span class="p">),</span>
    <span class="n">B</span> <span class="o">=</span> <span class="n">Matrix</span><span class="p">(</span><span class="n">n</span><span class="p">,</span> <span class="n">n</span><span class="p">),</span>
    <span class="n">x</span><span class="p">,</span> <span class="n">y</span> <span class="o">=</span> <span class="n">Vector</span><span class="p">(</span><span class="n">n</span><span class="p">);</span>

<span class="n">fillRandom</span><span class="p">(</span><span class="n">B</span><span class="p">);</span>
<span class="n">fillRandom</span><span class="p">(</span><span class="n">x</span><span class="p">);</span>

<span class="n">y</span> <span class="o">=</span> <span class="n">dot</span><span class="p">(</span><span class="n">B</span><span class="p">,</span> <span class="n">x</span><span class="p">);</span>
<span class="n">A</span> <span class="o">=</span> <span class="n">outer</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y</span><span class="p">);</span>

<span class="n">writeln</span><span class="p">(</span><span class="n">A</span><span class="p">[</span><span class="mi">1</span><span class="p">,</span><span class="mi">1</span><span class="p">]);</span>

<span class="n">var</span> <span class="n">X</span> <span class="o">=</span> <span class="n">Matrix</span><span class="p">(</span><span class="n">n</span><span class="p">,</span><span class="mi">1</span><span class="p">);</span>
<span class="n">var</span> <span class="n">Y</span> <span class="o">=</span> <span class="n">Matrix</span><span class="p">(</span><span class="n">n</span><span class="p">,</span><span class="mi">1</span><span class="p">);</span>
<span class="n">X</span><span class="p">({</span><span class="mi">1</span><span class="p">..</span><span class="n">n</span><span class="p">},</span><span class="mi">1</span><span class="p">)</span> <span class="o">=</span> <span class="n">x</span><span class="p">({</span><span class="mi">1</span><span class="p">..</span><span class="n">n</span><span class="p">});</span>

<span class="n">A</span> <span class="o">=</span> <span class="n">eye</span><span class="p">(</span><span class="n">n</span><span class="p">);</span>
<span class="n">var</span> <span class="n">ipiv</span> <span class="o">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">..</span><span class="n">n</span><span class="p">]</span> <span class="n">c_int</span><span class="p">;</span>
<span class="n">Y</span> <span class="o">=</span> <span class="n">X</span><span class="p">;</span>
<span class="n">var</span> <span class="n">info</span> <span class="o">=</span> <span class="n">gesv</span><span class="p">(</span><span class="n">lapack_memory_order</span><span class="p">.</span><span class="n">row_major</span><span class="p">,</span> <span class="n">A</span><span class="p">,</span> <span class="n">ipiv</span><span class="p">,</span> <span class="n">Y</span><span class="p">);</span>

<span class="n">var</span> <span class="n">res</span> <span class="o">=</span> <span class="o">+</span> <span class="n">reduce</span> <span class="nf">abs</span><span class="p">(</span><span class="n">x</span><span class="o">-</span><span class="n">y</span><span class="p">);</span>

<span class="n">writeln</span><span class="p">(</span><span class="n">res</span><span class="p">);</span></code></pre></figure>

</td></tr>
<tr><td><strong>Python</strong></td>
<td>

<figure class="highlight"><pre><code class="language-python"><span class="kn">from</span> <span class="nn">__future__</span> <span class="kn">import</span> <span class="n">print_function</span>
<span class="kn">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="n">np</span>

<span class="n">n</span> <span class="o">=</span> <span class="mi">500</span>
<span class="n">B</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">random</span><span class="p">.</span><span class="n">rand</span><span class="p">(</span><span class="mi">500</span><span class="p">,</span> <span class="mi">500</span><span class="p">)</span>
<span class="n">x</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">random</span><span class="p">.</span><span class="n">rand</span><span class="p">(</span><span class="mi">500</span><span class="p">)</span>

<span class="n">A</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">outer</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">np</span><span class="p">.</span><span class="n">transpose</span><span class="p">(</span><span class="n">x</span><span class="p">))</span>
<span class="n">y</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">dot</span><span class="p">(</span><span class="n">B</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span>

<span class="k">print</span><span class="p">(</span><span class="n">A</span><span class="p">[</span><span class="mi">0</span><span class="p">,</span><span class="mi">0</span><span class="p">])</span>

<span class="n">A</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">eye</span><span class="p">(</span><span class="n">n</span><span class="p">)</span>
<span class="n">y</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">linalg</span><span class="p">.</span><span class="n">solve</span><span class="p">(</span><span class="n">A</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span>

<span class="k">print</span><span class="p">(</span><span class="n">np</span><span class="p">.</span><span class="nb">sum</span><span class="p">(</span><span class="n">np</span><span class="p">.</span><span class="nb">abs</span><span class="p">(</span><span class="n">x</span><span class="o">-</span><span class="n">y</span><span class="p">)))</span></code></pre></figure>

</td></tr>
</tbody>
</table>

<p>The new Chapel <code>LinearAlgebra</code> and <code>LAPACK</code> modules don’t really 
work well together yet, so one has to awkwardly switch between
the two idioms, but that’s readily easily fixed.  Julia’s nice
matrix type system allows “do the right-thing” type linear solves,
which is incredibly handy for interactive work, although for a 
compiled program that will be used repeatedly, the clarity of
specifying a specific solver (which Julia also allows) is probably
advantageous.</p>


<h3 id="stencil-calculation">Stencil calculation</h3>

<p>Below we take a look at a simple 1-d explicit heat diffusion equation,
requiring a small stencil, and see how it compares across the languges.</p>


<table style="border: 1px solid black;">
<tbody>
<tr><td><strong>Julia</strong></td>
<td>

<figure class="highlight"><pre><code class="language-julia"><span class="c"># ...</span>
<span class="k">for</span> <span class="n">i</span> <span class="k">in</span> <span class="mi">2</span><span class="o">:</span><span class="n">ngrid</span><span class="o">+</span><span class="mi">1</span>
  <span class="nd">@inbounds</span> <span class="n">temp</span><span class="x">[</span><span class="n">i</span><span class="x">]</span> <span class="o">=</span> <span class="mf">0.</span>
<span class="k">end</span>

<span class="n">temp</span><span class="x">[</span><span class="mi">1</span><span class="x">]</span> <span class="o">=</span> <span class="n">tleft</span>
<span class="n">temp</span><span class="x">[</span><span class="n">ngrid</span><span class="o">+</span><span class="mi">2</span><span class="x">]</span> <span class="o">=</span> <span class="n">tright</span>

<span class="k">for</span> <span class="n">iteration</span> <span class="k">in</span> <span class="mi">1</span><span class="o">:</span><span class="n">ntimesteps</span>
  <span class="k">for</span> <span class="n">i</span> <span class="k">in</span> <span class="mi">2</span><span class="o">:</span><span class="n">ngrid</span><span class="o">+</span><span class="mi">1</span>
      <span class="nd">@inbounds</span> <span class="n">temp_new</span><span class="x">[</span><span class="n">i</span><span class="x">]</span> <span class="o">=</span> <span class="n">temp</span><span class="x">[</span><span class="n">i</span><span class="x">]</span> <span class="o">+</span> <span class="n">kappa</span><span class="o">*</span><span class="n">dt</span><span class="o">/</span><span class="x">(</span><span class="n">dx</span><span class="o">*</span><span class="n">dx</span><span class="x">)</span><span class="o">*</span>
                      <span class="x">(</span><span class="n">temp</span><span class="x">[</span><span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="x">]</span> <span class="o">-</span> <span class="mi">2</span><span class="o">*</span><span class="n">temp</span><span class="x">[</span><span class="n">i</span><span class="x">]</span> <span class="o">+</span> <span class="n">temp</span><span class="x">[</span><span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="x">])</span>
  <span class="k">end</span>
  <span class="k">for</span> <span class="n">i</span> <span class="k">in</span> <span class="mi">2</span><span class="o">:</span><span class="n">ngrid</span><span class="o">+</span><span class="mi">1</span>
      <span class="nd">@inbounds</span> <span class="n">temp</span><span class="x">[</span><span class="n">i</span><span class="x">]</span> <span class="o">=</span> <span class="n">temp_new</span><span class="x">[</span><span class="n">i</span><span class="x">]</span>
  <span class="k">end</span>
<span class="k">end</span>
<span class="c"># ...</span></code></pre></figure>

</td></tr>
<tr><td><strong>Chapel</strong></td>
<td>

<figure class="highlight"><pre><code class="language-c"><span class="c1">// ...</span>
<span class="k">const</span> <span class="n">ProblemSpace</span> <span class="o">=</span> <span class="p">{</span><span class="mi">1</span><span class="p">..</span><span class="n">ngrid</span><span class="p">},</span>
      <span class="n">BigDomain</span> <span class="o">=</span> <span class="p">{</span><span class="mi">0</span><span class="p">..</span><span class="n">ngrid</span><span class="o">+</span><span class="mi">1</span><span class="p">};</span>
<span class="n">var</span> <span class="n">T</span><span class="p">,</span> <span class="n">TNew</span><span class="o">:</span> <span class="p">[</span><span class="n">BigDomain</span><span class="p">]</span> <span class="n">real</span><span class="p">(</span><span class="mi">64</span><span class="p">)</span> <span class="o">=</span> <span class="mi">0</span><span class="p">.</span><span class="mi">0</span><span class="p">;</span>

<span class="n">var</span> <span class="n">iteration</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>
<span class="n">T</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">=</span> <span class="n">tleft</span><span class="p">;</span>
<span class="n">T</span><span class="p">[</span><span class="n">ngrid</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="n">tright</span><span class="p">;</span>

<span class="k">const</span> <span class="n">left</span> <span class="o">=</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">right</span> <span class="o">=</span> <span class="mi">1</span><span class="p">;</span>

<span class="k">for</span> <span class="n">iteration</span> <span class="n">in</span> <span class="mi">1</span><span class="p">..</span><span class="n">ntimesteps</span> <span class="p">{</span>
  <span class="k">for</span> <span class="n">i</span> <span class="n">in</span> <span class="n">ProblemSpace</span> <span class="p">{</span>
    <span class="n">TNew</span><span class="p">(</span><span class="n">i</span><span class="p">)</span> <span class="o">=</span> <span class="n">T</span><span class="p">(</span><span class="n">i</span><span class="p">)</span> <span class="o">+</span> <span class="n">kappa</span><span class="o">*</span><span class="n">dt</span><span class="o">/</span><span class="p">(</span><span class="n">dx</span><span class="o">*</span><span class="n">dx</span><span class="p">)</span> <span class="o">*</span>
          <span class="p">(</span><span class="n">T</span><span class="p">(</span><span class="n">i</span><span class="o">+</span><span class="n">left</span><span class="p">)</span> <span class="o">-</span> <span class="mi">2</span><span class="o">*</span><span class="n">T</span><span class="p">(</span><span class="n">i</span><span class="p">)</span> <span class="o">+</span> <span class="n">T</span><span class="p">(</span><span class="n">i</span><span class="o">+</span><span class="n">right</span><span class="p">));</span>
  <span class="p">}</span>
  <span class="k">for</span> <span class="n">i</span> <span class="n">in</span> <span class="n">ProblemSpace</span> <span class="p">{</span>
    <span class="n">T</span><span class="p">(</span><span class="n">i</span><span class="p">)</span> <span class="o">=</span> <span class="n">TNew</span><span class="p">(</span><span class="n">i</span><span class="p">)</span>
  <span class="p">}</span>
<span class="p">}</span>
<span class="c1">// ...</span></code></pre></figure>

</td></tr>
<tr><td><strong>Python</strong></td>
<td>

<figure class="highlight"><pre><code class="language-python"><span class="c1"># ...
</span><span class="o">@</span><span class="n">jit</span><span class="p">(</span><span class="s">'f8[:](i4, i4, f8, f8, f8, f8, f8)'</span><span class="p">,</span> <span class="n">nopython</span><span class="o">=</span><span class="bp">True</span><span class="p">,</span> <span class="n">nogil</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">onedheat</span><span class="p">(</span><span class="n">ngrid</span><span class="p">,</span> <span class="n">ntimesteps</span><span class="p">,</span> <span class="n">kappa</span><span class="p">,</span> <span class="n">xleft</span><span class="p">,</span> <span class="n">xright</span><span class="p">,</span> <span class="n">tleft</span><span class="p">,</span> <span class="n">tright</span><span class="p">):</span>
    <span class="n">dx</span> <span class="o">=</span> <span class="p">(</span><span class="n">xright</span><span class="o">-</span><span class="n">xleft</span><span class="p">)</span><span class="o">/</span><span class="p">(</span><span class="n">ngrid</span><span class="o">-</span><span class="mi">1</span><span class="p">)</span>
    <span class="n">dt</span> <span class="o">=</span> <span class="mf">0.25</span><span class="o">*</span><span class="n">dx</span><span class="o">*</span><span class="n">dx</span><span class="o">/</span><span class="n">kappa</span>

    <span class="n">temp</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">ngrid</span><span class="o">+</span><span class="mi">2</span><span class="p">,</span> <span class="n">dtype</span><span class="o">=</span><span class="n">np</span><span class="p">.</span><span class="n">double</span><span class="p">)</span>
    <span class="n">temp_new</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">zeros</span><span class="p">(</span><span class="n">ngrid</span><span class="o">+</span><span class="mi">2</span><span class="p">,</span> <span class="n">dtype</span><span class="o">=</span><span class="n">np</span><span class="p">.</span><span class="n">double</span><span class="p">)</span>
    <span class="n">temp</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">temp</span><span class="p">[</span><span class="n">ngrid</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="n">tleft</span><span class="p">,</span> <span class="n">tright</span>

    <span class="k">for</span> <span class="n">iteration</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">ntimesteps</span><span class="p">):</span>
        <span class="n">temp_new</span><span class="p">[</span><span class="mi">1</span><span class="p">:</span><span class="n">ngrid</span><span class="p">]</span> <span class="o">=</span> <span class="n">temp</span><span class="p">[</span><span class="mi">1</span><span class="p">:</span><span class="n">ngrid</span><span class="p">]</span> <span class="o">+</span> <span class="n">kappa</span><span class="o">*</span><span class="n">dt</span><span class="o">/</span><span class="p">(</span><span class="n">dx</span><span class="o">*</span><span class="n">dx</span><span class="p">)</span> <span class="o">*</span> \
            <span class="p">(</span><span class="n">temp</span><span class="p">[</span><span class="mi">2</span><span class="p">:</span><span class="n">ngrid</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="o">-</span> <span class="mf">2.</span><span class="o">*</span><span class="n">temp</span><span class="p">[</span><span class="mi">1</span><span class="p">:</span><span class="n">ngrid</span><span class="p">]</span> <span class="o">+</span> <span class="n">temp</span><span class="p">[</span><span class="mi">0</span><span class="p">:</span><span class="n">ngrid</span><span class="o">-</span><span class="mi">1</span><span class="p">])</span>

        <span class="n">temp</span><span class="p">[</span><span class="mi">1</span><span class="p">:</span><span class="n">ngrid</span><span class="p">]</span> <span class="o">=</span> <span class="n">temp_new</span><span class="p">[</span><span class="mi">1</span><span class="p">:</span><span class="n">ngrid</span><span class="p">]</span>

    <span class="k">return</span> <span class="n">temp</span><span class="p">[</span><span class="mi">1</span><span class="p">:</span><span class="n">ngrid</span><span class="p">]</span>
<span class="c1"># ...</span></code></pre></figure>

</td></tr>
</tbody>
</table>

<p>The main difference above is that the easiest way to get fast array
operations out of Julia is to explicitly write out the loops as vs.
numpy, and of explicitly using domains in Chapel.  Timings are
below, for 10,000 timesteps of a domain of size 1,001.  The Julia
script included a “dummy” call to the main program to “warm up” the
JIT, and then called on the routine.  In Julia, for performance we
have to include the <code>@inbounds</code> macro; Julia’s JIT doesn’t recognize
that the stencil calculation over fixed bounds is in bounds of the
array defined with those same fixed bounds a couple of lines before.
Compile times are included for the Julia and Python JITs (naively
calculated as total run time minus the final time spent running the
calculation)</p>


<table style="border: 1px solid black; margin: 0 auto; border-collapse: collapse;">
<thead>
<th>time</th> <th>Julia</th> <th>Chapel</th> <th>Python + Numpy + Numba</th><th>Python + Numpy</th>
</thead>
<tbody style="border: 1px solid black;">
<tr><td style="border: 1px solid black;">run</td><td style="border: 1px solid black;">0.0084</td><td style="border: 1px solid black;">0.0098 s</td><td style="border: 1px solid black;">0.017 s</td><td style="border: 1px solid black;">0.069 s</td></tr>
<tr><td style="border: 1px solid black;">compile</td><td style="border: 1px solid black;">0.57 s</td><td style="border: 1px solid black;">4.8s</td><td style="border: 1px solid black;">0.73 s</td><td style="border: 1px solid black;"> - </td></tr>
</tbody>
</table>

<p>Julia wins this test, edging out Chapel by 16%; Python with numba is 
surprisingly (to me) fast, coming within a factor of two.</p>


<h3 id="kmer-counting">Kmer counting</h3>

<p>Fields like bioinformatics or digital humanities push research
computing beyond matrix-slinging and array manipulations into the
more difficult areas of text handling, string manipulation, and
indexing.  Here we mock up a trivial kmer-counter, reading in 
genomic sequence data and counting the distribution of k-length
substrings.  A real implementation (such as in BioJulia or BioPython)
would optimize for the special case we’re in – a small fixed known
alphabet, and a hash function which takes advantage of the fact that
two neighbouring kmers overlap in k-1 characters – but
but here we’re just interested in the dictionary/associative array
handling and simple string slicing.  Here we’re using pure Python for
the Python implementation:</p>


<table style="border: 1px solid black;">
<tbody>
<tr><td><strong>Julia</strong></td>
<td>

<figure class="highlight"><pre><code class="language-julia"><span class="c"># ...</span>
<span class="n">sequences</span> <span class="o">=</span> <span class="n">read_sequences</span><span class="x">(</span><span class="n">infile</span><span class="x">)</span>

<span class="n">counts</span> <span class="o">=</span> <span class="n">DefaultDict</span><span class="x">{</span><span class="kt">String</span><span class="x">,</span> <span class="kt">Int8</span><span class="x">}(</span><span class="mi">0</span><span class="x">)</span>
<span class="k">for</span> <span class="n">seq</span> <span class="k">in</span> <span class="n">sequences</span>
    <span class="k">for</span> <span class="n">i</span> <span class="o">=</span> <span class="mi">1</span><span class="o">:</span><span class="n">length</span><span class="x">(</span><span class="n">seq</span><span class="x">)</span><span class="o">-</span><span class="n">k</span><span class="o">+</span><span class="mi">1</span>
        <span class="n">kmer</span> <span class="o">=</span> <span class="n">seq</span><span class="x">[</span><span class="n">i</span> <span class="o">:</span> <span class="n">i</span><span class="o">+</span><span class="n">k</span><span class="o">-</span><span class="mi">1</span><span class="x">]</span>
        <span class="n">counts</span><span class="x">[</span><span class="n">kmer</span><span class="x">]</span> <span class="o">+=</span> <span class="mi">1</span>
    <span class="k">end</span>
<span class="k">end</span> 
<span class="c"># ...</span></code></pre></figure>

</td></tr>
<tr><td><strong>Chapel</strong></td>
<td>

<figure class="highlight"><pre><code class="language-c"><span class="c1">// ...</span>
<span class="n">var</span> <span class="n">sequences</span> <span class="o">=</span> <span class="n">readfasta</span><span class="p">(</span><span class="n">input_filename</span><span class="p">);</span>

<span class="n">var</span> <span class="n">kmers</span> <span class="o">:</span> <span class="n">domain</span><span class="p">(</span><span class="n">string</span><span class="p">);</span>
<span class="n">var</span> <span class="n">kmer_counts</span><span class="o">:</span> <span class="p">[</span><span class="n">kmers</span><span class="p">]</span> <span class="kt">int</span><span class="p">;</span>

<span class="k">for</span> <span class="n">sequence</span> <span class="n">in</span> <span class="n">sequences</span> <span class="p">{</span>
  <span class="k">for</span> <span class="n">i</span> <span class="n">in</span> <span class="mi">1</span><span class="p">..(</span><span class="n">sequence</span><span class="p">.</span><span class="n">length</span><span class="o">-</span><span class="n">k</span><span class="o">+</span><span class="mi">1</span><span class="p">)</span> <span class="p">{</span>
    <span class="n">var</span> <span class="n">kmer</span><span class="o">:</span> <span class="n">string</span> <span class="o">=</span> <span class="n">sequence</span><span class="p">[</span><span class="n">i</span><span class="p">..</span><span class="err">#</span><span class="n">k</span><span class="p">];</span>
    <span class="k">if</span> <span class="o">!</span><span class="n">kmers</span><span class="p">.</span><span class="n">member</span><span class="p">(</span><span class="n">kmer</span><span class="p">)</span> <span class="p">{</span>
      <span class="n">kmer_counts</span><span class="p">[</span><span class="n">kmer</span><span class="p">]</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span>
    <span class="p">}</span>
    <span class="n">kmer_counts</span><span class="p">[</span><span class="n">kmer</span><span class="p">]</span> <span class="o">+=</span> <span class="mi">1</span><span class="p">;</span>
  <span class="p">}</span>
<span class="p">}</span>
<span class="c1">// ...</span></code></pre></figure>

</td></tr>
<tr><td><strong>Python</strong></td>
<td>

<figure class="highlight"><pre><code class="language-python"><span class="c1"># ...
</span><span class="k">def</span> <span class="nf">kmer_counts</span><span class="p">(</span><span class="n">filename</span><span class="p">,</span> <span class="n">k</span><span class="p">):</span>
    <span class="n">sequences</span> <span class="o">=</span> <span class="n">readfasta</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span>
    <span class="n">counts</span> <span class="o">=</span> <span class="n">collections</span><span class="p">.</span><span class="n">defaultdict</span><span class="p">(</span><span class="nb">int</span><span class="p">)</span>
    <span class="k">for</span> <span class="n">sequence</span> <span class="ow">in</span> <span class="n">sequences</span><span class="p">:</span>
        <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">sequence</span><span class="p">)</span><span class="o">-</span><span class="n">k</span><span class="o">+</span><span class="mi">1</span><span class="p">):</span>
            <span class="n">kmer</span> <span class="o">=</span> <span class="n">sequence</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">i</span><span class="o">+</span><span class="n">k</span><span class="p">]</span>
            <span class="n">counts</span><span class="p">[</span><span class="n">kmer</span><span class="p">]</span> <span class="o">+=</span> <span class="mi">1</span>
    <span class="k">return</span> <span class="n">counts</span>

<span class="c1"># ...</span></code></pre></figure>

</td></tr>
</tbody>
</table>

<p>Other than the syntax differences, the main difference here is
Python and Chapel have convenience functions in their <code>defaultdict</code>s
which mean you don’t have to handle the key-not-yet-found case
separately, and Chapel has the user explicitly declare the domain
of keys.  All perform quite well, particularly Julia; on a 4.5Mb
FASTA file for the reference genome of a strain of E. coli,
we get timings as below</p>


<table style="border: 1px solid black; margin: 0 auto; border-collapse: collapse;">
<thead>
<th>time</th> <th>Julia</th> <th>Chapel</th> <th>Python</th>
</thead>
<tbody style="border: 1px solid black;">
<tr><td style="border: 1px solid black;">run</td><td style="border: 1px solid black;">5.3 s</td><td style="border: 1px solid black;">6.6s</td><td style="border: 1px solid black;">7.7s</td></tr>
<tr><td style="border: 1px solid black;">compile</td><td style="border: 1px solid black;">-</td><td style="border: 1px solid black;">6.2s</td><td style="border: 1px solid black;">-</td></tr>
</tbody>
</table>

<p>Beating pure Python on dictionary and string operations isn’t
actually a given, even for a compiled language, as those features
are heavily optimized in Python implementations.</p>


<p>(One caveat about the timings; pairwise string concatenation in Julia is <em>slow</em>; 
in reading in the file, concatenating the sequence data in Julia
as it was done in the other languages resulted in a runtime of 54 seconds!
Instead, all sequence fragments were read in and the result put together
at once with <code>join()</code>.)</p>


<h2 id="parallel-primitives">Parallel primitives</h2>

<p>Since we’re interested in large-scale computation, parallel features are of
particular interest to us; here we walk through the parallel primitives 
available to the languages and compare them.</p>


<h3 id="remote-function-execution">Remote function execution</h3>

<p>Both Julia and Chapel make it easy to explicitly launch tasks on other 
processors:</p>


<table style="border: 1px solid black;">
<tbody>
<tr><td><strong>Julia</strong></td>
<td>

<figure class="highlight"><pre><code class="language-julia"><span class="nd">@everywhere</span> <span class="k">function</span><span class="nf"> whoami</span><span class="x">()</span>
    <span class="n">println</span><span class="x">(</span><span class="n">myid</span><span class="x">(),</span> <span class="n">gethostname</span><span class="x">())</span>
<span class="k">end</span>

<span class="n">remotecall_fetch</span><span class="x">(</span><span class="n">whoami</span><span class="x">,</span> <span class="mi">2</span><span class="x">)</span>
<span class="n">remotecall_fetch</span><span class="x">(</span><span class="n">whoami</span><span class="x">,</span> <span class="mi">4</span><span class="x">)</span></code></pre></figure>

</td></tr>
<tr><td><strong>Chapel</strong></td>
<td>

<figure class="highlight"><pre><code class="language-c"><span class="n">proc</span> <span class="nf">main</span><span class="p">()</span> <span class="p">{</span>
  <span class="k">const</span> <span class="n">numTasks</span> <span class="o">=</span> <span class="n">here</span><span class="p">.</span><span class="n">numPUs</span><span class="p">();</span>
  <span class="k">for</span> <span class="n">taskid</span> <span class="n">in</span> <span class="mi">0</span><span class="p">..</span><span class="err">#</span><span class="n">numTasks</span> <span class="p">{</span>
      <span class="n">begin</span> <span class="p">{</span>
          <span class="n">writeln</span><span class="p">(</span><span class="n">here</span><span class="p">.</span><span class="n">id</span><span class="p">,</span> <span class="s">" "</span><span class="p">,</span> <span class="n">here</span><span class="p">.</span><span class="n">name</span><span class="p">,</span> <span class="s">" "</span><span class="p">,</span> <span class="n">taskid</span><span class="p">);</span>
      <span class="p">}</span>
  <span class="p">}</span>

  <span class="n">coforall</span> <span class="n">loc</span> <span class="n">in</span> <span class="n">Locales</span> <span class="p">{</span>
    <span class="n">on</span> <span class="n">loc</span> <span class="p">{</span>
      <span class="n">writeln</span><span class="p">(</span><span class="n">loc</span><span class="p">.</span><span class="n">id</span><span class="p">,</span> <span class="s">" "</span><span class="p">,</span> <span class="n">loc</span><span class="p">.</span><span class="n">name</span><span class="p">);</span>
    <span class="p">}</span>
  <span class="p">}</span>
<span class="p">}</span></code></pre></figure>

</td></tr>
</tbody>
</table>

<p>In Julia, starting julia with <code>juila -p 4</code> will launch julia with
4 worker tasks (and one coordinator task) on the local host; a <code>--machinefile</code>
option can be set to launch the tasks on remote hosts (over ssh,
by default, although other “ClusterManager”s are available, for
instance launching tasks on SGE clusters).  In Chapel, launching a
chapel program with <code>-nl 4</code> will run a program distributed over 4
locales, with options for those hosts set by environment variables.
Within each locale, Chapel will by default run across as many threads as
sensible (as determined by the extremely useful
<a href="https://www.open-mpi.org/projects/hwloc/">hwloc</a> library).</p>


<p>As seen above, Chapel distinuishes between starting up local and 
remote tasks; this is intrinsic to its “multiresolution” approach
to parallelism, so that it can take advantage of within-NUMA-node,
across-NUMA-node, and across-the-network parallism in different
ways.</p>


<h3 id="futures-atomics-and-synchronization">Futures, atomics and synchronization</h3>

<p>Once one can have tasks running asynchronously, synchronization
becomes an issue.  Julia and Chapel both have “futures” for 
asynchronous (non-blocking) function calls; futures can be
tested on, waited on or fetched from, with a fetch generally
blocking until the future has been “filled”.  Futures can only
be filled once.</p>


<p>In fact, in the above, Julia’s <code>remotecall_fetch</code> performs
the remote call and then fetches, mimicing a blocking call; the
<code>begin</code> blocks in Chapel do not block.</p>


<p>Futures work the following way in Julia and Chapel:</p>


<table style="border: 1px solid black;">
<tbody>
<tr><td><strong>Julia</strong></td>
<td>

<figure class="highlight"><pre><code class="language-julia"><span class="n">A</span> <span class="o">=</span> <span class="nd">@async</span> <span class="mi">2</span><span class="o">*</span><span class="mi">42</span>

<span class="n">println</span><span class="x">(</span><span class="n">fetch</span><span class="x">(</span><span class="n">A</span><span class="x">))</span></code></pre></figure>

</td></tr>
<tr><td><strong>Chapel</strong></td>
<td>

<figure class="highlight"><pre><code class="language-c"><span class="n">use</span> <span class="n">Futures</span><span class="p">;</span>
<span class="n">config</span> <span class="k">const</span> <span class="n">X</span> <span class="o">=</span> <span class="mi">42</span><span class="p">;</span>

<span class="k">const</span> <span class="n">A</span> <span class="o">=</span> <span class="n">async</span><span class="p">(</span><span class="n">lambda</span><span class="p">(</span><span class="n">x</span><span class="o">:</span> <span class="kt">int</span><span class="p">)</span> <span class="p">{</span> <span class="k">return</span> <span class="mi">2</span> <span class="o">*</span> <span class="n">x</span><span class="p">;</span> <span class="p">},</span> <span class="n">X</span><span class="p">);</span>

<span class="n">writeln</span><span class="p">(</span><span class="n">A</span><span class="p">.</span><span class="n">get</span><span class="p">());</span></code></pre></figure>

</td></tr>
</tbody>
</table>

<p>Both Julia and Chapel have thread-safe atomic primitive
variables, and <code>sync</code> blocks for joining tasks launched
within them before proceeding.</p>


<h3 id="parallel-loops-reductions-and-maps">Parallel loops, reductions, and maps</h3>

<p>Both languages make parallel looping, and reduction
over those parallel loops straightforward:</p>


<table style="border: 1px solid black;">
<tbody>
<tr><td><strong>Julia</strong></td>
<td>

<figure class="highlight"><pre><code class="language-julia"><span class="c"># parallel loop</span>
<span class="nd">@parallel</span> <span class="k">for</span> <span class="n">i</span><span class="o">=</span><span class="mi">1</span><span class="o">:</span><span class="mi">10000</span>
  <span class="n">a</span><span class="x">[</span><span class="n">i</span><span class="x">]</span> <span class="o">=</span> <span class="n">b</span><span class="x">[</span><span class="n">i</span><span class="x">]</span> <span class="o">+</span> <span class="n">alpha</span><span class="o">*</span><span class="n">c</span><span class="x">[</span><span class="n">i</span><span class="x">]</span>
<span class="k">end</span>

<span class="c"># parallel reduction</span>
<span class="n">asum</span> <span class="o">=</span> <span class="nd">@parallel</span> <span class="x">(</span><span class="o">+</span><span class="x">)</span> <span class="k">for</span> <span class="n">i</span><span class="o">=</span><span class="mi">1</span><span class="o">:</span><span class="mi">10000</span>
  <span class="n">a</span><span class="x">[</span><span class="n">i</span><span class="x">]</span>
<span class="k">end</span>

<span class="k">function</span><span class="nf"> twox</span><span class="x">(</span><span class="n">x</span><span class="x">)</span>
    <span class="mi">2</span><span class="n">x</span>
<span class="k">end</span>

<span class="n">pmap</span><span class="x">(</span><span class="n">twox</span><span class="x">,</span> <span class="n">a</span><span class="x">)</span></code></pre></figure>

</td></tr>
<tr><td><strong>Chapel</strong></td>
<td>

<figure class="highlight"><pre><code class="language-c"><span class="n">forall</span> <span class="n">i</span> <span class="n">in</span> <span class="mi">1</span><span class="p">..</span><span class="mi">10000</span> <span class="p">{</span>
    <span class="n">a</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">=</span> <span class="n">b</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">+</span> <span class="n">alpha</span><span class="o">*</span><span class="n">c</span><span class="p">[</span><span class="n">i</span><span class="p">]</span>
<span class="p">}</span>

<span class="n">var</span> <span class="n">asum</span> <span class="o">=</span> <span class="o">+</span> <span class="n">reduce</span> <span class="n">a</span>

<span class="n">b</span> <span class="o">=</span> <span class="mi">2</span><span class="o">*</span><span class="n">a</span><span class="p">;</span></code></pre></figure>

</td></tr>
</tbody>
</table>

<h3 id="threading">Threading</h3>

<p>In Chapel, parallel for loops are automatically assigned hierarchically
according to what the runtime knows about the architecture; threading is
used on-node if multiple cores are available.  Threading is an
<a href="https://docs.julialang.org/en/stable/manual/parallel-computing/#multi-threading-experimental">experimental feature</a> 
in Julia, not quite ready to use for production work yet.</p>


<h3 id="distributed-data">Distributed data</h3>

<p>Julia has a
<a href="https://github.com/JuliaParallel/DistributedArrays.jl">DistributedArrays</a>
package which are sort of half-PGAS arrays: they can be read from
at any index, but only the local part can be written to.  Chapel
is built around its PGAS distributions and iterators atop them.</p>


<p>Julia’s DistributedArrays are known not to perform particularly well,
and have been taken out of the base language since 0.4.  They have
been worked on since in preparation for the 0.6 release; however,
the main branch does not appear to be working with 0.6-rc2, or
at least I couldn’t get it working.  This section then mostly covers the
previous version of DistributedArrays.</p>


<p>Accessing remote values over DistributedArrays is quite slow.  As
such, DistributedArrays performs quite badly for the sort of thing
one might want to use Chapel distributed arrays for; they’re really
more for Monte-Carlo or other mostly-embarrasingly-parallel
calculations, where read access is only needed at the end of the
comptuation or a small number of other times.  Programming for a
stencil-type case or other iterative non-local computations is also
a little awkard; currently one has to remotely spawn tasks where
on the remote array fragments repeatedly to usher along each element
of the computation.  The new version of the arrays will have a
<code>simd()</code> function which makes doing that nicer;  it also allows for
MPI-style communications, which seems like it is faster than accessing
the data through the distributed array, but for use cases where
that is handy, it’s not clear what one would use the distributed
array for rather than just having each task have its own local
array.</p>


<p>However, for largely local computation (such as coordinator-worker type
operations), the distributed arrays work well.  Here
we have a STREAM calculation:</p>


<table style="border: 1px solid black;">
<tbody>
<tr><td><strong>Julia</strong></td>
<td>

<figure class="highlight"><pre><code class="language-julia"><span class="k">using</span> <span class="n">DistributedArrays</span>
<span class="nd">@everywhere</span> <span class="n">importall</span> <span class="n">DistributedArrays</span>

<span class="nd">@everywhere</span> <span class="k">function</span><span class="nf"> dostreamcalc</span><span class="x">(</span><span class="n">alpha</span><span class="x">,</span> <span class="n">bval</span><span class="x">,</span> <span class="n">cval</span><span class="x">,</span> <span class="n">A</span><span class="x">,</span> <span class="n">B</span><span class="x">,</span> <span class="n">C</span><span class="x">)</span>
    <span class="k">for</span> <span class="n">i</span> <span class="k">in</span> <span class="mi">1</span><span class="o">:</span><span class="n">length</span><span class="x">(</span><span class="n">localindexes</span><span class="x">(</span><span class="n">B</span><span class="x">)[</span><span class="mi">1</span><span class="x">])</span>
        <span class="n">localpart</span><span class="x">(</span><span class="n">B</span><span class="x">)[</span><span class="n">i</span><span class="x">]</span> <span class="o">=</span> <span class="n">bval</span>
    <span class="k">end</span>
    <span class="k">for</span> <span class="n">i</span> <span class="k">in</span> <span class="mi">1</span><span class="o">:</span><span class="n">length</span><span class="x">(</span><span class="n">localindexes</span><span class="x">(</span><span class="n">C</span><span class="x">)[</span><span class="mi">1</span><span class="x">])</span>
        <span class="n">localpart</span><span class="x">(</span><span class="n">C</span><span class="x">)[</span><span class="n">i</span><span class="x">]</span> <span class="o">=</span> <span class="n">cval</span>
    <span class="k">end</span>

    <span class="k">for</span> <span class="n">i</span> <span class="k">in</span> <span class="mi">1</span><span class="o">:</span><span class="n">length</span><span class="x">(</span><span class="n">localindexes</span><span class="x">(</span><span class="n">A</span><span class="x">)[</span><span class="mi">1</span><span class="x">])</span>
        <span class="n">localpart</span><span class="x">(</span><span class="n">A</span><span class="x">)[</span><span class="n">i</span><span class="x">]</span> <span class="o">=</span> <span class="n">localpart</span><span class="x">(</span><span class="n">B</span><span class="x">)[</span><span class="n">i</span><span class="x">]</span> <span class="o">+</span> <span class="n">alpha</span><span class="o">*</span><span class="n">localpart</span><span class="x">(</span><span class="n">C</span><span class="x">)[</span><span class="n">i</span><span class="x">]</span>
    <span class="k">end</span>
<span class="k">end</span>

<span class="c">#...</span>

<span class="n">A</span> <span class="o">=</span> <span class="n">dzeros</span><span class="x">(</span><span class="n">problem_size</span><span class="x">)</span>
<span class="n">B</span> <span class="o">=</span> <span class="n">copy</span><span class="x">(</span><span class="n">A</span><span class="x">)</span>
<span class="n">C</span> <span class="o">=</span> <span class="n">copy</span><span class="x">(</span><span class="n">A</span><span class="x">)</span>

<span class="n">ps</span> <span class="o">=</span> <span class="n">procs</span><span class="x">(</span><span class="n">A</span><span class="x">)</span>
<span class="n">refs</span> <span class="o">=</span> <span class="x">[(</span><span class="nd">@spawnat</span> <span class="n">p</span> <span class="n">dostreamcalc</span><span class="x">(</span><span class="n">alpha</span><span class="x">,</span> <span class="n">bval</span><span class="x">,</span> <span class="n">cval</span><span class="x">,</span> <span class="n">A</span><span class="x">,</span> <span class="n">B</span><span class="x">,</span> <span class="n">C</span><span class="x">))</span> <span class="k">for</span> <span class="n">p</span> <span class="k">in</span> <span class="n">ps</span><span class="x">]</span>
<span class="n">pmap</span><span class="x">(</span><span class="n">fetch</span><span class="x">,</span> <span class="n">refs</span><span class="x">)</span>
<span class="c"># ...</span></code></pre></figure>

</td></tr>
<tr><td><strong>Chapel</strong></td>
<td>

<figure class="highlight"><pre><code class="language-c"><span class="c1">// ...</span>
  <span class="k">const</span> <span class="n">ProblemSpace</span><span class="o">:</span> <span class="n">domain</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span> <span class="n">dmapped</span> <span class="n">Block</span><span class="p">(</span><span class="n">boundingBox</span><span class="o">=</span><span class="p">{</span><span class="mi">1</span><span class="p">..</span><span class="n">problem_size</span><span class="p">})</span> <span class="o">=</span> <span class="p">{</span><span class="mi">1</span><span class="p">..</span><span class="n">problem_size</span><span class="p">};</span>

  <span class="n">var</span> <span class="n">A</span><span class="p">,</span> <span class="n">B</span><span class="p">,</span> <span class="n">C</span><span class="o">:</span> <span class="p">[</span><span class="n">ProblemSpace</span><span class="p">]</span> <span class="n">real</span><span class="p">;</span>

  <span class="n">A</span> <span class="o">=</span> <span class="mi">0</span><span class="p">.</span><span class="mi">0</span><span class="p">;</span>
  <span class="n">B</span> <span class="o">=</span> <span class="n">bval</span><span class="p">;</span>
  <span class="n">C</span> <span class="o">=</span> <span class="n">cval</span><span class="p">;</span>

  <span class="n">forall</span> <span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">c</span><span class="p">)</span> <span class="n">in</span> <span class="n">zip</span><span class="p">(</span><span class="n">A</span><span class="p">,</span> <span class="n">B</span><span class="p">,</span> <span class="n">C</span><span class="p">)</span> <span class="k">do</span>
     <span class="n">a</span> <span class="o">=</span> <span class="n">b</span> <span class="o">+</span> <span class="n">alpha</span> <span class="o">*</span> <span class="n">c</span><span class="p">;</span>

<span class="c1">// ...</span></code></pre></figure>

</td></tr>
</tbody>
</table>

<h3 id="communications">Communications</h3>

<p>Julia has explicit support for <a href="https://en.wikipedia.org/wiki/Communicating_sequential_processes">CSP-style</a>
channels, like <code>go</code>, which are something like a cross between queues and futures; they can keep being written to from multiple
tasks:</p>


<figure class="highlight"><pre><code class="language-julia"><span class="nd">@everywhere</span> <span class="k">function</span><span class="nf"> putmsg</span><span class="x">(</span><span class="n">pid</span><span class="x">)</span>
    <span class="n">mypid</span> <span class="o">=</span> <span class="n">myid</span><span class="x">()</span>
    <span class="n">msg</span> <span class="o">=</span> <span class="s">"Hi from </span><span class="si">$</span><span class="s">mypid"</span>
    <span class="n">rr</span> <span class="o">=</span> <span class="kt">RemoteChannel</span><span class="x">(</span><span class="n">pid</span><span class="x">)</span>
    <span class="n">put!</span><span class="x">(</span><span class="n">rr</span><span class="x">,</span> <span class="n">msg</span><span class="x">)</span>
    <span class="n">println</span><span class="x">(</span><span class="n">myid</span><span class="x">(),</span> <span class="s">" sent "</span><span class="x">,</span> <span class="n">msg</span><span class="x">,</span> <span class="s">" to "</span><span class="x">,</span> <span class="n">pid</span><span class="x">)</span>
    <span class="k">return</span> <span class="n">rr</span>
<span class="k">end</span>

<span class="nd">@everywhere</span> <span class="k">function</span><span class="nf"> getmsg</span><span class="x">(</span><span class="n">rr</span><span class="x">)</span>
    <span class="n">msg</span>  <span class="o">=</span> <span class="n">fetch</span><span class="x">(</span><span class="n">rr</span><span class="x">)</span>
    <span class="n">println</span><span class="x">(</span><span class="n">myid</span><span class="x">(),</span> <span class="s">" got: "</span><span class="x">,</span> <span class="n">msg</span><span class="x">)</span>
<span class="k">end</span>

<span class="n">rr</span> <span class="o">=</span> <span class="n">remotecall_fetch</span><span class="x">(</span><span class="n">putmsg</span><span class="x">,</span> <span class="mi">2</span><span class="x">,</span> <span class="mi">3</span><span class="x">)</span>
<span class="n">remotecall_wait</span><span class="x">(</span><span class="n">getmsg</span><span class="x">,</span> <span class="mi">3</span><span class="x">,</span> <span class="n">rr</span><span class="x">)</span></code></pre></figure>

<p>Chapel, by contrast, doesn’t expose these methods; communications
is done implicitly through remote data access or remote code
invocation.</p>


<h2 id="a-2d-advection-problem">A 2d advection problem</h2>

<p>Having seen the parallel computing tools available in each language,
we try here a simple distributed computation.  Here we try Julia,
Chapel, and Python using <a href="http://dask.pydata.org/en/latest/">Dask</a>
on a simple distributed-memory stencil problem, two dimensional
upwinded advection.  A Gaussian blob is advected by a constant
velocity field; shown below is the initial condition, the blob moved
slightly after a few timesteps, and the difference.</p>


<p><img alt="2D Advection Plot" src="https://www.dursi.ca/assets/julia_v_chapel/twod_advection.png" /></p>


<p>We do this in Julia using DistributedArrays, in Chapel using Stencil-distributed
arrays, and in Python using Dask arrays.  The relevant code snippets follow below.</p>


<table style="border: 1px solid black;">
<tbody>
<tr><td><strong>Julia</strong></td>
<td>

<figure class="highlight"><pre><code class="language-julia"><span class="nd">@everywhere</span> <span class="k">function</span><span class="nf"> get_data_plus_gc</span><span class="x">(</span><span class="n">domain</span><span class="x">,</span> <span class="n">nguard</span><span class="x">,</span> <span class="n">ngrid</span><span class="x">)</span>
    <span class="k">if</span> <span class="n">myid</span><span class="x">()</span> <span class="k">in</span> <span class="n">procs</span><span class="x">(</span><span class="n">domain</span><span class="x">)</span>
        <span class="n">li</span> <span class="o">=</span> <span class="n">localindexes</span><span class="x">(</span><span class="n">domain</span><span class="x">)</span>
        <span class="n">lp</span> <span class="o">=</span> <span class="n">localpart</span><span class="x">(</span><span class="n">domain</span><span class="x">)</span>

        <span class="n">s</span> <span class="o">=</span> <span class="n">size</span><span class="x">(</span><span class="n">lp</span><span class="x">)</span>
        <span class="n">data_plus_gc</span> <span class="o">=</span> <span class="n">zeros</span><span class="x">(</span><span class="n">s</span><span class="x">[</span><span class="mi">1</span><span class="x">]</span><span class="o">+</span><span class="mi">2</span><span class="o">*</span><span class="n">nguard</span><span class="x">,</span> <span class="n">s</span><span class="x">[</span><span class="mi">2</span><span class="x">]</span><span class="o">+</span><span class="mi">2</span><span class="o">*</span><span class="n">nguard</span><span class="x">)</span>
        <span class="k">for</span> <span class="n">j</span> <span class="k">in</span> <span class="mi">1</span><span class="o">:</span><span class="n">s</span><span class="x">[</span><span class="mi">2</span><span class="x">]</span>
            <span class="k">for</span> <span class="n">i</span> <span class="k">in</span> <span class="mi">1</span><span class="o">:</span><span class="n">s</span><span class="x">[</span><span class="mi">1</span><span class="x">]</span>
                <span class="n">data_plus_gc</span><span class="x">[</span><span class="n">i</span><span class="o">+</span><span class="n">nguard</span><span class="x">,</span> <span class="n">j</span><span class="o">+</span><span class="n">nguard</span><span class="x">]</span> <span class="o">=</span> <span class="n">lp</span><span class="x">[</span><span class="n">i</span><span class="x">,</span><span class="n">j</span><span class="x">]</span>
            <span class="k">end</span>
        <span class="k">end</span>

        <span class="n">xstart</span> <span class="o">=</span> <span class="n">li</span><span class="x">[</span><span class="mi">1</span><span class="x">][</span><span class="mi">1</span><span class="x">]</span>
        <span class="n">xend</span>   <span class="o">=</span> <span class="n">li</span><span class="x">[</span><span class="mi">1</span><span class="x">][</span><span class="k">end</span><span class="x">]</span>
        <span class="n">ystart</span> <span class="o">=</span> <span class="n">li</span><span class="x">[</span><span class="mi">2</span><span class="x">][</span><span class="mi">1</span><span class="x">]</span>
        <span class="n">yend</span>   <span class="o">=</span> <span class="n">li</span><span class="x">[</span><span class="mi">2</span><span class="x">][</span><span class="k">end</span><span class="x">]</span>

        <span class="k">for</span> <span class="n">g</span> <span class="k">in</span> <span class="mi">1</span><span class="o">:</span><span class="n">nguard</span>
            <span class="n">xsg</span> <span class="o">=</span> <span class="x">(</span><span class="n">xstart</span><span class="o">-</span><span class="mi">1</span><span class="o">-</span><span class="n">g</span> <span class="o">+</span> <span class="n">ngrid</span><span class="x">)</span> <span class="o">%</span> <span class="n">ngrid</span> <span class="o">+</span> <span class="mi">1</span>
            <span class="n">xeg</span> <span class="o">=</span> <span class="x">(</span><span class="n">xend</span><span class="o">-</span><span class="mi">1</span><span class="o">+</span><span class="n">g</span><span class="x">)</span> <span class="o">%</span> <span class="n">ngrid</span> <span class="o">+</span> <span class="mi">1</span>

            <span class="k">for</span> <span class="n">j</span> <span class="k">in</span> <span class="mi">1</span><span class="o">+</span><span class="n">nguard</span><span class="o">:</span><span class="n">s</span><span class="x">[</span><span class="mi">2</span><span class="x">]</span><span class="o">+</span><span class="n">nguard</span>
                <span class="n">data_plus_gc</span><span class="x">[</span><span class="n">nguard</span><span class="o">+</span><span class="mi">1</span><span class="o">-</span><span class="n">g</span><span class="x">,</span> <span class="n">j</span><span class="x">]</span> <span class="o">=</span> <span class="n">domain</span><span class="x">[</span><span class="n">xsg</span><span class="x">,</span> <span class="n">j</span><span class="o">-</span><span class="n">nguard</span><span class="o">+</span><span class="n">ystart</span><span class="o">-</span><span class="mi">1</span><span class="x">]</span>
                <span class="n">data_plus_gc</span><span class="x">[</span><span class="n">s</span><span class="x">[</span><span class="mi">1</span><span class="x">]</span><span class="o">+</span><span class="n">nguard</span><span class="o">+</span><span class="n">g</span><span class="x">,</span> <span class="n">j</span><span class="x">]</span> <span class="o">=</span> <span class="n">domain</span><span class="x">[</span><span class="n">xeg</span><span class="x">,</span> <span class="n">j</span><span class="o">-</span><span class="n">nguard</span><span class="o">+</span><span class="n">ystart</span><span class="o">-</span><span class="mi">1</span><span class="x">]</span>
            <span class="k">end</span>

            <span class="c">#...</span>
        <span class="k">end</span>
    <span class="k">end</span>
    <span class="k">return</span> <span class="n">data_plus_gc</span>
<span class="k">end</span>

<span class="nd">@everywhere</span> <span class="k">function</span><span class="nf"> advect_data</span><span class="x">(</span><span class="n">dens</span><span class="x">,</span> <span class="n">nguard</span><span class="x">,</span> <span class="n">ngrid</span><span class="x">,</span> <span class="n">velx</span><span class="x">,</span> <span class="n">vely</span><span class="x">,</span> <span class="n">dx</span><span class="x">,</span> <span class="n">dy</span><span class="x">,</span> <span class="n">dt</span><span class="x">)</span>
    <span class="n">locdens</span> <span class="o">=</span> <span class="n">get_data_plus_gc</span><span class="x">(</span><span class="n">dens</span><span class="x">,</span> <span class="n">nguard</span><span class="x">,</span> <span class="n">ngrid</span><span class="x">)</span>

    <span class="c">#...calculate gradients on locdens</span>

    <span class="k">for</span> <span class="n">j</span> <span class="k">in</span> <span class="mi">1</span><span class="o">+</span><span class="n">nguard</span><span class="o">:</span><span class="n">ny</span><span class="o">+</span><span class="n">nguard</span>
        <span class="k">for</span> <span class="n">i</span> <span class="k">in</span> <span class="mi">1</span><span class="o">+</span><span class="n">nguard</span><span class="o">:</span><span class="n">nx</span><span class="o">+</span><span class="n">nguard</span>
            <span class="n">localpart</span><span class="x">(</span><span class="n">dens</span><span class="x">)[</span><span class="n">i</span><span class="o">-</span><span class="n">nguard</span><span class="x">,</span> <span class="n">j</span><span class="o">-</span><span class="n">nguard</span><span class="x">]</span> <span class="o">-=</span> <span class="n">dt</span><span class="o">*</span><span class="x">(</span><span class="n">velx</span><span class="o">*</span><span class="n">gradx</span><span class="x">[</span><span class="n">i</span><span class="x">,</span><span class="n">j</span><span class="x">]</span> <span class="o">+</span> <span class="n">vely</span><span class="o">*</span><span class="n">grady</span><span class="x">[</span><span class="n">i</span><span class="x">,</span><span class="n">j</span><span class="x">])</span>
        <span class="k">end</span>
    <span class="k">end</span>
<span class="k">end</span>

<span class="c">#...</span>

<span class="k">function</span><span class="nf"> timestep</span><span class="x">(</span><span class="n">dens</span><span class="x">,</span> <span class="n">nguard</span><span class="x">,</span> <span class="n">ngrid</span><span class="x">,</span> <span class="n">velx</span><span class="x">,</span> <span class="n">vely</span><span class="x">,</span> <span class="n">dx</span><span class="x">,</span> <span class="n">dy</span><span class="x">,</span> <span class="n">dt</span><span class="x">)</span>
    <span class="n">ps</span> <span class="o">=</span> <span class="n">procs</span><span class="x">(</span><span class="n">dens</span><span class="x">)</span>
    <span class="n">refs</span> <span class="o">=</span> <span class="x">[(</span><span class="nd">@spawnat</span> <span class="n">p</span> <span class="n">advect_data</span><span class="x">(</span><span class="n">dens</span><span class="x">,</span> <span class="n">nguard</span><span class="x">,</span> <span class="n">ngrid</span><span class="x">,</span> <span class="n">velx</span><span class="x">,</span> <span class="n">vely</span><span class="x">,</span> <span class="n">dx</span><span class="x">,</span> <span class="n">dy</span><span class="x">,</span> <span class="n">dt</span><span class="x">))</span> <span class="k">for</span> <span class="n">p</span> <span class="k">in</span> <span class="n">ps</span><span class="x">]</span>
    <span class="n">pmap</span><span class="x">(</span><span class="n">fetch</span><span class="x">,</span> <span class="n">refs</span><span class="x">)</span>
<span class="k">end</span>

<span class="c">#...</span></code></pre></figure>

</td></tr>
<tr><td><strong>Chapel</strong></td>
<td>

<figure class="highlight"><pre><code class="language-c"><span class="c1">//...</span>

  <span class="k">const</span> <span class="n">ProblemSpace</span> <span class="o">=</span> <span class="p">{</span><span class="mi">1</span><span class="p">..</span><span class="n">ngrid</span><span class="p">,</span> <span class="mi">1</span><span class="p">..</span><span class="n">ngrid</span><span class="p">},</span>
        <span class="n">ProblemDomain</span> <span class="o">:</span> <span class="n">domain</span><span class="p">(</span><span class="mi">2</span><span class="p">)</span> <span class="n">dmapped</span> <span class="n">Stencil</span><span class="p">(</span><span class="n">boundingBox</span><span class="o">=</span><span class="n">ProblemSpace</span><span class="p">,</span> <span class="n">fluff</span><span class="o">=</span><span class="p">(</span><span class="n">nguard</span><span class="p">,</span><span class="n">nguard</span><span class="p">),</span> <span class="n">periodic</span><span class="o">=</span><span class="nb">true</span><span class="p">)</span> <span class="o">=</span> <span class="n">ProblemSpace</span><span class="p">;</span>

  <span class="c1">//...</span>
  <span class="n">var</span> <span class="n">dens</span><span class="o">:</span> <span class="p">[</span><span class="n">ProblemDomain</span><span class="p">]</span> <span class="n">real</span> <span class="o">=</span> <span class="mi">0</span><span class="p">.</span><span class="mi">0</span><span class="p">;</span>

  <span class="c1">// density a gaussian of width sigma centred on (initialposx, initialposy)</span>
  <span class="n">forall</span> <span class="n">ij</span> <span class="n">in</span> <span class="n">ProblemSpace</span> <span class="p">{</span>
    <span class="n">var</span> <span class="n">x</span> <span class="o">=</span> <span class="p">(</span><span class="n">ij</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span><span class="o">-</span><span class="mi">1</span><span class="p">.</span><span class="mi">0</span><span class="p">)</span><span class="o">/</span><span class="n">ngrid</span><span class="p">;</span>
    <span class="n">var</span> <span class="n">y</span> <span class="o">=</span> <span class="p">(</span><span class="n">ij</span><span class="p">(</span><span class="mi">2</span><span class="p">)</span><span class="o">-</span><span class="mi">1</span><span class="p">.</span><span class="mi">0</span><span class="p">)</span><span class="o">/</span><span class="n">ngrid</span><span class="p">;</span>
    <span class="n">dens</span><span class="p">(</span><span class="n">ij</span><span class="p">)</span> <span class="o">=</span> <span class="n">exp</span><span class="p">(</span><span class="o">-</span><span class="p">((</span><span class="n">x</span><span class="o">-</span><span class="n">initialposx</span><span class="p">)</span><span class="o">**</span><span class="mi">2</span> <span class="o">+</span> <span class="p">(</span><span class="n">y</span><span class="o">-</span><span class="n">initialposy</span><span class="p">)</span><span class="o">**</span><span class="mi">2</span><span class="p">)</span><span class="o">/</span><span class="p">(</span><span class="n">sigma</span><span class="o">**</span><span class="mi">2</span><span class="p">));</span>
  <span class="p">}</span>

  <span class="k">for</span> <span class="n">iteration</span> <span class="n">in</span> <span class="mi">1</span><span class="p">..</span><span class="n">ntimesteps</span>  <span class="p">{</span>
    <span class="c1">// update the boundary conditions - periodic</span>
    <span class="n">dens</span><span class="p">.</span><span class="n">updateFluff</span><span class="p">();</span>

    <span class="c1">// calculate the upwinded gradient</span>
    <span class="c1">// ...</span>

    <span class="n">dens</span> <span class="o">=</span> <span class="n">dens</span> <span class="o">-</span> <span class="n">dt</span><span class="o">*</span><span class="p">(</span><span class="n">velx</span><span class="o">*</span><span class="n">gradx</span> <span class="o">+</span> <span class="n">vely</span><span class="o">*</span><span class="n">grady</span><span class="p">);</span>
<span class="c1">//...</span>
<span class="p">}</span></code></pre></figure>

</td></tr>
<tr><td><strong>Python + Dask</strong></td>
<td>

<figure class="highlight"><pre><code class="language-python"><span class="c1">#...
</span>
<span class="k">def</span> <span class="nf">dask_step</span><span class="p">(</span><span class="n">subdomain</span><span class="p">,</span> <span class="n">nguard</span><span class="p">,</span> <span class="n">dx</span><span class="p">,</span> <span class="n">dy</span><span class="p">,</span> <span class="n">dt</span><span class="p">,</span> <span class="n">u</span><span class="p">):</span>
    <span class="s">"""
    map_overlap applies a function to a subdomain of a dask array,
    filling the guardcells in first
    """</span>
    <span class="k">return</span> <span class="n">subdomain</span><span class="p">.</span><span class="n">map_overlap</span><span class="p">(</span><span class="n">advect</span><span class="p">,</span> <span class="n">depth</span><span class="o">=</span><span class="n">nguard</span><span class="p">,</span> <span class="n">boundary</span><span class="o">=</span><span class="s">'periodic'</span><span class="p">,</span>
                                 <span class="n">dx</span><span class="o">=</span><span class="n">dx</span><span class="p">,</span> <span class="n">dy</span><span class="o">=</span><span class="n">dy</span><span class="p">,</span> <span class="n">dt</span><span class="o">=</span><span class="n">dt</span><span class="p">,</span> <span class="n">u</span><span class="o">=</span><span class="n">u</span><span class="p">)</span>


<span class="k">def</span> <span class="nf">initial_conditions</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y</span><span class="p">,</span> <span class="n">initial_posx</span><span class="o">=</span><span class="mf">0.3</span><span class="p">,</span> <span class="n">initial_posy</span><span class="o">=</span><span class="mf">0.3</span><span class="p">,</span> <span class="n">sigma</span><span class="o">=</span><span class="mf">0.15</span><span class="p">):</span>
    <span class="n">xx</span><span class="p">,</span> <span class="n">yy</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">meshgrid</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y</span><span class="p">)</span>
    <span class="n">density</span> <span class="o">=</span> <span class="n">np</span><span class="p">.</span><span class="n">exp</span><span class="p">(</span><span class="o">-</span><span class="p">((</span><span class="n">xx</span><span class="o">-</span><span class="n">initial_posx</span><span class="p">)</span><span class="o">**</span><span class="mi">2</span> <span class="o">+</span> <span class="p">(</span><span class="n">yy</span><span class="o">-</span><span class="n">initial_posy</span><span class="p">)</span><span class="o">**</span><span class="mi">2</span><span class="p">)</span><span class="o">/</span><span class="p">(</span><span class="n">sigma</span><span class="o">**</span><span class="mi">2</span><span class="p">))</span>
    <span class="k">return</span> <span class="n">density</span>


<span class="k">if</span> <span class="n">__name__</span> <span class="o">==</span> <span class="s">"__main__"</span><span class="p">:</span>
    <span class="c1">#...
</span>
    <span class="n">dens</span> <span class="o">=</span> <span class="n">initial_conditions</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y</span><span class="p">)</span>
    <span class="n">subdomain_init</span> <span class="o">=</span> <span class="n">da</span><span class="p">.</span><span class="n">from_array</span><span class="p">(</span><span class="n">dens</span><span class="p">,</span> <span class="n">chunks</span><span class="o">=</span><span class="p">((</span><span class="n">npts</span><span class="o">+</span><span class="mi">1</span><span class="p">)</span><span class="o">//</span><span class="mi">2</span><span class="p">,</span> <span class="p">(</span><span class="n">npts</span><span class="o">+</span><span class="mi">1</span><span class="p">)</span><span class="o">//</span><span class="mi">2</span><span class="p">))</span>

    <span class="c1"># These create the steps, but they don't actually perform the execution...
</span>    <span class="n">subdomain</span> <span class="o">=</span> <span class="n">dask_step</span><span class="p">(</span><span class="n">subdomain_init</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="n">dx</span><span class="p">,</span> <span class="n">dy</span><span class="p">,</span> <span class="n">dt</span><span class="p">,</span> <span class="n">u</span><span class="p">)</span>
    <span class="k">for</span> <span class="n">step</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">nsteps</span><span class="p">):</span>
        <span class="n">subdomain</span> <span class="o">=</span> <span class="n">dask_step</span><span class="p">(</span><span class="n">subdomain</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="n">dx</span><span class="p">,</span> <span class="n">dy</span><span class="p">,</span> <span class="n">dt</span><span class="p">,</span> <span class="n">u</span><span class="p">)</span>

    <span class="c1"># _this_ performs the execution
</span>    <span class="n">start</span> <span class="o">=</span> <span class="n">time</span><span class="p">.</span><span class="n">clock</span><span class="p">()</span></code></pre></figure>

</td></tr>
</tbody>
</table>

<p>As with the stream benchmark, we see that the Julia DistributedArrays
require a lot of bookkeeping to use; both Chapel and Dask are much
more straightforward.</p>


<p>The one-node timings here aren’t even close.  By forcing Chapel to run
on each core separately, the performance isn’t that different than Julia.
But when informed that there is one “locale” and letting
it sort out the details, Chapel benefits dramatically from being
able to use multiple levels of parallelism, and with no extra work;
on a single 8-processor node, running a 1000x1000 grid with all cores
takes the following amount of time:</p>


<table style="border: 1px solid black; margin: 0 auto; border-collapse: collapse;">
<thead>
<th>Julia -p=1</th><th>Julia -p=8</th><th>Chapel -nl=1 ParTasksPerLocale=8</th><th>Chapel -nl=8 ParTasksPerLocale=1</th><th>Python</th>
</thead>
<tbody style="border: 1px solid black;">
<tr>
<td style="border: 1px solid black;">177s s</td>
<td style="border: 1px solid black;">264 s</td>
<td style="border: 1px solid black;"><b>0.4 s</b></td>
<td style="border: 1px solid black;">145 s</td>
<td style="border: 1px solid black;">193 s</td></tr>
</tbody>
</table>

<p>The 0.4s is not a typo. Threading matters.  Admittedly,
this is a bit of an extreme case, 1000x1000 isn’t a big
grid to distribute over 8 processes, so communications
overhead dominates; Julia seems to suffer that overhead even
with just one process.</p>


<p>Another interesting thing here is that Python+Numpy+Dask (numba didn’t
help here) is competitive even with Chapel <em>if</em> you force Chapel
to not use threading on-node, and either made it much easier to
write the program than Julia.</p>


<h2 id="strengths-weaknesses-and-future-prospects">Strengths, Weaknesses, and Future Prospects</h2>

<p>Both Julia and Chapel are perfectly useable today for problems that
fall within their current bailiwicks, at least for advanced users.
They are strong projects and interesting technologies.  In addition,
both have significant potential and “room to grow” beyond their
current capabilities; but both face challenges as well.</p>


<h3 id="julia-1">Julia</h3>

<p>Julia’s great flexibility - the metaprogramming and the type system
in particular - gives it a very real opportunity to become a platform
on which many domanin-specific language are written for particular scientific problems.
We see some of that potential in tools like <a href="https://github.com/JuliaDiffEq/DifferentialEquations.jl">DifferentialEquations.jl</a>,
where a simple, general API can nonetheless be used to provide efficient
solutions to problems that span a wide range of regimes and structures;
the <code>solve()</code> function and the problem definition language essentially
becomes a DSL for a wide range of differential equation problems.
And Julia’s interactive and dynamic nature makes it a natural for 
scientists noodling around on problems, performing numerical
experiments and looking at the results.  While large-scale computing
— in an HPC or Spark-style Big-data sense — is not a forte of
Julia’s right now, the basic pieces are there and it certainly could
be in the future.</p>


<p>Many of Julia’s disadvantages are inevitable flip sides of some of
those advantages.  Because of the dynamic nature of
the language and its reliance on JIT and type inference, it is
<a href="https://discourse.julialang.org/t/julia-static-compilation/296/27">still not
possible</a>
to fully compile a Julia script into a static executable, meaning
that there will be JIT pauses in initial iterations of running code;
too, the dynamic nature of the language relies on garbage collection,
which can cause either GC pauses (and thus jitter at scale) or
unexpected memory pressure throughout execution.  Similarly, the
fact that it’s so easy to contribute a package to the Julia package
ecosystem means that the package listing is littered with abandoned
and broken packages.</p>


<p>But some of the disadvantages seem more self-inflicted.  While the
language has been public and actively developed for <a href="https://julialang.org/blog/2012/02/why-we-created-julia">over five
years</a>,
the language is still at v0.6.  While any language will evolve over
time, the Julia community has spent the past five years contininually
re-litigating minor but foundational decisions of syntax and behaviour
in the interests of conceptual purity – v0.4 in late 2015 changed
the capitalization of unsigned integer types and radically changed
the dictionary syntax, while 0.5 in late 2016 dramatically (although
less dramatically than originally proposed after community pushback)
changed the behaviour of arrays (!!) in an event termed the
Arraypocolypse.  Discussions on the correct choice for string
concatenation operator span enormous and non-stop github issue
discussions from late 2012 to mid 2015.  At least one more round
of significant breaking changes are planned before a 1.0 release.
As a result, most non-trivial example code online simply doesn’t
work; thus also the accelerated bitrot of software in the Julia
package listing.  It has been difficult to implement new functionality
on top of base Julia; it’s hard to build powerful parallel computing
tools when one can’t even depend on the behavour of arrays.
I would have liked to use Intel’s ParallelAccelerator for Julia to
see how it worked on the advection problem above, for instance, but Julia 0.6
breaks the ParallelAccelerator, and Julia 0.6 is needed for the <code>@simd</code>
feature with DistributedArrays.</p>


<p>So Julia living up to its potential is not a given.  If I were on
Julia’s project team, things that would concern me would include:</p>


<dl>
  <dt><strong>Peak Julia?</strong></dt>
  <dd>Julia grew very quickly early on, but since then seems to have topped out;
for example, <a href="https://g.co/trends/qzmA9">flat google trends interest</a>,
and falling off the radar of “languages to watch” lists such as the
<a href="http://redmonk.com/sogrady/2017/03/17/language-rankings-1-17/">Redmonk language rankings</a>,
This may be unfair; these trends may say more about the large initial
surge of interest than stagnation or decline.  “A hugely popular
scientific programing language” almost seems like an oxymoron, after all.
<a href="https://insights.stackoverflow.com/trends?tags=julia-lang">Declining Stack Overflow</a> 
interest may simply reflect that the community has successfully moved discussion
to its <a href="https://discourse.julialang.org">discourse</a> site.
A five-year old language for numerical computing that still hasn’t
reached 1.0 but has popularity comparable to Rust (which started
at the same time but is a more general systems-programming language)
or Fortran (which has an enormous installed base) is pretty remarkable;
further growth may inevitably be more modest simply because of the
small number of scientific programmers out there.  Still, I think
one would want to see interest growing ahead of a 1.0 release,
rather than flat or declining.</dd>
  <dt><strong>Instability driving off users, developers</strong></dt>
  <dd>Very early on, community members who used Julia started building
what became <a href="http://juliastats.github.io">JuliaStats</a>, with R-like
data frames, data tables, random distributions, and a growing number
of statistics and machine-learning tools built atop.  This took
significant developer effort, as fundamental to statistical use
cases is “Not Available” or “NA” values, with semantics different
from the NaNs that we in the simulation computing community are so
frequently (if usually unintentionally) familar with.  Thus dataframes
and tables couldn’t simply be built directly on top of numerical
arrays of basic numerical types, but took some effort to build
efficient “nullable” types atop of.  But partly because of instability
in the underlying language, Julia DataFrames and DataArrays have
themselves been under flux, which is show-stopping to R users
considering Julia, and demoralizing to developers.  Many other similar
examples exist in other domains.  If it is true that there is
declining or stagnant interest in Julia, this would certainly be a
contributing factor.</dd>
  <dt><strong>The JIT often needs help, even for basic numerical computing tasks</strong></dt>
  <dd>Julia is designed around its JIT compiler, which enables some
of the language’s very cool features - the metaprogramming, the
dynamic nature of the language, the interactivity.  But the JIT
compiler often needs a lot of help to get reasonable performance,
such as use of the the <code>@inbounds</code> macro in the stencil calculation.
Writing numerical operations in the more readable
vectorized form (like for the stream example in Chapel, <code>C = A + B</code>
rather than looping over the indices) <a href="http://www.johnmyleswhite.com/notebook/2013/12/22/the-relationship-between-vectorized-and-devectorized-code/">has long been slow in Julia</a>,
although <a href="https://julialang.org/blog/2017/01/moredots">a new feature</a>
may have fixed that.  <a href="http://parallelacceleratorjl.readthedocs.io/en/latest/index.html">A third party package</a>
exists which helps many of the common cases (speeding up stencil
operations on rectangular arrays), which on one hand indicates the
power of Julia metaprogramming capabilities.  But on the other, one
might naturally think that fast numerical operations on arrays would
be something that the core language came with.  Part of the problem here
is that while the Julia ecosystem broadly has a very large number of
contributors, the core language internals (like the JIT itself) 
has only a handful, and complex issues like performance problems
can take a very long time to get solved.</dd>
  <dt><strong>The 800lb pythonic gorilla</strong></dt>
  <dd>Python is enormously popular in scientific and data-science type
applications, has huge installed base and number of packages, and
with <a href="http://www.numpy.org">numpy</a> and <a href="http://numba.pydata.org">numba</a>
can be quite fast.  The scientific computing community is now 
grudgingly starting to move to Python 3, and with Python 3.5+ 
supporting <a href="https://docs.python.org/3/library/typing.html">type annotations</a>,
I think there’d start to be a quite real concern that Python would get
Julia-fast (or close enough) before Julia got Python-big.  The fact
that some of Julia’s nicest features like notebook support and coolest new projects
like <a href="https://github.com/JuliaParallel/Dagger.jl">Dagger</a> rely on
or are ports of work originally done for Python (ipython notebook
and <a href="http://dask.pydata.org/en/latest/">Dask</a>) indicate the danger
if Python gets fast enough.</dd>
</dl>

<p>Of those four, only the middle two are completely under the Julia
team’s control; a v1.0 released soon, and with solemn oaths sworn
to have no more significant breaking changes until v2.0 would help
developers and users, and onboarding more people into core internals
development would help the underlying technology.</p>


<h3 id="chapel-1">Chapel</h3>

<p>If I were on the Chapel team, my concerns would be different:</p>


<dl>
  <dt><strong>Adoption</strong></dt>
  <dd>It’s hard to escape the fact that Chapel’s user base is very
small.  The good news is that Chapel’s niche, unlike Julia’s, has
no serious immediate competitor — I’d consider other productive
parallel scientific programming languages to be more research
projects than products — which gives it a bit more runway.  But
the niche itself is small, and Chapel’s modest adoption rate within
that niche needs to be addressed in the near future if the language
is to thrive.  The Chapel team is doing many of the right things
—  the package is easy to install (no small feat for a performant
parallel programming language); the compiler is getting faster and
producing faster code; there’s lots of examples, tutorials and
documentation available; and the community is extremely friendly
and welcoming — but it seems clear that users need to be given
more reason to start trying the language.</dd>
  <dt><strong>Small number of external contributors</strong></dt>
  <dd>Admittedly, this is related to the fact that the number of users
is small, but it’s also the case that contributing code is nontrivial
if you want to contribute it to the main project, and there’s no central
place where other people could look for your work if you wanted to have
it as an external package.  A package manager would be a real help, 
and it doesn’t have to be elaborate (especially in the initial version).</dd>
  <dt><strong>Not enough packages</strong></dt>
  <dd>In turn, this is caused by the small number of external contributors,
and helps keep the adoption low.  Chapel already has the fundamentals
to start building some really nice higher-level packages and solvers
that would make it easy to start writing some types of scientific
codes.  A distributed-memory n-dimensional FFT over one of its
domains; the beginnings of a Chapel-native set of solvers from
<a href="http://www.netlib.org/scalapack/">Scalapack</a> or
<a href="http://www.mcs.anl.gov/petsc/index.html">PETSc</a> (both of which are
notoriously hard to get started with, and in PETSc’s case, even
install); simple static-sized R-style dataframes with some analysis
routines; these are tools which would make it very easy to get
started writing some non-trivial scientific software in Chapel.</dd>
  <dt><strong>Too few domain maps and layouts</strong></dt>
  <dd>Being able to, in a few lines of code, write performant, threaded,
NUMA-aware, and distributed memory operations on statically-decomposed
rectangular multidimensional arrays, and have that code work on a
cluster or your desktop is amazing.  But many scientific problems
do not match neatly onto these domains.  Many require dynamically-sized
domains (block-adaptive meshes) or load balancing (tree codes,
dynamic hash tables); others may be static but not quite look like
CSR-sparse arrays.  Domain maps, layouts, and the parallel iterators
which loop over them are the “secret sauce” of Chapel, and can be
written in user code if the underlying capabilities they need are
supported, so they can be contributed externally, but there is little
documention/examples (compared to that on using existing domain maps) available.</dd>
</dl>

<p>The good news is that these items are all under the Chapel community’s
control.  Programs that are natural to write in Chapel currently are
easy to write and can perform quite well; the goal then is to expand
the space of those programs by leveraging early adopters into writing
packages.</p>


<h2 id="my-conclusions">My conclusions</h2>

<p>This is entitled “<em>My</em> conclusions” because my takeaways might reasonably be
different than yours.  Here’s my take.</p>


<h3 id="both-projects-are-strong-and-useable-right-now-at-different-things">Both projects are strong and useable, right now, at different things</h3>

<p>I’d have no qualms about recommending Chapel to someone who wanted
to tackle computations on large distributed rectangular arrays,
dense or sparse, or Julia for someone who had a short-lived project
and wanted something interactive and requiring only single-node or
coordinator-worker computations (or patterns that were more about
concurrency than parallelism).  Julia also seems like a good choice for
prototyping a DSL for specific scientific problems.</p>


<p>Neither project is really a competitor for the other; for Julia the
nearest competitor is likely the Python ecosystem, and for Chapel
it would be status quo (X + MPI + OpenMP/OpenACC) or that people
might try investigating a research project or start playing with
Spark (which is good at a lot of things, but not really scientific
simulation work.)</p>


<p>Scientific computing communities are very wary of new technologies
(it took 10+ years for Python to start getting any traction), with
the usual, self-fulfulling, fear being “what if it goes away”.  I
don’t think there’s any concern about dead code here for projects
that are started with either.  Chapel will be actively supported
for another couple of years at least, and the underlying tools (like
GASNet) underpin many projects and aren’t going anywhere.  One’s
code wouldn’t be “locked into” Chapel at any rate, as there are MPI
bindings, so that there’s always a path to incrementally port your
code back to MPI if you chose to.  For Julia, the immediate worry
is less about lack of support and more that the project might be
<em>too</em> actively maintained; that one would have to continually exert
effort to catch your code up with the current version.  In either
case, there are clear paths to follow (porting or upgrading) to
keep your code working.</p>


<h3 id="both-projects-have-as-yet-untapped-potential">Both projects have as-yet untapped potential</h3>

<p>What’s exciting about both of these projects is how far they could
go.  Chapel already makes certain class of MPI+OpenMP type programs
extremely simple to write with fairly good performance; if that
class of programs expands (either through packages built atop of
current functionality, or expanded functionality through additional
well-supported domain maps) and as performance continues to improve,
it could make large-scale scientific computation accessible to a
much broader community of scientists (and thus science).</p>


<p>Julia has the same potential to broaden computational science on
the desktop, and (at least in the near term) for computations
requiring only minimal communication like coordinator-worker computations.
But Python is already doing this, and making suprising inroads on
the distributed-memory computing front, and there will be something of a
race to see which gets there first.</p>


<hr />
<div class="footnotes">
  <ol>
    <li id="fn:1">
      <p>Yes, I said it.  Offsets into buffers can begin at 0, sure, but indices into mathematical objects begin at 1; anything else is madness.  Also: oxford comma, two spaces after a period, and vi are all the correct answers to their respective questions. <a class="reversefootnote" href="https://www.dursi.ca/feed.xml#fnref:1">&#8617;</a></p>

    </li>
    <li id="fn:2">
      <p>“Do the right thing” isn’t free, however; as with matlab or numpy, when combining objects of different shapes or sizes, the “right thing” can be a bit suprising unless one is very familiar with the tool’s <a href="https://docs.julialang.org/en/stable/manual/arrays/?highlight=broadcasting#broadcasting">broadcasting rules</a> <a class="reversefootnote" href="https://www.dursi.ca/feed.xml#fnref:2">&#8617;</a></p>

    </li>
  </ol>
</div>