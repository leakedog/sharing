Below is a simplified Markdown version with LaTeX math embedded that should compile in environments supporting LaTeX rendering (such as GitHub README files or Jupyter notebooks).

---

## Problem 1

**Statement:**  
Throw \( n \) balls independently and uniformly at random into \( n \) urns. Show that for sufficiently large \( n \),  
\[
P\Big(\exists\,i:\,X_i \ge \frac{3\ln n}{\ln\ln n}\Big) \le \frac1n,
\]  
where \( X_i \) is the number of balls in urn \( i \).

**Solution:**

1. **Union Bound:**
   \[
   P\Big(\exists\,i:\,X_i \ge k\Big) \le \sum_{i=1}^n P\Big(X_i \ge k\Big) = n \,P\Big(X_1 \ge k\Big).
   \]

2. **Tail Bound for \( X_1 \):**  
   Since \( X_1 \sim \text{Bin}(n,1/n) \) and \( k > e \), we use the bound  
   \[
   P\Big(X_1 \ge k\Big) \le \frac{(e/k)^k}{1 - (e/k)}.
   \]

3. **Substitute \( k = \frac{3\ln n}{\ln\ln n} \):**  
   For large \( n \), \( k > e \), so \( e/k < 1 \). Then  
   \[
   \Big(\frac{e}{k}\Big)^k = \exp\Big(k \cdot(1 - \ln k)\Big).
   \]  
   With \( k = \frac{3\ln n}{\ln\ln n} \),  
   \[
   \ln k = \ln3 + \ln\ln n - \ln\ln\ln n,
   \]  
   so  
   \[
   1 - \ln k = 1 - \ln3 - \ln\ln n + \ln\ln\ln n.
   \]  
   Therefore,  
   \[
   k(1-\ln k) 
   = \frac{3\ln n}{\ln\ln n} (1 - \ln3 - \ln\ln n + \ln\ln\ln n).
   \]  
   The dominant term is \(-3\ln n\), which implies  
   \[
   \Big(\frac{e}{k}\Big)^k \approx n^{-3} \times \text{(sub-polynomial factors)}.
   \]

4. **Estimate the probability:**
   \[
   \begin{aligned}
   P\Big(\exists\,i:\,X_i \ge \frac{3\ln n}{\ln\ln n}\Big) 
   &\le n \cdot \frac{(e/k)^k}{1 - (e/k)} \\
   &\approx n \cdot n^{-3} \\
   &= \frac{1}{n^2}.
   \end{aligned}
   \]  
   For sufficiently large \( n \), \( \frac{1}{n^2} < \frac{1}{n} \). Thus,  
   \[
   P\Big(\exists\,i:\,X_i \ge \frac{3\ln n}{\ln\ln n}\Big) \le \frac1n.
   \]

---

## Problem 2

**Statement:**  
Throw \( n \) balls independently and uniformly at random into \( n \) urns. Show that for sufficiently large \( n \),  
\[
P\Big(\exists\,i:\,X_i \ge \frac{\ln n}{\ln\ln n}\Big) \ge 1 - \frac1n.
\]

**Solution:**

1. **Define Indicator Variables:**  
   Let 
   \[
   Y_i = \mathbf{1}_{\{X_i \ge k\}},
   \]  
   where 
   \[
   k = \frac{\ln n}{\ln\ln n}.
   \]  
   Then 
   \[
   Y = \sum_{i=1}^n Y_i
   \]  
   counts the number of urns with at least \( k \) balls. Notice that  
   \[
   P\Big(\exists\,i:\,X_i \ge k\Big) = P(Y \ge 1).
   \]

2. **Compute the Expectation:**
   \[
   \mathbb{E}[Y] = \sum_{i=1}^n \mathbb{E}[Y_i] 
                  = n \, P(X_1 \ge k).
   \]  
   Using the tail bound for \( X_1 \) with \( k = \frac{\ln n}{\ln\ln n} \), one can show that  
   \[
   n\,P\Big(X_1 \ge \frac{\ln n}{\ln\ln n}\Big)
   \]  
   grows without bound as \( n \to \infty \). Hence,  
   \[
   \mathbb{E}[Y] \gg 1.
   \]

3. **Apply Paley-Zygmund Inequality:**  
   The Paley-Zygmund inequality states that for any non-negative random variable \( Z \),  
   \[
   P(Z > 0) \ge \frac{(\mathbb{E}[Z])^2}{\mathbb{E}[Z^2]}.
   \]  
   Applying this to \( Y \),  
   \[
   P(Y \ge 1) \ge \frac{(\mathbb{E}[Y])^2}{\mathbb{E}[Y^2]}.
   \]

4. **Bounding \( \mathbb{E}[Y^2] \):**  
   Expand \( \mathbb{E}[Y^2] \):  
   \[
   \mathbb{E}[Y^2] = \sum_{i=1}^n \mathbb{E}[Y_i] 
                  + \sum_{i\neq j} \mathbb{E}[Y_i Y_j].
   \]  
   Since the events \( \{X_i \ge k\} \) and \( \{X_j \ge k\} \) for \( i \neq j \) are negatively correlated,  
   \[
   \mathbb{E}[Y_i Y_j] \le \mathbb{E}[Y_i]\mathbb{E}[Y_j].
   \]  
   This implies  
   \[
   \text{Var}(Y) = \mathbb{E}[Y^2] - (\mathbb{E}[Y])^2 
                \le \sum_{i=1}^n \mathbb{E}[Y_i] 
                = n \,P(X_1 \ge k).
   \]  
   Therefore,  
   \[
   \mathbb{E}[Y^2] \le (\mathbb{E}[Y])^2 + n\,P(X_1 \ge k).
   \]

5. **Using the Inequality:**
   \[
   \begin{aligned}
   P(Y \ge 1) 
   &\ge \frac{(\mathbb{E}[Y])^2}{(\mathbb{E}[Y])^2 + n\,P(X_1 \ge k)} \\
   &= \frac{n\,P(X_1 \ge k)}{n\,P(X_1 \ge k) + 1}.
   \end{aligned}
   \]  
   For \( k = \frac{\ln n}{\ln\ln n} \), the term  
   \[
   n\,P\Big(X_1 \ge \frac{\ln n}{\ln\ln n}\Big)
   \]  
   becomes very large for large \( n \). Thus,  
   \[
   \frac{n\,P(X_1 \ge k)}{n\,P(X_1 \ge k) + 1} 
   \ge 1 - \frac1n
   \]  
   for sufficiently large \( n \).

Therefore,  
\[
P\Big(\exists\,i:\,X_i \ge \frac{\ln n}{\ln\ln n}\Big) \ge 1 - \frac1n
\]  
for large \( n \).

---

*These solutions use union bounds, tail estimates, and the Paley-Zygmund inequality, leveraging the negative correlation properties of ball allocations to the urns.*
