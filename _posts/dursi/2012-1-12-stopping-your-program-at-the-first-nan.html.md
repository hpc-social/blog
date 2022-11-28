---
author: Jonathan Dursi's Blog
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2012-01-12 00:00:00'
layout: post
original_url: http://www.dursi.ca/post/stopping-your-program-at-the-first-nan.html
title: Stopping your program at the first NaN
---

<p>If you know that somewhere in your program, there lurks a catastrophic numerical bug that puts NaNs or Infs into your results and you want to know where it first happens, the search can be a little frustrating.   However, as before, the IEEE standard can help you; these illegal events (divide by zero, underflow or overflow, or invalid operations which cause NaNs) can be made to trigger exceptions, which will stop your code right at the point where it happens; then if you run your code through a debugger, you can find the very line where it happens.</p>

<p>We’ll discuss using the gnu compilers here; other compiler suites have similar options.</p>

<p>Let’s take a look at the following Fortran code:</p>

<pre><code>program nantest
    real :: a, b, c

    a = 1.
    b = 2.

    c = a/b
    print *, c,a,b

    a = 0.
    b = 0.

    c = a/b
    print *, c,a,b

    a = 2.
    b = 1.

    c = a/b
    print *,c,a,b
end program nantest
</code></pre>

<p>If we compile this code with <code>-ffpe-trap=invalid</code> (I usually add <code>,zero,overflow</code> , and even <code>underflow</code> if I think that’s causing me a problem in intermediate results), then the debugger can tell us the line where it all goes wrong:</p>

<pre><code class="language-bash">$ gfortran -o nantest nantest.f90 -ffpe-trap=invalid,zero,overflow -g -static
$ gdb nantest
[...]
(gdb) run
Starting program: /scratch/ljdursi/Testing/fortran/nantest
  0.50000000       1.0000000       2.0000000    

Program received signal SIGFPE, Arithmetic exception.
0x0000000000400384 in nantest () at nantest.f90:13
13          c = a/b
Current language:  auto; currently fortran
</code></pre>

<p>With the intel fortran compiler (ifort), using the option <code>-fpe0</code> will do the same thing.</p>

<p>It’s a little tricker with C code; we have to actually insert a call to <code>feenableexcept()</code>, which enables floating point exceptions, and is defined in fenv.h;</p>

<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;fenv.h&gt;

int main(int argc, char **argv) {
    float a, b, c;
    feenableexcept(FE_DIVBYZERO | FE_INVALID | FE_OVERFLOW);

    a = 1.;
    b = 2.;

    c = a/b;
    printf("%f %f %f\n", a, b, c);

    a = 0.;
    b = 0.;

    c = a/b;
    printf("%f %f %f\n", a, b, c);

    a = 2.;
    b = 1.;

    c = a/b;
    printf("%f %f %f\n", a, b, c);

    return 0;
}
</code></pre>
<p>but the effect is the same:</p>

<pre><code class="language-bash">$ gcc -o nantest nantest.c -lm -g
$ gdb ./nantest
[...]
(gdb) run
Starting program: /scratch/s/scinet/ljdursi/Testing/exception/nantest
1.000000 2.000000 0.500000

Program received signal SIGFPE, Arithmetic exception.
0x00000000004005d0 in main (argc=1, argv=0x7fffffffe4b8) at nantest.c:17
17	    c = a/b;
</code></pre>

<p>either way, you have a much better handle on where the errors are occuring.</p>