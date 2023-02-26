"""Script to test the metric for evaluating concept prediction via kNN in the ResNet latent space"""

y_true = [0, 2]
y_pred = [1, 2]
acc = 0.0

if sorted(y_true) == sorted(y_pred):
    acc = 1.0
else:
    inter = set(y_true) & set(y_pred)
    if len(inter) > 0:
        acc = 0.5
print(acc)
