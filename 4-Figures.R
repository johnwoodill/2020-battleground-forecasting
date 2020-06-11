library(tidyverse)

# Load data
dat = read_csv("data/model_results.csv")


ggplot() +
  geom_line(data = filter(dat, candidate == "Biden"), aes(date, pct, group=factor(sample)), color='blue', alpha=0.05) +
  geom_line(data = filter(dat, candidate == "Trump"), aes(date, pct, group=factor(sample)), color='red', alpha=0.05) +
  theme_bw() +
  # theme(legend.position="none") +
  ylim(.20, .80) +
  labs(x=NULL, y="Share of Vote") +
  facet_wrap(~state) +
  NULL

