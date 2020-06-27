data {
  int<lower=0> N;
  real x[N];
  vector[N] y;
}

transformed data {
  real delta = 1e-9;
}

parameters {
  real<lower=0> rho;
  real<lower=0> alpha;
  real<lower=0> sigma;
  vector[N] eta;
  real gamma;
  real mu_gamma;
  real<lower=0> sigma_gamma;
}

model {
  vector[N] f;
  {
    matrix[N, N] L_K;
    matrix[N, N] K = cov_exp_quad(x, alpha, rho);

    // diagonal elements
    for (n in 1:N)
      K[n, n] = K[n, n] + delta;

    L_K = cholesky_decompose(K);
    f = L_K * eta;
  }

  rho ~ inv_gamma(5, 5);
  alpha ~ normal(0, 0.07);  //wiggle magnitude (change from pt to pt)
  sigma ~ normal(0, 0.08);  //model error
  eta ~ normal(0, 1);
  mu_gamma ~ normal(0.5, 0.5);
  sigma_gamma ~ normal(0, 1);
  gamma ~ normal(mu_gamma, sigma_gamma);

  y ~ normal(gamma + f, sigma);
}

generated quantities {
  vector[N] predicted_y;
  vector[N] f_new;
  real gamma_new;
  {
    matrix[N, N] L_K_new;
    matrix[N, N] K_new = cov_exp_quad(x, alpha, rho);

    // diagonal elements
    for (n in 1:N)
      K_new[n, n] = K_new[n, n] + delta;

    L_K_new = cholesky_decompose(K_new);
    f_new = L_K_new * eta;
  }
  
  gamma_new = normal_rng(mu_gamma, sigma_gamma);
  
  for (i in 1:N)
  predicted_y[i] = normal_rng(gamma_new + f_new[i], sigma);
}
