---
author: Vanessasaurus
author_tag: vsoch
blog_subtitle: dinosaurs, programming, and parsnips
blog_title: VanessaSaurus
blog_url: https://vsoch.github.io/
category: vsoch
date: '2022-01-07 12:30:00'
layout: post
original_url: https://vsoch.github.io/2022/what-is-hard/
slug: things-that-are-hard
title: Things that are Hard
---

<p>I saw a funny tweet on Twitter the other night - it was someone from a large consumer company sharing
their vision for “<a href="https://hypebeast.com/2022/1/walmart-2017-mutual-mobile-metaverse-shopping-video-resurfaces" target="_blank">the next generation shopping experience</a>” and it was a virtual person walking through a supermarket aisle and reaching out to pick up a bottle of wine.
I can’t find the specific tweet, but it said something to the effect of:</p>


<blockquote>
  <p>Nobody asked for this. Stop making stuff to solve problems that people don’t have</p>

</blockquote>

<p>My dear reader, it me! 😲️ This message hit me really hard, because I am definitely one to build niche tools for use cases that likely don’t exist but seem fun or interesting to me. I also feel pretty <a href="https://twitter.com/vsoch/status/1478913234136494081" target="_blank">disconnected</a> from communities that are innovating and testing new ideas.</p>


<h2 id="what-is-hard">What is hard?</h2>

<p>This is a problem that a lot of us have. We build things that nobody needs. We need to focus more on the problems that people are actually facing. I would also scope that to developer workflows, which includes automation, testing, and development. Since I have a nice view into my own mental space, here is my list of things that are hard.</p>


<ol class="custom-counter">
  <li>When I am trying to develop software and I can't open an interface with the code and environment I need</li>
  <li>That my main interaction with a resource is via SSH</li>
  <li>When a workflow or even container works in one place but not another</li>
  <li>When I need to develop, build in CI, push to a registry, and pull. One mistake? Start from scratch</li>
  <li>When I need to run a job and I have to interact with a job manager and it's hard and annoying</li>
  <li>Logging or monitoring means looking at text files with cryptic names</li>
  <li>Automated testing on HPC is not a thing. Build on GitHub and pray.</li>
  <li>When I can't easily navigate code, documentation, or it's completely missing</li>
  <li>When I set up everything the way I like it and I have to login to a new system and do it all over again</li>
  <li>When I want to develop something that uses a cluster resource but there are no exposed APIs.</li>
  <li>When it's impossible to compare between systems because they are special snowflakes</li>
  <li>When I can't easily test across the systems that my software is intended for.</li>
  <li>To scale anything I have to use a job manager, wait hours, and then again if there is one mistake</li>
  <li>When it takes 2 hours or more to get a node allocated</li>
  <li>When I can't really make tools for HPC because I'm trying to find workarounds for all these problems</li>
</ol>

<p>And I’d add a “thing that is annoying” to be this obsessive focus on power and scale, in a competitive sense, and this race
to be in the top 500 and beat the other guy over all else. The constant need to rebuild clusters means we never
focus on the details of how we use them. We do the same things over again. I’ve mentioned these things before, possibly many times, but I need to point it out again.</p>


<blockquote>
  <p>Our current developer environments are more like handcuffs than places we are enabled to thrive.</p>

</blockquote>

<p>The reality for me is that I tend to put myself in a new role or environment, and then think of lots of cool ways to extend a particular tool, or build something before it. This is why I’ve made a ton of visualizations, associated tools, or posts for spack - it’s literally just the thing that is right in front of me. Put something else in front of me, such as an entire infrastructure with APIs, and I’d do the same. So why can’t a nice set of developer tools be available for the resources I’m supposed to be using?</p>


<h2 id="develop-based-on-specific-problems">Develop based on specific problems</h2>

<p>I think I want to develop more focusing on these problems. Don’t get me wrong - I’ll definitely keep making silly projects. But my vision for the future needs to be oriented toward these pains. These in particular are the problems that I think our community needs to look at, at least given this developer perspective.
I say this because I’ve seen and used the dark side - having free rein of beautiful cloud APIs to let me automate to my heart’s content! 
I only now, without being a part of some cloud or container cluster deployed project, am aware that I don’t have access to these development tools.
 What is my solution now? I largely don’t ssh into an HPC cluster until I absolutely have to - either to scale something, or reproduce a workflow on GitHub actions that works there (but then is really challenging to get it working on the cluster resource). Indeed <a href="https://twitter.com/vsoch/status/1461908217223528448" target="_blank">this entire thread</a> resulted after a frustrating evening of exactly that.</p>


<p>What isn’t helpful? What isn’t helpful is telling me “This center / place / person has this thing that has solved this problem.” Can I easily access it, and what about the entire research software engineering community? This kind of response shuts down the conversation 
and makes the developer (myself for example) realize that the person I’m talking to is not interested in thinking about how to inspire change.
I’ve been really frustrated recently with mentioning even an abstract idea, and getting shut down that “Oh that sounds like this other tool.”
For a project to reach this “mention status” it needs to be easy to install or use, and not have a barrier of privilege that you have to work at a certain place or know people. Telling me that there is a solution that requires some convoluted steps and permissions not only implies that it is only available to those in privilege, but that the solution is not well adopted enough or shared enough to be truly a solution for our community.</p>


<h2 id="inspiring-vision">Inspiring Vision</h2>

<p>If we aren’t happy with the current state of the world, what are our options? Well, we could leave our current roles to find another state that is more similar to what we want. Personally speaking, I haven’t hit that point quite yet. I want to try my hardest to formulate a vision for how I want the world to be, and then find opportunity to work on it from where I am. The wisdom here is that no specific role is perfect, and optimally we should place ourself somewhere where there are resources and open mindedness for change. it’s up to us to extend our influence as best we can to help drive some possible future. If you try that and fail? At least you tried.</p>


<p>These are the things that are hard. I am going to try harder to have them be the focus of my thinking about the future. I want to make them easier. I’m starting to realize that possibly the reality is that I should think beyond the constraints of HPC, and more toward the kind of infrastructure that I want, and then
figure out how to slowly integrate it as a part of our culture too. We can start with a core vision for a future that we want, and then
slowly build up tooling and community around that.</p>


<p>Happy Friday, friends!</p>