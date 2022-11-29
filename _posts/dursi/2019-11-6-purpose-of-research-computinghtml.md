---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2019-11-06 00:00:00'
layout: post
original_url: http://www.dursi.ca/post/purpose-of-research-computing.html
slug: the-purpose-of-research-computing-is-the-research-not-the-computing
title: The Purpose of Research Computing is the Research, not the Computing
---

<p>Absolutely everyone in research computing will agree that supporting
research is their centre’s highest goal.  And they’re not lying,
but at many centres I’ve visited, they aren’t really correct, either.</p>


<p>The day-to-day work in such a centre, naturally enough, is all about
technical operations - keeping the computers running, updating
software, making sure <code>/scratch</code> has enough space free, answering
emails.  And of course, it has to be.  But without internal champions
actively and continually turning the focus back to the <em>purpose</em>
of those activities - the research outcomes that those activities
are meant to support - the internal, technical, activities <em>become</em>
the purpose of the centre.</p>


<p>Pretty quickly, you end up with centres that are ranking their
performance quarter to quarter with cluster utilization numbers,
or having all researcher interactions occurring via “tickets” and
measuring volume and mean-time-to-closure of those tickets (because
shorter conversations with researchers are better, right?)  And
once that’s happened, it becomes very hard to change; bytes and
flops and closure rates have become the reason for coming to work.
It’s baked into the reporting, the funding, the staff’s annual
performance review.  Sure, many of these same centres do collect
and in some way report publications, but if publication rates
resulting from work with the centre are down 5% last year because
two productive groups need new capabilities but the centre has
decided to grow current capability, no one is getting an uncomfortable
call from the boss at these centres.  Ticket closure rates going
down 5% though… maybe you’re getting a call.</p>


<p><img alt="Organizations that care about their clients make their offerings very clear." src="https://www.dursi.ca/assets/purpose_research_computing/pexels_inside-a-store-2199190_crop.jpg" style="float: left; width: 33%; padding: 15px 15px 15px 0px;" /></p>


<p>It doesn’t take very long to spot centres like this, even from the
outside.  On their websites, most prominently of all, are the
statistics that their biggest cluster premiered at position X on
the Top 500, it has such-and-such much disk space, umpty-ump GPUs,
and even more CPUs.  There are elaborate multi-stage sign-up
procedures which make the centre’s own reporting easy but getting
a graduate student started on the cluster tedious.  Their website
will show a couple of dated research success stories, but if a
researcher is visiting the website for the first time and wants to
know basic facts relevant to them, things like “What is a list of
services that the centre offers”, “Can you help my grad student do
X and if so how long would it take”,  “What is current wait times
for resources/for software installation”, the researcher is out of
luck - they’re just directed to a “contact us” email address (which,
of course, feeds into a ticket tracker).</p>


<p>(Have you ever visited a restaurant webpage and needed like 4 or 5
clicks to get to the menu and their hours?  If the restaurant took
the menu off the website entirely and you instead had to file a
ticket so you could ask specifically if they made spaghetti carbonara,
that’s what most research computing centre websites are like for
researchers.  Organizations that care about their customers make
their offerings very clear.)</p>


<p>The thing is, using metrics like utilization, tickets, storage and
the like to measure how much research support is happening is
madness, and we all know it’s madness.  You can goose utilization
numbers by letting researchers run jobs inefficiently, by prioritizing
job size distributions that may or may not represent researcher
needs, or by having staff do a lot of benchmarks “just to make
everything’s still good”.  You can keep ticket closure rates up by
having something that should be clarified or automated or fixed and
instead leaving it vague or manual or broken so that there’s a
stream of tickets coming in that are easily closed; or by irrelevantly
dicing what could be a long, productive discussion with a researcher
into a series of shorter “tickets”.</p>


<p>It’s madness because neither utilization, nor ticket closure rates,
nor storage use, nor even training course enrolment are valuable
to research <em>in and of themselves</em>.  They are <em>inputs</em> to the process
of supporting research via computing; not the purpose, not the
desired outcomes.  Being guided by metrics of those inputs and just
hoping that as long as those numbers stay good the best possible
science outcomes will just happen of their own accord is an abdication
of responsibility, and a squandering of scarce research-support
resources.</p>


<p>And it’s worse than that, of course.  Even a focus on inputs, if
it was being honest, would focus on <em>all</em> the inputs, and certainly
the most valuable and hardest-to-replace inputs - the technical
staff.   What’s the “utilization” of the staff?  What fraction of
that Ph.D. chemist’s time over there is spent actually enabling
research projects, versus updating software packages or responding
to “why is my job still in the queue” tickets?  How much time does
our data centre monitoring expert spend swapping memory and cables?
Is that up this quarter, or down; and if it’s down, why?  What
fraction of the expertise of the support staff is being used?  What
is the meaningful contribution rate?</p>


<p><img alt="Inputs produce outpus which produce outcoms which produce impact.  The inputs are not what you should measure." src="https://www.dursi.ca/assets/purpose_research_computing/shutterstock_input_outcome.jpg" style="float: right; width: 50%; padding: 15px 0px 15px 15px;" /></p>


<p>The reason that those staff input metrics aren’t being measured and
others are is simple, and clarifying.  The hardware inputs aren’t
being used as metrics due to a (false) belief that they are meaningful
in and of themselves, nor because of an (incorrect) understanding
that they are they can be taken in a principled way as a proxy for
the desired research outcomes.  They’re used because they’re easy
to gather.  And they’re comfortable to use because they don’t really
require centre managers to make any hard choices.</p>


<p>Focussing on the inputs instead of the outputs - or even better,
outcomes - isn’t only a research computing thing, of course.  It’s
an absolutely classic mistake in a lot of sectors; a google search
for <a href="https://www.google.com/search?q=focus+on+outcomes%2C+not+inputs&amp;oq=focus+on+outcomes%2C+not+inputs">focus on outcomes, not
inputs</a>
returns 139 million results.</p>


<p>There are two prototypical reasons why it happens.  If I were feeling
in a twitter-ranty mood again, I might be tempted to draw the analogy
to the first case - lack of competition, due to private- or
public-sector monopolies, reducing the urgency of focusing on
customer’s needs.  You see this in internal departments of large
organizations, where the “customer base” is locked in, or in other
places where there’s no real competition (Hello most departments
of motor vehicles, or cable companies, or Google Mail support!).
These departments end up developing a relentless internal focus,
having cryptic and opaque internal decision-making processes seemingly
unrelated to what their clients actually want, and famously make
clients jump through hoops to get their needs met.  This isn’t
caused by malevolence, or even indifference; it couldn’t be for it
to be so widespread.  It’s just that, absent any real driver to
focus on <em>customer</em> outcomes, it is almost impossible to drive
internal priorities towards anything other than internal efficiencies.
Those few companies in this situation that <em>do</em> manage to maintain
a focus on client outcomes are doing so by constantly expending
almost heroic levels of unseen effort inside the organization.</p>


<p>But I don’t actually think that’s what driving some research computing
centres inputs focus when it comes to operations and technical
decision making.  I think it comes almost from the other direction,
the other classic case; that of small nonprofits, typically enormously
concerned with their clients, who focus first on a very basic need
and then don’t know how to generalize beyond that as they grow.</p>


<p>Imagine a small nonprofit, passionately committed to helping people,
that gets its start meeting a very basic need - let’s say they’re
providing before-school breakfasts to children in or near poverty.
At that level, the activity <em>is</em> the outcome; they can count the
number of breakfasts served, try to get better at serving breakfasts
with a given amount of donations, work on raising money to fund
more breakfasts, maybe expand to different schools or supplying a
wider range of breakfasts to be inclusive of students with particular
dietary needs.  They are <em>super</em> committed to their clients.</p>


<p>But as that nonprofit starts expanding, it becomes clear their
client base needs a wider range of services.  It starts partnering
with food banks, to help fight student hunger at home; its staff
participate in some after-school tutoring programs.  But it has no
way to prioritize these activities.  Is it a hunger-fighting
nonprofit?  Is it a help-underprivledged-students-succeed-at-school
nonprofit?  If they could double the tutoring efforts at the cost
of slowing the growth of the breakfast program next year, is that
the right thing to do, or not?  How would they know?</p>


<p>This is a terrifying transition for a nonprofit to go through.
Before, it knew exactly what it was doing, and had very clear metrics
for success.  In this intermediate stage, it probably has some
earmarked resources to participate in the tutoring and foodbanks,
and it touts that work, but it doesn’t know how to do anything but
report on school breakfasts.  To go beyond this means making choices
about what it will prioritize - and more scarily, what it will <em>not</em>
prioritize - and working on program evaluation plans for the much
more ambitious but more ambiguous goals of “fighting hunger” or
“helping students succeed at school”.   Many nonprofits never make
that transition.  Some stay small and focussed, which works well
but limits their impact; many stay in limbo in that uncomfortable
intermediate state until they are overtaken by events or other
organizations.</p>


<p>At most research computing centres, I think the story is more like
that of the nonprofit.  Except let’s be honest, while providing
breakfasts is inherently meaningful and has very few organizations
willing to do it, providing cycles and storage isn’t, and has many
alternate providers.</p>


<p>But going beyond meeting the basic needs of providing research
computing cycles and storage, which was a much greater need in the
90s than it is today, is genuinely hard.  It’s very labour intensive -
it requires going out to the entire research community you aim
to support, including those who you’ve never had a working relationship
with, and understanding needs.  It’s very uncomfortable - you have
to then prioritize those needs based on their value to the larger
enterprise and to where you can make the most difference, and that
means having awkward conversations bout <em>not</em> prioritizing other
needs.  And it’s incredibly uncertain - it means going from evaluations
based on numbers on a dashboard that are largely under your control,
to unfamiliar qualitative evaluations and doing the hard work of
trying to measure research outcomes.</p>


<p>But there’s a relatively straightforward approach to get there
starting from where you are.  It takes some work, but just going
through the process is clarifying.</p>


<ol>
  <li><strong>What do you do now?</strong>  You know, broadly, what services you offer to
researchers, you’ve just never had to make it explicit.  Start to put
together a very simple <a href="https://www.cherwell.com/library/blog/7-steps-to-defining-and-designing-an-effective-service-catalog/">service catalog</a>.
It doesn’t have to be very complicated; figure out internally what
services you offer, at quite a high level, in language that researchers
would care about.  Get staff to offer suggestions.  For each service,
for internal consumption only, figure out what’s involved in providing it - what are 
typical amount of hours involved, who has to coordinate with whom, <em>etc.</em>.</li>
  <li><strong>How do those services help researchers?</strong>  Again, you have a broad
sense of this, but make it concrete.  Is it more publications?
Higher-impact publications?  <em>Faster</em> publication?  Better collaboration
opportunties?  Higher funding success rates?  Better job prospects for
students and postdocs?  More successful faculty or postdoc recruitment?
Friendly users or your VPR can help with this. Come up with a handful
that seem most important in your user community.</li>
  <li><strong>Connect services and benefits.</strong> Come up with some concrete
examples of how you’ve provided each of those benefits with the services you
make available.  You may find benefits that you can’t yet justify claiming
you provide, or services you’ve forgotten about.</li>
  <li><strong>Refine your services and benefits lists.</strong> Start talking about
these benefits and services, in talks at user groups or when doing
outreach to departments, new hires, incoming graduate student
training, and the like.  Find out which ones attract attention,
which ones don’t.  Ask for suggestions for new items for the lists,
and new conncetions between the two.</li>
  <li><strong>Start thinking about indicators and evaluation.</strong>  Besides anecdotes,
how could you convince your funder, or senior leadership at your institution,
that you provide those benefits?  How could you show you were getting
better? How could you convince them that a 15% increase in funding would
provide some meaningful improvement to research institution?  The answer
will depend on the benefits you’ve chosen, but there are lots of
<a href="https://www.councilofnonprofits.org/tools-resources/evaluation-and-measurement-of-outcomes">resources</a>
out <a href="https://managementhelp.org/evaluation/outcomes-evaluation-guide.htm">there</a>
to help you with this.  Closer to home, I absolutely promise you
there are people at your instution who will talk to you about program
evaluation until you want to pass out just to enjoy some quiet.
What you come up with will seem quite different to you.  They won’t
be instruments with 3 decimal places of accuracy; they
may be citation counts or randomly sampled surveys or qualitative
interviws.  Measuring research is hard - but everyone in research
knows and understands this.  Approaches like short surveys or
interviews are labour intensive, but provide amazing information -
they will provide a constant stream of incoming success stories that
you can make use of, and less successful storis you can learn from.</li>
  <li><strong>Start thinking about rebalancing your service offerings</strong>.  Once
you have these lists, and approaches to evaluations, then and only
then do you have a principled way to make decisions about in which services
to invest more, and in which to invest less.  And you’ll have very
convincing arguments to take to funders and leadership.</li>
</ol>

<p>I get it that going through this process to the point where you
can meaningfully what ask the right next thing to do to help
research isn’t easy.  It absolutely isn’t.  It’s a lot of work,
and while it is useful in many different ways, it still doesn’t
make things easy - if anything, it forces you to confront tradeoffs
and hard choices that focusing on inputs may have let you avoid.  A centre that hasn’t
been thinking this way for a while will have some low-hanging fruit
that can be picked to start, but after that there will be  multiple
ways for a centre to be supporting research, and no clear answer
which is the “best”.   Making those choices will require knowing
the strengths of the centre and knowing where those strengths are
needed in the research community it serves — and not all research
needs are the same!  But <em>those</em> are questions that team leaders
need to be wrestling with.</p>


<p>The alternative, just running a set of computers for the same
friendly user group of people year after year, isn’t research
support; it’s a hobby.</p>