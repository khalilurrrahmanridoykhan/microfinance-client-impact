import "./styles.css";

type ReportBundle = {
    outcomes: {
        overall: OutcomeGroup;
        by_gender: Record<string, OutcomeGroup>;
        by_district: Record<string, OutcomeGroup>;
    };
    financialHealth: {
        overall: FinancialGroup;
        by_gender: Record<string, FinancialGroup>;
        by_district: Record<string, FinancialGroup>;
    };
    clientVoice: {
        active_clients: number;
        satisfaction_response_n: number;
        mean_satisfaction_score: number;
        complaint_n: number;
        complaint_rate_per_1000: number;
        complaint_resolution_rate: number;
        median_resolution_days: number;
        voluntary_exit_n: number;
        voluntary_exit_rate: number;
        complaints_by_category: Record<string, number>;
        exits_by_reason: Record<string, number>;
    };
    inclusion: { overall: { n: number; suppressed: boolean; mean_loan_control_score?: number } };
    uncertainty: { median_change_intervals: { income: { lower: number; upper: number } } };
    evaluation: { readiness: { causal_ready: boolean; reasons: string[] } };
};

type OutcomeGroup = {
    n: number;
    median_income_change: number;
    median_savings_change: number;
    median_business_profit_change: number;
    business_survival_rate: number;
    essential_expense_reduction_rate: number;
};

type FinancialGroup = {
    n: number;
    median_total_debt_service_ratio: number;
    multiple_borrowing_rate: number;
    debt_replacement_rate: number;
    support_review_flag_rate: number;
};

type DashboardView = "Overview" | "Financial health" | "Inclusion & voice" | "Methods";

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
      <button class="tab is-active" data-view="Overview" type="button" aria-current="page">Overview</button>
      <button class="tab" data-view="Financial health" type="button">Financial health</button>
      <button class="tab" data-view="Inclusion & voice" type="button">Inclusion & voice</button>
      <button class="tab" data-view="Methods" type="button">Methods</button>
    </nav>
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
    <section class="view-panel" id="view-panel" aria-live="polite" aria-label="Dashboard detail"></section>
    <footer class="footer-note">Methods and limitations are part of the product, not an appendix.</footer>
  </main>
`;

const metrics = root.querySelector<HTMLDivElement>("#metrics");

async function loadReports(): Promise<ReportBundle> {
    const [outcomes, financialHealth, clientVoice, inclusion, uncertainty, evaluation] = await Promise.all([
        fetch("./data/outcomes.json").then((response) => response.json()),
        fetch("./data/financial-health.json").then((response) => response.json()),
        fetch("./data/client-voice.json").then((response) => response.json()),
        fetch("./data/inclusion.json").then((response) => response.json()),
        fetch("./data/uncertainty.json").then((response) => response.json()),
        fetch("./data/evaluation.json").then((response) => response.json()),
    ]);
    return { outcomes, financialHealth, clientVoice, inclusion, uncertainty, evaluation };
}

function renderView(view: DashboardView, reports?: ReportBundle): void {
    const panel = document.querySelector<HTMLElement>("#view-panel");
    if (!panel) return;
    const views: Record<DashboardView, string> = {
        Overview: reports
            ? `<div class="section-heading"><p class="eyebrow">Overview</p><h3>Read the client story in three layers</h3><p>Outcome change shows what moved between two synthetic observations. Financial health shows where repayment pressure may need human attention. Client voice shows satisfaction, complaints and exit signals.</p></div><div class="detail-grid"><article class="detail-card"><span class="card-kicker">Economic outcome</span><strong>${money(reports.outcomes.overall.median_income_change)}</strong><h4>Median income change</h4><p>Half of paired synthetic clients are at or below this reported change; half are above it.</p></article><article class="detail-card"><span class="card-kicker">Resilience</span><strong>${money(reports.outcomes.overall.median_savings_change)}</strong><h4>Median savings change</h4><p>This is change in the generated savings balance, not total household wealth.</p></article><article class="detail-card"><span class="card-kicker">Business continuity</span><strong>${percent(reports.outcomes.overall.business_survival_rate)}</strong><h4>Business survival</h4><p>Share with an operating business at follow-up among the paired observations.</p></article></div><div class="comparison-block"><div><p class="eyebrow">What to notice</p><h4>Positive movement is not proof of impact</h4><p>These are paired descriptive changes in generated records. They show how the analytical workflow works, not what real borrowers experienced.</p></div><div class="signal-list"><span><b>${reports.outcomes.overall.n}</b> paired clients</span><span><b>${percent(reports.outcomes.overall.essential_expense_reduction_rate)}</b> reported essential-spending reduction</span><span><b>${percent(reports.financialHealth.overall.support_review_flag_rate)}</b> met a support-review signal</span></div></div>`
            : loadingPanel("Overview"),
        "Financial health": reports
            ? `<div class="section-heading"><p class="eyebrow">Financial health</p><h3>Signals for support, never automatic decisions</h3><p>A support signal means the synthetic record may deserve a conversation, affordability review or hardship support. It does not mean a borrower is unsafe or should be rejected.</p></div><div class="detail-grid"><article class="detail-card"><span class="card-kicker">Support signal</span><strong>${percent(reports.financialHealth.overall.support_review_flag_rate)}</strong><h4>Flagged for human review</h4><p>At least one configured signal: high total debt-service ratio, multiple borrowing or debt-replacement purpose.</p></article><article class="detail-card"><span class="card-kicker">Debt burden</span><strong>${percent(reports.financialHealth.overall.median_total_debt_service_ratio)}</strong><h4>Median total debt-service ratio</h4><p>Estimated monthly debt payments divided by monthly household income.</p></article><article class="detail-card"><span class="card-kicker">Lender overlap</span><strong>${percent(reports.financialHealth.overall.multiple_borrowing_rate)}</strong><h4>Multiple borrowing</h4><p>Share reporting at least two other lenders in the synthetic ledger.</p></article></div>${financialTable(reports.financialHealth.by_district)}<p class="table-note">Other debt payments are estimated by dividing outstanding debt by 12 months. This is a modelling assumption, not a regulatory threshold.</p>`
            : loadingPanel("Financial health"),
        "Inclusion & voice": reports
            ? `<div class="section-heading"><p class="eyebrow">Inclusion & voice</p><h3>Measure agency and service experience together</h3><p>A borrower count alone cannot show who controls the loan or whether clients feel heard. These synthetic indicators combine reported agency, satisfaction, complaints and exits.</p></div><div class="detail-grid"><article class="detail-card"><span class="card-kicker">Agency</span><strong>${reports.inclusion.overall.suppressed ? "Hidden" : score(reports.inclusion.overall.mean_loan_control_score)}</strong><h4>Loan-use control</h4><p>Average reported control score among women in the synthetic follow-up survey.</p></article><article class="detail-card"><span class="card-kicker">Experience</span><strong>${score(reports.clientVoice.mean_satisfaction_score)}/5</strong><h4>Mean satisfaction</h4><p>${reports.clientVoice.satisfaction_response_n} synthetic follow-up responses were available.</p></article><article class="detail-card"><span class="card-kicker">Client voice</span><strong>${reports.clientVoice.complaint_n}</strong><h4>Complaints recorded</h4><p>${reports.clientVoice.complaint_resolution_rate * 100}% were marked resolved in the synthetic records.</p></article></div><div class="voice-columns"><div><h4>Complaint categories</h4>${countList(reports.clientVoice.complaints_by_category)}</div><div><h4>Voluntary exit reasons</h4>${countList(reports.clientVoice.exits_by_reason)}</div></div>`
            : loadingPanel("Inclusion & voice"),
        Methods: reports
            ? `<div class="section-heading"><p class="eyebrow">Methods & limits</p><h3>Evidence before interpretation</h3><p>This dashboard is designed to make uncertainty visible. It does not turn synthetic records into evidence about real borrowers.</p></div><div class="method-grid"><article class="method-card"><span class="status-dot status-warn"></span><h4>Data layer</h4><p><strong>Synthetic</strong><br />Generated from a fixed seed and documented assumptions. No real client records are used.</p></article><article class="method-card"><span class="status-dot status-warn"></span><h4>Causal readiness</h4><p><strong>${reports.evaluation.readiness.causal_ready ? "Ready for further review" : "Not causal-ready"}</strong><br />There is no comparison group in this release.</p></article><article class="method-card"><span class="status-dot status-ok"></span><h4>Income interval</h4><p><strong>${money(reports.uncertainty.median_change_intervals.income.lower)} to ${money(reports.uncertainty.median_change_intervals.income.upper)}</strong><br />Reproducible bootstrap interval for the synthetic median change.</p></article></div><div class="method-list"><h4>Use this dashboard to</h4><ul><li>understand indicator definitions and data relationships;</li><li>compare synthetic segments as an analytical exercise; and</li><li>identify questions that require real, ethically collected evaluation data.</li></ul><h4>Do not use it to</h4><ul><li>approve, reject or price an individual loan;</li><li>claim that borrowing caused an observed change; or</li><li>describe Bangladesh's real microfinance clients.</li></ul></div>`
            : loadingPanel("Methods"),
    };
    panel.innerHTML = views[view];
}

function money(value: number): string {
    return `${value >= 0 ? "+" : ""}${Math.round(value).toLocaleString()} BDT`;
}

function percent(value: number): string {
    return `${Math.round(value * 100)}%`;
}

function score(value?: number): string {
    return value === undefined ? "Hidden" : value.toFixed(2);
}

function loadingPanel(title: string): string {
    return `<div class="section-heading"><p class="eyebrow">${title}</p><h3>Aggregate reports are loading</h3><p class="muted">The dashboard is ready. Its synthetic report bundle will appear here when available.</p></div>`;
}

function financialTable(groups: Record<string, FinancialGroup>): string {
    const rows = Object.entries(groups).map(([name, group]) => `<tr><th scope="row">${name}</th><td>${group.n}</td><td>${percent(group.median_total_debt_service_ratio)}</td><td>${percent(group.multiple_borrowing_rate)}</td><td>${percent(group.support_review_flag_rate)}</td></tr>`).join("");
    return `<div class="table-wrap"><div class="table-heading"><div><p class="eyebrow">District comparison</p><h4>Where support signals are concentrated</h4></div><span>n = paired records</span></div><table><thead><tr><th scope="col">District</th><th scope="col">Clients</th><th scope="col">Median debt burden</th><th scope="col">Multiple borrowing</th><th scope="col">Support signal</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}

function countList(values: Record<string, number>): string {
    return `<ul class="count-list">${Object.entries(values).map(([name, count]) => `<li><span>${name.replaceAll("_", " ")}</span><b>${count}</b></li>`).join("")}</ul>`;
}

let loadedReports: ReportBundle | undefined;

for (const tab of root.querySelectorAll<HTMLButtonElement>(".tab")) {
    tab.addEventListener("click", () => {
        for (const item of root.querySelectorAll<HTMLButtonElement>(".tab")) {
            const isActive = item === tab;
            item.classList.toggle("is-active", isActive);
            item.toggleAttribute("aria-current", isActive);
        }
        renderView(tab.dataset.view as DashboardView, loadedReports);
        document.querySelector<HTMLElement>("#view-panel")?.scrollIntoView({
            behavior: "smooth",
            block: "nearest",
        });
    });
}

renderView("Overview");

loadReports()
    .then((reports) => {
        if (!metrics) return;
        metrics.innerHTML = `
      <article class="metric-card"><span class="metric-label">Paired clients</span><strong>${reports.outcomes.overall.n}</strong><small>Baseline and follow-up observations</small></article>
      <article class="metric-card"><span class="metric-label">Support-review signals</span><strong>${Math.round(reports.financialHealth.overall.support_review_flag_rate * 100)}%</strong><small>Human-review signals, not decisions</small></article>
      <article class="metric-card"><span class="metric-label">Satisfaction responses</span><strong>${reports.clientVoice.satisfaction_response_n}</strong><small>Follow-up synthetic responses</small></article>
    `;
        loadedReports = reports;
        renderView("Overview", reports);
    })
    .catch(() => {
        if (metrics) metrics.innerHTML = `<p class="load-error" role="alert">Aggregate reports could not be loaded. Run <code>make webdata</code> and reload.</p>`;
        renderView("Overview");
    });
