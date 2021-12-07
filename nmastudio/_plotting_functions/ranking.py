import numpy as np, pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.cluster import KMeans
from collections import Counter

def _ranking_scatter(net_data, ranking_data,
                      outcome_direction_1=True, outcome_direction_2=True):
    ranking_data = ranking_data.copy(deep=True)
    ranking_data = ranking_data.loc[:, ~ranking_data.columns.str.contains('^Unnamed')]  # Remove unnamed columns

    # True=harmful

    if not outcome_direction_1: ranking_data.pscore1 = 1 - ranking_data.pscore1.values
    if not outcome_direction_2: ranking_data.pscore2 = 1 - ranking_data.pscore2.values
    ranking_data.sort_values(by=["pscore1", "pscore2"],
                    ascending=[False, False], inplace=True)

    kmeans = KMeans(n_clusters=int(round(len(ranking_data.treatment) / float(5.0), 0)),
                    init='k-means++', max_iter=300, n_init=10, random_state=0)
    labels = kmeans.fit(ranking_data[['pscore1', 'pscore2']])
    ranking_data['Trt groups'] = labels.labels_.astype(str)
    df_full = net_data.groupby(['treat1', 'treat2']).TE.count().reset_index()
    df_full_2 = net_data.groupby(['treat1', 'treat2']).TE2.count().reset_index()
    node_weight, node_weight_2 = {}, {}
    for treat in ranking_data.treatment:
        n1 = df_full[df_full.treat1 == treat].TE.sum()
        n2 = df_full[df_full.treat2 == treat].TE.sum()
        node_weight[treat] = (n1 + n2) / float(np.shape(ranking_data)[0])

        n1 = df_full_2[df_full_2.treat1 == treat].TE2.sum()
        n2 = df_full_2[df_full_2.treat2 == treat].TE2.sum()
        node_weight_2[treat] = (n1 + n2) / float(np.shape(ranking_data)[0])

    sum_weight = dict((Counter(node_weight) + Counter(node_weight_2)))
    mean_weight = {k: v / 2.0 for k, v in
                   sum_weight.items()}  # Node size prop to mean count of node size in outcome 1 and outcome 2
    ranking_data["node weight"] = ranking_data["treatment"].map(mean_weight)

    fig = px.scatter(ranking_data, x="pscore1", y="pscore2",
                      color="Trt groups", size='node weight',
                      hover_data=["treatment"],
                      text='treatment')

    fig.update_layout(coloraxis_showscale=True,
                       showlegend=False,
                       paper_bgcolor='white',
                       plot_bgcolor='white',
                       modebar=dict(orientation='h'),
                       xaxis=dict(showgrid=False, autorange=True, dtick=0.1,
                                  tickcolor='black', ticks="outside", tickwidth=1,
                                  showline=True, linewidth=1, linecolor='black',
                                  zeroline=False, zerolinecolor='black', zerolinewidth=1,
                                  range=[0, 1]),
                       yaxis=dict(showgrid=False, autorange=True, dtick=0.1,
                                  showline=True, linewidth=1, linecolor='black',
                                  tickcolor='black', ticks="outside", tickwidth=1,
                                  zeroline=False, zerolinecolor='black', zerolinewidth=1,
                                  range=[0, 1]
                                  ))
    fig.update_traces(textposition='top center', textfont_size=10,
                       marker=dict(line=dict(width=1, color='black'))
                       )
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.layout.margin = dict(l=30, r=30, t=10, b=80)

    return fig






def _ranking_heatmap(ranking_data, outcome_direction_1=True, outcome_direction_2=True):
    ranking_data = ranking_data.copy(deep=True)
    ranking_data = ranking_data.loc[:, ~ranking_data.columns.str.contains('^Unnamed')]  # Remove unnamed columns
    # True=harmful
    ranking_data.sort_values(by=["pscore1", "pscore2"],
                             ascending=[False, False], inplace=True)
    outcomes = ("Outcome 1", "Outcome 2")


    if "pscore2" in ranking_data.columns:
        if not outcome_direction_1: ranking_data.pscore1 = 1 - ranking_data.pscore1.values
        if not outcome_direction_2: ranking_data.pscore2 = 1 - ranking_data.pscore2.values
        ranking_data.sort_values(by=["pscore1", "pscore2"],
                        ascending=[False, False], inplace=True)
        z_text = (tuple(ranking_data.pscore1.round(2).astype(str).values),
                  tuple(ranking_data.pscore2.round(2).astype(str).values))
        pscores = (tuple(ranking_data.pscore1), tuple(ranking_data.pscore2))
    else:
        outcomes = ("Outcome",)
        pscore = 1 - ranking_data.pscore if not outcome_direction_1 else ranking_data.pscore
        pscore = pscore.sort_values(ascending=False)
        z_text = (tuple(pscore.round(2).astype(str).values),)
        pscores = (tuple(pscore),)

    treatments = tuple(ranking_data.treatment)

    #################### heatmap ####################
    if len(pscores) + len(outcomes) + len(z_text) == 3:
        pscores, outcomes, z_text = list(pscores), list(outcomes), list(z_text)

    fig = ff.create_annotated_heatmap(pscores, x=treatments, y=outcomes,
                                      reversescale=True,
                                      annotation_text=z_text, colorscale='Viridis',
                                      hoverongaps=False)
    for annotation in fig.layout.annotations: annotation.font.size = 9
    fig.update_layout(paper_bgcolor='white',  # transparent bg
                      plot_bgcolor='white',
                      modebar=dict(orientation='h'),
                      xaxis=dict(showgrid=False, autorange=True, title='',
                                 tickmode='linear', type="category"),
                      yaxis=dict(showgrid=False, autorange=True, title='', range=[0, len(outcomes)]),
                      )

    fig['layout']['xaxis']['side'] = 'bottom'
    fig['data'][0]['showscale'] = True
    fig['layout']['yaxis']['autorange'] = "reversed"
    # fig['layout']['xaxis']['autorange'] = "reversed"
    fig.layout.margin = dict(l=0, r=0, t=70, b=180)


    return fig


