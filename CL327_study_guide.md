# CL327 Study Guide: Multistage Separation Processes

Built from your 26 pages of handwritten notes. Sections follow the order of your notes. Items marked **⚠ check** are places where the handwriting was unclear or the notes look inconsistent, so verify them against lecture slides.

---

## 1. Why distillation?

- One stage is not enough for high purity, so we use multiple stages. This course covers the design of **one column**. The next course covers sequences of columns.
- Distillation is the "king of separations" because it is:
  - widely applicable
  - able to reach high purity
  - a simple process. Simplicity is what makes it popular.
- Other separations (absorption, adsorption, membranes, solvent extraction) all need an extra "thing" such as an absorbent, adsorbent, membrane or solvent.
- Distillation can be more expensive at times, but it is still used because it is simple and mature.

### Volatility vs boiling point
- Distillation relies on the difference in **volatility**, which is not the same as the difference in boiling points.
- Boiling-point difference corresponds to vapour-pressure difference.
- Volatility accounts for **non-ideality**, meaning the presence of other components in the mixture.
- **HCl example:** HCl has a low boiling point but a great affinity for water, so it does not evaporate out of water. It has a low boiling point and low volatility.
- Ideal mixtures: boiling point and volatility convey the same idea.
- Non-ideal mixtures: other components affect volatility but not the boiling point.

---

## 2. VLE (vapour–liquid equilibrium)

**General:** φᵢ yᵢ P_T = γᵢ xᵢ Pᵢˢᵃᵗ

**Ideal mixture** (φ = γ = 1): **yᵢ P_T = xᵢ Pᵢˢᵃᵗ** (Raoult's law).
- Species with similar molecules behave ideally.
- Mixing polar with non-polar gives a non-ideal mixture.

### Relative volatility
- α_AB, with B as the reference component, so α_BB = 1.
- α_AB > 1 means A is more volatile. α_AB < 1 means A is less volatile.
- A is usually the lighter and more volatile component, so α_AB is typically > 1.
- Binary: **α_AB = [y_A/(1−y_A)] / [x_A/(1−x_A)]**
- Combined with Raoult's law: **y_A = α x_A / (1 + (α−1) x_A)**
- Multicomponent: **yᵢ = αᵢ xᵢ / Σ αⱼ xⱼ**, where αᵢ = Pᵢˢᵃᵗ / P_refˢᵃᵗ (you were asked to derive this yourself).
- In the multicomponent notes the reference is the *heaviest* component, so α > 1 for the others and α_ref = 1.

### Degrees of freedom (DOF) for the ternary system
- Unknowns: P, T, x₁–x₃, y₁–y₃ (8 unknowns).
- Equations: 3 VLE equations plus Σx = 1 and Σy = 1 (5 equations).
- DOF = 3. Typically you fix P and any two xᵢ (or any two yᵢ).

---

## 3. The column and the equilibrium-stage model

- Feed F enters mid-column. Distillate D leaves at the top and bottoms B at the bottom.
- On each stage n, vapour yₙ leaves upward and liquid xₙ leaves downward. Vapour yₙ₊₁ enters from below and liquid xₙ₋₁ enters from above.
- Mass and heat transfer happen at every stage.
- **Theoretical (equilibrium) tray:** the V and L leaving are in equilibrium.
- Profiles in the column:
  - Concentration profile of the *least volatile* component: it jumps at the feed stage, and in the notes xᵢᴵ > yᵢᴵ near the feed.
  - Temperature profile: it falls from reboiler to condenser, with the steepest change around the feed.

---

## 4. Binary distillation (McCabe–Thiele, MT)

> The MT method works **only for binary mixtures**.

- **Reflux ratio:** R = L/D
- **Vapour flow:** V = L + D = D(1+R)
- **Rectification (operating) line:** yₙ₊₁ = [R/(R+1)] xₙ + x_D/(R+1). The slope is R/(R+1).
- Effect of reflux ratio R:
  - High R gives high purity, but also high energy needs.
  - For a given D, raising R raises V, so condenser and reboiler duties go up.
  - As R rises the slope tends to 1, so the operating line moves away from the equilibrium curve. The driving force goes up and the **number of trays goes down**.
- **Optimum R:**
  - High R: less CapEx (fewer trays) but more OpEx (energy).
  - Low R: more CapEx but less OpEx.
  - Total cost has a minimum at R_opt.
  - Thumb rule: **R_opt = (1.2–1.5) × R_min**. It is based on experience with several mixtures.
  - ⚠ check: the Gilliland page says 1.3–1.5 for R_op. Use whichever range your instructor gives.
- **CMO (constant molar overflow):**
  - In a given section (rectifying or stripping), V and L stay constant across stages.
  - It is valid only when all components have similar molar latent heats. This holds for ideal mixtures such as benzene–toluene.
  - It is a very idealised situation.
- Self-study items from your notes: the azeotrope y–x diagram, where y = x and volatility reverses, and T–x,y diagrams with a minimum or maximum.

---

## 5. Multicomponent distillation

### Basics
- Example: A, B, C all needed at 99% purity. Assume an ideal mixture.
- You **cannot use McCabe–Thiele**, so you use the **FUG shortcut method** (Fenske–Underwood–Gilliland).
- FUG limitation: it assumes the components form an ideal mixture.
- **Key components:**
  - **LK** = light key and **HK** = heavy key.
  - The split is defined between them.
  - Example: A→top with B,C,D,E→bottom, or A,B→top with C,D,E→bottom.
- At total reflux (R→∞), yₙ₊₁,ᵢ = xₙ,ᵢ. That is, the operating line is y = x.
- q = fraction of feed that goes to the stripping section (think about its meaning: q = 1 is saturated liquid feed).

### Design degrees of freedom
- Given F, x_f,i and q:
  - Unknowns: B, D, x_D,i, x_B,i, which is 2C + 2.
  - Equations: Σx_D = 1, Σx_B = 1, F = B + D, and the component balances. In total C + 2 independent equations.
  - **DOF = C**, so any C of B, D, x_D,i, x_B,i must be specified.

### The three FUG equations

| Step | Equation | Gives |
|---|---|---|
| **Fenske** | 1 + N_min = ln[(x_D,LK / x_B,LK) · (x_B,HK / x_D,HK)] / ln[α_LK–HK] | Minimum number of stages (total reflux) |
| **Underwood** | 1 − q = Σ αᵢ x_f,i / (αᵢ − φ), then R_min + 1 = Σ αᵢ x_D,i / (αᵢ − φ) | Minimum reflux ratio. Solve the first equation for φ, then the second. |
| **Gilliland** | (N − N_min)/(N + 1) = 0.75 · [1 − ((R − R_min)/(R + 1))^0.57] | Actual number of stages N at a chosen R |

- ⚠ check: your notes write the Gilliland denominator as "N − 1" and the bracket as (R−R_min)/R. The standard Gilliland (Molokanov) correlation uses **(N+1)** and **(R+1)**. Confirm which form your course uses.
- Operating reflux: R_op = R_min × (1.3–1.5). Gilliland is applicable to any mixture.

### Midterm-style worked example (from your notes)
Feed: A = 0.5, B = 0.3, C = 0.2. α_A = 5, α_B = 3, α_C = 1. q = 1. Distillate: A = 0.9, B = 0.09. Bottoms: C = 0.02.

1. Because q = 1, the left-hand side is zero: **0 = 5(0.5)/(5−φ) + 3(0.3)/(3−φ) + 1(0.2)/(1−φ)**
2. Solve numerically. The root that matters lies between the αs of the two key components (here between 1 and 3). **φ ≈ 1.174**.
3. Substitute φ into R_min + 1 = Σ αᵢ x_D,i/(αᵢ − φ) to get R_min. The sum includes every component present in the distillate.

(There is also a root between 3 and 5. Pick the one between the key components' α values.)

### Feed tray location
- McCabe–Thiele logic: switch from the rectification line to the stripping line as soon as you cross the q-line.
- Why? Staying on the rectification line past the q-line can still reach the same separation, but needs **more trays**. Switching at the q-line gives the optimum feed tray, with the minimum trays for the given R.
- **Kirk–Brides correlation** (for the ratio of stages above and below the feed):
  ln(N_R/N_S) = 0.206 · ln[(B/D) · (x_HK,F / x_LK,F) · (x_LK,B / x_HK,D)²]
  where N_R is the number of stages in the rectification section and N_S the number in the stripping section.
  ⚠ check the exact subscripts in the bracket against the slides.

---

## 6. Rigorous simulation (the equilibrium-stage model)

Equations for each stage n:
- Overall balance: Vₙ + Lₙ = Vₙ₊₁ + Lₙ₋₁ (+ F if it is the feed stage)
- Component balance: Vₙ yₙ,ᵢ + Lₙ xₙ,ᵢ = Vₙ₊₁ yₙ₊₁,ᵢ + Lₙ₋₁ xₙ₋₁,ᵢ
- Energy balance: Vₙ hₙᵛ + Lₙ hₙᴸ = Vₙ₊₁ hₙ₊₁ᵛ + Lₙ₋₁ hₙ₋₁ᴸ
- Equilibrium: φ y P = γ x Pˢᵃᵗ
- Summation: Σx = 1, Σy = 1
- **Total: 2NC + 3N equations**, matching the unknowns (Lₙ, Vₙ, xₙ,ᵢ, yₙ,ᵢ, Tₙ).
  - N is the total number of stages, including the condenser and reboiler.

Key points:
- **Main assumption:** all streams leaving a stage are in equilibrium. This is obviously not true in practice. The model is called the **EQ stage model**. Non-equilibrium stage models exist but are not in the syllabus.
- **Pressure:**
  - It is defined in the condenser.
  - Pressure increases going down the column, so the pressure profile needs a momentum balance (e.g. Ergun's equation).
  - Rule of thumb: if the top is at 1 atm, the bottom will not exceed about 1.4–1.5 atm.
- **Condensers:**
  - Total condenser: all vapour condenses to liquid.
  - Partial condenser: a vapour product V′ and a liquid L′ leave. It acts as an extra equilibrium stage and is useful for non-condensable gases.
- The **reboiler** is always an equilibrium stage.
- **Specifications:** the variables are Q_c, Q_B, S (= V′/B), R, D, B. You need only **any two**, typically R and one other. In a simulation you cannot specify both B and D, since F = B + D.
- **FUG only gives a starting point for simulation.** Before simulators, people over-designed, which meant high CapEx. Columns are still over-designed (because of the equilibrium-stage assumption), but by less.

---

## 7. Sizing the column

### Height
- **Tray column:** Height = [(N_stages − 2)/η] × tray spacing (t.s.). The −2 removes the condenser and reboiler. η is the tray efficiency, which depends on the column internals.
  - ⚠ check: the notes show "N−2 over [symbol] × t.s." and the symbol looks like an efficiency. Confirm against the slides.
- Tray spacing = hold-up height + vapour-disengagement height (t.s. = L_h + V_h).
  - You do not want **backmixing**: the vapour should not entrain liquid droplets.
  - The vapour needs enough residence time between two trays to reach a certain composition.
- **Packed column:** Height = (N_stages − 2) × **HETP** (Height Equivalent of a Theoretical Plate). HETP is a function of many things.

### Tray vs packed columns

| | Tray | Packed |
|---|---|---|
| Flow | Cross-current | Counter-current |
| Continuous phase | Liquid | Vapour |
| Dispersed phase | Vapour | Liquid (forms a film on the packing) |
| Pressure drop | Higher (vapour pushes through a liquid pool) | Lower (structured packing is lower than random packing) |
| Best for | **High capacity.** In big packed columns the liquid channels toward the walls and contact is minimised. | Vacuum distillation and other low-ΔP duties |

- Column internals are judged on two parameters: **HETP (or t.s.)** and **ΔP**. Both should be minimised.

### Diameter
- Larger flow rates need a larger diameter.
- **Flooding:**
  - At very high vapour velocity the liquid is fluidised and carried along with the vapour, even up the downcomer.
  - At very high liquid rate, liquid weeps and flows down through the holes.
  - Fix: size the diameter so V and L velocities stay below the maximum allowable.
- **Generalised pressure-drop correlation chart (GPDC)** for packed columns:
  - X-axis: (L/V)·√(ρ_G/ρ_L)
  - Y-axis: f(G) = 13.1 G² F_p (μ_L/ρ_L)^0.1 / [ρ_G(ρ_L − ρ_G)]
  - Curves: lines of constant ΔP, plus a flooding boundary.
  - F_p is the packing factor, which accounts for the type of packing.
  - G = mass velocity of vapour = (mass flow rate)/(cross-section area) = V ρ_G / (πD²/4). It is the superficial velocity times density.
- **How to use it:**
  1. Calculate X = (L/V)√(ρ_G/ρ_L).
  2. From the **boundary (flooding) line**, read f(G) and calculate G_max.
  3. Operate at **G = 0.7 × G_max** (typically 70% of flooding).
  4. Calculate the diameter D_T from G.
- **Tray columns** use a similar chart with tray spacing as the parameter. Calculate G_max, then operate at 70%.
- Reading the chart:
  - Increasing V alone, or increasing L alone, moves you toward flooding.
  - Increasing L alone can push the operating point toward the boundary with ΔP rising.
- Height depends on **purity**. To change **capacity**, change the **diameter**.
- X changes from tray to tray, but varying the diameter along the column is expensive. So the stripping and rectification sections have different diameters, because the flows change substantially at the feed stage.

---

## 8. Absorption and stripping

### Concepts
- A solvent removes a solute from a gas stream.
- **Properties of a good solvent:** optimum affinity for the solute, cheap and safe, and low volatility (low vapour pressure).
- Solvent is recovered by **stripping**, which is the exact opposite of absorption.
  - Absorption is favoured at **low T and high P**.
  - Stripping is favoured at **high T and low P**.
  - Low P can also mean low partial pressure. Add inert gases (**stripping agents**) to lower the solute's partial pressure.
  - Stripping section of a distillation column = where the more volatile component is removed from the liquid.
- Solvent can be reactive:
  - It consumes solute, so the driving force is maintained.
  - Non-reactive = **physical absorption**.
  - Reactive = **chemical absorption**.
- **Examples:**
  - CO₂ removal in an ammonia plant (reformer → WGS → absorber). Chemical absorption: K₂CO₃ + CO₂ + H₂O ⇌ 2KHCO₃ (⚠ check the stoichiometry; the notes show KHCO₃ without the 2). The solvent is recovered by heating.
  - CO₂ with methanol at about −60 °C (cryogenic). This is physical absorption and is proven to be economical.
  - Refinery side stripper: a side draw contains some C₃, C₆ and so on. These are removed by stripping with steam as the stripping agent.
  - Ethanol→IPA process flowsheet with an absorption column and water recycle.
- Design variables for an absorption column: number of stages, solvent flow rate, height of column, diameter of column.

### Graphical design (dilute system)
- L and V do change because of mass transfer, but if the solute concentration is sufficiently small you can treat them as constant.
- **Operating line** (from a balance over the top of the column):
  y = (L/V) x + (y_out − (L/V) x_in)
- **Equilibrium:** Henry's law, Pᵢ = Hᵢ xᵢ, so **yᵢ = Kᵢ xᵢ**, with K = H/P. Treat it as a straight line, with K constant over the small concentration range.
- The solvent flow rate L sets the **slope** of the operating line.
- **Minimum solvent rate (MSR):** the operating line touches the equilibrium curve at the pinch point (x_out^max, y_in).
  - Assume x_in = 0 (ideal case). y_in and y_out are set by process requirements.
  - **x_out^max = y_in/K** (for MSR).
  - Increasing L lowers x_out.
- **Kremser equation** (number of stages, absorption):
  N = log[ ((A−1)/A) · ((y_in − K x_in)/(y_out − K x_in)) + 1/A ] / ln A
  - ⚠ check: the notes also show a version with K x_out in some terms. Use the Kremser form given in lecture.
- **Absorption factor: A = L/(K V)**. **Recommended A = 1.5.**
- **Stripping Kremser:**
  N = log[ (A−1) · ((x_in − y_in/K)/(x_out − y_in/K)) + A ] / ln(1/A)
  - ⚠ check: the stripping equation in your notes has handwriting that is hard to read, and the "A" and "1/A" placement is unclear. Verify the form on the slides.

### Why simulate?
- Henry's law may not be valid.
- The L, V = constant assumption is not valid because there is mass transfer.

---

## 9. Liquid–liquid extraction (LLE)

- Feed + solvent form two liquid phases, the raffinate and the extract, which are in equilibrium.
- **Counter-current** operation:
  - The driving force is maintained.
  - Advantages: smaller equipment for the same amount of solvent, or less solvent for the same equipment size.
  - Drawback: there is a risk of flooding. Co-current or cross-current is used to reduce that risk.
- **Choice of solvent is crucial.** The solvent should have:
  - high affinity for the solute
  - low solubility in the feed
  - easy and economical recovery (often by distillation)
  - a large enough density difference for fast decantation
  - **no emulsion formation.** Examples of stable emulsions: milk and Limca, which stay stable for years.
  - It should also be cheap, safe, non-corrosive and non-flammable.
- **Interfacial tension:** the smaller the interfacial tension, the larger the stability of the emulsion (smaller droplets, more chance of homogenisation). Therefore **small interfacial tension is undesired for LLE**.
- **Extraction column:** it is similar to a distillation column.
  - Packed, sieve-tray and other internals are used.
  - Vapour ↔ light phase and liquid ↔ heavy phase.
- **Equilibrium:** xᵢᴿ γᵢᴿ = xᵢᴱ γᵢᴱ
  - Distribution coefficient: **β = xᵢᴱ/xᵢᴿ = γᵢᴿ/γᵢᴱ**
  - The fact that two phases form is itself a non-ideality.
  - β is not constant, but within a certain concentration range it can be treated as constant. The ternary diagram (e.g. acetic acid/ester/water) shows the tie lines with different slopes.
- **Number of stages** (Kremser-type):
  N = log[ ((1−ε)/ε) · ((x_F − x_S/K)/(x_R − x_S/K)) + 1/ε ] / log(1/ε), with **ε = K S/F** (K = β).
  - ⚠ check: the notes' symbols were hard to read. Confirm the exact form against the slides.
- **Solute-free basis:**
  - x_F, x_S, x_R, S and F are all on a solute-free basis.
  - Why: this lets the lines be linear. Solute is transferred, so S and F are not constant, and you cannot neglect solute concentration because of the bulk transfer of solute.
- **Assumptions:** K is constant, and the liquids are completely insoluble in each other.

---

## 10. Quick-review: questions to test yourself

1. Why is volatility a better measure than boiling-point difference? Give the HCl–water example.
2. Write Raoult's law, and the binary and multicomponent y–x relations in terms of α.
3. How many DOF does a ternary VLE system have, and what do you typically fix?
4. Derive the rectification line. What happens to the slope as R rises, and why does the number of trays fall?
5. Why does total cost have a minimum in R? What is the thumb rule for R_opt?
6. State the CMO assumption and when it holds.
7. What are the LK and HK, and why can't you use McCabe–Thiele for multicomponent mixtures?
8. Which equation gives N_min, R_min, and N at a given R? State the FUG order.
9. Why does the McCabe–Thiele method switch lines at the q-line?
10. Count the unknowns and equations in the equilibrium-stage model (2NC + 3N).
11. How many specifications can you give for a column simulation (any two of Q_c, Q_B, S, R, D, B), and why not both D and B?
12. What does a partial condenser do, and when is it used?
13. Compare tray vs packed columns on ΔP, flow pattern, capacity and use-case.
14. Why is the column operated at 70% of flooding, and how do you get D_T from the GPDC chart?
15. Why do the stripping and rectification sections have different diameters?
16. What makes a good absorption solvent? What are the T/P conditions for absorption vs stripping?
17. Physical vs chemical absorption: give one example each.
18. Where is the MSR on the y–x diagram, and what is x_out^max?
19. What is the absorption factor, and what value is recommended?
20. Why must LLE use a solute-free basis, and what are the Kremser-type assumptions?
21. Why is low interfacial tension bad for LLE?
22. Why do we need a simulation when shortcut methods exist?

---

## Formula sheet

| Topic | Formula |
|---|---|
| Raoult's law | yᵢ P = xᵢ Pᵢˢᵃᵗ |
| Relative volatility | α_AB = (y_A/y_B)/(x_A/x_B) |
| Binary VLE | y = αx/(1+(α−1)x) |
| Multicomponent VLE | yᵢ = αᵢxᵢ/Σαⱼxⱼ |
| Reflux ratio | R = L/D; V = D(R+1) |
| Rectification line | y = [R/(R+1)]x + x_D/(R+1) |
| Optimum reflux | R_opt ≈ (1.2–1.5) R_min |
| Fenske | 1 + N_min = ln[(x_D,LK/x_B,LK)(x_B,HK/x_D,HK)] / ln α_LK–HK |
| Underwood | 1 − q = Σ αᵢx_f,i/(αᵢ−φ); R_min + 1 = Σ αᵢx_D,i/(αᵢ−φ) |
| Gilliland | (N−N_min)/(N+1) = 0.75[1 − ((R−R_min)/(R+1))^0.57] |
| Kirk–Brides | ln(N_R/N_S) = 0.206 ln[(B/D)(x_HK,F/x_LK,F)(x_LK,B/x_HK,D)²] |
| Equilibrium stage model | 2NC + 3N equations |
| Tray column height | [(N−2)/η] × t.s. |
| Packed column height | (N−2) × HETP |
| Mass velocity | G = Vρ_G/(πD²/4) |
| Design velocity | G = 0.7 G_max |
| Absorption operating line | y = (L/V)x + (y_out − (L/V)x_in) |
| Henry's law | y = Kx, K = H/P |
| Absorption factor | A = L/(KV); recommended A ≈ 1.5 |
| MSR (x_in = 0) | x_out^max = y_in/K |
| LLE distribution | β = xᴱ/xᴿ = γᴿ/γᴱ |
| LLE extraction factor | ε = KS/F |
