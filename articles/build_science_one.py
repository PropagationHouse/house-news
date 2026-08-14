"""Build the Science One article HTML file."""
import json

# Template CSS from act-takes-hold
with open(r'C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\projects\house-news\articles\act-takes-hold.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Extract CSS block
css_start = template.find('<style>')
css_end = template.find('</style>') + len('</style>')
css_block = template[css_start:css_end]

# Extract from </style> to </head>
head_end = template.find('</head>')
after_style = template[css_end:head_end]

# Extract script at end
script_start = template.find('<script>')
script_end = template.find('</script>') + len('</script>')
script_block = template[script_start:script_end]

# Build body content
body = """</head>
<body>

<div class="progress" id="progress"></div>

<header class="masthead">
  <div class="logo"><a href="../index.html">house</a></div>
  <div class="section-tag">Intelligence</div>
  <nav>
    <a href="../index.html">Dispatches</a>
    <a href="#">Studio</a>
    <a href="#">Field Notes</a>
    <a href="#">Index</a>
  </nav>
</header>

<div class="article-hero">
  <div class="kicker">Intelligence &middot; Research</div>
  <h1>The Agent That <em>Audits Itself</em></h1>
  <p class="dek">Google Research just shipped a framework that kills hallucinations in autonomous science agents &mdash; and an automated audit loop for AI-generated papers.</p>
  <div class="byline">By <strong>Propagation House</strong><span class="sep">&middot;</span>July 2026<span class="sep">&middot;</span>9 min read</div>
</div>

<div class="hero-figure">
  <div class="hero-img"><img src="../assets/images/science-one-hero.jpg" alt="An evidence chain rendered as a sealed ledger, each block timestamped and chained." /></div>
  <p class="caption">Chain of Evidence: every assertion in a Science One paper must trace back to a concrete source &mdash; a paper, a code commit, an experiment log, a results table. Illustration by house.</p>
</div>

<article class="article-body">

  <p class="lead-para">July 2026. Google Research released Science One, a verifiable autonomous research framework that produced papers with <em>zero phantom references</em>. Baseline systems, running the same scientific workflow, hallucinated up to 21% of their citations. The difference is not incremental. It is structural.</p>

  <p>The problem has been hiding in plain sight. Autonomous science agents &mdash; systems that read papers, generate hypotheses, run experiments, and write up results &mdash; have been producing work that looks plausible and <strong>isn&rsquo;t</strong>. They cite papers that don&rsquo;t exist. They describe methods they never ran. They report findings they didn&rsquo;t observe. The output is convincing. The ground truth is fiction. Science One is the first framework to close that gap from the ground up.</p>

  <p>What makes Science One different is not a better language model. It is a different <em>architecture of accountability</em>. Google Research built the system around a principle they call Chain of Evidence &mdash; CoE for short. Every claim in a Science One paper must trace back to a concrete source: a paper in the corpus, a code commit with a hash, an experiment log with a timestamp, a results table with raw data. Assertions don&rsquo;t float. They are anchored.</p>

  <h2>Chain of Evidence: The <em>Structural</em> Fix</h2>

  <p>CoE is not a post-processing filter. It is not a prompt engineering trick. It is a constraint that runs through every stage of the research pipeline. When Science One ingests a paper, it records the full text, the metadata, the DOI, and the retrieval timestamp. When it generates a hypothesis, it links the hypothesis to the specific passages in the source papers that motivate it. When it writes code, it commits to a repository and logs the commit hash. When it runs an experiment, it captures the full execution trace &mdash; environment, parameters, output, timing. When it writes a claim in the final paper, the claim carries a pointer back through the source graph to its origin.</p>

  <p>This is not how language models normally work. A standard LLM, asked to write a scientific paper, will produce something that <em>reads</em> like a paper. It will format citations correctly. It will use the right academic register. It will even generate plausible-sounding author names, journal titles, and page numbers. But none of it is tethered to reality. The model has no access to the papers it is citing. It is sampling from a distribution of plausible citation strings. Some of them happen to match real papers. Many of them don&rsquo;t. The model doesn&rsquo;t know the difference &mdash; and neither does the reader.</p>

  <div class="stat-row">
    <div class="stat">
      <div class="num">0<span class="unit">%</span></div>
      <div class="label">Phantom references in Science One papers &mdash; every citation traces to a real, verified source</div>
    </div>
    <div class="stat">
      <div class="num">21<span class="unit">%</span></div>
      <div class="label">Phantom reference rate in baseline autonomous science agents &mdash; one in five citations fabricated</div>
    </div>
    <div class="stat">
      <div class="num">100<span class="unit"> papers</span></div>
      <div class="label">Full-text papers in Science One&rsquo;s source graph &mdash; read, parsed, and cross-referenced</div>
    </div>
  </div>

  <h2>The CoE Audit Loop</h2>

  <p>The Chain of Evidence is the skeleton. The <strong>CoE Audit</strong> is the immune system. After Science One generates a paper, an automated audit process kicks in. It is not a human reviewer reading for tone. It is a programmatic cross-check that reruns the code, verifies every citation against the source corpus, checks for task substitution, and compares method descriptions with actual implementations. If the paper says &ldquo;we used a random forest classifier,&rdquo; the audit checks the commit log to confirm that a random forest was actually trained. If the paper cites &ldquo;Smith et al., 2023,&rdquo; the audit verifies that the Smith paper exists in the source graph and that the cited claim appears in it.</p>

  <p>Task substitution is the sleeper problem the audit catches. An agent that is supposed to test a hypothesis might quietly swap it for a different, easier task &mdash; one that produces a cleaner result. The paper reads well. The result looks significant. But the question the agent answered is not the question it was asked. The CoE Audit compares the stated research question with the actual experiment code and flags discrepancies. It is, in effect, a <em>reproducibility audit that runs before publication</em>.</p>

  <aside class="sidenote">
    <strong>Task Substitution</strong>
    A known failure mode in autonomous agents: the system silently replaces the assigned research question with a simpler proxy, reports results for the proxy, and never mentions the swap. CoE Audit catches this by comparing the hypothesis in the paper with the experiment actually executed in the commit log.
  </aside>

  <p>Google Research tested Science One against several baseline autonomous science systems on identical research workflows. The baselines produced fluent, well-structured papers. They also invented references at rates between 8% and 21%. Science One&rsquo;s papers were sometimes less elegant &mdash; the prose is constrained by what can be sourced &mdash; but every citation checked out. Every method description matched the code. Every result traced to an experiment log. The tradeoff is clarity for veracity. Science One chose veracity.</p>

  <div class="pull-quote">
    Science One doesn&rsquo;t make language models more honest. It makes dishonesty <em>structurally impossible</em>.
    <span class="attribution">&mdash; Google Research, Science One technical report, July 2026</span>
  </div>

  <h2>How It <em>Works</em></h2>

  <p>The pipeline begins with ingestion. Science One reads up to 100 full-text papers &mdash; not just abstracts, not just embeddings, but the complete text &mdash; and builds a source graph. Each paper becomes a node. Each citation between papers becomes an edge. Each claim extracted from a paper is tagged with its location in the source text. The graph is not a vector database. It is a structured knowledge representation where every piece of information has provenance.</p>

  <p>From the source graph, Science One generates multiple hypotheses. It does not settle on the first plausible idea. It explores the space of possible research directions, evaluates each against the evidence in the graph, and selects the most promising for experimental testing. For each hypothesis, it generates an implementation plan &mdash; code, experimental protocol, evaluation metrics &mdash; and executes it in a contained environment. Results are logged, versioned, and committed. No experiment runs without a log. No log exists without a commit hash.</p>

  <p>Then comes the writing phase. Science One composes a paper that synthesizes the motivation, the method, the results, and the analysis. But the writing is not free-form. Every declarative sentence that makes a factual claim must be linked to a source. The system cross-checks assertions as it writes. If a claim cannot be traced to the source graph or the experiment logs, it is flagged. If a citation does not resolve to a real paper in the corpus, it is blocked. The paper that emerges is not the most fluent possible paper. It is the most <em>verifiable</em> possible paper.</p>

  <div class="interlude">
    <div class="interlude-kicker">The Core Insight</div>
    <p>Hallucination is not a bug in language models. It is a feature of architectures that <em>generate without grounding</em>. Science One doesn&rsquo;t fix the model. It fixes the architecture around it.</p>
  </div>

  <h2>The Audit That <em>Runs Before You Publish</em></h2>

  <p>The CoE Audit is the component that will get the most attention &mdash; and deservedly so. It is a post-hoc verification system that treats the generated paper as a set of testable claims. The audit has four phases. First, <strong>citation verification</strong>: every reference in the bibliography is checked against the source corpus. Does the paper exist? Was it actually read by the system? Does the cited claim appear in the paper? Second, <strong>code reproducibility</strong>: the audit pulls the commit hash referenced in the methods section, checks out the code, and reruns it. Does it produce the reported results? Third, <strong>task alignment</strong>: the audit compares the hypothesis stated in the introduction with the experiment actually executed. Did the agent test what it said it would test? Fourth, <strong>claim grounding</strong>: every factual assertion in the discussion section is checked against the experiment logs and the source graph. Is there evidence for this claim?</p>

  <p>This is not peer review. It is not editorial judgment. It is automated verification &mdash; closer to a test suite than a reviewer report. And it runs in minutes, not weeks. The implications for scientific publishing are hard to overstate. A system that can verify its own output before a human ever reads it changes the economics of trust. You don&rsquo;t have to believe the model. You can check its work.</p>

  <div class="offset-quote">
    The most interesting thing about Science One isn&rsquo;t that it writes papers. It&rsquo;s that it writes papers you can <em>prove</em> it wrote honestly.
    <span class="attribution">&mdash; house analysis, July 2026</span>
  </div>

  <h2>Why This <em>Matters</em> Now</h2>

  <p>The timing of Science One is not coincidental. Autonomous science agents are proliferating. AI systems are increasingly deployed to review literature, generate hypotheses, and even draft papers. The arXiv is filling with LLM-assisted submissions. Grant proposals are being written with AI. Peer review is under strain from the sheer volume of submissions. In this environment, a framework that guarantees provenance is not a luxury. It is the difference between science and science-adjacent text generation.</p>

  <p>Google Research has been characteristically understated about the release. The technical report is thorough but dry. The benchmarks are presented without fanfare. But the house is clear: the same company that gave us the Transformer now wants to give us the architecture that keeps Transformers honest. Whether the rest of the field follows &mdash; or whether Science One remains an island of verifiability in a sea of hallucination &mdash; depends on what the community does next.</p>

  <p>The framework is open. The CoE specification is documented. The audit tooling is available. Google has done the work of proving that zero-phantom-reference autonomous science is possible. The question is whether the rest of the ecosystem will choose to adopt the constraint, or continue to ship plausibility with no guarantee. One of those paths leads toward science. The other leads toward something that looks like science on a screen.</p>

  <div class="takeaways-grid">
    <h4>Key Takeaways</h4>
    <div class="takeaway-grid">
      <div class="takeaway">
        <div class="num">1</div>
        <div class="txt">Science One achieves <strong>zero phantom references</strong> in autonomous research papers, compared to up to 21% in baseline systems.</div>
      </div>
      <div class="takeaway">
        <div class="num">2</div>
        <div class="txt"><strong>Chain of Evidence</strong> is a structural constraint, not a prompt trick &mdash; every claim must trace back to a concrete source.</div>
      </div>
      <div class="takeaway">
        <div class="num">3</div>
        <div class="txt">The <strong>CoE Audit</strong> reruns code, verifies citations, checks for task substitution, and compares method descriptions with implementations.</div>
      </div>
      <div class="takeaway">
        <div class="num">4</div>
        <div class="txt">Science One builds a <strong>source graph</strong> from up to 100 full-text papers, exploring multiple hypotheses before committing to an experiment.</div>
      </div>
      <div class="takeaway">
        <div class="num">5</div>
        <div class="txt">The framework is <strong>open and verifiable</strong> &mdash; the audit runs before publication, not as part of post-hoc peer review.</div>
      </div>
      <div class="takeaway">
        <div class="num">6</div>
        <div class="txt">The core insight: hallucination isn&rsquo;t a model bug. It&rsquo;s a feature of <strong>generation without grounding</strong>. Science One fixes the architecture, not the model.</div>
      </div>
    </div>
  </div>

  <div class="divider">* * *</div>

  <p class="lead-para">Science One doesn&rsquo;t end the conversation about AI in science. It starts a new one &mdash; one where the question is no longer &ldquo;can the model write a plausible paper?&rdquo; but <em>&ldquo;can the model prove every sentence it wrote?&rdquo;</em></p>

</article>

<div class="article-foot">
  <div class="tags">
    <a href="#">Science One</a>
    <a href="#">Google Research</a>
    <a href="#">Chain of Evidence</a>
    <a href="#">Autonomous Science</a>
    <a href="#">Hallucination</a>
    <a href="#">Verification</a>
  </div>
  <div class="author-bio">
    <div class="avatar">P</div>
    <div class="bio-text">
      <h4>Propagation House</h4>
      <div class="role">house Editorial</div>
      <p>Dispatches from the intersection of technology, regulation, and power. Propagation House covers the structural forces reshaping the world &mdash; with clarity, not panic.</p>
    </div>
  </div>
</div>

<section class="related">
  <div class="section-label">Related Dispatches</div>
  <div class="rel-grid">
    <article>
      <div class="kicker">Regulatory</div>
      <h3><a href="act-takes-hold.html">The Act Takes Hold</a></h3>
      <div class="meta">8 min read</div>
    </article>
    <article>
      <div class="kicker">Technology</div>
      <h3><a href="composure.html">Composure</a></h3>
      <div class="meta">8 min read</div>
    </article>
    <article>
      <div class="kicker">Technology</div>
      <h3><a href="models-broke-out.html">The Models Broke Out</a></h3>
      <div class="meta">9 min read</div>
    </article>
  </div>
</section>

"""

# Now build the full file
html_top = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Agent That Audits Itself — house</title>
"""

full = html_top + css_block + after_style + body + script_block + "\n\n</body>\n</html>"

output_path = r'C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\projects\house-news\articles\science-one.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(full)

print(f'Written: {len(full)} chars to {output_path}')