# Fit Gaussian process model to poll data

library(tidyverse)
library(lubridate)
library(rstan)

swing <- c("North Carolina", "Michigan", "Arizona", "Wisconsin", "Florida", "Pennsylvania")
canidate <- c("Biden", "Trump")

# Load and filter data
dat <- read_csv("data/president_polls.csv") %>%
  # keep only swing states
  filter(state %in% swing) %>%
  # define date of the the ending date
  mutate(date = mdy(end_date)) %>%
  # keep only polls started after sanders droped out on April 8 2020
  filter(mdy(start_date) > mdy("04/8/2020")) %>%
  # convert percent to decimal
  mutate(pct = pct / 100)

# Iteratively fit the model for each state and candidate
rstan_options(auto_write = TRUE)
options(mc.cores = parallel::detectCores())

model_results <- list(list(), list())

for (c in 1:2) {
  for (s in 1:6) {
    dat_mod <- dat %>%
      filter(state == swing[s] &
               answer == canidate[c]) %>%
      mutate(days = as.numeric(date - mdy("04/8/2020")))  %>%
      arrange(days)
    
    # Make stan data list
    stan_dat <- list(N = nrow(dat_mod),
                     x = dat_mod$days,
                     y = dat_mod$pct)
    
    fit <- stan(file = "GP.stan",
                data = stan_dat,
                iter = 4000,
                chains = 4)
    
    p <- rstan::extract(fit, pars = "predicted_y")[[1]]
    p_subset <- p[sample(1:nrow(p), 100, replace = F),]
    
    model_results[[c]][[s]] <- p_subset
  }
}


# Plot GP results
# Plot Biden/Trump by state
plot_list <- list()
grob_list <- list()

for(i in 1: length(swing)) {
  plot_list[[i]] <- ggplot() +
    geom_point(data = dat[dat$state == swing[i] & dat$answer == "Biden",], aes(x = date, y = pct * 100), color = "blue") +
    geom_point(data = dat[dat$state == swing[i] & dat$answer == "Trump",], aes(x = date, y = pct * 100), color = "red") +
    scale_y_continuous(limits = c(20, 80)) +
    scale_x_date(limits = c(min(dat$date), max(dat$date))) +
    labs(x = "Date", y = "Percent", title = swing[i]) +
    theme_minimal()
  
  dat_plot <- dat %>%
    filter(state == swing[i] &
             answer == "Biden") %>%
    mutate(days = as.numeric(date - mdy("04/8/2020")))  %>%
    arrange(days)
  
  for (j in 1:100) {
    plot_list[[i]] <- plot_list[[i]] +
      geom_line(data = data.frame(p = as.vector(model_results[[1]][[i]][j,]), 
                                  t = dat_plot$date),
                aes(x = t, y = p * 100), 
                col = "blue", alpha = .2, size = .1) +
      geom_line(data = data.frame(p = as.vector(model_results[[2]][[i]][j,]), 
                                  t = dat_plot$date),
                aes(x = t, y = p * 100), 
                col = "red", alpha = .2, size = .1)
  }
  
  grob_list[[i]] <- ggplotGrob(plot_list[[i]])
}

g <- grid.arrange(grob_list[[1]],
                  grob_list[[2]],
                  grob_list[[3]],
                  grob_list[[4]],
                  grob_list[[5]],
                  grob_list[[6]], ncol = 2)

g

ggsave("figures/swing_gp_predictions.jpg", plot = g, width = 8, height = 6, units = "in")


##########
# Below is my testing code for biden in NC
##########
# Data for testing
dat_NC_Biden <- dat %>%
  filter(state == "North Carolina" &
           answer == "Biden") %>%
  mutate(days = as.numeric(date - mdy("04/8/2020")))  %>%
  arrange(days)

# Make stan data list
stan_dat <- list(N = nrow(dat_NC_Biden),
                 x = dat_NC_Biden$days,
                 y = dat_NC_Biden$pct)

rstan_options(auto_write = TRUE)
options(mc.cores = parallel::detectCores())

fit <- stan(file = "GP.stan",
            data = stan_dat,
            iter = 4000,
            chains = 4)

check_hmc_diagnostics(fit)

print(fit)

# Extract predicted percents
p <- rstan::extract(fit, pars = "predicted_y")[[1]]
p_subset <- p[sample(1:nrow(p), 100, replace = F),]

g <- ggplot() +
  geom_point(data = dat[dat$state == swing[1] & dat$answer == "Biden",], aes(x = date, y = pct * 100), color = "blue")

for (i in 1:100) {
  g <- g +
    geom_line(data = data.frame(p = as.vector(p_subset[i,]), 
                                         t = dat_NC_Biden$date),
                       aes(x = t, y = p * 100), 
                       col = "blue", alpha = .2, size = .1)
}
g