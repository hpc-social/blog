---
author: Vanessasaurus
blog_subtitle: dinosaurs, programming, and parsnips
blog_title: VanessaSaurus
blog_url: https://vsoch.github.io/
category: vsoch
date: '2021-09-19 09:30:00'
layout: post
original_url: https://vsoch.github.io/2021/uptodate/
title: Uptodate
---

<p>I recently had an itch to scratch - and that itch was writing a library in Go.
We don’t use Go much for my work, so I figured out a compelling reason to start a new personal project -
a command line tool written in Go (and matching GitHub action) to help keep things up to
date in a repository. Appropriately, I called it <a href="https://vsoch.github.io/uptodate/docs/#/" target="_blank">uptodate</a>!
It was hugely inspired from the <a href="https://github.com/autamus/binoc" target="_blank">binoc</a> (short for “binoculars”)
library that can also perform specific kinds of updates, but I wanted more of a focus on
Docker, and to have total control so I could go wild and crazy with writing Go code
without worrying about forcing it on the owner, <a href="https://github.com/alecbcs" target="_blank">alecbcs</a>, to merge my wild ideas.</p>

<p><br /></p>

<div class="padding:20px">
<img src="https://vsoch.github.io/uptodate/assets/img/uptodate.png" />
</div>

<h2 id="uptodate">Uptodate</h2>

<p>Uptodate is a command line tool in Go and GitHub action that makes it easy to:</p>

<ol class="custom-counter">
  <li> Update FROM statements in Dockerfile to have the latest shas</li>
  <li> Update build arguments that are for spack versions, GitHub releases and commits, and container hashes.</li>
  <li> Generate a matrix of Docker builds from a single configuration file</li>
  <li> Generate a matrix of changed files in a repository.</li>
  <li> List Dockerfile in a repository that have been changed.</li>
</ol>

<p>With all of the above, you can imagine a workflow that first updates Dockerfile
FROM statements and build args, and then re-builds and deploys these containers - 
the assumption being that the underlying dependency such as a GitHub commit
or spack version has an update. Uptodate also will take a nested structure
that I call a docker “build hierarchy” and add new folders and Dockerfile when
a new tag is detected. A kind of updater in uptodate is naturally called an “updater”
and this means for the docker build and docker hierarchy updaters, we can write
a yaml configuration file with our preferences for versions to be added, and
other metadata. You should check out the <a href="https://vsoch.github.io/uptodate/docs/#/user-guide/user-guide" target="_blank">user guide</a>
for detailed usage, or read about <a href="https://vsoch.github.io/uptodate/docs/#/user-guide/github-action" target="_blank">the GitHub action</a></p>

<h2 id="how-does-it-work">How does it work?</h2>

<p>I’ll give a brief overview of a few of the commands and then a quick example GitHub workflow,
and I’ll recommend that you read the documentation for the latest updates on uptodate, harharhar.
The examples below assumed that you’ve <a href="https://vsoch.github.io/uptodate/docs/#/user-guide/user-guide?id=install" target="_blank">installed</a> uptodate 
and have the binary “uptodate” in your path.</p>

<h3 id="dockerfile">Dockerfile</h3>

<p>If you have one or more Dockerfile in your repository you can run uptodate to update digests.
For example:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ uptodate dockerfile .
</code></pre></div></div>

<p>will find Dockerfile in the present working directory and subfolders and update.
For digests, you might see that:</p>

<div class="language-dockerfile highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">FROM</span><span class="s"> ubuntu:20.04</span>
</code></pre></div></div>

<p>is updated to</p>

<div class="language-dockerfile highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">FROM</span><span class="s"> ubuntu:18.04@sha256:9bc830af2bef73276515a29aa896eedfa7bdf4bdbc5c1063b4c457a4bbb8cd79</span>
</code></pre></div></div>

<p>Note in the above we still have the digest and the tag, so subsequent updates can
further update the sha by looking up the container based on the tag.
And we can also update build arguments that match a particular format! This one,
specifically:</p>

<div class="language-dockerfile highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">ARG</span><span class="s"> uptodate_&lt;build-arg-type&gt;_&lt;build-arg-value&gt;=&lt;default&gt;</span>
</code></pre></div></div>

<p>The above flags the build argument for uptodate to look at using the prefix of the library
name, and then the next string after the underscore is the kind of update, followed by
specific metadata for that updater, and of course the value! A few examples are provided below.</p>

<h4 id="spack-build-arguments">Spack Build Arguments</h4>

<p><a href="https://github.com/spack/spack" target="_blank">Spack</a> is a package manager intended for HPC, and it’s
huge at the lab where I work. So naturally, it made sense for uptodate to be able to
look up the latest spack versions for some package.
To create an argument that matched to a spack package (and its version) you might see:</p>

<div class="language-dockerfile highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">ARG</span><span class="s"> uptodate_spack_ace=6.5.6</span>
</code></pre></div></div>

<p>After the updater runs, if it finds a new version 6.5.12, the line will read:</p>

<div class="language-dockerfile highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">ARG</span><span class="s"> uptodate_spack_ace=6.5.12</span>
</code></pre></div></div>

<p>This works by using the static API that is deployed alongside the <a href="https://spack.github.io/packages/" target="_blank">Spack Packages</a>
repository that I designed earlier this year. So the updater will get the latest versions
as known within the last 24 hours.</p>

<h4 id="github-release-build-argument">GitHub Release Build Argument</h4>

<p>If we want an updated version from a GitHub release (let’s say the spack software itself)
we might see this:</p>

<div class="language-dockerfile highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">ARG</span><span class="s"> uptodate_github_release_spack__spack=v0.16.1</span>
</code></pre></div></div>

<p>The above will look for new releases from spack on GitHub and update as follows:</p>

<div class="language-dockerfile highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">ARG</span><span class="s"> uptodate_github_release_spack__spack=v0.16.2</span>
</code></pre></div></div>

<h4 id="github-commit-build-argument">GitHub Commit Build Argument</h4>

<p>Similarity, if we want more “bleeding edge” changes we can ask for a commit
from a specific branch, following this pattern:</p>

<div class="language-dockerfile highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">ARG</span><span class="s"> uptodate_github_commit_&lt;org&gt;__&lt;name&gt;__&lt;branch&gt;=&lt;release-tag&gt;</span>
</code></pre></div></div>

<p>Here is an example of asking for updates for the develop branch.</p>

<div class="language-dockerfile highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">ARG</span><span class="s"> uptodate_github_commit_spack__spack__develop=NA</span>
</code></pre></div></div>

<p>which wouldn’t care about the first “commit” NA as it would update to:</p>

<div class="language-dockerfile highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">ARG</span><span class="s"> uptodate_github_commit_spack__spack__develop=be8e52fbbec8106150680fc628dc72e69e5a20be</span>
</code></pre></div></div>

<p>And then to use it in your Dockerfile, you might pop into an environment variable:</p>

<div class="language-dockerfile highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">ENV</span><span class="s"> spack_commit=${uptodate_github_commit_spack__spack__develop}</span>
</code></pre></div></div>

<p>See the <a href="https://vsoch.github.io/uptodate/docs/#/user-guide/user-guide?id=dockerfile" target="_blank">docs</a> for more detailed usage and an example for the Dockerfile updater.</p>

<h3 id="docker-build">Docker Build</h3>

<p>The second updater that I think is pretty useful is the Docker build updater.
This updated will read a config file, an uptodate.yaml, and then follow instructions
for version regular expressoins and different kinds of builds args to generate a matrix of
builds (intended for GitHub actions). For example, let’s say that we start with this configuration file:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="na">dockerbuild</span><span class="pi">:</span>
  <span class="na">build_args</span><span class="pi">:</span>

    <span class="c1"># This is an example of a manual build arg, versions are required</span>
    <span class="na">llvm_version</span><span class="pi">:</span>

      <span class="c1"># The key is a shorthand used for naming (required)</span>
      <span class="na">key</span><span class="pi">:</span> <span class="s">llvm</span>
      <span class="na">versions</span><span class="pi">:</span>
       <span class="pi">-</span> <span class="s2">"</span><span class="s">4.0.0"</span>
       <span class="pi">-</span> <span class="s2">"</span><span class="s">5.0.1"</span>
       <span class="pi">-</span> <span class="s2">"</span><span class="s">6.0.0"</span>

    <span class="c1"># This is an example of a spack build arg, the name is the package</span>
    <span class="na">abyss_version</span><span class="pi">:</span>
      <span class="na">key</span><span class="pi">:</span> <span class="s">abyss</span>
      <span class="na">name</span><span class="pi">:</span> <span class="s">abyss</span>
      <span class="na">type</span><span class="pi">:</span> <span class="s">spack</span>

    <span class="c1"># This will be parsed by the Dockerfile parser, name is the container name</span>
    <span class="na">ubuntu_version</span><span class="pi">:</span>

      <span class="na">key</span><span class="pi">:</span> <span class="s">ubuntu</span>
      <span class="na">name</span><span class="pi">:</span> <span class="s">ubuntu</span>
      <span class="na">type</span><span class="pi">:</span> <span class="s">container</span>
      <span class="na">startat</span><span class="pi">:</span> <span class="s2">"</span><span class="s">16.04"</span>
      <span class="na">endat</span><span class="pi">:</span> <span class="s2">"</span><span class="s">20.04"</span>
      <span class="na">filter</span><span class="pi">:</span> 
        <span class="pi">-</span> <span class="s2">"</span><span class="s">^[0-9]+[.]04$"</span> 
      <span class="na">skips</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="s2">"</span><span class="s">17.04"</span>
      <span class="pi">-</span> <span class="s2">"</span><span class="s">19.04"</span>
</code></pre></div></div>

<p>You’ll see the primary section of interest is under “dockerbuild” and under this
we have three build args for a manually defined set of versions, a version from
a spack package, and a container. You could run this in a repository root
to look for these config files (and a Dockerfile that they render with in
the same directory or below it) to generate a build matrix.</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>uptodate dockerbuild 
</code></pre></div></div>

<p>Or to only include changed uptodate.yaml files:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>uptodate dockerbuild <span class="nt">--changes</span>
</code></pre></div></div>

<p>If you provide a registry URI that the containers build to, we can actually check
these containers to look at current build args (that are saved as labels and then
viewable in the image config by uptodate) to determine if an update is needed.</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>uptodate dockerbuild <span class="nt">--registry</span> ghcr.io/rse-radiuss
</code></pre></div></div>

<p>the container. I think this is one of the neatest features - it was just added
in evenings this last week! Check out an
<a href="https://crane.ggcr.dev/config/ghcr.io/rse-radiuss/ubuntu:20.04" target="_blank">example image config</a> that has these labels!
This registry URI will also be included in the output to make it easy to build
In a GitHub action, it might be used like this:</p>

<div class="language-yaml highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="na">jobs</span><span class="pi">:</span>
  <span class="na">generate</span><span class="pi">:</span>
    <span class="na">name</span><span class="pi">:</span> <span class="s">Generate Build Matrix</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>
    <span class="na">outputs</span><span class="pi">:</span>
      <span class="na">dockerbuild_matrix</span><span class="pi">:</span> <span class="s">${{ steps.dockerbuild.outputs.dockerbuild_matrix }}</span>
      <span class="na">empty_matrix</span><span class="pi">:</span> <span class="s">${{ steps.dockerbuild.outputs.dockerbuild_matrix_empty }}</span>

    <span class="na">steps</span><span class="pi">:</span>
    <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
      <span class="na">if</span><span class="pi">:</span> <span class="s">github.event_name == 'pull_request'</span>
      <span class="na">with</span><span class="pi">:</span>
         <span class="na">fetch-depth</span><span class="pi">:</span> <span class="m">0</span>
         <span class="na">ref</span><span class="pi">:</span> <span class="s">${{ github.event.pull_request.head.ref }}</span>

    <span class="pi">-</span> <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>
      <span class="na">if</span><span class="pi">:</span> <span class="s">github.event_name != 'pull_request'</span>
      <span class="na">with</span><span class="pi">:</span>
         <span class="na">fetch-depth</span><span class="pi">:</span> <span class="m">0</span>

    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Generate Build Matrix</span>
      <span class="na">uses</span><span class="pi">:</span> <span class="s">vsoch/uptodate@main</span>
      <span class="na">id</span><span class="pi">:</span> <span class="s">dockerbuild</span>
      <span class="na">with</span><span class="pi">:</span> 
        <span class="na">root</span><span class="pi">:</span> <span class="s">.</span>
        <span class="na">parser</span><span class="pi">:</span> <span class="s">dockerbuild</span>
        <span class="na">flags</span><span class="pi">:</span> <span class="s2">"</span><span class="s">--registry</span><span class="nv"> </span><span class="s">ghcr.io/myreponame"</span>

    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">View and Check Build Matrix Result</span>
      <span class="na">env</span><span class="pi">:</span>
        <span class="na">result</span><span class="pi">:</span> <span class="s">${{ steps.dockerbuild.outputs.dockerbuild_matrix }}</span>
      <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">echo ${result}</span>

  <span class="na">build</span><span class="pi">:</span>
    <span class="na">needs</span><span class="pi">:</span>
      <span class="pi">-</span> <span class="s">generate</span>
    <span class="na">runs-on</span><span class="pi">:</span> <span class="s">ubuntu-latest</span>
    <span class="na">strategy</span><span class="pi">:</span>
      <span class="na">fail-fast</span><span class="pi">:</span> <span class="no">false</span>
      <span class="na">matrix</span><span class="pi">:</span>
        <span class="na">result</span><span class="pi">:</span> <span class="s">${{ fromJson(needs.generate.outputs.dockerbuild_matrix) }}</span>
    <span class="na">if</span><span class="pi">:</span> <span class="s">${{ needs.generate.outputs.empty_matrix == 'false' }}</span>

    <span class="na">name</span><span class="pi">:</span> <span class="s2">"</span><span class="s">Build</span><span class="nv"> </span><span class="s">${{</span><span class="nv"> </span><span class="s">matrix.result.container_name</span><span class="nv"> </span><span class="s">}}"</span>
    <span class="na">steps</span><span class="pi">:</span>
    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Checkout Repository</span>
      <span class="na">uses</span><span class="pi">:</span> <span class="s">actions/checkout@v2</span>

    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Set up Docker Buildx</span>
      <span class="na">uses</span><span class="pi">:</span> <span class="s">docker/setup-buildx-action@v1</span>

    <span class="pi">-</span> <span class="na">name</span><span class="pi">:</span> <span class="s">Build ${{ matrix.result.container_name }}</span>
      <span class="na">id</span><span class="pi">:</span> <span class="s">builder</span>
      <span class="na">env</span><span class="pi">:</span>
        <span class="na">container</span><span class="pi">:</span> <span class="s">${{ matrix.result.container_name }}</span>
        <span class="na">prefix</span><span class="pi">:</span> <span class="s">${{ matrix.result.command_prefix }}</span>
        <span class="na">filename</span><span class="pi">:</span> <span class="s">${{ matrix.result.filename }}</span>
      <span class="na">run</span><span class="pi">:</span> <span class="pi">|</span>
        <span class="s">basedir=$(dirname $filename)</span>
        <span class="s">cd $basedir</span>
        <span class="s">${prefix} -t ${container} .</span>
</code></pre></div></div>

<p>Of course you’d want to login to a registry, and then also possibly calculate metrics for
the container, so consider this a very simple example.
The build matrix that is being passed between those steps has entries like this:</p>

<div class="language-json highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">[</span><span class="w">
  </span><span class="p">{</span><span class="w">
    </span><span class="nl">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"ubuntu/clang/uptodate.yaml"</span><span class="p">,</span><span class="w">
    </span><span class="nl">"container_name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"ghcr.io/rse-radiuss/clang-ubuntu-20.04:llvm-10.0.0"</span><span class="p">,</span><span class="w">
    </span><span class="nl">"filename"</span><span class="p">:</span><span class="w"> </span><span class="s2">"ubuntu/clang/Dockerfile"</span><span class="p">,</span><span class="w">
    </span><span class="nl">"parser"</span><span class="p">:</span><span class="w"> </span><span class="s2">"dockerbuild"</span><span class="p">,</span><span class="w">
    </span><span class="nl">"buildargs"</span><span class="p">:</span><span class="w"> </span><span class="p">{</span><span class="w">
      </span><span class="nl">"llvm_version"</span><span class="p">:</span><span class="w"> </span><span class="s2">"10.0.0"</span><span class="p">,</span><span class="w">
      </span><span class="nl">"ubuntu_version"</span><span class="p">:</span><span class="w"> </span><span class="s2">"20.04"</span><span class="w">
    </span><span class="p">},</span><span class="w">
    </span><span class="nl">"command_prefix"</span><span class="p">:</span><span class="w"> </span><span class="s2">"docker build -f Dockerfile --build-arg llvm_version=10.0.0 --build-arg ubuntu_version=20.04"</span><span class="p">,</span><span class="w">
    </span><span class="nl">"description"</span><span class="p">:</span><span class="w"> </span><span class="s2">"ubuntu/clang llvm_version:10.0.0 ubuntu_version:20.04"</span><span class="w">
  </span><span class="p">},</span><span class="w">
  </span><span class="err">...</span><span class="w">
</span><span class="p">]</span><span class="w">
</span></code></pre></div></div>

<h3 id="git-updater">Git Updater</h3>

<p>I also like this updater because it easily generates for you a matrix of files
that are changed, according to git. Running locally it looks like this:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>./uptodate git /path/to/repo
              _            _       _       
  _   _ _ __ | |_ ___   __| | __ _| |_ ___ 
 | | | | <span class="s1">'_ \| __/ _ \ / _  |/ _  | __/ _ \
 | |_| | |_) | || (_) | (_| | (_| | ||  __/
  \__,_| .__/ \__\___/ \__,_|\__,_|\__\___|
       |_|                          git


  ⭐️ Changed Files ⭐️
    .github/workflows/build-matrices.yaml: Modify
</span></code></pre></div></div>

<p>And would generate a matrix for a GitHub action too:</p>

<div class="language-json highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="p">[</span><span class="w">
  </span><span class="p">{</span><span class="w">
    </span><span class="nl">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Modify"</span><span class="p">,</span><span class="w">
    </span><span class="nl">"filename"</span><span class="p">:</span><span class="w"> </span><span class="s2">"cli/dockerbuild.go"</span><span class="w">
  </span><span class="p">},</span><span class="w">
  </span><span class="p">{</span><span class="w">
    </span><span class="nl">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Modify"</span><span class="p">,</span><span class="w">
    </span><span class="nl">"filename"</span><span class="p">:</span><span class="w"> </span><span class="s2">"parsers/common.go"</span><span class="w">
  </span><span class="p">},</span><span class="w">
  </span><span class="p">{</span><span class="w">
    </span><span class="nl">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Insert"</span><span class="p">,</span><span class="w">
    </span><span class="nl">"filename"</span><span class="p">:</span><span class="w"> </span><span class="s2">"parsers/docker/buildargs.go"</span><span class="w">
  </span><span class="p">},</span><span class="w">
  </span><span class="p">{</span><span class="w">
    </span><span class="nl">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Modify"</span><span class="p">,</span><span class="w">
    </span><span class="nl">"filename"</span><span class="p">:</span><span class="w"> </span><span class="s2">"parsers/docker/docker.go"</span><span class="w">
  </span><span class="p">},</span><span class="w">
  </span><span class="p">{</span><span class="w">
    </span><span class="nl">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Modify"</span><span class="p">,</span><span class="w">
    </span><span class="nl">"filename"</span><span class="p">:</span><span class="w"> </span><span class="s2">"tests/ubuntu/21.04/Dockerfile"</span><span class="w">
  </span><span class="p">},</span><span class="w">
  </span><span class="p">{</span><span class="w">
    </span><span class="nl">"name"</span><span class="p">:</span><span class="w"> </span><span class="s2">"Modify"</span><span class="p">,</span><span class="w">
    </span><span class="nl">"filename"</span><span class="p">:</span><span class="w"> </span><span class="s2">"tests/ubuntu/clang/Dockerfile"</span><span class="w">
  </span><span class="p">}</span><span class="w">
</span><span class="p">]</span><span class="w">
</span></code></pre></div></div>

<p>And of course you can change the default “main” to another branch:</p>

<div class="language-bash highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nv">$ </span>./uptodate git /path/to/repo <span class="nt">--branch</span> master
</code></pre></div></div>

<p>and that also pipes into a GitHub action. I don’t want to redundantly reproduce the docs,
so if you are interested you can read more
at the <a href="https://vsoch.github.io/uptodate/docs/#/user-guide/user-guide" target="_blank">user guide</a>
or <a href="https://vsoch.github.io/uptodate/docs/#/user-guide/github-action" target="_blank">GitHub action pages</a>.
Mind you that the library is heavily under develop, so if you have a request for a new updater or want to report
a a bug, please <a href="https://github.com/vsoch/uptodate/issues" target="_blank">let me know!</a>.</p>

<h2 id="overview">Overview</h2>

<p>I have loved working on this library. I think it’s the first library in Go where
I’ve been proficient enough to not look everything up that I need - the code has just
flowed from my fingers! Mind you I’m still figuring out my own design preferences,
and I’m at the stage where I’ll write a new functionality, and then immediately not like
my design, and want to re-write it. But I think that means I’ll eventually get better.
But it’s always good to have one or more projects you are passionate about, because
I don’t personally see a point in being a software engineer if I don’t (yes, I know it
makes a salary, but I require more than that).</p>