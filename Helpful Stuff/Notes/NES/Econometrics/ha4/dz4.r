library(sandwich)
library(stargazer)
library(lmtest)
library(car)
library(margins)
options(scipen=999)


df <- read.csv('wage2.csv')
df <- within(df, interaction <- educ * pareduc)
m <- lm(log(age) ~ educ + pareduc + educ , data=df)


# =============== TASK 2 ===============
df <- read.csv('attend.csv')
df <- within(df,  priGPA2 <- priGPA * priGPA)
df <- within(df,  ACT2 <- ACT * ACT)
df <- within(df,  priGPA_x_atndrte <- priGPA * atndrte)

df <- within(df,  atndrte2 <- atndrte * atndrte)
df <- within(df,  atndrte_x_ACR<- ACT * atndrte)

m <- lm(stndfnl ~ atndrte + priGPA + ACT + priGPA2 + ACT2 + priGPA_x_atndrte, data=df)
summary(m)


m1 <- lm(stndfnl ~ atndrte + priGPA + ACT + priGPA2 + ACT2 + priGPA_x_atndrte
         + atndrte2 + atndrte_x_ACR, data=df) 
summary(m1)
linearHypothesis(m1, c('atndrte2 = 0', 'atndrte_x_ACR = 0'), )
# =============== TASK 4 ===============
df <- read.csv('hprice1.csv')
m <- lm(price ~ lotsize + sqrft + bdrms, data=df)
summary(m)

stargazer(coeftest(m, vcov=vcovHC(m, type='HC1')))
predict(m, newdata=list('lotsize'=10000, 'sqrft'=2300, 'bdrms'=4))

df <- read.csv('hprice1.csv')
df <- within(df, lotsize <- lotsize - 10000)
df <- within(df, sqrft <- sqrft - 2300 )
df <- within(df, bdrms <- bdrms - 4)

m <- lm(price ~ lotsize + sqrft + bdrms, data=df)
summary(m)

stargazer(confint(m, '(Intercept)'))

# =============== TASK 5 ===============
df <- read.csv('cps99_ps3.csv')
df <- within(df, female_x_yrseduc <- female * yrseduc)
m <- lm(log(ahe) ~ yrseduc + female +female_x_yrseduc, data=df)
stargazer(m)

plot(df[['yrseduc']], log(df[['ahe']]), pch = 16, cex = 1.3,
     col = "blue", main = "HEIGHT PLOTTED AGAINST BODY MASS",
     xlab = "BODY MASS (kg)", ylab = "HEIGHT (cm)")



male <- function(x) 1.587570 + 0.082676 * x
plot(male, 0, 10, col='blue', lwd=3, ylab='log(ahe)', xlab='yrseduc')
female <- function(x) (1.587570 - 0.463508)  + (0.082676 + 0.016665) * x
plot(female, 0, 10,col='red', add=TRUE, lwd=2)
legend('topleft', legend=c("male", "female"),
       col=c("blue", "red"), lty=1:1)


summary(m)
linearHypothesis(m, c('female = 0', 'female_x_yrseduc = 0'), )


# =============== TASK 6 ===============

df <- read.csv('cps99_ps3.csv')

df <- within(df, male <- abs(df[['female']] - 1))
df <- within(df, male_x_yrseduc <- male  * yrseduc)
df <- within(df, female_x_yrseduc <- female  * yrseduc)

m <- lm(log(ahe) ~ yrseduc + female + male_x_yrseduc + female_x_yrseduc, data=df)
summary(m)

df[['yrseduc']] - df[['male_x_yrseduc']] - df[['female_x_yrseduc']]


alias(df)



# =============== TASK 7 ===============
df <- read.csv('cps99_ps3.csv')
df <- within(df, age2 <- age * age)
df <- within(df, age3 <- age2 * age)

m1 <- lm(log(ahe) ~ yrseduc + female + female * yrseduc + age + age2 + age3, data=df)
m2 <- lm(log(ahe) ~ yrseduc + female + female * yrseduc + age + age2 + age3 + female* age + female * age2 + female * age3, data=df)
stargazer(m1)
stargazer(m2)

summary(m2)

lhs <- predict(m2, newdata=list('female'=0, age=55, age2=3025, age3=166375, yrseduc=16))
rhs <- predict(m2, newdata=list('female'=1, age=55, age2=3025, age3=166375, yrseduc=16))
lhs - rhs

0.041506426 + 0.020453557

