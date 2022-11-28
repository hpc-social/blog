---
author: Vanessasaurus
blog_subtitle: dinosaurs, programming, and parsnips
blog_title: VanessaSaurus
blog_url: https://vsoch.github.io/
category: vsoch
date: '2022-11-18 08:30:00'
layout: post
original_url: https://vsoch.github.io/2022/converged-computing/
title: Converged Computing
---

<p>For many years, there has been a battle between cloud and HPC. The cloud side of the equation says “micro services, cloud native!”
and the HPC side says “too expensive!” Conversations often don’t progress because both sides are up-in-arms and 
focused on why they cannot work together. At best, we might get access to cloud from an HPC center,
or an company might present a product as branded for “HPC.” But it’s not truly collaborative in the way that I’d like.</p>

<p>I’ll also step back and comment that (I do not believe) folks (myself included) on the HPC side have done enough
to sit at the table. For example, we haven’t been a voice in the Open Containers Initiative (<a href="https://supercontainers.github.io/containers-wg/" target="_blank">although I’ve tried</a>), nor have we been present (historically) for conferences that are more focused around cloud native technologies.
There is no pointing fingers or fault here - it’s just a matter of two different cultures, and it’s been challenging figuring out how to talk to one another, and how to work together. I’ve tried my best to be involved, to the best of my ability, in small ways on both sides. But I’m only one person. This isn’t to say there haven’t been small collaborations, but I believe we can do more.</p>

<h2 id="change-is-coming">Change is Coming</h2>

<p>I think this is going to change. The reason is because both sides of the equation have started to realize we have similar goals,
and it’s not about creating hybrid environments – having both pancakes and waffles for breakfast – but rather convergence – recognizing that pancakes and waffles are both kinds of breakfast cakes, and we can take features that we like of each to create a breakfast cake that will make everyone happy.
The idea of “Converged Computing” comes from my amazing team (see <a href="https://www.youtube.com/watch?v=9VwAcSOtph0" target="_blank">Dan’s talk at KubeCon here</a>) and is the idea that technologies from HPC can be integrated into more traditionally cloud approaches to produce a solution that
solves problems on both sides. Explicitly for these projects, it means testing the Flux Framework scheduler alongside Kubernetes. Do we still want portable workflows that can move from an HPC environment to cloud? Of course.
However, the niche or gradient that I’m interested in is the space that lives <em>between</em> these two worlds.</p>

<p>While I won’t go into huge detail (this would be more appropriate for a talk) the lab openly works on 
<a href="https://github.com/flux-framework" target="_blank">Flux Framework</a>, a resource manager that (in my opinion) is one of the coolest projects coming out of our space. I started working with these teams a few months ago, and am bringing my excitement and vision for (what I hope to be) a future where we are actively developing alongside other Kubernetes projects, and our work is well-known and established in this space.
What does that mean? Let me share some cool work under development. This is all being done publicly on GitHub, so there is
no issue to talk about it! My first year or so at the lab I was hired under a research project, and although I learned a lot, I haven’t felt inspired and driven until starting this work. Let’s talk about some of it! 🎉️</p>

<h3 id="the-flux-operator">The Flux Operator</h3>

<div style="padding: 20px;">
<img src="https://flux-framework.org/flux-operator/_images/the-operator.jpg" />
</div>

<p>If you aren’t familiar with Kubernetes Operators, let’s step back and talk about a human operator. If you are a syadmin managing apps
with associated services and databases on a cluster, you often had to do maintenance or update tasks like increasing a storage volume,
or modifying a service to a new user need. As this pattern has emerged as a common thing, they have come up with the concept of a Kubernetes Operator - an actual controller you install to your cluster that can automate this. In simple terms, after you install an operator to your cluster,
you can hand it a desired state (represented in a yaml configuration file) and the operator will do whatever it takes to reach that state. What does that means in the context of Flux? The Flux Operator is interested in creating
what we are calling a “Mini Cluster,” illustrated below.</p>

<div style="padding: 20px;">
<img src="https://flux-framework.org/flux-operator/_images/design-three-team1.png" />
</div>

<p>In Kubernetes object terms this is an <a href="https://kubernetes.io/docs/tasks/job/indexed-parallel-processing-static/" target="_blank">Indexed Job</a>, a few config maps, secrets, and a <a href="https://flux-framework.org/flux-restful-api/" target="_blank">RESTFul API</a> and user interface that I designed exposed as a service.  You can read more about our current design <a href="https://flux-framework.org/flux-operator/development/designs.html" target="_blank">here</a>.</p>

<p>This Mini Cluster is generated from a “custom resource definition” or CRD (the yaml you provide), and it can take <a href="https://flux-framework.org/flux-operator/getting_started/custom-resource-definition.html" target="_blank">these parameters</a>. Concetually, you as the user own the Mini Cluster and can submit jobs to it (either via the web interface or the API) until you are done. When you are done, you can bring down the cluster.</p>

<p>We are excited for this work because in the next months (to a bit longer) we are going to be testing different kinds of workloads 
running using Flux alongside this Mini Cluster, but on Kubernetes! I’ve started a small repository of dummy examples that I’m extending quickly at
<a href="https://github.com/rse-ops/flux-hpc" target="_blank">rse-ops/flux-hpc</a> and please open an issue there if you have a suggestion.</p>

<h3 id="stay-tuned">Stay Tuned!</h3>

<p>Stay tuned for more work in this space! I’ve been doing a ton of programming in Go, Python, and working
on a wide range of technologies, and fairly quickly, and I am very much in my happy place. Please come and join us! ❤️</p>