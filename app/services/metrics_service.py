from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score

def calculate_metrics(y_true, y_pred):
    label_map = {'positif': 1, 'négatif': 0}

    y_true_bin = [label_map[label] for label in y_true]
    y_pred_bin = [label_map[label] for label in y_pred]

    cm = confusion_matrix(y_true_bin, y_pred_bin)

    accuracy = accuracy_score(y_true_bin, y_pred_bin)
    precision = precision_score(y_true_bin, y_pred_bin)
    recall = recall_score(y_true_bin, y_pred_bin)
    f1 = f1_score(y_true_bin, y_pred_bin)

    return {
        'confusion_matrix': cm.tolist(),
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }
