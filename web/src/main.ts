import "./styles.css";

type ReportBundle = {
  outcomes: { overall: { n: number; median_income_change: number } };
  financialHealth: { overall: { support_review_flag_rate: number } };
  clientVoice: { satisfaction_response_n: number };
};

const root = document.querySelector<HTMLDivElement>("#root");

if (!root) {
  throw new Error("Dashboard root element was not found.");
}

root.innerHTML = `
  <main class="app-shell">
    <header class="topbar">
      <div>
        <p class="eyebrow">Client impact observatory</p>
        <h1>Microfinance client wellbeing</h1>
      </div>
      <span class="data-badge">SYNTHETIC DATA</span>
    </header>
    <nav class="tabs" aria-label="Dashboard sections">
      <button class="tab is-active" type="button" aria-current="page">Overview</button>
      <button class="tab" type="button">Financial health</button>
      <button class="tab" type="button">Inclusion & voice</button>
      <button class="tab" type="button">Methods</button>
    </nav>
    <section class="notice" aria-label="Data notice">
      <strong>Illustrative analysis</strong>
      <span>This dashboard uses generated records and cannot describe real borrowers or make credit decisions.</span>
    </section>
    <section class="hero-grid">
      <div>
        <p class="eyebrow">Paired observation view</p>
        <h2>Are clients becoming more resilient without taking on unsafe debt?</h2>
        <p class="lede">Track reported change, financial-health signals and client voice together. Every result carries its source layer and limits.</p>
      </div>
      <div class="hero-mark" aria-hidden="true"><span>CI</span><i></i><i></i><i></i></div>
    </section>
    <section class="metric-grid" aria-label="Dashboard status" id="metrics" aria-live="polite">
      <article class="metric-card"><span class="metric-label">Outcome coverage</span><strong>Loading</strong><small>Paired baseline and follow-up</small></article>
      <article class="metric-card"><span class="metric-label">Financial health</span><strong>Loading</strong><small>Support signals, not decisions</small></article>
      <article class="metric-card"><span class="metric-label">Client voice</span><strong>Loading</strong><small>Satisfaction and complaints</small></article>
    </section>
    <footer class="footer-note">Methods and limitations are part of the product, not an appendix.</footer>
  </main>
`;

const metrics = root.querySelector<HTMLDivElement>("#metrics");

async function loadReports(): Promise<ReportBundle> {
  const [outcomes, financialHealth, clientVoice] = await Promise.all([
    fetch("./data/outcomes.json").then((response) => response.json()),
    fetch("./data/financial-health.json").then((response) => response.json()),
    fetch("./data/client-voice.json").then((response) => response.json()),
  ]);
  return { outcomes, financialHealth, clientVoice };
}

loadReports()
  .then((reports) => {
    if (!metrics) return;
    metrics.innerHTML = `
      <article class="metric-card"><span class="metric-label">Paired clients</span><strong>${reports.outcomes.overall.n}</strong><small>Baseline and follow-up observations</small></article>
      <article class="metric-card"><span class="metric-label">Support-review signals</span><strong>${Math.round(reports.financialHealth.overall.support_review_flag_rate * 100)}%</strong><small>Human-review signals, not decisions</small></article>
      <article class="metric-card"><span class="metric-label">Satisfaction responses</span><strong>${reports.clientVoice.satisfaction_response_n}</strong><small>Follow-up synthetic responses</small></article>
    `;
  })
  .catch(() => {
    if (metrics) metrics.innerHTML = `<p class="load-error" role="alert">Aggregate reports could not be loaded. Run <code>make webdata</code> and reload.</p>`;
  });

for (const tab of root.querySelectorAll<HTMLButtonElement>(".tab")) {
  tab.addEventListener("click", () => {
    for (const item of root.querySelectorAll<HTMLButtonElement>(".tab")) {
      item.classList.toggle("is-active", item === tab);
      item.toggleAttribute("aria-current", item === tab);
    }
  });
}
