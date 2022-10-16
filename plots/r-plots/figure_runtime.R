library(magrittr) # needs to be run every time you start R and want to use %>%
library(dplyr)    # alternatively, this also loads %>%
library(ggplot2)
library(withr)
library(RColorBrewer)
# put your working directory
wd <- getwd()
setwd(wd)

# pos paris
df <- read.csv('./Data/runtime.csv')
#head(df)

png("runtime.png",width=4, height=2.7 ,units="in",res=500) #9*6.5 for 3X3#9*8.4 for 3X4 # 9*4.3for 3X2
df %>% ggplot() + 
  #facet_wrap(vars(drug_pairs), ncol = 3) +
  geom_point(aes(x = factor(Method, level = c('Semantic','OneHop','TwoHop'))  , y = Runtime,  color = Method))+ 
  scale_y_log10("Runtime (seconds)")+
  scale_color_brewer(palette="Set1")+
  scale_x_discrete("Method") +
  theme_bw()+
  theme(legend.position = "none") 
  
dev.off()

