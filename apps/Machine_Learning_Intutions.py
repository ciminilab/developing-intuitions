import marimo

__generated_with = "0.14.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import sklearn
    import numpy
    import pandas
    import drawdata
    import matplotlib.pyplot as plt
    return drawdata, mo, numpy, pandas, plt, sklearn


@app.cell
def _():
    # create 4 groups - 1A, 1B, 2A, 2B
    # vary them on size, shape/footprint (https://scikit-image.org/docs/stable/auto_examples/numpy_operations/plot_structuring_elements.html), color (https://scikit-image.org/docs/stable/auto_examples/color_exposure/plot_tinting_grayscale_images.html); have "wiggle" factor, count
    # Display up to 20 random, hiding black background
    # Run sklearn random forest (https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier), report accuracy, top discriminating features (https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html#sphx-glr-auto-examples-ensemble-plot-forest-importances-py)
    return


@app.cell
def _(mo):
    mo.md("""# Developing Classical Machine Learning Intuitions""")
    return


@app.cell
def _(drawdata, mo):
    widget = mo.ui.anywidget(drawdata.ScatterWidget(height=300))
    widget
    return (widget,)


@app.cell
def _(mo):
    a_group = mo.ui.radio(options=["1","2"],value="1",label="What classification group should the blue points from 'a' be assigned to?")
    b_group = mo.ui.radio(options=["1","2"],value="1",label="What classification group should the orange points from 'b' be assigned to?")
    c_group = mo.ui.radio(options=["1","2"],value="2",label="What classification group should the green points from 'c' be assigned to?")
    d_group = mo.ui.radio(options=["1","2"],value="2",label="What classification group should the red points from 'd' be assigned to?")
    mo.vstack([mo.hstack([a_group,b_group]),mo.hstack([c_group,d_group])])
    return a_group, b_group, c_group, d_group


@app.cell
def _(
    a_group,
    b_group,
    c_group,
    d_group,
    mo,
    numpy,
    pandas,
    plt,
    sklearn,
    widget,
):
    class_dict = {'a':int(a_group.value),'b':int(b_group.value),'c':int(c_group.value),'d':int(d_group.value)}
    list_of_features = ["x","y"]
    output = ""
    fig = mo.md("")
    if widget.value["data"]:
        widget_data = numpy.array(widget.data_as_pandas[list_of_features+["label"]])
        label = numpy.array(widget.data_as_pandas["label"].map(lambda x: class_dict[x])).T
        X_train_with_label, X_test_with_label, y_train, y_test = sklearn.model_selection.train_test_split(widget_data, label, stratify=label, random_state=42,test_size=0.5)
        test_wtih_all_labels = pandas.DataFrame(X_test_with_label,columns=["x","y","label"])
        test_wtih_all_labels["numeric_label"] =y_test
        X_train = X_train_with_label[:,:-1]
        X_test = X_test_with_label[:,:-1]
        forest = sklearn.ensemble.RandomForestClassifier(random_state=0)
        forest.fit(X_train, y_train)
        importances=forest.feature_importances_
        indices = numpy.argsort(importances)[::-1]
        output = f"### The accuracy of separating class 1 from class 2 is {(100*forest.score(X_test,y_test)):.2f}%.\n ### The most important features are "+", ".join([f"{list_of_features[indices[f]]}({(100*importances[indices[f]]):.2f}%)" for f in range(len(list_of_features))])
        true_test_classes = test_wtih_all_labels["label"].unique()
        true_test_classes.sort()
        for true_class in true_test_classes:
            to_test = test_wtih_all_labels.query(f'label=="{true_class}"')
            to_test_labels = numpy.array(to_test["numeric_label"]).T
            to_test_data = numpy.array(to_test[list_of_features])
            output += f"\n ### The per-class accuracy for class {true_class} is {(100*forest.score(to_test_data,to_test_labels)):.2f}%."
        fig, axs = plt.subplots(3,3,figsize=(10, 10), layout='constrained')
        for ax, i in zip(axs.flat,range(9)):
            tree = forest.estimators_[i]
            sklearn.tree.plot_tree(tree,feature_names=list_of_features, class_names=["1","2"],ax=ax,rounded=True)
    mo.md(output)
    return fig, forest, list_of_features


@app.cell
def _(mo):
    mo.md("""----- \n ## What do some of those decision trees actually look like? Let's check out the top 9""")
    return


@app.cell
def _(fig):
    fig
    return


@app.cell
def _(mo):
    tree_to_look = mo.ui.number(label="Look up tree number:", start=0,stop=99,step=1)
    mo.vstack([mo.md("## Call up any individual tree you want"),tree_to_look])
    return (tree_to_look,)


@app.cell
def _(forest, list_of_features, plt, sklearn, tree_to_look):
    fig2,ax2 = plt.subplots(1,1,figsize=(10, 10), layout='constrained')
    sklearn.tree.plot_tree(forest.estimators_[tree_to_look.value],feature_names=list_of_features, class_names=["1","2"],rounded=True,ax=ax2)

    return


@app.cell
def _():
    #color_variability = mo.ui.slider(start=0, stop=128, step=2, value=2)


    return


@app.cell
def _():
    #mo.hstack([color_variability, mo.md(f"Has value: {color_variability.value}")],justify="start")
    return


@app.cell
def _():
    #shape_variability = mo.ui.range_slider(start=0, stop=3, step=0.1, value=[1,2])
    #shape_variability
    return


if __name__ == "__main__":
    app.run()
