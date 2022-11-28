---
author: Vanessasaurus
blog_subtitle: dinosaurs, programming, and parsnips
blog_title: VanessaSaurus
blog_url: https://vsoch.github.io/
category: vsoch
date: '2022-06-26 13:30:00'
layout: post
original_url: https://vsoch.github.io/2022/ssh-tunnels/
title: SSH Tunnels
---

<p>Today I want to talk about ssh tunnels. Very abstractly, we would want to use an ssh
tunnel to securely send information. In the case of HPC, you are probably familiar with ssh,
(Secure Shell or Secure Socket Shell) when you login to your node. You might do something like this:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>ssh dinosaur@server.address.edu
</code></pre></div></div>

<p>Or if you have a proper setup in your <code class="language-plaintext highlighter-rouge">~/.ssh/config</code> (with a named server) you might just do:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>ssh dinosaur
</code></pre></div></div>

<p>I like to use <a href="https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Multiplexing" target="_blank">ssh connection multiplexing</a>
so the connection is kept alive for a bit, but I won’t go into detail because
this post isn’t specifically about the details of ssh. The use case I’m interested in (and the thing
that HPC is very bad at) is how to deploy something interactive on an HPC cluster.</p>

<h2 id="ssh-tunnel-with-ports">SSH Tunnel with Ports</h2>

<p>Given that a cluster has exposed ports (either the login node, or both the login node and compute nodes)
creating a tunnel is fairly straight forward! In the past I created a tool called <a href="https://github.com/vsoch/forward" target="_blank">forward</a> to handle all the manual steps to get this working, meaning:</p>

<ol class="custom-counter">
  <li>Show the user <a href="https://github.com/vsoch/forward#ssh-config" target="_blank">how to set up their ~/.ssh/config</a> (once)</li>
  <li>Define (once) parameters like a port, memory, GPUs, and if the cluster has isolated nodes</li>
  <li>Start any number of provided apps that come with forward (e.g., jupyter, singularity, etc.)</li>
</ol>

<p>An interaction using forward might look like any of the following:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c"># Run a Singularity container that already exists on your resource (recommended)</span>
bash start-node.sh singularity-run /scratch/users/vsochat/share/pytorch-dev.simg

<span class="c"># Execute a custom command to the same Singularity container</span>
bash start-node.sh singularity-exec /scratch/users/vsochat/share/pytorch-dev.simg <span class="nb">echo</span> <span class="s2">"Hello World"</span>

<span class="c"># Run a Singularity container from a url, `docker://ubuntu`</span>
bash start-node.sh singularity-run docker://ubuntu

<span class="c"># Execute a custom command to the same container</span>
bash start-node.sh singularity-exec docker://ubuntu <span class="nb">echo</span> <span class="s2">"Hello World"</span>

<span class="c"># To start a jupyter notebook in a specific directory ON the cluster resource</span>
bash start.sh jupyter &lt;cluster-dir&gt;

<span class="c"># To start a jupyter notebook with tensorflow in a specific directory</span>
bash start.sh py3-tensorflow &lt;cluster-dir&gt;
</code></pre></div></div>

<p>Note that the last set of commands are pertaining to notebooks, which is where these tunnels come into play!
A notebook is going to be run on a compute node that looks something like the following:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>jupyter notebook <span class="nt">--no-browser</span> <span class="nt">--port</span><span class="o">=</span><span class="nv">$PORT</span>
</code></pre></div></div>

<p>And if you ran this with a Singularity container, you’d also want to bind jovyan’s home to be the user’s, along with the jupyter config directory:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>singularity <span class="nb">exec</span> <span class="nt">--home</span> <span class="k">${</span><span class="nv">HOME</span><span class="k">}</span> <span class="se">\</span>
    <span class="nt">--bind</span> <span class="k">${</span><span class="nv">HOME</span><span class="k">}</span>/.local:/home/jovyan/.local <span class="se">\</span>
    <span class="nt">--bind</span> <span class="k">${</span><span class="nv">HOME</span><span class="k">}</span>/.jupyter:/home/jovyan/.jupyter <span class="se">\ </span> 
    datascience_notebook.sif jupyter notebook <span class="nt">--no-browser</span> <span class="nt">--port</span><span class="o">=</span><span class="nv">$PORT</span> <span class="nt">--ip</span> 0.0.0.0
</code></pre></div></div>

<p>As we described earlier <a href="https://github.com/vsoch/forward#ssh-port-forwarding-considerations" target="_blank">here</a>,
there are subtle differences between making a tunnel (with a port) given that you have isolated nodes (or not).
You can determine this based on your ability to ssh into a non-login node (meaning where your job is running) from “the outside world”
that is your computer. If you cannot, your nodes are isolated, which we will discuss next.</p>

<h3 id="isolated-nodes">Isolated Nodes</h3>

<p>Let’s say that we need to create a tunnel (using ports) to an isolated node. This means that we are basically going
to establish a tunnel to the login node, and then from the login node another one to the compute node.
We might use a command that looks like this:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>ssh <span class="nt">-L</span> <span class="nv">$PORT</span>:localhost:<span class="nv">$PORT</span> <span class="k">${</span><span class="nv">RESOURCE</span><span class="k">}</span> ssh <span class="nt">-L</span> <span class="nv">$PORT</span>:localhost:<span class="nv">$PORT</span> <span class="nt">-N</span> <span class="s2">"</span><span class="nv">$MACHINE</span><span class="s2">"</span> &amp;
</code></pre></div></div>

<p>In the command above, the first half (<code class="language-plaintext highlighter-rouge">ssh -L $PORT:localhost:$PORT ${RESOURCE}</code>) is executed on the local machine, which establishes a port forwarding to the login node. The “-L” in the above (from the <a href="https://linuxcommand.org/lc3_man_pages/ssh1.html" target="_blank">man pages</a>) :</p>

<blockquote>
  <p>Specifies that connections to the given TCP port or Unix socket on the local (client) host are to be forwarded to the
given host and port, or Unix socket, on the remote side.
This works by allocating a socket to listen to either a TCP
port on the local side, optionally bound to the specified
bind_address, or to a Unix socket.  Whenever a connection is
made to the local port or socket, the connection is for‐
warded over the secure channel, and a connection is made to
either host port hostport, or the Unix socket remote_socket,
from the remote machine.</p>
</blockquote>

<p>Or in layman’s terms:</p>

<blockquote>
  <p>Forward whatever is running on the second port on my resource to my local machine.</p>
</blockquote>

<p>Since we are forwarding ports, this would require minimally the login node to expose ports.
The next line <code class="language-plaintext highlighter-rouge">ssh -L $PORT:localhost:$PORT -N "$MACHINE" &amp;</code> is a second command run from the login node, 
and port forwards it to the compute node, since you can only access the compute node from the login nodes.
You’ll notice it looks just like the first, and this works because ssh commands can be chained.
The <code class="language-plaintext highlighter-rouge">-N</code> says “don’t execute a remote command (and just forward the port).”
Finally, the last <code class="language-plaintext highlighter-rouge">$MACHINE</code> is the node that the jupyter notebook is running on.</p>

<h3 id="not-isolated">Not Isolated</h3>

<p>For HPCs where the compute node is not isolated from the outside world the ssh command for port forwarding first establishes a connection the login node, but then continues to pass on the login credentials to the compute node to establish a tunnel between the localhost and the port on the compute node. The ssh command in this case utilizes the flag <code class="language-plaintext highlighter-rouge">-K</code> that forwards the login credentials to the compute node:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>ssh <span class="s2">"</span><span class="nv">$DOMAINNAME</span><span class="s2">"</span> <span class="nt">-l</span> <span class="nv">$FORWARD_USERNAME</span> <span class="nt">-K</span> <span class="nt">-L</span>  <span class="nv">$PORT</span>:<span class="nv">$MACHINE</span>:<span class="nv">$PORT</span> <span class="nt">-N</span>  &amp;
</code></pre></div></div>

<p>I’m not sure in practice how common this is anymore. At least at my current employer it’s not even the case
that ports are exposed on the login node! It’s probably better that way, because in cases where you do get ports it’s sort of a 
“pick a port above this range and hope that no other user picks the same one!” It’s messy. 
So let’s talk about the case of not having ports exposed next, since this was the entire reason I wanted to write this post!</p>

<h2 id="ssh-tunnel-with-socket">SSH Tunnel with Socket</h2>

<p>More than a year ago, I had this realization that a lot of people at Stanford used the “forward” tool, and just for notebooks (and this
was before they were available via Open OnDemand, which is what I’d recommend to a Stanford user at this point). I decided I wanted to make a new 
open source tool, “tunel” (an elegant derivation of “tunnel”) <a href="https://github.com/vsoch/tunel" target="_blank">vsoch/tunel</a> to make it easy
to run what I call “apps” on an HPC cluster. Are there better ways of exposing user interfaces on HPC? Yes, indeed. But not everyone
has easy access. It was also a stubborn “I want this to work” proof of concept. This new tool would be like forward, but a little nicer.
Because I, along with every other HPC developer and user, wishes we could have nice things 😭️.</p>

<p>At this time I had just started a new role at a national lab, and I realized that none of my old techniques for launching
the job worked because of the lack of exposed ports. Thinking this was impossible, I abandoned it for a year. But then this last week I found 
<a href="https://github.com/jupyter/notebook/pull/4835" target="_blank">this</a>! I was motivated! I was excited! The basic launch command of the notebook looks like this:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>jupyter notebook <span class="nt">--sock</span> /tmp/test.sock <span class="nt">--no-browser</span>
</code></pre></div></div>

<p>And then with a different looking tunnel, we could forward this socket to the host, and map it to a port! My excitement was then brought down
by what led to two days of struggling. I first tried my entire tunel workflow, meaning launching a job on a node,
and then running that command, and providing the instruction to the user to create the tunnel as follows:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>ssh <span class="nt">-L</span> 8888:/tmp/test.sock <span class="nt">-N</span> user@this_host
</code></pre></div></div>

<p>That didn’t work (and remember this socket was created on the isolated node, that’s important to remember for later). So I started looking at the socket with “nc”  - “arbitrary TCP and UDP connections and listens” from the login node. The “-U” below is for UNIX sockets:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>nc <span class="nt">-U</span> /tmp/test.sock
</code></pre></div></div>

<p>And from the head node I saw:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Ncat: Connection refused.
</code></pre></div></div>

<p>So then I knew I needed a simpler, dummier example. I got rid of tunel and just ran the notebook command on the head node.
Dear reader, it still did not work. I <a href="https://github.com/jupyter/notebook/issues/6459" target="_blank">opened an issue</a> and asked <a href="https://twitter.com/vsoch/status/1540546526044250112" target="_blank">Twitter for help</a>. Someone else on Twitter reported that <a href="https://twitter.com/al3x609/status/1540846694262243328" target="_blank">it worked for them</a>, and that (in my opinion) is the challenge and story of HPC - given the huge differences in setups, it’s hard to reproduce what another person does unless you scope to a very specific
environment or technology and hugely go out of your way to do it. I’m always grateful when someone tries to help, but when the ultimate answer is just
“But it works on my machine!” I (and I think all of us) are like:</p>

<p><span style="font-size: 50px; color: darkorchid;">(╯°□°)╯︵ ┻━┻</span></p>

<p>🤣️</p>

<p>Please know that is intended to be funny, and I really am grateful for the attempt to help! Anyway, the first night I was devastated because I was so excited about the possibility of this working! But of course (as it usually does) my quasi-sadness turned again into relentless stubborn-ness, and for my Saturday
I embarked on trying everything. I call this the stubborn brute force approach, and it actually leads to some pretty good outcomes?</p>

<h3 id="socket-from-login-node">Socket from Login Node</h3>

<p>First from the login node, I started reading about flags in detail, again from the <a href="https://linuxcommand.org/lc3_man_pages/ssh1.html" target="_blank">man pages</a>. It occurred to me that the suggested command included “-L” (discussed earlier) but there were a ton of other flags to try, and maybe I need them for my setup? The command that wound up working (after much trial and error) was just:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c"># Running on login node</span>
<span class="nv">$ </span>ssh <span class="nt">-NT</span> <span class="nt">-L</span> 8888:/tmp/test.sock user@server
</code></pre></div></div>

<p>And here again was the suggested command:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>ssh <span class="nt">-L</span> 8888:/tmp/test.sock <span class="nt">-N</span> user@this_host
</code></pre></div></div>

<p>So they are very similar - and the main difference is the <code class="language-plaintext highlighter-rouge">-T</code> is to “Disable pseudo-terminal allocation.”
So I suspect (also based on the version of ssl I’m using) that without the flag, you might be making a request for a pty to the server
(<a href="https://stackoverflow.com/questions/10330678/gitolite-pty-allocation-request-failed-on-channel-0/10346575#10346575" target="_blank">more details here</a>) and then it could abort. Adding the flag just skips this, because we don’t need that - we just need the simple forward. And yes, this indeed feels very specific to your ssh setup, version of ssh, and server configuration. Of course, this was only the beginning of figuring things out, because I had no idea how to get this working from one level deeper - an isolated compute node.</p>

<h3 id="socket-with-isolated-nodes">Socket with Isolated Nodes</h3>

<p>Remember that when we created the socket on the isolated node and we tried this out from the login node:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>nc <span class="nt">-U</span> /tmp/test.sock
</code></pre></div></div>

<p>And the result was this:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Ncat: Connection refused.
</code></pre></div></div>

<p>My spidey senses were telling me that this should work. Indeed, when I ssh into the isolated node from the login node,
that same command allowed me to connect (meaning it hung / there was no error output). So my first task, I decided, was to try
and “forward” this socket to the login node. Again, back to the man pages! I wound up with something like this (run from the login node):</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>ssh isolated-node <span class="nt">-NT</span> <span class="nt">-L</span> /home/dinosaur/login-node.sock:/home/dinosaur/jupyter.sock
</code></pre></div></div>

<p>The above is again using <code class="language-plaintext highlighter-rouge">-L</code> but instead of a port (which aren’t exposed) we are using a socket! It’s kind of neat you can switch out those two. 
When I tried the same nc command from the login
node, we had progress (no connection refused message!) 🎉️ And then I moved this up one level to see if I could make this same request from my local machine, sort of combining the first command that worked with the login node notebook with this one. That looked like this (and yes this took more trial and error):</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>ssh <span class="nt">-NT</span> user@server ssh isolated-node <span class="nt">-NT</span> <span class="nt">-L</span> /home/dinosaur/login-node.sock:/home/dinosaur/jupyter.sock
</code></pre></div></div>

<p>And to confirm it was working, I’d ssh into the server and again run that nc command to ensure that the newly forwarded socket was readable from
the login node. After this, again with more trial and error, I tried running a second command to just forward that (now working socket) to my host.
That eventually looked like this:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="c"># And another for the local socket</span>
<span class="nv">$ </span>ssh <span class="nt">-NT</span> <span class="nt">-L</span> 8899:/home/dinosaur/login-node.sock user@server
</code></pre></div></div>

<p>And then (all together now!) I tried putting them together.</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>ssh <span class="nt">-NT</span> <span class="nt">-L</span> 8899:/home/dinosaur/login-node.sock user@server ssh isolated-node <span class="se">\</span>
       <span class="nt">-NT</span> <span class="nt">-L</span> /home/dinosaur/login-node.sock:/home/dinosaur/jupyter.sock
</code></pre></div></div>

<p>And then I spent some time integrating it into tunel, and <em>surprise!</em> the first implementation didn’t work. The first bug was that I needed to clean up old sockets each time the “same” app was run (determined by the job name and organizational namespace so the user can only run one of a particular interactive app at once, and not forget about previous runs). The second issue was about opening the tunnel - it didn’t seem to work if the process exited and/or it was run in a subshell (that also probably exits). I realized that (for the time being) running this connection step on behalf of the user, since it’s something the user should have more control over, probably wasn’t the right way to go. If the user hasn’t added something like an rsa key to <code class="language-plaintext highlighter-rouge">~/.ssh/authorized_keys</code> on their clusters, it would also ask for a password interactively, making it harder for me to manage. So for simplicity sake, and assuming that we really should put the user in control of deciding when to start/stop the tunnel, I simply print the full ssh command in the terminal and let them copy paste it. A successful connection might then prompt them for their password for that second ssh, which (by default) I don’t think is carrying forward auth from the first.</p>

<p>So that was my adventure! Mind you, this entire adventure was only about two days, and that included time to write this post, so I still have lots in front of me to work on. However, with these updated commands (and some nice tweaks from Python’s <a href="https://github.com/Textualize/rich" target="_blank">rich</a> library) I quickly had a nice set of commands to run and stop an app with an interactive jupyter notebook, and using sockets on isolated nodes!</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>tunel run-app server slurm/socket/jupyter
<span class="nv">$ </span>tunel stop-app server slurm/socket/jupyter
</code></pre></div></div>



<p>As a sidenote, one thing I like about rich is that it puts the aesthetic as a first class citizen.
So many tools just don’t consider this, and I love that with rich I can think about colors, presentation,
and even animations like spinners!</p>



<p>Getting a socket working  means I’ll be able to continue working on this library (hooray!) so if you have ideas or requests for apps
you’d like to run on HPC, assuming just this basic technology, please give me a ping and I’d love to chat and support them.
I’m also going to be requesting an allocation on the Open Science Grid, which hopefully will give me other kinds of clusters
to test on. I hope this was interesting to read, thanks for doing that!</p>