# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "matplotlib",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Multi-Armed Bandits: Why Greedy Agents Fail

    A classic problem in decision theory: you face multiple options ("arms") with unknown rewards. Each pull reveals a sample from that arm's reward distribution. The dilemma: **explore** to learn which arm is best, or **exploit** the arm you currently believe is best.

    This is the same trade-off every AI agent faces when choosing which skill to invoke, which data source to query, or which market to trade.
    """).callout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Setup

    We have $K$ arms. Each arm $k$ has a true mean reward $\mu_k$ drawn from a normal distribution. When you pull arm $k$, you observe $\mu_k + \mathcal{N}(0, 1)$.

    Three strategies compared:

    | Strategy | Rule |
    |----------|------|
    | **Greedy** | Always pull the arm with highest *sample mean* so far. No exploration. |
    | **$\epsilon$-Greedy** | With probability $\epsilon$, explore randomly. With probability $1-\epsilon$, exploit the best sample mean. |
    | **Thompson Sampling** | Maintain a posterior belief over each $\mu_k$, then sample from that posterior and pull the arm with highest sampled value. |

    Thompson Sampling is Bayesian: it naturally balances exploration (arms with uncertain posteriors get a chance to win the sample) and exploitation (arms with high sample means are likely to win).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    n_arms_slider = mo.ui.slider(2, 10, value=5, label="Number of arms (K)")
    epsilon_slider = mo.ui.slider(0.0, 1.0, value=0.1, step=0.05, label="Epsilon (exploration rate)")
    n_steps_slider = mo.ui.slider(100, 2000, value=500, step=100, label="Number of pulls")
    n_runs_slider = mo.ui.slider(10, 200, value=50, step=10, label="Monte Carlo runs (for smooth curves)")

    controls = mo.hstack([n_arms_slider, epsilon_slider, n_steps_slider, n_runs_slider], wrap=True)
    controls
    return n_arms_slider, epsilon_slider, n_steps_slider, n_runs_slider, controls


@app.cell(hide_code=True)
def _(np, plt):
    def run_bandit_experiment(K, n_steps, epsilon, n_runs, strategy="epsilon-greedy"):
        """Run n_runs independent bandit experiments, return cumulative regret."""
        regrets = np.zeros((n_runs, n_steps))
        for run in range(n_runs):
            # True means (unknown to agent)
            true_means = np.random.normal(0, 1, K)
            best_mean = true_means.max()

            # Agent's state
            counts = np.zeros(K)
            sums = np.zeros(K)

            for t in range(n_steps):
                if strategy == "greedy":
                    # Break ties randomly
                    q_values = np.where(counts > 0, sums / counts, 0)
                    max_q = q_values.max()
                    candidates = np.where(q_values == max_q)[0]
                    arm = np.random.choice(candidates)
                elif strategy == "epsilon-greedy":
                    if np.random.random() < epsilon:
                        arm = np.random.randint(K)
                    else:
                        q_values = np.where(counts > 0, sums / counts, 0)
                        max_q = q_values.max()
                        candidates = np.where(q_values == max_q)[0]
                        arm = np.random.choice(candidates)
                elif strategy == "thompson":
                    # Sample from posterior: N(mu_hat, 1/(n+1))
                    # Prior: mu ~ N(0, 1), likelihood: N(mu, 1), so posterior precision = n+1
                    samples = np.random.normal(
                        loc=np.where(counts > 0, sums / counts, 0),
                        scale=np.sqrt(1.0 / (counts + 1))
                    )
                    arm = np.argmax(samples)

                # Pull
                reward = np.random.normal(true_means[arm], 1.0)
                counts[arm] += 1
                sums[arm] += reward
                regrets[run, t] = best_mean - true_means[arm]

        cumulative_regret = regrets.cumsum(axis=1)
        return cumulative_regret.mean(axis=0), cumulative_regret.std(axis=0)
    return (run_bandit_experiment,)


@app.cell(hide_code=True)
def _(mo):
    run_button = mo.ui.run_button(label="Run Experiment")
    run_button
    return (run_button,)


@app.cell(hide_code=True)
def _(run_button, n_arms_slider, epsilon_slider, n_steps_slider, n_runs_slider, run_bandit_experiment):
    K = n_arms_slider.value
    n_steps = n_steps_slider.value
    epsilon = epsilon_slider.value
    n_runs = n_runs_slider.value

    if run_button.value:
        greedy_mean, greedy_std = run_bandit_experiment(K, n_steps, 0, n_runs, "greedy")
        egreedy_mean, egreedy_std = run_bandit_experiment(K, n_steps, epsilon, n_runs, "epsilon-greedy")
        thompson_mean, thompson_std = run_bandit_experiment(K, n_steps, 0, n_runs, "thompson")

        results = {
            "greedy": {"mean": greedy_mean, "std": greedy_std},
            "epsilon": {"mean": egreedy_mean, "std": egreedy_std},
            "thompson": {"mean": thompson_mean, "std": thompson_std},
        }
    else:
        results = None

    return K, epsilon, n_runs, n_steps, results


@app.cell(hide_code=True)
def _(plt, mo, results, n_steps):
    if results is None:
        output = mo.md("Click **Run Experiment** above to see the comparison.")
    else:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        steps = np.arange(1, n_steps + 1)

        # Plot 1: Cumulative Regret
        ax = axes[0]
        ax.plot(steps, results["greedy"]["mean"], label="Greedy", color="#EF4444", linewidth=2)
        ax.fill_between(steps, results["greedy"]["mean"] - results["greedy"]["std"],
                        results["greedy"]["mean"] + results["greedy"]["std"], alpha=0.15, color="#EF4444")

        ax.plot(steps, results["epsilon"]["mean"], label=f"$\\epsilon$-Greedy", color="#F59E0B", linewidth=2)
        ax.fill_between(steps, results["epsilon"]["mean"] - results["epsilon"]["std"],
                        results["epsilon"]["mean"] + results["epsilon"]["std"], alpha=0.15, color="#F59E0B")

        ax.plot(steps, results["thompson"]["mean"], label="Thompson Sampling", color="#34D399", linewidth=2)
        ax.fill_between(steps, results["thompson"]["mean"] - results["thompson"]["std"],
                        results["thompson"]["mean"] + results["thompson"]["std"], alpha=0.15, color="#34D399")

        ax.set_xlabel("Number of pulls")
        ax.set_ylabel("Cumulative Regret")
        ax.set_title("Cumulative Regret Over Time")
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.2)

        # Plot 2: Instant regret (last 100 steps)
        ax = axes[1]
        window = min(100, n_steps)
        window_slice = slice(-window, None)

        strategies = ["Greedy", "$\\epsilon$-Greedy", "Thompson"]
        means = [results["greedy"]["mean"][window_slice].mean(),
                 results["epsilon"]["mean"][window_slice].mean(),
                 results["thompson"]["mean"][window_slice].mean()]
        colors = ["#EF4444", "#F59E0B", "#34D399"]

        bars = ax.bar(strategies, means, color=colors, edgecolor="white", linewidth=0.5)
        ax.set_ylabel(f"Avg Regret (last {window} pulls)")
        ax.set_title("Exploitation Quality")
        ax.grid(True, alpha=0.2, axis="y")

        fig.tight_layout()
        plot_output = fig
    plot_output
    return


@app.cell(hide_code=True)
def _(mo, results, n_steps):
    if results is not None:
        final_greedy = results["greedy"]["mean"][-1]
        final_epsilon = results["epsilon"]["mean"][-1]
        final_thompson = results["thompson"]["mean"][-1]

        improvement = (final_greedy - final_thompson) / final_greedy * 100 if final_greedy > 0 else 0

        results_output = mo.md(f"""
        ## Results

        After **{n_steps} pulls**:

        | Strategy | Final Cumulative Regret |
        |----------|------------------------|
        | Greedy | {final_greedy:.1f} |
        | $\\epsilon$-Greedy | {final_epsilon:.1f} |
        | Thompson Sampling | {final_thompson:.1f} |

        Thompson Sampling achieves **{improvement:.0f}% lower regret** than Greedy.
        """)
    else:
        results_output = mo.md("")
    results_output
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Lesson for Agent Design

    Greedy agents get stuck in local optima. They find the first arm that looks good and never question it again. In a multi-agent swarm, this is death -- the agent that always routes to the same specialist, the trader that always bets the same market, the researcher that always queries the same source.

    $\\epsilon$-Greedy is the "spray and pray" approach: explore randomly, sometimes get lucky. It works but is inefficient. Most random exploration hits bad arms.

    Thompson Sampling is smarter: it explores *structured uncertainty*. An arm with few pulls has high variance in its posterior, so it occasionally wins the sample and gets tested. An arm with many pulls and a high mean is hard to dethrone. The exploration is naturally calibrated to information gain.

    For Edgeless: this is why our agents maintain confidence scores, run A/B tests on routing decisions, and periodically sample "unproven" skills. The swarm doesn't just exploit what works -- it maintains a posterior over what *might* work better.
    """)
    return


@app.cell(hide_code=True)
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    return np, plt


if __name__ == "__main__":
    app.run()
