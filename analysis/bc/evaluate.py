import pandas as pd
from sklearn.metrics import confusion_matrix


def calc_results(y_true, y_pred):
    """
    Calculate performance metrics. Input variables are array-likes of true
    outcomes and predicted outcomes.

    Returns the confusion matrix, the proportion of correct predictions,
    and the final score

    One for each beat type?

    """
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    cm = pd.DataFrame(cm, columns=['Predict 0', 'Predict 1'], index=['Actual 0', 'Actual 1'])

    # Correct classification proportion
    p_correct = (cm.iloc[0,0]+cm.iloc[1,1])/len(y_pred)

    score = auroc(cm)

    return cm, p_correct, auroc


def display_results(cm, pcorrect, score):
    """
    Display the performance results

    """
    print('Confusion Matrix:')
    display(cm)
    print('Proportion Correct:', pcorrect)
    print('AUROC:', score)

