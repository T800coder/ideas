# Phase 1 schedule: up to the meeting on Friday 20 November

Goal for the meeting: **your own SINDy code in MATLAB, working on test problems and on Lorenz, with every run documented.**

Fixed dates: quizzes/assessments on 6, 10, 12, 14, 15 Nov · Diwali 8 Nov · endsems 19 and 21 Nov.
Rules: **no project work on the day of a quiz or exam, and none on Wed 18 (the day before your first endsem).** Sessions the day before a quiz are kept short.

| Day | Time | What |
|---|---|---|
| Wed 4 Nov | 45 min | Send the mail · Phase 0: git, folders |
| Thu 5 Nov | 45 min | Phase 0: template, `publishRun`, first commit |
| Fri 6 Nov | — | quiz |
| **Sat 7 Nov** | 2 h | Step 1 (paper) + Step 2 (least squares, one variable) |
| Sun 8 – Tue 10 | — | Diwali, then assessment on the 10th |
| **Wed 11 Nov** | 1 h | Step 3 (`stlsq.m`) |
| Thu 12 – Sun 15 | — | assessments on 12, 14 and 15 |
| **Mon 16 Nov** | 2 h | Step 4 (two variables) + start Step 5 (Lorenz data) |
| **Tue 17 Nov** | 2–3 h | Step 5 (Lorenz) + Step 6a if time allows |
| Wed 18 – Thu 19 | — | endsem preparation, endsem |
| **Fri 20 Nov** | 1 h before the meeting | One-page summary, check folders, commit |

This is tight. If a session overruns, **cut Step 6a**, not your exam preparation: Steps 1–5 alone are a good Phase 1 update. Error measures (E_train, E_dv, E_sim) and the R4 rule (Step 6b) come after the 21st.

---

## Wed 4 Nov (45 min): set up

1. Send the mail to Prof. Picardo.
2. Do PLAN.md sections **0.1, 0.2 and 0.6** (install git, make `~/CL443` and its folders, `git init`).
   Skip 0.7 and 0.8 (moving Experiments 1–5 and the AI code) until after the exams. Phase 1 doesn't need them.
3. Make the first journal file `journal/2026-11-04.md`: one line, "set up project".

**Done when:** `git log --oneline` in Terminal shows one commit.

## Thu 5 Nov (45 min): template and publishing

1. PLAN.md **0.4**: create `common/run_template.m` (`edit common/run_template.m` in MATLAB, paste, save).
2. PLAN.md **0.5**: create `common/publishRun.m` the same way.
3. In MATLAB: `cd ~/CL443`, then `addpath('common')`, then `savepath`, so MATLAB always finds `common/`.
4. **Test run:** make `exp6_sindy/phase1_learning/step0_test/`. Copy the template into it as `step0_test.m`, add one line in "Computation", `x = linspace(0,1,5)`, and one plot, `plot(x, x.^2)`. Then run:
   ```matlab
   publishRun('exp6_sindy/phase1_learning/step0_test/step0_test.m')
   ```
5. Commit: `git add .` then `git commit -m "Template, publishRun, test run"`.

**Done when:** `step0_test/results/step0_test.pdf` exists and shows the code, the printed `x` and the plot.

## Sat 7 Nov (2 h): Steps 1 and 2

### Step 1: the paper (45 min)
Brunton, Proctor & Kutz (2016), *PNAS* 113, 3932–3937. Read the abstract, the "Sparse identification" section and the Lorenz example.
In `journal/2026-11-07.md`, answer in your own words:
- What are Ẋ, Θ(X) and Ξ? If there are m time points, n variables and p library terms, what is the size of each?
- Why sparse? What would plain least squares give?
- The STLSQ steps, as a numbered list.

### Step 2: least squares by hand, one variable (1 h)
Folder: `exp6_sindy/phase1_learning/step2_one_variable/`

1. Solve dx/dt = −2x, x(0) = 1, on `t = (0:0.01:5)'` with `ode45`, using `odeset('RelTol',1e-10,'AbsTol',1e-10)`.
2. Exact derivative: `dX = -2*x`.
3. Library: `Theta = [ones(size(x)), x, x.^2]`. Check `size(Theta)`: 501 × 3.
4. `xi = Theta \ dX` and print it with `fprintf('%.3e\n', xi)`.
5. Second part: replace `dX` with your own 2nd-order central difference, `(x(3:end) - x(1:end-2)) / (2*0.01)`, and use the matching rows of `Theta` (`Theta(2:end-1,:)`). Print `xi` again.

**Check:** part 1 gives about [0, −2, 0], with both zeros smaller than 1e-8. In part 2 the x coefficient moves slightly away from −2. Write the value in `notes.md`.

Publish, commit (`"step2: least squares, one variable"`).

## Wed 11 Nov (1 h): Step 3

### Step 3: your `stlsq.m`
File: `common/stlsq.m`, signature `Xi = stlsq(Theta, dX, lambda, nIter)`.
Write it from your Step 1 notes, without looking anything up. Hints only:
- `Xi = Theta \ dX` handles all columns of `dX` at once.
- `small = abs(Xi) < lambda` gives a logical matrix.
- In the refit, loop over the columns of `dX` (`for j = 1:size(dX,2)`), because each column keeps different terms.

Test folder: `exp6_sindy/phase1_learning/step3_stlsq_test/`
1. Same data as Step 2 (exact derivative), plus noise: `rng(1); dXn = dX + 0.01*randn(size(dX));`
2. Print plain least squares `Theta \ dXn`, then `stlsq(Theta, dXn, 0.1, 10)`, then `stlsq(Theta, dXn, 3, 10)`.

**Check:**
- Plain least squares: small non-zero values on 1 and x² (about −2×10⁻⁴ and 0.009).
- λ = 0.1: those two are exactly 0, and the x coefficient is about −2.001.
- λ = 3: everything is 0.

Your exact noise values will differ from Python's, but the pattern must be the same.

Publish, commit (`"step3: stlsq"`).

## Mon 16 Nov (2 h): Step 4, then start Step 5

### Step 4: two variables (1 h)
Folder: `exp6_sindy/phase1_learning/step4_two_variables/`
1. Damped oscillator dx/dt = y, dy/dt = −x − 0.1y, start (1, 0), `t = (0:0.01:20)'`.
2. Exact derivatives from the equations, evaluated on the data: `dX = [y, -x - 0.1*y]`.
3. Write `common/polyLibrary.m`: input the data matrix `X` (m × n) and the maximum order; output `Theta` and a cell array of term names (`'1'`, `'x'`, `'y'`, `'x^2'`, `'x y'`, …). For 2 variables and order 2, it must give 6 columns.
   Hint: loop over all exponent combinations whose sum is ≤ order.
4. `Xi = stlsq(Theta, dX, 0.05, 10)` and print it as a table with the term names.

**Check:** exactly 3 non-zero values: 1 (y in dx/dt), −1 (x in dy/dt), −0.1 (y in dy/dt).

Publish, commit.

If time is left: write the first part of Step 5 (generating the Lorenz data and building the library) and run it once.

## Tue 17 Nov (2–3 h): Step 5, then Step 6a if time allows

### Step 5: Lorenz (1.5–2 h)
Folder: `exp6_sindy/lorenz/run01_lorenz_recovery/` (this is Experiment 6 proper)
1. σ = 10, ρ = 28, β = 8/3, start (−8, 7, 27), `t = (0:0.001:100)'`, `ode45` with tolerances 1e-12. This takes a little while.
2. `polyLibrary(X, 5)`. **Check:** 56 columns.
3. Three derivatives:
   - A: exact, from the equations;
   - C2: `(X(3:end,:) - X(1:end-2,:)) / (2*dt)`, with `Theta(2:end-1,:)`;
   - C4: `(-X(5:end,:) + 8*X(4:end-1,:) - 8*X(2:end-3,:) + X(1:end-4,:)) / (12*dt)`, with `Theta(3:end-2,:)`.
4. `stlsq(..., 0.5, 10)` for each; print the non-zero coefficients with their names.

**Check** (Table 5 of the report): 7 non-zero terms in every case, and

| Term | A | C2 | C4 |
|---|---|---|---|
| ẋ: x | −10.000000 | −9.99978 | −10.000000 |
| ẏ: x | 28.000000 | 27.99798 | 28.000000 |
| ż: z | −2.666667 | −2.66659 | −2.666667 |

The last digits may differ slightly (ODE solver). A wrong term or a missing term means a bug: check the row alignment of `Theta` and `dX` for C2 and C4 first.

### Step 6a: λ sweep, number of terms only (1 h, optional)
Folder: `exp6_sindy/lorenz/run02_lambda_sweep_terms/`
1. `lams = 10.^((6:-1:-48)/4);` (55 values, from about 32 down to 1e-12).
2. For each λ and each case (A, C2, C4): run `stlsq` and store the number of non-zero coefficients.
3. Plot the number of terms against λ (log x-axis, reversed with `set(gca,'XDir','reverse')`), one line per case.

**Check** (Tables 6–8): 7 terms from λ = 0.562 down to 1e-12 (A), down to about 5.6e-5 (C2), and down to about 1.8e-8 (C4); more terms below those.

## Fri 20 Nov (1 h before the meeting)

1. Check every step folder has its `results/*.pdf` and `notes.md`.
2. Write a **one-page summary** (`exp6_sindy/phase1_learning/summary.md`, or one slide per step):

   | Step | What I did | Check | My result | OK? |
   |---|---|---|---|---|
   | 2 | dx/dt = −2x, least squares | [0, −2, 0] | … | ✓ |
   | … | | | | |

3. Write down **2–3 questions** for the professor, for example anything that surprised you in the C2 results, or how to choose λ (that leads into Step 6b after the exams).
4. Commit: `"Phase 1 ready for meeting 20 Nov"`.

Take to the meeting: the summary, the published PDFs (laptop or printed) and your questions.

## After the 21st
Step 6b: E_train, E_dv, E_sim and the R4 rule (PLAN.md Step 6, items 3–6), then Phase 2.
