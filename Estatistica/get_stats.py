import pandas as pd
from sklearn.metrics import (
accuracy_score,
f1_score,
recall_score,
precision_score,
confusion_matrix)

# table = pd.DataFrame(elementos)
table = pd.read_csv("teste_botometer.csv")

#print (table)

y_pred = table.pred_saraV1
y_true = table.classe

print("Stats v1")
print("Acuracy",accuracy_score(y_true, y_pred))
print("Precision",precision_score(y_true,y_pred,average='macro'))
print("Recall",recall_score(y_true,y_pred,average='macro'))
print("F1 Macro ",f1_score(y_true, y_pred, average='macro'))
print("Matriz Confusao\n",confusion_matrix(y_true, y_pred))
# print(accuracy_score(y_true, y_pred, normalize=False))

print("Stats v2")
y_pred = table.pred_saraV2
y_true = table.classe
print("Acuracy",accuracy_score(y_true, y_pred))
print("Precision",precision_score(y_true,y_pred,average='macro'))
print("Recall",recall_score(y_true,y_pred,average='macro'))
print("F1 Macro",f1_score(y_true, y_pred, average='macro'))
print("Matriz Confusao\n",confusion_matrix(y_true, y_pred))

print("Botometer")
y_pred = table.botometer
y_true = table.classe
print("Acuracy",accuracy_score(y_true, y_pred))
print("Precision",precision_score(y_true,y_pred,average='macro'))
print("Recall",recall_score(y_true,y_pred,average='macro'))
print("F1 Macro",f1_score(y_true, y_pred, average='macro'))
print("Matriz Confusao\n",confusion_matrix(y_true, y_pred))
