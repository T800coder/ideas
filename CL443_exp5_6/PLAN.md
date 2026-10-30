# CL 443: doing it yourself. A step-by-step plan

Four phases, as discussed:

0. Set up your folder, git and documentation (once)
1. Learn SINDy by building it yourself (no AI-written code)
2. The PDE with your own solver
3. Compare your results with the AI results
4. Only then: AI on your own computer, under fixed rules

Everything below assumes a **Mac** (your screenshots show macOS) and **MATLAB** installed locally.

---

## Phase 0: set up the project (half a day)

### 0.1 Install git and tell it who you are

Open **Terminal** (Cmd+Space, type "Terminal", Enter).

Check whether git is already installed:

```bash
git --version
```

If it prints a version, go on. If a window pops up offering to install "command line developer tools", click **Install**, wait, then run `git --version` again.

Tell git your name and email (stored in every commit):

```bash
git config --global user.name "Ishitva Yadav"
```

```bash
git config --global user.email "your-email@example.com"
```

### 0.2 Make the project folder

```bash
mkdir -p ~/CL443
```

```bash
cd ~/CL443
```

Create the folder structure in one go (copy the whole block):

```bash
mkdir -p common journal report reference_ai \
  exp1_flux_shape exp2_frequency exp3_diffusivity exp4_random_flux \
  exp5_galerkin \
  exp6_sindy/phase1_learning exp6_sindy/lorenz exp6_sindy/pde
```

What each folder is for:

| Folder | Contents |
|---|---|
| `common/` | functions used by more than one experiment, e.g. your `relErr.m`, `stlsq.m`, your PDE solver |
| `exp1_flux_shape/` … `exp5_galerkin/` | one folder per experiment of the report |
| `exp6_sindy/phase1_learning/` | the learning exercises of Phase 1 |
| `exp6_sindy/lorenz/`, `exp6_sindy/pde/` | the two parts of Experiment 6 |
| `journal/` | your lab journal, one file per day |
| `report/` | the LaTeX report |
| `reference_ai/` | the AI-written code and results, kept apart. **Do not open until Phase 3.** |

### 0.3 One folder per run: "code → result"

Inside every experiment, each run gets its own numbered folder:

```
exp6_sindy/lorenz/
  run01_generate_data/
    run01_generate_data.m      <- the code (the ONLY thing you edit)
    results/
      run01_generate_data.pdf  <- code + printed output + figures, made by MATLAB's publish
      data.mat                 <- the numbers, saved by the script
      fig_*.png                <- figures, saved by the script
    notes.md                   <- 3-5 lines: what you ran, what came out, anything odd
  run02_stlsq_exact_derivative/
    ...
```

The rule: **a result exists only if it is in a `results/` folder next to the code that made it.** Never copy a number by hand from the command window.

Each experiment folder also gets a `README.md` that maps the report to the runs, e.g.

```
Table 7 (Lorenz, case C2)  <- exp6_sindy/lorenz/run04_sweep_C2/results/
Figure 37                  <- exp6_sindy/lorenz/run06_sweep_plot/results/fig_sweep.png
```

### 0.4 A template for every run script

Save this as `common/run_template.m` and copy it for each new run:

```matlab
%% runNN_short_name
% Purpose : what this run checks or produces (one sentence)
% Report  : which table / figure / section it feeds (or "learning")
% Date    : 2026-11-..
% Inputs  : what it loads (or "none")

clear; close all; clc
here   = fileparts(mfilename('fullpath'));
outDir = fullfile(here, 'results');
if ~exist(outDir, 'dir'), mkdir(outDir); end
addpath(fullfile(here, '..', '..', '..', 'common'))   % adjust the depth if needed

%% Parameters (every number the run depends on, in one place)
dt = 1e-3;

%% Computation

%% Print the results that matter
% fprintf(...)

%% Save
save(fullfile(outDir, 'data.mat'))                    % all variables
% exportgraphics(gcf, fullfile(outDir, 'fig_name.png'), 'Resolution', 200)
```

### 0.5 Run it so the code and the result are saved together

Use MATLAB's `publish` instead of screenshots. It runs the script and writes **one PDF with the code, everything it printed, and every figure** from that same run. That is your "code → result" record.

Save this helper as `common/publishRun.m`:

```matlab
function publishRun(scriptPath)
%PUBLISHRUN  Run a script and save code + output + figures as one PDF
%   in the script's results/ folder.
[folder, name] = fileparts(scriptPath);
outDir = fullfile(folder, 'results');
if ~exist(outDir, 'dir'), mkdir(outDir); end
publish(scriptPath, 'format', 'pdf', 'outputDir', outDir);
fprintf('Published to %s\n', fullfile(outDir, [name '.pdf']));
end
```

Then, in MATLAB, a run is always:

```matlab
publishRun('exp6_sindy/lorenz/run01_generate_data/run01_generate_data.m')
```

(Screenshots are still fine for anything outside MATLAB, but the published PDF is stronger evidence: the code and output cannot get out of sync.)

### 0.6 Put the folder under git

Create a `.gitignore` so temporary files are not tracked:

```bash
cd ~/CL443
```

```bash
printf '*.asv\n*.aux\n*.log\n*.out\n.DS_Store\n' > .gitignore
```

Start tracking:

```bash
git init
```

```bash
git add .
```

```bash
git commit -m "Project structure, run template and publish helper"
```

From now on, **after every run**:

```bash
git add .
```

```bash
git commit -m "exp6 lorenz run04: lambda sweep, case C2"
```

Useful commands:
- `git status`: what has changed since the last commit
- `git log --oneline`: the list of all commits (your full history)

Optional, recommended: a **private GitHub repository** as an online backup. Create an empty private repository on github.com called `CL443`, then run the two lines GitHub shows you under "push an existing repository" (`git remote add origin …` and `git push -u origin main`). If you prefer buttons to commands, **GitHub Desktop** (desktop.github.com) does all of the above.

### 0.7 Bring in your existing work (Experiments 1 to 5)

1. Copy your existing MATLAB code for Experiments 1–4 and the Galerkin test into the matching `expN_…/runNN_…/` folders. Put shared pieces (the `pdepe` wrapper, the flux profiles, `trueRandom`) in `common/`.
2. Re-run each one with `publishRun`, so every figure and table of Sections 3–7 of the report has a published PDF behind it.
3. Write each experiment's `README.md` (report item → run folder).
4. Commit.

### 0.8 Put the AI code aside

Copy the AI-written code and results (the `python/` and `matlab/` folders of `CL443_exp5_6`, and the full and professor PDFs) into `reference_ai/`. Commit. **Don't open it again until Phase 3.**

### 0.9 Lab journal

One file per working day, `journal/2026-11-03.md`, with:
- what you ran (run folder names),
- what came out (one line each),
- what surprised you or did not work,
- what is next.

---

## Phase 1: learn SINDy by building it yourself

Put each step in `exp6_sindy/phase1_learning/stepN_…/`, using the run template. Each step has a **check**: a result you should get. Don't move on until you get it.

### Step 1: read the paper (1 to 2 hours)
Brunton, Proctor & Kutz, *Discovering governing equations from data by sparse identification of nonlinear dynamical systems*, PNAS 113 (2016). Read the abstract, the method section and the Lorenz example. Write in your journal, in your own words:
- what Θ(X), Ξ and Ẋ are, and the size of each matrix;
- what "sparse" means and why it is wanted;
- the STLSQ steps.

### Step 2: least squares by hand, one variable
Problem: dx/dt = −2x, x(0) = 1.
1. Make data with `ode45` on `t = 0:0.01:5` (set `RelTol` and `AbsTol` to 1e-10).
2. Exact derivative: `dX = -2*x`.
3. Library with 3 columns: `Theta = [ones(size(x)), x, x.^2]`.
4. Solve: `xi = Theta \ dX`.

**Check:** `xi` ≈ [0, −2, 0], with the zeros smaller than about 1e-8.
Then replace the exact derivative with your own finite difference and note how `xi` changes.

### Step 3: write `stlsq.m` yourself (put it in `common/`)
Signature: `Xi = stlsq(Theta, dX, lambda, nIter)`. The algorithm, in words:
1. least squares on all terms;
2. set every coefficient with |value| < λ to zero;
3. least squares again, using only the remaining terms (do each column of dX separately);
4. repeat steps 2–3 `nIter` times.

**Checks:**
- On step 2's data with noise added to the derivative (`dX + 0.01*randn(size(dX))`, and `rng(1)` first so it repeats): plain least squares gives small non-zero values on 1 and x² (about −2×10⁻⁴ and 0.009); `stlsq` with λ = 0.1 sets those two *exactly* to zero and gives about −2.001 on x.
- λ = 3 removes everything (because |−2| < 3).

### Step 4: two variables
Damped oscillator: dx/dt = y, dy/dt = −x − 0.1y, start (1, 0), `t = 0:0.01:20`.
Use the exact derivatives (dx/dt = y, dy/dt = −x − 0.1y evaluated on the data). Write your own function that builds the library of all polynomials in x, y up to order 2 (1, x, y, x², xy, y²: 6 columns).

**Check:** `stlsq` with λ = 0.05 finds exactly 3 non-zero coefficients: 1 (y in dx/dt), −1 (x in dy/dt), −0.1 (y in dy/dt).

### Step 5: Lorenz
1. Data: σ = 10, ρ = 28, β = 8/3, start (−8, 7, 27), Δt = 0.001 up to t = 100, `ode45` with tolerances 1e-12.
2. Library: first order 2 (10 terms), then order 5 (56 terms). Write the library function so the order is an input.
3. Three derivatives: A (exact, from the equations), C2 (2nd-order central differences), C4 (4th-order central differences). For C2/C4, drop the end points where the formula does not apply.
4. `stlsq` with λ = 0.5.

**Check (Table 5 of the report):**

| Term | A | C2 | C4 |
|---|---|---|---|
| ẋ: x | −10.000000 | −9.99978 | −10.000000 |
| ẏ: x | 28.000000 | 27.99798 | 28.000000 |
| ż: z | −2.666667 | −2.66659 | −2.666667 |

Small differences in the last digits are fine (they come from the ODE solver). Seven non-zero terms in all three cases.

### Step 6: the λ sweep and the error measures
1. λ from 10^1.5 down to 10^−12, four values per decade: `lams = 10.^((6:-1:-48)/4)`.
2. For each λ: run `stlsq`, record the number of terms and which ones.
3. Write `relErr.m` (in `common/`): for each column, RMS(pred − ref) / (max(ref) − min(ref)), then the mean over columns.
4. Make three validation runs from (5, −5, 20), (−3, 4, 30), (8, 8, 15), up to t = 20. Compute E_train, E_dv and E_sim(T = 1) for each model (definitions in Section 8.2.3 of the report).
5. Plot error against λ (log axes); plot the number of terms in a separate panel.
6. Write `selectLambdaR4.m`: drop unstable models, then take the model just after the largest drop in log10(error).

**Check (Tables 6–8 and 10 of the report):** the 7-term model is selected in all three cases, and its λ range has upper end 0.562.

---

## Phase 2: the PDE with your own solver

Folder: `exp6_sindy/pde/`. Use **your own `pdepe` code** from Experiments 1–5, with constant f = 1, A = 0.025, starting from C = 1.

### Step 7: one frequency, ω = 1
1. Training run: δ = A sin(τ), 5 periods (τ from 0 to 10π), Δτ = P/200, so 1001 points.
2. From your solution: Cs = value at r = 1; Cavg = 3∫C r² dr (use `trapz` over your radial grid).
3. dCs/dτ by 2nd-order differences.
4. Library [Cs, Cavg, δ]; sweep λ from 10^3 down to 10^−6.

**Check:** the three-term model with about −35.04, +35.04, −10.004 (Table 17).

**Warning, a trap we found:** MATLAB's built-in `gradient` uses a *first-order* difference at the two end points. The report used a *second-order* one there:
- first point: (−3y₁ + 4y₂ − y₃)/(2Δτ)
- last point: (3yₙ − 4yₙ₋₁ + yₙ₋₂)/(2Δτ)

At ω = 1 this barely matters. At ω = 0.1, `gradient` gives about −33.7 instead of −34.6. Write your own derivative function, or note the difference.

### Step 8: all frequencies, validation, test, cross-test
In order, one run folder each:
1. Training at ω = 0.1, 10, 100 (same recipe). **Check:** Table 17.
2. Four validation runs per ω, 10 periods each: cos, sin late (continue the training run from τ = 5P), sin ph, cos ph. Solve each candidate model; compute E_sim (whole run). **Check:** Table 14.
3. Selection with R4 on the stacked E_sim. **Check:** Table 15.
4. Test on the random multisine (parameters in Table 13), once. **Check:** Table 16.
5. Cross-test, Cs and gap, last period. **Check:** Table 18.

Expect agreement in the first 2 to 3 digits, not all digits: `pdepe` and the AI's solver are different numerical methods.

---

## Phase 3: compare your results with the AI results

1. Now open `reference_ai/`.
2. Make `exp6_sindy/comparison.md` with one row per quantity:

| Quantity | Report table | Your MATLAB value | AI value | Difference | Run folder |
|---|---|---|---|---|---|
| Lorenz C2, ẋ: x | 5 | | −9.999779 | | |
| PDE ω = 1, Cs coefficient | 17 | | −35.039 | | |
| … | | | | | |

3. For every difference larger than you expect:
   - first suspect a difference in **settings** (Δt, end points of the derivative, tolerances, run length);
   - then a **bug** on either side. Find which one; write it in the journal.
4. Show your professor the comparison table together with your published run PDFs.

---

## Phase 4: AI on your own computer, under fixed rules

### 4.1 Install Claude Code
In Terminal:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

(Check the current instructions at docs.claude.com if this command has changed.) Then start it inside your project folder:

```bash
cd ~/CL443
```

```bash
claude
```

### 4.2 Let it run MATLAB from the command line
Find your MATLAB version:

```bash
ls /Applications | grep MATLAB
```

A run then looks like this (replace R2024b with your version):

```bash
/Applications/MATLAB_R2024b.app/bin/matlab -batch "addpath('common'); publishRun('exp6_sindy/lorenz/run07_test/run07_test.m')"
```

This is the **same** `publishRun` you use by hand, so AI runs and your runs produce the same kind of record.

### 4.3 Fix the rules in `CLAUDE.md`
Claude Code reads a file called `CLAUDE.md` in the project folder at the start of every session. Create `~/CL443/CLAUDE.md` with:

```markdown
# Rules for this project

- All computation is done in MATLAB on this computer, through
  `matlab -batch "addpath('common'); publishRun('<path to run script>')"`.
  Never state a numerical result that did not come from such a run.
- Every run lives in its own folder: <experiment>/runNN_short_name/
  with the script runNN_short_name.m, a results/ folder (published PDF,
  data.mat, figures) and notes.md. Use common/run_template.m as the start.
- Never edit an existing run folder to change its result. A new attempt is a
  new run folder (runNN+1).
- Shared functions go in common/. Do not change a common/ function that
  existing runs use without saying so and re-running those runs.
- Report tables are generated from data.mat files, never typed by hand.
  Each table/figure in the report must be listed in the experiment's
  README.md with the run folder it comes from.
- After each run: update notes.md and the experiment README.md, then
  git add . and git commit with a message "<experiment> runNN: <what>".
- Ask before deleting any file.
- reference_ai/ is read-only.
```

### 4.4 Your part in every AI-assisted session
1. Say what the run should do, and which table or figure it is for.
2. **Read the code before it runs.** You should be able to explain every line.
3. Open the published PDF and check that the numbers make sense.
4. Check the commit (`git log --oneline`).

That gives you a full record of who wrote what, what ran, and what came out.
