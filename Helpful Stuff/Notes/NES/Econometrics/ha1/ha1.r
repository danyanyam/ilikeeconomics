library(lmtest)
library(sandwich)
library(stargazer)

getwd()

df <- read.table('cps99_ps1.csv', sep=',', header=TRUE)


# ================================= TASK 5 =====================================
# 5. Using R, compute the sample mean and standard deviation of ahe
# (average hourly earnings), yrseduc (years of education), and female.

sample_std <- function(df, colname) {
  sample_mean <- lapply(df[colname], mean)
  sample_size <- length(df[[colname]]) - 1
  return(sqrt(1/(sample_size - 1) * sum((df[colname] - sample_mean)^2)))
}

sample_mean <- function(df, colname) {
  return(lapply(df[colname], mean))
}

sample_std(df, 'ahe')        # 8.028319
sample_std(df, 'yrseduc')    # 2.48002
sample_std(df, 'female')     # 0.4963357

sample_mean(df, 'ahe')       # 15.19042
sample_mean(df, 'yrseduc')   # 13.46549
sample_mean(df, 'female')    # 0.4385083

# ================================= TASK 6 =====================================
#  Estimate a regression of ahe on yrseduc

model <- lm(ahe ~ yrseduc, data=df)

# a. What is the coefficient on yrseduc? Explain in words what it means.
# Is the numerical value of your estimate large or small in an economic
# (real-world) sense?

summary(model)
# Answer: Coefficient is 1.32186. It means that one additional year of education
# on average increases average hourly earnings for 1.32186 dollars.
# It means that each additional year of education increases daily earnings by
# 1.32186 * 8 = 10 dollars and monthly earnings by 10 * 30 = 300 dollars.
# Therefore, starting from 6th class of school, each additional year gives us
# approximately 20k rubles. By now i have studied for 9 years which would 
# promise me a salary of 180k rubles. For my opinion it is quite a lot in
# real-world Russian situation.
# ------------------------------------------------------------------------------
# b. Graph the data points and the estimated regression line.

plot(x=df[['yrseduc']], y=df[['ahe']], col='blue',
     ylab='average hourly earnings', xlab='years of education') 
abline(model, col='red') 
# ------------------------------------------------------------------------------
# c. Is the slope coefficient statistically significantly different from zero?
# Show how you reach this conclusion. Use heteroskedasticity-robust standard 
# errors to answer this question.

coeftest(model, vcov = vcovHC(model, type = "HC1"))
# Answer:
# 
# Estimate Std. Error t value  Pr(>|t|)    
# (Intercept) -2.609050   0.647177 -4.0314 5.653e-05 ***
# yrseduc      1.321859   0.050043 26.4145 < 2.2e-16 ***
# ---
# Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# 
# Since P-value is far below 0.05, that means that the probability of obtaining
# the same value for coefficient yrseduc assuming zero hypothesis relevance
# (coeff equals to zero) is very low. Therefore the slope is statistically 
# significantly different from zero.
# ------------------------------------------------------------------------------
# d. Report the 95% confidence interval for β1, the slope of the population
# regression line. Use heteroskedasticity-robust standard errors to answer this
# question.

confint(model, vcov = vcovHC(model, type = "HC1"))
#                 2.5 %    97.5 %
# yrseduc      1.227613  1.416104
# ------------------------------------------------------------------------------
# e. What is the R2 of this regression? What does this mean?

summary(model)
# Multiple R-squared: 0.1667. It means that years of education explain earnings 
# varinace by fraction of 0.1667. It also means that correlation between
# years of education and hourly earnings is 0.16^2 = 0.4.
# ------------------------------------------------------------------------------
# f. Compute the correlation coefficient between ahe and yrseduc, and compare
# its square to the R2. How are the correlation coefficient and the R2 related

cor(df['ahe'], df['yrseduc'])   # 0.4083341
# We see that correlation is very close to the square root of R^2:
# 0.4082891 vs 0.4083341
# ------------------------------------------------------------------------------
# g. What is the root mean squared error of the regression? What does this mean?
sqrt(mean(model$residuals^2))
# ------------------------------------------------------------------------------
# h. Based on your graph from (b), does the error term appear to be
# homoskedastic or heteroskedastic?

# Answer: seems like the average hourly earnings distribution becomes more 
# heavy tailed with each additional year of education. It implies that variance
# of ahe depends on yrseduc and therefore the error term appear to be
# heteroskedastic.

# ================================= TASK 7 =====================================
# Estimate a regression of ahe on female.
m <- lm(ahe ~ female, data=df)

# a. What is the coefficient on female? Explain in words what this means. Is the
# numerical value of your estimate large or small in an economic(real-world)
# sense?

summary(m)
# Answer: Coefficient on female is -3.2026. It means that women on average 
# receive hourly by 3.2026 less dollars. It means that women receive (other 
# factors excluded) by 3.2026 * 8 * 30 = 768.6 dollars less monthly than men.
# In terms of rubles it would be around 50k per month. Honestly, it is difficult
# to say, whether women in Russia receive so much less compared to men, because
# a lot of factors (such as education for example) are not taken into
# consideration.

plot(x=df[['female']], y=df[['ahe']], col='blue',
     ylab='average hourly earnings', xlab='female') 
abline(m, col='red') 
# ------------------------------------------------------------------------------
# b. Test the hypothesis that average hourly earnings are the same for male and
# female workers, against the alternative that they differ, at the 5% 
# significance level. Make sure to use heteroskedasticity-robust standard errors
# to answer this question.
stargazer(coeftest(m, vcov = vcovHC(m, type = "HC1")))


df_f = df[df$female == 1,]
df_m = df[df$female == 0,]
summary(df)

t.test(df_f["ahe"], df_m["ahe"], alternative="two.sided", var.equal = FALSE)

# ------------------------------------------------------------------------------
# c. Compute the sample average of ahe for women, and the sample average of ahe
# for men; from this compute an estimate of the “gender gap” in earnings; and
# construct the t-statistic testing the hypothesis that the gender gap is zero.
# Make sure to use heteroskedasticity-robust standard errors to answer this
# question. Compare your results to those in parts (a) and (b).
# ------------------------------------------------------------------------------
f_mean = mean(df_f$ahe)
f_std = sd(df_f$ahe)

m_mean = mean(df_m$ahe)
m_std = sd(df_m$ahe)

gap = m_mean - f_mean
denominator = sqrt(f_std^2/nrow(df_f) + m_std^2/nrow(df_m))

gap/denominator

