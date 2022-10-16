
library(magrittr) # needs to be run every time you start R and want to use %>%
library(dplyr)    # alternatively, this also loads %>%
library(tidyr)
library(ggplot2)
library(withr)
library(RColorBrewer)

# put your working directory
wd <- getwd()
setwd(wd)

# load SRW data 
df2 <- read.csv('./Data/robokop_pos_nonsemantic.csv')
df3 <- read.csv('./Data/robokop_pos_nonsemantic_lower.csv')

# add levels
Level <- 'non-semantic I'
df2 <- cbind(Level ,df2)
Level <- 'non-semantic II'
df3 <- cbind(Level ,df3)
df <- rbind(df2, df3)
head(df)

# remove metapath2vec
tt<- df$method != 'metapath2vec'
df <- df[tt,]

# pick 3 pairs
tt <- df$drug_pairs == "['fluconazole', 'voriconazole']" | df$drug_pairs == "['lapatinib', 'afatinib']" | df$drug_pairs == "['captopril', 'enalapril']"
df <- df[tt,]

# plot: cos_sim vs SR_W
png("SRW.png",width=9, height=2.7 ,units="in",res=500) #9*6.5 for 3X3#9*8.4 for 3X4 # 9*4.3for 3X2
df %>% ggplot(aes(x = SR_walks , y = cos_sim)) + 
  facet_wrap(vars(drug_pairs), ncol = 3) +
  geom_point(aes(x = SR_walks , y = cos_sim, color=walk_length, shape=Level))+
  scale_x_continuous("Semantic ratio in walks") +
  scale_y_continuous("cosine similarity")+theme_bw()
dev.off()
# the syntax png and dev can be used if you want to output the resulted figure
