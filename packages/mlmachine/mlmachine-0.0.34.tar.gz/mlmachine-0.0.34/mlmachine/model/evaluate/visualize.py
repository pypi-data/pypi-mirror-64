import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.model_selection import (
    KFold,
    train_test_split,
    GridSearchCV,
    StratifiedKFold,
    cross_val_score,
    RandomizedSearchCV,
)
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    explained_variance_score,
    mean_squared_log_error,
    mean_absolute_error,
    median_absolute_error,
    mean_squared_error,
    r2_score,
    confusion_matrix,
    roc_curve,
    accuracy_score,
    roc_auc_score,
    homogeneity_score,
    completeness_score,
    classification_report,
    silhouette_samples,
    plot_confusion_matrix,
)

from scipy import stats

from prettierplot.plotter import PrettierPlot
from prettierplot import style


def binary_classification_panel(self, model, X_train, y_train, X_valid=None, y_valid=None, labels=None,
                        n_folds=None, title_scale=1.0, color_map="viridis", random_state=1, chart_scale=15):
    """
    Documentation:
        Description:
            generate a panel of reports and visualizations summarizing the
            performance of a classification model.
        paramaters:
            model : model object
                instantiated model object.
            X_train : Pandas DataFrame
                training data observations.
            y_train : Pandas Series
                training data labels.
            X_valid : Pandas DataFrame, default=None
                validation data observations.
            y_valid : Pandas Series, default=None
                validation data labels.
            labels : list, default=None
                custom labels for confusion matrix axes. if left as none,
                will default to 0, 1, 2...
            n_folds : int, default=None
                number of cross_validation folds to use when generating
                cv roc graph. If validation data is provided through X_valid/y_valid,
                n_folds is ignored
            color_map : string specifying built_in matplotlib colormap, default="viridis"
                colormap from which to draw plot colors.
            title_scale : float, default=1.0
                controls the scaling up (higher value) and scaling down (lower value) of the size of
                the main chart title, the x_axis title and the y_axis title.
            random_state : int, default=1
                random number seed.
            chart_scale : int or float, default=15
                controls chart size and proportions. higher value creates larger plots and increases visual elements proportionally.
    """

    print("*" * 55)
    print("* Estimator: {}".format(model.estimator_name))
    print("* Parameter set: {}".format(model.model_iter))
    print("*" * 55)

    print("\n" + "*" * 55)
    print("Training data evaluation\n")

    ## training panel
    # generate predictions
    y_pred = model.fit(X_train, y_train).predict(X_train)
    print(
            classification_report(
                y_train,
                y_pred,
                target_names=labels if labels is not None else np.unique(y_train.values),
            )
        )

    # create canvas
    p = PrettierPlot(chart_scale=chart_scale, plot_orientation="wide_narrow")

    # confusion matrix
    ax = p.make_canvas(
        title="Confusion matrix - training data\nModel: {}\nParameter set: {}".format(
            model.estimator_name, model.model_iter
        ),
        y_shift=0.4,
        x_shift=0.25,
        position=121,
        title_scale=title_scale,
    )

    plot_confusion_matrix(
        estimator=model,
        X=X_train,
        y_true=y_train,
        display_labels=labels if labels is not None else np.unique(y_train.values),
        cmap=color_map,
        values_format=".0f",
        ax=ax,
    )

    # ROC curve
    ax = p.make_canvas(
        title="ROC curve - training data\nModel: {}\nParameter set: {}".format(
            model.estimator_name,
            model.model_iter,
        ),
        x_label="False positive rate",
        y_label="True positive rate",
        y_shift=0.35,
        position=122,
        # position=111 if X_valid is not None else 121,
        title_scale=title_scale,
    )
    p.roc_curve_plot(
        model=model,
        X_train=X_train,
        y_train=y_train,
        linecolor=style.style_grey,
        ax=ax,
    )
    plt.subplots_adjust(wspace=0.3)
    plt.show()

    # if cross-validation
    if X_valid is not None:
        print("\n" + "*" * 55)
        print("Validation data evaluation\n")

        # generate colors
        # color_list = style.color_gen(color_map, num=len(cv))

        # generate predictions
        y_pred = model.fit(X_train, y_train).predict(X_valid)

        print(
            classification_report(
                y_valid,
                y_pred,
                target_names=labels if labels is not None else np.unique(y_train.values),
            )
        )

        # create canvas
        p = PrettierPlot(chart_scale=chart_scale, plot_orientation="wide_narrow")

        # visualize results with confusion matrix
        ax = p.make_canvas(
            title="Confusion matrix - validation data\nModel: {}\nParameter set: {}".format(
                model.estimator_name, model.model_iter
            ),
            y_shift=0.4,
            x_shift=0.25,
            position=121,
            title_scale=title_scale,
        )

        plot_confusion_matrix(
            estimator=model,
            X=X_valid,
            y_true=y_valid,
            display_labels=labels if labels is not None else np.unique(y_train.values),
            cmap=color_map,
            values_format=".0f",
            ax=ax,
        )

        # ROC curve
        ax = p.make_canvas(
            title="ROC curve - validation data\nModel: {}\nParameter set: {}".format(
                model.estimator_name,
                model.model_iter,
            ),
            x_label="False positive rate",
            y_label="True positive rate",
            y_shift=0.35,
            position=122,
            # position=111 if X_valid is not None else 121,
            title_scale=title_scale,
        )
        p.roc_curve_plot(
            model=model,
            X_train=X_train,
            y_train=y_train,
            X_valid=X_valid,
            y_valid=y_valid,
            linecolor=style.style_grey,
            ax=ax,
        )
        plt.subplots_adjust(wspace=0.3)
        plt.show()

    elif isinstance(n_folds, int):
        print("\n" + "*" * 55)
        print("Cross validation evaluation\n")

        # cross_validated roc curve
        cv = list(
            StratifiedKFold(
                n_splits=n_folds, shuffle=True, random_state=random_state
            ).split(X_train, y_train)
        )

        # generate colors
        color_list = style.color_gen(color_map, num=len(cv))

        for i, (train_ix, valid_ix) in enumerate(cv):
            print("\n" + "*" * 55)
            print("CV Fold {}\n".format(i + 1))

            X_train_cv = X_train.iloc[train_ix]
            y_train_cv = y_train.iloc[train_ix]
            X_valid_cv = X_train.iloc[valid_ix]
            y_valid_cv = y_train.iloc[valid_ix]

            # generate predictions
            y_pred = model.fit(X_train_cv, y_train_cv).predict(X_valid_cv)
            print(
            classification_report(
                    y_valid_cv,
                    y_pred,
                    target_names=labels if labels is not None else np.unique(y_train.values),
                )
            )

            # create canvas
            p = PrettierPlot(chart_scale=chart_scale, plot_orientation="wide_narrow")

            # visualize results with confusion matrix
            ax = p.make_canvas(
                title="Confusion matrix - CV Fold {}\nModel: {}\nParameter set: {}".format(
                    i + 1, model.estimator_name, model.model_iter
                ),
                y_shift=0.4,
                x_shift=0.25,
                position=121,
                title_scale=title_scale,
            )

            plot_confusion_matrix(
                estimator=model,
                X=X_valid_cv,
                y_true=y_valid_cv,
                display_labels=labels if labels is not None else np.unique(y_train.values),
                cmap=color_map,
                values_format=".0f",
                ax=ax,
            )

            # ROC curve
            ax = p.make_canvas(
                title="ROC curve - CV Fold {}\nModel: {}\nParameter set: {}".format(
                    i + 1,
                    model.estimator_name,
                    model.model_iter,
                ),
                x_label="False positive rate",
                y_label="True positive rate",
                y_shift=0.35,
                position=122,
                # position=111 if X_valid is not None else 121,
                title_scale=title_scale,
            )
            p.roc_curve_plot(
                model=model,
                X_train=X_train_cv,
                y_train=y_train_cv,
                X_valid=X_valid_cv,
                y_valid=y_valid_cv,
                linecolor=style.style_grey,
                ax=ax,
            )
            plt.subplots_adjust(wspace=0.3)
            plt.show()

def regression_panel(self, model, X_train, y_train, X_valid=None, y_valid=None, n_folds=None, title_scale=1.0,
                    color_map="viridis", random_state=1, chart_scale=15):
    """
    Documentation:
        Description:
            creates a set of residual plots and pandas DataFrames, where each row captures various summary statistics
            pertaining to a model's performance. generates residual plots and captures performance data for training
            and validation datasets. if no validation set is provided, then cross_validation is performed on the
            training dataset.
        paramaters:
            model : model object
                instantiated model object.
            X_train : Pandas DataFrame
                training data observations.
            y_train : Pandas Series
                training data labels.
            X_valid : Pandas DataFrame, default=None
                validation data observations.
            y_valid : Pandas Series, default=None
                validation data labels.
            n_folds : int, default=3
                number of cross_validation folds to use when generating
                cv roc graph.
            random_state : int, default=1
                random number seed.
            title_scale : float, default=1.0
                controls the scaling up (higher value) and scaling down (lower value) of the size of
                the main chart title, the x_axis title and the y_axis title.
            color_map : string specifying built_in matplotlib colormap, default="viridis"
                colormap from which to draw plot colors.
            chart_scale : int or float, default=15
                controls chart size and proportions. higher value creates larger plots and increases visual elements proportionally.
    """

    print("*" * 55)
    print("* Estimator: {}".format(model.estimator_name))
    print("* Parameter set: {}".format(model.model_iter))
    print("*" * 55)

    print("\n" + "*" * 55)
    print("Training data evaluation")

    model.fit(X_train.values, y_train.values)

    ## training dataset
    y_pred = model.predict(X_train.values)
    residuals = y_pred - y_train.values

    # residual plot
    p = PrettierPlot(plot_orientation="wide_narrow")
    ax = p.make_canvas(
        title="Residual plot - training data\nModel: {}\nParameter set: {}".format(
            model.estimator_name,
            model.model_iter,
        ),
        x_label="Predicted values",
        y_label="Residuals",
        y_shift=0.55,
        title_scale=title_scale,
        position=121,
    )

    # x units
    if -1 <= np.nanmax(y_pred) <= 1:
        x_units = "fff"
    elif -100 <= np.nanmax(y_pred) <= 100:
        x_units = "ff"
    else:
        x_units = "f"

    # y units
    if -0.1 <= np.nanmax(residuals) <= 0.1:
        y_units = "ffff"
    elif -1 <= np.nanmax(residuals) <= 1:
        y_units = "fff"
    elif -10 <= np.nanmax(residuals) <= 10:
        y_units = "ff"
    else:
        y_units = "f"

    # x rotation
    if -10000 < np.nanmax(y_pred) < 10000:
        x_rotate = 0
    else:
        x_rotate = 45

    p.scatter_2d(
        x=y_pred,
        y=residuals,
        size=7,
        color=style.style_grey,
        y_units=y_units,
        x_units=x_units,
        ax=ax,
    )
    plt.hlines(
        y=0, xmin=np.min(y_pred), xmax=np.max(y_pred), color=style.style_grey, lw=2
    )

    ## univariate plot
    ax = p.make_canvas(
        title="Residual distribution - training data\nModel: {}\nParameter set: {}".format(
            model.estimator_name,
            model.model_iter,
        ),
        title_scale=title_scale,
        position=122,
    )

    p.dist_plot(
        residuals,
        fit=stats.norm,
        color=style.style_grey,
        y_units="ff",
        x_units="fff",
        ax=ax,
    )
    plt.show()

    # training data results summary
    results = self.regression_stats(
        model=model,
        y_true=y_train.values,
        y_pred=y_pred,
        feature_count=X_train.shape[1],
    )
    # create shell results DataFrame and append
    regression_results_summary = pd.DataFrame(columns=list(results.keys()))
    regression_results_summary = regression_results_summary.append(
        results, ignore_index=True
    )

    ## validation dataset
    # if validation data is provided...
    if X_valid is not None:
        print("\n" + "*" * 55)
        print("Training data evaluation")

        y_pred = model.predict(X_valid.values)
        residuals = y_pred - y_valid.values

        # residual plot
        p = PrettierPlot(plot_orientation="wide_narrow")
        ax = p.make_canvas(
            title="Residual plot - training data\nModel: {}\nParameter set: {}".format(
                model.estimator_name,
                model.model_iter,
            ),
            x_label="Predicted values",
            y_label="Residuals",
            y_shift=0.55,
            title_scale=title_scale,
            position=121,
        )

        p.scatter_2d(
            x=y_pred,
            y=residuals,
            size=7,
            color=style.style_grey,
            y_units=y_units,
            x_units=x_units,
            ax=ax,
        )
        plt.hlines(
            y=0, xmin=np.min(y_pred), xmax=np.max(y_pred), color=style.style_grey, lw=2
        )

        ## univariate plot
        ax = p.make_canvas(
            title="Residual distribution - training data\nModel: {}\nParameter set: {}".format(
                model.estimator_name,
                model.model_iter,
            ),
            title_scale=title_scale,
            position=122,
        )

        p.dist_plot(
            residuals,
            fit=stats.norm,
            color=style.style_grey,
            y_units="ff",
            x_units="fff",
            ax=ax,
        )
        plt.show()

        # validation data results summary
        y_pred = model.predict(X_valid.values)
        results = self.regression_stats(
            model=model,
            y_true=y_valid.values,
            y_pred=y_pred,
            feature_count=X_train.shape[1],
            data_type="validation",
        )
        regression_results_summary = regression_results_summary.append(
            results, ignore_index=True
        )
        display(regression_results_summary)

    elif isinstance(n_folds, int):
        # if validation data is not provided, then perform k_fold cross validation on
        # training data
        cv = list(
            KFold(
                n_splits=n_folds, shuffle=True, random_state=random_state
            ).split(X_train, y_train)
        )

        # generate colors
        # color_list = style.color_gen(color_map, num=len(cv))

        print("\n" + "*" * 55)
        print("Cross validation evaluation")

        # residual plot

        for i, (train_ix, valid_ix) in enumerate(cv):
            X_train_cv = X_train.iloc[train_ix]
            y_train_cv = y_train.iloc[train_ix]
            X_valid_cv = X_train.iloc[valid_ix]
            y_valid_cv = y_train.iloc[valid_ix]

            y_pred = model.fit(X_train_cv.values, y_train_cv.values).predict(
                X_valid_cv.values
            )
            residuals = y_pred - y_valid_cv.values

            p = PrettierPlot(plot_orientation="wide_narrow")
            ax = p.make_canvas(
                title="Residual plot - CV fold {}\nModel: {}\nParameter set: {}".format(
                    i + 1,
                    model.estimator_name,
                    model.model_iter,
                ),
                x_label="Predicted values",
                y_label="Residuals",
                y_shift=0.55,
                position=121,
                title_scale=title_scale,
            )

            p.scatter_2d(
                x=y_pred,
                y=residuals,
                size=7,
                color=style.style_grey,
                # color=color_list[i],
                y_units=y_units,
                x_units=x_units,
                ax=ax,
            )
            plt.hlines(
                y=0,
                xmin=np.min(y_pred),
                xmax=np.max(y_pred),
                color=style.style_grey,
                lw=2,
            )

            ## univariate plot
            ax = p.make_canvas(
                title="Residual distribution - CV fold {}\nModel: {}\nParameter set: {}".format(
                    i + 1,
                    model.estimator_name,
                    model.model_iter,
                ),
                title_scale=title_scale,
                position=122,
            )

            p.dist_plot(
                residuals,
                fit=stats.norm,
                color=style.style_grey,
                y_units="ff",
                x_units="fff",
                ax=ax,
            )
            plt.show()

            # cv fold results summary
            results = self.regression_stats(
                model=model,
                y_true=y_valid_cv,
                y_pred=y_pred,
                feature_count=X_valid_cv.shape[1],
                data_type="validation",
                fold=i + 1,
            )
            regression_results_summary = regression_results_summary.append(
                results, ignore_index=True
            )
        print("\n" + "*" * 55)
        print("Summary")

        display(regression_results_summary)
    else:
        display(regression_results_summary)
