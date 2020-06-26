library(ggplot2)

### Load result data
dat = read.csv("data/model_results.csv")

### Load polling data
pdat = read.csv("data/processed_economist_data.csv")


ggplot() +
  geom_line(data = subset(dat, candidate == "Biden"), aes(date, pct, group=factor(sample)), color='blue', alpha=0.05) +
  geom_line(data = subset(dat, candidate == "Trump"), aes(date, pct, group=factor(sample)), color='red', alpha=0.05) +
  geom_smooth(data = subset(dat, candidate == "Trump"), aes(date, pct), color='red', size=0.5, se = FALSE) +
  geom_smooth(data = subset(dat, candidate == "Biden"), aes(date, pct), color='blue', size=0.5, se = FALSE) +
  geom_point(data = subset(pdat, candidate == "Biden"), aes(date, pct), color='blue', alpha=0.5) +
  geom_point(data = subset(pdat, candidate == "Trump"), aes(date, pct), color='red', alpha=0.5) +
  theme_bw() +
  theme(legend.position="none") +
  ylim(.20, .80) +
  labs(x=NULL, y="Share of Vote") +
  facet_wrap(~state, ncol = 3) +
  NULL


ggsave("figures/GP_model_results.png", width=18, height = 12)
