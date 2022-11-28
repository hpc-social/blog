---
author: Vanessasaurus
blog_subtitle: dinosaurs, programming, and parsnips
blog_title: VanessaSaurus
blog_url: https://vsoch.github.io/
category: vsoch
date: '2022-05-07 13:30:00'
layout: post
original_url: https://vsoch.github.io/2022/pipelib/
title: Pipelib- Simple Library to Parse, Filter, and Sort Things
---

<p>In early April I added an “update” command to Singularity Registry HPC (<a href="https://github.com/singularityhub/singularity-hpc/pull/538" target="_blank">see the pull request here</a> and needed to start with a list of docker tags and
parse them into version strings to sort, and still return the original tag for later use.
I wound up creating a <a href="https://github.com/singularityhub/singularity-hpc/blob/main/shpc/main/container/update/versions.py" target="_blank">custom class and set of functions</a> that use 
<a href="https://github.com/python/cpython/blob/bd030b633f98ea5d9f93ef0105a51d2faf67070d/Lib/distutils/version.py#L269" target="_blank">distutils.LooseVersion</a> to support that, but in creating this
“hard coded thing” I stepped back and had a question.</p>

<blockquote>
  <p>Can we more intelligentally compose custom parsing pipelines?</p>
</blockquote>

<p>Specifically I wanted to:</p>

<ol class="custom-counter">
<li>Start with a list of container tags for an image from a registry</li>
<li>Filter out anything that looks like a commit, but isn't a string (e.g., latest)</li>
<li>Derive a major, minor, and patch version for each, and filter to newest</li>
<li>Sort!</li>
</ol>

<p>For step 3, as an example if there was a <code class="language-plaintext highlighter-rouge">1.2.3-commitA</code> and <code class="language-plaintext highlighter-rouge">1.2.3-commitB</code> I’d only want to keep one, and the newer one of the two,
so I could ask for “unique by patch” and filter the older one out.
Ultimately of course I <a href="https://twitter.com/vsoch/status/1516197732708282369" target="_blank">dove right in</a>,
and this led to the creation of <a href="https://vsoch.github.io/pipelib" target="_blank">Pipelib</a>, which was an itch I terribly wanted to scratch! In this quick post, I want to share the overall design, because it was really fun to make.</p>

<div style="padding: 20px;">
<img src="https://raw.githubusercontent.com/vsoch/pipelib/main/docs/assets/pipelib-small.png" />
</div>

<h2 id="design">Design</h2>

<p>Before we talk about the design, let me show it to you.</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="kn">import</span> <span class="nn">pipelib.steps</span> <span class="k">as</span> <span class="n">step</span>
<span class="kn">import</span> <span class="nn">pipelib.pipeline</span> <span class="k">as</span> <span class="n">pipeline</span>

<span class="c1"># A pipeline to process a list of strings
</span><span class="n">steps</span> <span class="o">=</span> <span class="p">(</span>

   <span class="c1"># convert everything to lowercase
</span>   <span class="n">step</span><span class="p">.</span><span class="n">transform</span><span class="p">.</span><span class="n">ToLowercase</span><span class="p">(),</span>

   <span class="c1"># don't include anything with "two"
</span>   <span class="o">~</span><span class="n">step</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasPatterns</span><span class="p">(</span><span class="n">filters</span><span class="o">=</span><span class="p">[</span><span class="s">"two"</span><span class="p">])</span>
<span class="p">)</span>

<span class="c1"># Strings to process
</span><span class="n">items</span> <span class="o">=</span> <span class="p">[</span><span class="s">'item-ONE'</span><span class="p">,</span> <span class="s">'item-TWO'</span><span class="p">,</span> <span class="s">'item-two-THREE'</span><span class="p">]</span>

<span class="n">p</span> <span class="o">=</span> <span class="n">pipeline</span><span class="p">.</span><span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="p">)</span>

<span class="c1"># The updated and transformed items
</span><span class="n">updated</span> <span class="o">=</span> <span class="n">p</span><span class="p">.</span><span class="n">run</span><span class="p">(</span><span class="n">items</span><span class="p">)</span>
<span class="c1"># ['item-one']
</span>
</code></pre></div></div>

<p>In the above, we take a pipeline object and add steps to it. That design is fairly simple,
as the Pipeline class takes an optional iterable of things to process. I say “things” because
we can give it steps, composed steps, or even entire other pipelines. Here is an example
of adding an entire other Pipeline!</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="kn">import</span> <span class="nn">pipelib.steps</span> <span class="k">as</span> <span class="n">step</span>
<span class="kn">import</span> <span class="nn">pipelib.pipeline</span> <span class="k">as</span> <span class="n">pipeline</span>

<span class="n">fruits</span> <span class="o">=</span> <span class="p">[</span><span class="s">"Orange"</span><span class="p">,</span> <span class="s">"Melon"</span><span class="p">,</span> <span class="s">"Watermelon"</span><span class="p">,</span> <span class="s">"Fruit23"</span><span class="p">]</span>
<span class="n">preprocess</span> <span class="o">=</span> <span class="n">pipeline</span><span class="p">.</span><span class="n">Pipeline</span><span class="p">(</span>
    <span class="n">steps</span> <span class="o">=</span> <span class="p">(</span>
        <span class="c1"># Example of chaining steps together
</span>        <span class="n">step</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasMaxLength</span><span class="p">(</span><span class="n">length</span><span class="o">=</span><span class="mi">8</span><span class="p">)</span> <span class="o">&amp;</span> <span class="n">step</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasAllLetters</span><span class="p">(),</span>
    <span class="p">)</span>
<span class="p">)</span>

<span class="c1"># Add this preprocess step alongside other steps (make lowercase)
</span><span class="n">steps</span> <span class="o">=</span> <span class="p">(</span>
   <span class="n">step</span><span class="p">.</span><span class="n">transform</span><span class="p">.</span><span class="n">ToLowercase</span><span class="p">(),</span>
   <span class="n">preprocess</span><span class="p">,</span>
<span class="p">)</span>

<span class="c1"># Create a new pipeline and run
</span><span class="n">p</span> <span class="o">=</span> <span class="n">pipeline</span><span class="p">.</span><span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="p">)</span>

<span class="c1"># We should expect orange and melon!
</span><span class="n">updated</span> <span class="o">=</span> <span class="n">p</span><span class="p">.</span><span class="n">run</span><span class="p">(</span><span class="n">fruits</span><span class="p">)</span>
<span class="p">[</span><span class="s">'orange'</span><span class="p">,</span> <span class="s">'melon'</span><span class="p">]</span>

</code></pre></div></div>

<p>Implementation-wise, this is also fairly simple. We can check the underlying class of the provided object
and either add a single step, or insert a set of steps given another pipeline. In fact, pipelib comes with a
small set of “pipelines” that are ready for you to use. For example, here is one to
filter out “things that look like complete or partial git commits”</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="kn">import</span> <span class="nn">pipelib.steps</span> <span class="k">as</span> <span class="n">step</span>
<span class="kn">import</span> <span class="nn">pipelib.pipeline</span> <span class="k">as</span> <span class="n">pipeline</span>

<span class="c1"># Pre-generated sets of steps we can use
</span><span class="kn">import</span> <span class="nn">pipelib.pipelines</span> <span class="k">as</span> <span class="n">pipelines</span>

<span class="n">pipeline</span><span class="p">.</span><span class="n">Pipeline</span><span class="p">(</span>
    <span class="n">pipelines</span><span class="p">.</span><span class="n">git</span><span class="p">.</span><span class="n">RemoveCommits</span>
<span class="p">).</span><span class="n">run</span><span class="p">([</span><span class="s">"832b1c"</span><span class="p">,</span> <span class="s">"832b1c645e562d5cc6e376e5a3e058c02a40d92a"</span><span class="p">,</span> <span class="s">"123-abcd"</span><span class="p">])</span>
<span class="p">[</span><span class="s">"123-abcd"</span><span class="p">]</span>

</code></pre></div></div>

<p>This is something I found useful because people sometimes use commits as Docker tags, and I don’t find this 
incredibly meaningful as a version to compare to (and want to remove them). Under the hood, it looks like this:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="n">RemoveCommits</span> <span class="o">=</span> <span class="n">pipeline</span><span class="p">.</span><span class="n">Pipeline</span><span class="p">(</span>
    <span class="n">steps</span><span class="o">=</span><span class="p">(</span>
        <span class="n">step</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasMinLength</span><span class="p">(</span><span class="n">length</span><span class="o">=</span><span class="mi">8</span><span class="p">)</span> <span class="o">&amp;</span> <span class="o">~</span><span class="n">step</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasAllLowerLettersNumbers</span><span class="p">(),</span>
    <span class="p">)</span>
<span class="p">)</span>

</code></pre></div></div>

<p>Do you also notice something interesting in the above? We are actually combining steps akin to logical operations.
The above “pipeline” is actually just one step that combined other steps!</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="n">pipelines</span><span class="p">.</span><span class="n">git</span><span class="p">.</span><span class="n">RemoveCommits</span><span class="p">.</span><span class="n">steps</span>
<span class="p">[</span><span class="n">HasMinLength_AND_NotHasAllLowerLettersNumbers</span><span class="p">]</span>

</code></pre></div></div>

<p>Let’s step back and talk about some concepts that allow this.</p>

<h2 id="concepts">Concepts</h2>

<h3 id="pipeline">Pipeline</h3>

<p>As we’ve seen above, a pipeline is a collection of steps that take, as input, a listing of items and return a parser and filtered list.</p>

<h3 id="step">Step</h3>

<p>A step is some action in a pipeline. The way this works is that we have different kinds of steps, and this makes them easy
to implement and even test. A <em>boolean</em> step is akin to a filter, and is expected to return True or False to indicate if the item passes, e.g., False means it’s filtered out. Boolean steps are neat because they afford different kinds of logic and combination.</p>

<h4 id="logical-operations">Logical Operations</h4>

<p>Let’s say that we have a step that checks that an input is all letters:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">step</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasAllLetters</span><span class="p">()</span>
</code></pre></div></div>

<p>For the above, anything that had a number (e.g., orange123) would be filtered out. But what if we wanted to inverse that, and allow passing of inputs that don’t have all letters (meaning we want numbers or special characters?) We can simply do that:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="o">~</span><span class="n">step</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasAllLetters</span><span class="p">()</span>
</code></pre></div></div>

<p>Implementation wise, this was really fun to do! For Python to respect the logical operator <code class="language-plaintext highlighter-rouge">~</code> I simply define the “<strong>invert</strong>” function for the BooleanStep class.</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">def</span> <span class="nf">__invert__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
    <span class="s">"""
    We can say "~step" and reverse the logic.
    """</span>
    <span class="bp">self</span><span class="p">.</span><span class="n">reverse</span> <span class="o">=</span> <span class="bp">True</span>
    <span class="k">return</span> <span class="bp">self</span>
</code></pre></div></div>

<p>It sets an attribute “reverse” to True, and returns itself, that way we use the same step, but with this variable set to be true.
What does that do? In the “run” <a href="https://github.com/vsoch/pipelib/blob/69d7d4ac677a24a31ffa9322f03090cf074442c8/pipelib/steps/step.py#L217-L238" target="_blank">function</a> of the BooleanStep we basically retrieve an outcome from the underlying step (True or False) and simply reverse it given that boolean is True! Again, it’s very simple, and allows for doing things like this:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="kn">from</span> <span class="nn">pipelib.pipeline</span> <span class="kn">import</span> <span class="n">Pipeline</span>
<span class="kn">import</span> <span class="nn">pipelib.steps</span> <span class="k">as</span> <span class="n">steps</span>

<span class="n">Pipeline</span><span class="p">(</span><span class="o">~</span><span class="n">steps</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasAllLetters</span><span class="p">()).</span><span class="n">run</span><span class="p">([</span><span class="s">"I-have-special-characters"</span><span class="p">,</span> <span class="s">"Idonot"</span><span class="p">])</span>
<span class="p">[</span><span class="s">'I-have-special-characters'</span><span class="p">]</span>

<span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasAllLetters</span><span class="p">()).</span><span class="n">run</span><span class="p">([</span><span class="s">"I-have-special-characters"</span><span class="p">,</span> <span class="s">"Idonot"</span><span class="p">])</span>
<span class="p">[</span><span class="s">'Idonot'</span><span class="p">]</span>

</code></pre></div></div>

<p>What if we wanted to combine steps? E.g., what if I want to say “has all letters” OR “has minimum length 10?” If we put the steps
side by side we would only be able to support an AND - allowing passing through of entries that have all letters and the minimum length of 10.
Pipelib supports both those operators - AND and OR as follows:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="o">&gt;</span> <span class="n">step</span> <span class="o">=</span> <span class="n">steps</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasAllLetters</span><span class="p">()</span> <span class="o">&amp;</span> <span class="n">steps</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasMinLength</span><span class="p">(</span><span class="n">length</span><span class="o">=</span><span class="mi">10</span><span class="p">)</span>
<span class="o">&gt;</span> <span class="n">step</span>
<span class="n">HasAllLetters_AND_HasMinLength</span>

<span class="n">Pipeline</span><span class="p">(</span><span class="n">step</span><span class="p">).</span><span class="n">run</span><span class="p">([</span><span class="s">"thisonewillpass"</span><span class="p">,</span> <span class="s">"thisoneno"</span><span class="p">,</span> <span class="s">"notthisone2"</span><span class="p">])</span>
<span class="p">[</span><span class="s">'thisonewillpass'</span><span class="p">]</span>

</code></pre></div></div>

<p>For both cases above, we are using the “<strong>and</strong>” and “<strong>or</strong> functions, respectively, and:</p>

<ol class="custom-counter">
<li>Checking for class compatibility (both must be BooleanStep)</li>
<li>Creating a list of composed steps to added to a class attribute "composed"</li>
<li>Add the previous run functions too, naming based on the step class name</li>
<li>Define a new run function that loops through the composed set, runs, updates and returns a shared result</li>
<li>Name the class based on the combined names of the composed classes</li>
</ol>

<p>For step 4 above, the operation (AND or OR) will vary depending on if the initial call was to “<strong>and</strong>” or “<strong>or</strong>”.
The main difference between the two is that “OR” starts with a default of False (otherwise it would always return True)
and AND starts with a default of True (otherwise it would always return False).
And since we are always taking the first class “composed” attribute, this means that you can compose
steps with other steps as many times as you like - a new check is simply added to the front or back of
the list. The result (returned) is the new class that is ready to run. Here is what an OR looks like:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="o">&gt;</span> <span class="n">step</span> <span class="o">=</span> <span class="n">steps</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasAllLetters</span><span class="p">()</span> <span class="o">|</span> <span class="n">steps</span><span class="p">.</span><span class="n">filters</span><span class="p">.</span><span class="n">HasMinLength</span><span class="p">(</span><span class="n">length</span><span class="o">=</span><span class="mi">10</span><span class="p">)</span>
<span class="o">&gt;</span> <span class="n">step</span>
<span class="n">HasAllLetters_OR_HasMinLength</span>

<span class="n">Pipeline</span><span class="p">(</span><span class="n">step</span><span class="p">).</span><span class="n">run</span><span class="p">([</span><span class="s">"thisonewillpass"</span><span class="p">,</span> <span class="s">"veryshort"</span><span class="p">,</span> <span class="s">"12345"</span><span class="p">])</span>
<span class="p">[</span><span class="s">'thisonewillpass'</span><span class="p">,</span> <span class="s">'veryshort'</span><span class="p">]</span>

</code></pre></div></div>

<p>If you are interested in this function, you can see the entire thing <a href="https://github.com/vsoch/pipelib/blob/832b1c645e562d5cc6e376e5a3e058c02a40d92a/pipelib/steps/step.py#L177-L241" target="_blank">here</a>.</p>

<h4 id="transformation-operations">Transformation Operations</h4>

<p>A base step can be thought of as a transformation. Instead of expecting a boolean to be returned, we are
instead expecting a new value or None. In this respect the transform step can also act as a boolean as a return
of “None” will be removed from the list, however in most cases a transform is intended to perform an operation 
on the item passed. Here is an example of a transformation operation:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="p">.</span><span class="n">transform</span><span class="p">.</span><span class="n">ToLowercase</span><span class="p">()).</span><span class="n">run</span><span class="p">([</span><span class="s">"AHHHH"</span><span class="p">])</span>
<span class="p">[</span><span class="s">'ahhhh'</span><span class="p">]</span>
</code></pre></div></div>

<h4 id="sort-operations">Sort Operations</h4>

<p>A sort operation is a step that is one level up. Instead of operating on individual items, the step
re-defines a the higher level “run” function and does operations across the iterable.
A good example from Pipelib is the use case that originally inspired me - to start with a messy
list of Docker tags, do some parsing to derive versions, and return back a sorted list.</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="n">pipeline</span><span class="p">.</span><span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="p">.</span><span class="n">container</span><span class="p">.</span><span class="n">ContainerTagSort</span><span class="p">(</span><span class="n">ascending</span><span class="o">=</span><span class="bp">False</span><span class="p">)).</span><span class="n">run</span><span class="p">([</span><span class="s">"1.2.3"</span><span class="p">,</span> <span class="s">"0.1.0"</span><span class="p">,</span> <span class="s">"8.3.2"</span><span class="p">])</span>
<span class="p">[</span><span class="s">'8.3.2'</span><span class="p">,</span> <span class="s">'1.2.3'</span><span class="p">,</span> <span class="s">'0.1.0'</span><span class="p">]</span>

<span class="n">pipeline</span><span class="p">.</span><span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="p">.</span><span class="n">container</span><span class="p">.</span><span class="n">ContainerTagSort</span><span class="p">(</span><span class="n">ascending</span><span class="o">=</span><span class="bp">True</span><span class="p">)).</span><span class="n">run</span><span class="p">([</span><span class="s">"1.2.3"</span><span class="p">,</span> <span class="s">"0.1.0"</span><span class="p">,</span> <span class="s">"8.3.2"</span><span class="p">])</span>
<span class="p">[</span><span class="s">'0.1.0'</span><span class="p">,</span> <span class="s">'1.2.3'</span><span class="p">,</span> <span class="s">'8.3.2'</span><span class="p">]</span>

</code></pre></div></div>

<p>In the above we also demonstrate that steps can take parameters, such as the order of a sort!
This particular sorting step also allows you to say you want to return unique major, minor, or patch
versions.</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="n">pipeline</span><span class="p">.</span><span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="p">.</span><span class="n">container</span><span class="p">.</span><span class="n">ContainerTagSort</span><span class="p">(</span><span class="n">unique_major</span><span class="o">=</span><span class="bp">True</span><span class="p">)).</span><span class="n">run</span><span class="p">([</span><span class="s">"1.2.3"</span><span class="p">,</span> <span class="s">"1.1.0"</span><span class="p">,</span> <span class="s">"8.3.2"</span><span class="p">])</span>
<span class="p">[</span><span class="s">'8.3.2'</span><span class="p">,</span> <span class="s">'1.2.3'</span><span class="p">]</span>

</code></pre></div></div>

<p>And if you wanted to do a more comprehensive clean up and sort, you could do <a href="https://vsoch.github.io/pipelib/getting_started/user-guide.html#a-real-world-example-docker-tags" target="_blank">something like this</a>.</p>

<h3 id="wrapper">Wrapper</h3>

<p>Pipelib needed a way to be able to pass around some parsed version of an item, but still maintain
the original. For example, let’s say I’m parsing Docker tags into something that resembles a loose
semantic version, I might have filtered <code class="language-plaintext highlighter-rouge">1.2.3-boop</code> to be just <code class="language-plaintext highlighter-rouge">1.2.3</code>, but at the end of the
day I need the original tag to pull. Pipelib accomplishes this via wrappers.</p>

<p>A wrapper is conceptually that - an internal wrapper class to an item that allows for storing
an original value, and still doing operations to change a current state. Wrappers are used inside 
steps and allow for things like sorting and comparison. You probably don’t need to worry about wrappers
unless you want to develop for pipelib. By default, wrappers and “extracted away” to return the basic
types. However, you can ask Pipelib to not do this unwrapping, and then you can get back
the derived and original values:</p>

<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="n">tags</span>  <span class="o">=</span> <span class="p">[</span><span class="s">"1.2.3"</span><span class="p">,</span> <span class="s">"1.1.0"</span><span class="p">,</span> <span class="s">"8.3.2"</span><span class="p">]</span>
<span class="n">updated</span> <span class="o">=</span> <span class="n">pipeline</span><span class="p">.</span><span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="p">.</span><span class="n">container</span><span class="p">.</span><span class="n">ContainerTagSort</span><span class="p">()).</span><span class="n">run</span><span class="p">(</span><span class="n">tags</span><span class="p">,</span> <span class="n">unwrap</span><span class="o">=</span><span class="bp">False</span><span class="p">)</span>

<span class="c1"># Notice that this just looks like a set of strings...
</span><span class="n">updated</span>
<span class="p">[</span><span class="s">'8.3.2'</span><span class="p">,</span> <span class="s">'1.2.3'</span><span class="p">]</span>

<span class="c1"># But actually we have wrappers, that each have an _original attribute
</span><span class="nb">type</span><span class="p">(</span><span class="n">updated</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
<span class="n">pipelib</span><span class="p">.</span><span class="n">wrappers</span><span class="p">.</span><span class="n">version</span><span class="p">.</span><span class="n">VersionWrapper</span>

</code></pre></div></div>

<h2 id="conclusion">Conclusion</h2>

<p>I’ve had so much fun making this library! Like many of my projects it’s probably not super useful,
but if you see a cool use case please let me know! I’m also happy to develop custom pipelines or steps
for a use case that you might be interested in. Please don’t hesitate to ask me for help, I’m always running
out of fun things to do :)</p>

<blockquote>
  <p>Why should I care?</p>
</blockquote>

<p>Arguably you could just hard code this kind of filtering and sorting, but I think the
idea of being able to customize and assemble steps is a cool one. If the steps are provided
in a library it might might it slightly easier, or your work more reproducible because 
someone else can use the steps. And if you don’t care? That’s okay too. I recognize this was
mostly a fun project, and yet-another-itch I really wanted to scratch because I’ve never
made a design like this before, either in terms of the idea or <a href="https://twitter.com/vsoch/status/1521670410852442112" target="_blank">underlying testing and automation</a>.</p>