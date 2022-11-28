---
author: Jonathan Dursi's Blog
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2011-11-23 00:00:00'
layout: post
original_url: http://www.dursi.ca/post/testing-roundoff-2.html
title: Testing Roundoff
---

<p>A <a href="http://www.cs.berkeley.edu/~wkahan/Stnfrd50.pdf">talk</a> has been circulating (HT: Hacker News) from a conference celebrating <a href="http://compmath50.stanford.edu/">50 years of scientific computing at Stanford</a> where the author, William Kahan, discusses an old and sadly disused trick for testing the numerical stability of the implementation of an algorithm that should work with any C99 or Fortran 2003 compiler without changing the underlying code.  It’s definitely a tool that’s worth having in your toolbox, so it’s worth mentioning here.</p>

<p>We’ll consider a simple numerical problem; imagine a projectile launched from height $h = 0$ with velocity $v_0=5000 \mathrm{m s}^{-1}$, and subject to the Earth’s gravitational accelleration, $g = 9.81 \mathrm{m} \mathrm{s}^{-2}$. We’re going to ask when the (first) time is that the projectile hits a height h.</p>

<p>This is going to be an application of our friend the quadratic equation:</p>

\[r = \frac{-b \pm \sqrt{b^2 - 4 a c}}{2 a}\]

<p>Now, because of the repeated subtraction, a naive implementation of this equation is known to undergo catastrophic cancellation near $b^2=4 a c$, or for where the discriminant is much less than \(b\) — in our case, near the ends and the peak of the projectile’s trajectory.   We’re going to demonstrate that below.</p>

<p>Now, before we show that such sensitivity can happen, we should ask — why would we care? If we test our code and know it gives “good enough” answers under the conditions that matter to us, does it really matter what could happen in other circumstances? The answer, of course, is yes. There are a lot of things we could want to do — increase the agressiveness of compiler optimizations when compiling our code, for instance — which will have the effect of numerically perturbing our computation; and we need to know if those small perturbations will have small, or large, effects on our answers.</p>

<p>It turns out that IEEE 754, the standard for floating point numbers, can give us some help with this. (Everyone who does numerical work should know at least a little bit about the floating point standard, or at least the issues involved with floating point numbers. <a href="http://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html">What every computer scientist should know about floating point</a>, particularly the first few sections, is an essential guide). The floating point standard - which almost all widely-used computing hardware should support - allows you to set certain properties of the mathematics “on the fly”. One particularly useful feature is the ability to set how the last digit of all floating point operations are rounded - to nearest (the default), to zero (eg, always truncate), to positive infinity (eg, always round up) or to negative infinity (always round down). In the C99 standard, this is implemented in the “fenv.h” header and the math library; in Fortran2003, this is part of the intrinsic IEEE_ARITHMETIC module, where you can call IEEE_SET_ROUNDING_MODE.</p>

<p>By changing the rounding, you are perturbing every floating point operation in your calculation. If this perturbation results in significant changes in your result, then your calculation is very fragile, and you may have to look into re-writing the calculation, using another algorithm, or resorting to using higher precision for that calculation (which will push the perturbations to less significant decimal places). If not, then you have some evidence that your calculation is robust to perturbations, at least in the last bit.</p>

<p>Below we have an example of how you’d do this in C. We have a simple routine which uses the obvious implementation of the quadratic equation to calculate the time when the projectile is at one meter, and we perform this calculation with all available rounding modes:</p>

<pre><code class="language-c">#include &lt;stdio.h&gt;
#include &lt;math.h&gt;
#include &lt;fenv.h&gt;

const int NOSOLN=-1;
const int SOLN  = 0;

int time(const float vo, const float g, const float ho, float *time) {
    float disc  = (vo*vo - 2.*g*ho);

    if (disc &lt; 0) return NOSOLN;

    disc = sqrt(disc);
    float root1 = (vo + disc)/g;
    float root2 = (vo - disc)/g;

    if ((root2 &gt;= 0.) &amp;&amp; root2 &lt; root1)
        *time = root2;
    else
        *time = root1;

    return SOLN;
}


int main(int argc, char **argv) {

    const float g =9.81;
    const float vo=5000.;
    const int   ho=1.;

    int nroundings=4;
    int roundings[]={FE_TONEAREST, FE_UPWARD, FE_DOWNWARD, FE_TOWARDZERO};
    char *names[]  ={"To nearest", "To +inf", "To -inf", "To zero"};

    for (int r=0; r&lt;nroundings; r++) {
        int status = fesetround(roundings[r]);
        if (status) {
            fprintf(stderr,"Could not set rounding to '%s'.\n", names[r]);
        } else {
            float soln;
            time(vo, g, ho, &amp;soln);
            printf("%s: %f\n", names[r], soln);
        }
    }

    return 0;
}
</code></pre>

<p>We compile the code with gcc (any C99 compiler should work):</p>

<pre><code class="language-bash">$ gcc -O0 -Wall -std=c99 quadratic.c -o quadratic -lm
</code></pre>
<p>Note that we need to explicitly link in the math library, and to turn off optimization (so that the compiler doesn’t replace the repeated calls to time() with a single call). Running this, we find:</p>

<pre><code>$ ./quadratic
To nearest: 0.000199
To +inf: 0.000149
To -inf: 0.000249
To zero: 0.000249
</code></pre>

<p>Changing the rounding modes changes the result by 50%! This shows that our current implementation - which is not giving obviously wrong answers - is extremely fragile in the presence of numerical noise, and we should exercise extreme caution with compiler flags, etc. (How to re-write the expression to be more robust to small changes is a topic for another day.)</p>