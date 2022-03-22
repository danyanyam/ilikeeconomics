library(sandwich)
library(stargazer)
library(lmtest)
library(car)
library(margins)
options(scipen=999)

# Task 3.
# You are interested in estimating and obtaining a confidence interval for the
# percentage change in price when a 150-square-foot bedroom is added to a house.
# In decimal form, this is θ1 = 150β1 + β2. Use the data in hprice1.csv to estimate θ1.

df <- read.csv('hprice1.csv')
df <- within(df, theta_factor <- sqrft - 150 * bdrms)
m <- lm(log(price) ~ theta_factor + bdrms, data=df)
coeftest(m, vcov=vcovHC(m, type='HC1'))
stargazer(confint(m, 'bdrms', vcov=vcovHC(m, type='HC1')))

# Task 4
# First use the data set 401ksubs.csv, keeping only observations with
# fsize = 1 . Find the skewness measure for inc. Do the same for inc.
# Which variable has more skewness
df <- read.csv('401ksubs.csv')
df <- subset(df,  fsize == 1)
df <- within(df, log_inc <- log(df[['inc']]))

normalized_inc <- (df['inc'] - mean(df[['inc']])) / sd(df[['inc']])
sum(normalized_inc^3) / nrow(normalized_inc)

normalized_ln_inc <- (df['log_inc'] - mean(df[['log_inc']])) / sd(df[['log_inc']])
sum(normalized_ln_inc^3) / nrow(normalized_ln_inc)
hist(normalized_ln_inc$log_inc)

# 
# Next use \textit{bwght2.csv}. Find the skewness measures for \textit{bwght} and
# log(\textit{bwght}). What do you conclude?
df <- read.csv('bwght2.csv')
df <- within(df, log_inc <- log(df[['bwght']]))

normalized_bwdgt <- (df['bwght'] - mean(df[['bwght']])) / sd(df[['bwght']])
sum(normalized_inc^3) / nrow(normalized_inc)
hist(normalized_inc$bwght)

normalized_ln_inc <- (df['log_inc'] - mean(df[['log_inc']])) / sd(df[['log_inc']])
sum(normalized_ln_inc^3) / nrow(normalized_ln_inc)
hist(normalized_ln_inc$log_inc)

# Task 5
df <- read.csv('cps99_ps3.csv')

m <- lm(log(ahe) ~ yrseduc + age + female + hsdipl, data=df)
coeftest(m, vcov=vcovHC(m, type='HC1'))
stargazer(coeftest(m, vcov=vcovHC(m, type='HC1')))

sqrt(mean(m$residuals^2))

# Using this regression, provide a $ 95\% $ confidence interval for the gender gap in
# earnings (controlling for \textit{age}, \textit{years} of \textit{education}, and obtaining
# a high school diploma).
confint(m, 'female', vcov=vcovHC(m, type='HC1'))

# What is the estimated marginal value of $ 12 $ years of education culminating in a HS
# diploma, relative to $ 12 $ years of education and no HS diploma? Test (at the $ 5\% $
# significance level) the hypothesis that this marginal value is zero, against the hypothesis
# that it is not. Is this marginal value large or small in a real-world sense? Explain.


(12 * m$coefficients['yrseduc'] + m$coefficients['hsdipl']) / (12 * m$coefficients['yrseduc'])

df <- within(df, transformed <- df[['yrseduc']] - 12 *df[['hsdipl']])
m <- lm(log(ahe) ~ transformed + age + female + hsdipl, data=df)
coeftest(m, vcov=vcovHC(m, type='HC1'))

df <- within(df, transformed_2 <- df[['yrseduc']] - 2 *df[['hsdipl']])
m <- lm(log(ahe) ~ transformed_2 + age + female + hsdipl, data=df)
coeftest(m, vcov=vcovHC(m, type='HC1'))

confint(m, 'hsdipl', vcov=vcovHC(m, type='HC1'))

# task 6
df <- read.csv('cps99_ps3.csv')
df <- within(df, age2 <- df[['age']]^2)

m <- lm(log(ahe) ~ yrseduc + age + age2 + female + hsdipl, data=df)
stargazer(coeftest(m, vcov=vcovHC(m, type='HC1')))

linearHypothesis(m, c('age2 = 0'), vcov=vcovHC(m, type='HC1'))
# gender gap:
m <- lm(log(ahe) ~ yrseduc + age + female + hsdipl, data=df)
coeftest(m, vcov=vcovHC(m, type='HC1'))
m <- lm(log(ahe) ~ yrseduc + age + age2 + female + hsdipl, data=df)
coeftest(m, vcov=vcovHC(m, type='HC1'))

# 5.4
df <- read.csv('cps99_ps3.csv')
df <- within(df, age2 <- df[['age']]^2)
df <- within(df, age3 <- df[['age']]^3)


m <- lm(log(ahe) ~ yrseduc + age + female + hsdipl, data=df)
sqrt(mean(m$residuals^2))


# 6.d
m <- lm(log(ahe) ~ yrseduc + age + age2 + female + hsdipl, data=df)
linearHypothesis(m, c('age3 = 0'), vcov=vcovHC(m, type='HC1'))
sqrt(mean(m$residuals^2))

# 6.e
m <- lm(log(ahe) ~ yrseduc + age + age2 +age3 + female + hsdipl, data=df)
linearHypothesis(m, c('age3 = 0', 'age2 = 0'), vcov=vcovHC(m, type='HC1'))
sqrt(mean(m$residuals^2))

# 7
m <- lm(log(ahe) ~ yrseduc + age  + female + hsdipl, data=df)
summary(m)
margins(m, at=list(age=31))

m <- lm(log(ahe) ~ yrseduc + age + age2  + female + hsdipl, data=df)
summary(m)
margins(m, at=list(age=31))

m <- lm(log(ahe) ~ yrseduc + age + age2 +age3  + female + hsdipl, data=df)
summary(m)

age = 60
m$coefficients['age'] + m$coefficients['age2'] * age + m$coefficients['age3'] * age^2








