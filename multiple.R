# Stepwise regression
# Samplle data
library(MASS)
boston_data <- Boston
boston_data <- data.frame(boston_data)


##データセットの用意
y <- boston_data[,c(14)]
X <- data.frame(boston_data[,c(1:13)])

# _____以下を使う________

##変数選択(変数増加法)
accepted_variables = c() #追加された変数のベクトル
target_variables = c(1:length(X)) #探索対象の変数
best_score = 0 #現状、最高のスコアを記録

#変数が10個になるように探索
while (length(accepted_variables) < 10) {
  #一時的に記録したtempの記録を削除
  temp <- NULL
  
  for (i in target_variables) {
    #探索対象を含めたデータを用いて回帰分析を実行
    temp_data <- data.frame(X[, append(accepted_variables, i)])
    res <- lm(y ~ ., data = temp_data)
    
    #決定係数、もしくはAICで計算
    score_temp <- summary(res)$adj.r.squared
    #score_temp <- AIC(res)
    
    #ベストスコアを上回るかどうかを判断
    if (best_score < score_temp){
      temp <- i　　　　　　　#一時的に記録を保持
      best_score <- score_temp #最高記録の更新
    }
  }
  
  target_variables <- setdiff(target_variables, temp) #今回採用されたものを除く
  accepted_variables <- append(accepted_variables, temp) #今回採用されたものを追加
}

#t追加された変数を参照
print(colnames(X[,accepted_variables]))


##AICを使ったstepwiseの方法について
res_2 <- stepAIC(lm(y ~ ., data = X), direction = 'forward')


###Lasso
library("glmnet")

#CVで最適なハイパーパラメータの計算
lasso.model.cv <- cv.glmnet(x = as.matrix(X), y = y, family = 'gaussian', alpha = 1)
best_lambda <- lasso.model.cv$lambda.min #最適なパラメータ

#最適なハイパーパラメータの設定における、モデルの確認
lasso.model <- glmnet(x = as.matrix(X), y = y, family = 'gaussian', lambda =  best_lambda, alpha = 1)
summary(lasso.model)
print(lasso.model$beta)

#Lasso pathの追加
library(ggfortify)
lasso.all_model <- glmnet(x = as.matrix(X), y = y, family = 'gaussian', alpha = 1)
ggplot2::autoplot(lasso.all_model, xvar = 'lambda')