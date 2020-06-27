library(ggplot2)


### Load result data
dat = read.csv("data/model_results.csv", stringsAsFactors = FALSE)
dat$date = as.Date(dat$date, format='%Y-%m-%d')

### Load polling data
pdat = read.csv("data/processed_economist_data.csv", stringsAsFactors = FALSE)
pdat$date = as.Date(pdat$date, format='%Y-%m-%d')


ggplot() +
  geom_line(data = subset(dat, candidate == "Biden"), aes(date, pct, group=factor(sample)), color='blue', alpha=0.05) +
  geom_line(data = subset(dat, candidate == "Trump"), aes(date, pct, group=factor(sample)), color='red', alpha=0.05) +
  geom_smooth(data = subset(dat, candidate == "Trump"), aes(date, pct), color='red', size=0.5, se = FALSE, method='loess') +
  geom_smooth(data = subset(dat, candidate == "Biden"), aes(date, pct), color='blue', size=0.5,  se = FALSE, method='loess') +
  geom_point(data = subset(pdat, candidate == "Biden"), aes(date, pct), color='blue', alpha=0.5) +
  geom_point(data = subset(pdat, candidate == "Trump"), aes(date, pct), color='red', alpha=0.5) +
  theme_bw() +
  theme(legend.position="none") +
  labs(x=NULL, y="Share of Vote") +
  facet_wrap(~state, ncol = 2, scales='free') +
  NULL


ggsave("figures/GP_model_results.png", width=12, height = 16)
