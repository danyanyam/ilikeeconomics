library(lmtest)
library(sandwich)
library(stargazer)
library(margins)

df <- read.csv('hprice1.csv')

model <- lm(price ~ sqrft + bdrms, data=df, )
model
summary(model)
coeftest(model, vcov = vcovHC(model, type = "HC1"))
summary(margins(model, at=list(sqrft=1400)))
predict(model, newdata = list(sqrft=2438, bdrms=4), )

# task 6
df <- read.csv('cps99_ps1.csv')
cor(df[['yrseduc']], df[['female']])

# task 8
df <- read.csv('cps99_ps1.csv')

m1 <- lm(ahe ~ yrseduc,  data=df)
m2 <- lm(ahe ~ yrseduc + female,  data=df)

summary(m1)
summary(m2)

stargazer(m2)
summary(m2)


# task 9
m <- lm(ahe ~ yrseduc + ba, data=df)
stargazer(coeftest(m, vcov = vcovHC(m, type = "HC1")))
margins(m)

stargazer(confint(m, vcov = vcovHC(m, type = "HC1"), level=0.9))
