---
author: Jonathan Dursi's Blog
author_tag: dursi
blog_subtitle: R&amp;D computing at scale
blog_title: Jonathan Dursi
blog_url: http://www.dursi.ca
category: dursi
date: '2021-06-06 01:00:00'
layout: post
original_url: http://www.dursi.ca/post/nobody-cares-tech-stack.html
title: Nobody Else Cares About Your Tech Stack
---

<h2 id="focus-on-your-researchers-and-funders-problems-not-your-technical-solution">Focus on your researchers’ and funders’ problems, not your technical solution</h2>

<p>(Note: This post is adapted from <a href="https://newsletter.researchcomputingteams.org/archive/research-computing-teams-link-roundup-22-may-2021/">#75</a> of the <a href="https://www.researchcomputingteams.org">Research Computing Teams Newsletter</a>)</p>

<p>Many of us who are managing research computing and data teams come up through the ranks doing research ourselves, and have
experience in grantwriting for open research calls.  That can actually <em>hold us back</em> from succeeding with getting grants
for “digital research infrastructure” — building teams and infrastructure to support research.</p>

<p>The thing is, digital research infrastructure calls, the sort that support research computing and data teams and tools,
are more like applying to grants as a nonprofit than as a researcher.  And we can learn a lot from how the nonprofit
community writes funding proposals.</p>

<p><img alt="We're not proposing a research project, we're proposing to solve problems a funder sees for a research community." src="https://www.dursi.ca/assets/nobody_tech_stack/nonprofit_not_researcher.png" style="float: right; width: 50%;" /></p>

<p>Any funder has things they want to accomplish, and the goal as a potential fundee is to find something in the intersection of
“work that helps the funder accomplish their goals” and “work that we are able to do and that is aligned
with our goals”.   Excellent work that isn’t in that first set won’t get funding.  Money attached to work that isn’t
in the second set is at best a distraction, at worst drains your teams’ credibility.</p>

<p>Most of us in research got our experience in grants from open disciplinary competitions where the funders and fundees goals
are aligned — be seen to be funding/doing the best research.  That means you don’t have to think about the distinction
very much.  The funder wants a portfolio of projects that are promising and could have impact - some will pan out and some
won’t, but such is research.   So everyone is focussed on “the best” work.  There’s a lot of focus on methods and technology
used, because those are relevant for assessing the best work.  A new technology or method might be why it’s important to
fund this work now - some key observation wasn’t possible before, but now it is, and the funder and team who makes the
observation now will get the impact.  And methods can sabotage a project - a team that does great work with the wrong
methods won’t get the best results.</p>

<p>Special digital research infrastructure calls — like those that research computing projects typically fall under —
and calls by nonprofit funders, are different.  The funder has some particular change they want to see in the world;
some community they want to see better served.  They are generally much less willing to take a flyer on projects with
only a modest chance of success, because failures won’t serve the community they want to see served.  Something that
successfully serves the community can always be improved in future iterations; something that fails to meet the communities
needs may well be unsalvagable.</p>

<p>Methods and technology matter much less to these funders.  They want to know that you can credibly deliver on the proposal,
and that you have a plan, but the nuts and bolts typically are much less interesting.</p>

<p>A nonprofit funder absolutely wants to understand how the after-school homework tutoring program you’re proposing will
interact with the community — how it will find underserved students, how the tutoring will be delivered to the
students, what indicators will be used to measure success — but the behind the scenes tech stack like what task
management and tutor booking software you’ll use is completely irrelevant unless it’s to justify that you’ll
be able to deliver the program.  (And if you are in a position where you need details like that to justify your
credibility for delivering the program, you are probably not in serious contention for the funding).  Every paragraph
you spend talking about the cool new tutor booking software you’re going to use is a paragraph that doesn’t get spent
highlighting the funder’s goals being achieved — more underserved students doing better in school.</p>

<p>A research computing funder who’s receptive to a “we’ll run a new research data management platform specifically
aimed at [discipline X]” proposal absolutely wants to know that you’re familiar with the underserved area, that
you’ve been successful delivering similar things before, and what metrics you’ll use for success.  They do not care
that your roadmap includes Kubernetes and some exciting new operators.  Would they be disappointed if mid-stream, you
pivoted to running the tasks on bare metal with Ansible?  If not, why draw their attention and yours to obscure and
uncertain details rather than to how your work will best advance their goals?</p>

<p>The thing is, this same approach applies to not just research funders, but anyone you plan to work with; any research
group that contacts your team looking for something.  They have a problem; the greater the up-front focus on understanding
 and solving researcher’s problem, the better the chance of success.</p>

<p>How will you know what the funder’s or researcher’s problems and goals are?  In the funder’s case, the call will sometimes
spell it out; in the researcher’s case, they’ll usually say something.  In both cases, it may require some question-asking
and digging deeper; the researcher’s or even the funder’s “presenting problem” may not be the underlying issue,
and the funder’s call may focus on one particular aspect rather than the overarching goals.  But the solution is the same;
just ask a bunch of questions.</p>

<p>“Do you mean they will they just tell you?”  I know a team in a Hackathon who went to an open pre-hackathon info
session, and approached the organizer and sponsor in a gaggle afterwards.  They asked the sponsor — the lead judge — what
a successful Hackathon would be from their point of view.  The sponsor — who, again, was the <em>lead judge</em> — answered with
a particular problem they’d like solved as an example.  That team and mystifyingly only that team delivered a partial but
promising solution to the exact problem described in detail and in public, and they of course won first prize.  How could
they not?  People organize special funding calls and hackathons <em>because</em> <em>they</em> <em>want</em> <em>other</em> <em>people</em> <em>to</em> <em>help</em> <em>them</em>
<em>achieve</em> <em>their</em> <em>goals</em>.  Yes, they’ll tell you, and if you keep asking questions they’ll keep talking about it until you politely explain
that you have to leave for the evening.  They put that contact information there and run informational sessions for a reason.</p>

<p>The stakeholder side of research computing isn’t rocket surgery.  But listening, digging in, and focussing on their goals
is still rare enough that doing it well is almost an unfair advantage.</p>