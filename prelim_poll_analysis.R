# Visualize raw democratic poll data for the swing states.

library(tidyverse)
library(lubridate)
library(gridExtra)

# Define swing states
swing <- c("North Carolina", "Michigan", "Arizona", "Wisconsin", "Florida", "Pennsylvania")

# Load and filter data
dat <- read_csv("data/president_polls.csv") %>%
  # keep only swing states
  filter(state %in% swing) %>%
  # define date of the the ending date
  mutate(date = mdy(end_date)) %>%
  # keep only polls started after sanders droped out on April 8 2020
  filter(mdy(start_date) > mdy("04/8/2020"))

# Plot Biden/Trump by state
plot_list <- list()
grob_list <- list()

for(i in 1: length(swing)) {
  plot_list[[i]] <- ggplot() +
    geom_point(data = dat[dat$state == swing[i] & dat$answer == "Biden",], aes(x = date, y = pct), color = "blue") +
    geom_point(data = dat[dat$state == swing[i] & dat$answer == "Trump",], aes(x = date, y = pct), color = "red") +
    scale_y_continuous(limits = c(20, 80)) +
    scale_x_date(limits = c(min(dat$date), max(dat$date))) +
    labs(x = "Date", y = "Percent", title = swing[i]) +
    theme_minimal()
  
  grob_list[[i]] <- ggplotGrob(plot_list[[i]])
}

g <- grid.arrange(grob_list[[1]],
             grob_list[[2]],
             grob_list[[3]],
             grob_list[[4]],
             grob_list[[5]],
             grob_list[[6]], ncol = 2)

ggsave("figures/swing_poll_prelim.jpg", plot = g, width = 8, height = 6, units = "in")