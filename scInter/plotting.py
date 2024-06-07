import altair as alt
import scanpy as sc
import pandas as pd
import re

alt.data_transformers.enable("vegafusion")
    
def single_plot(adata,coordinates,meta):
    
    df = pd.DataFrame(coordinates, index=adata.obs_names, columns=[f"{meta['embedding_type']}_1",f"{meta['embedding_type']}_2"])

    df = df.join(adata.obs[meta['color1']])


    selector = alt.selection_point(fields=[meta['color1']])
    opacity_cond = alt.condition(selector, alt.value(0.8), alt.value(0.2))
    colors = alt.condition(selector, meta['color1'], alt.value('lightgrey'))

    plot = alt.Chart(df).mark_circle(size=30).encode(
        x=alt.X(f"{meta['embedding_type']}_1", axis=alt.Axis(title=f"{meta['embedding_type']}_1", titleFontSize=20, labelFontSize=15)),
        y=alt.Y(f"{meta['embedding_type']}_2", axis=alt.Axis(title=f"{meta['embedding_type']}_2", titleFontSize=20, labelFontSize=15)),
        color=colors,
        opacity = opacity_cond,
        tooltip=[meta['color1']]
    ).properties(
        title=alt.TitleParams(f"colored by {meta['color1']}", fontSize=25),
        width=600,
        height=400
    ).add_params(selector
    ).interactive()


    return plot

def comparison_plot(adata, coordinates,meta:dict):
    df = pd.DataFrame(coordinates, index=adata.obs_names, columns=[f"{meta['embedding_type']}_1",f"{meta['embedding_type']}_2"])

    df = df.join(adata.obs[meta['color1']])
    df = df.join(adata.obs[meta['color2']])

    selector = alt.selection_point(fields=[meta['color1']])
    selector2 = alt.selection_point(fields=[meta['color2']])
    opacity_cond = alt.condition(selector, alt.value(0.8), alt.value(0.2))
    opacity_cond2 = alt.condition(selector2, alt.value(0.8), alt.value(0.2))
    colors1 = alt.condition(selector2, meta['color1'], alt.value('lightgrey'))
    colors2 = alt.condition(selector, meta['color2'], alt.value('lightgrey'))

    plot1 = alt.Chart(df).mark_circle(size=30).encode(
        x=alt.X(f"{meta['embedding_type']}_1", axis=alt.Axis(title=f"{meta['embedding_type']}_1", titleFontSize=20, labelFontSize=15)),
        y=alt.Y(f"{meta['embedding_type']}_2", axis=alt.Axis(title=f"{meta['embedding_type']}_2", titleFontSize=20, labelFontSize=15)),
        color=colors2,
        opacity = opacity_cond,
        tooltip=[meta['color1'],meta['color2']]
    ).properties(
        title=alt.TitleParams(f"colored by {meta['color2']}", fontSize=25),
        width=600,
        height=400
    ).add_params(selector2
    ).interactive()

    plot2 = alt.Chart(df).mark_circle(size=30).encode(
        x=alt.X(f"{meta['embedding_type']}_1", axis=alt.Axis(title=f"{meta['embedding_type']}_1", titleFontSize=20, labelFontSize=15)),
        y=alt.Y(f"{meta['embedding_type']}_2", axis=alt.Axis(title=f"{meta['embedding_type']}_2", titleFontSize=20, labelFontSize=15)),
        color=colors1,
        opacity = opacity_cond2,
        tooltip=[meta['color1'],meta['color2']]
    ).properties(
        title=alt.TitleParams(f"colored by {meta['color1']}", fontSize=25),
        width=600,
        height=400
    ).add_params(selector
    ).interactive()

    return plot1|plot2


def int_plot(adata, string):
    # get coordinates
    pattern = r'sc\.pl\.(\w+)\((\w+), color=\[(["\'])(\w+)\3(?:,["\'](\w+)\3)?\]\)'

    match = re.match(pattern, string)
    meta = {}
    if match:
        meta['embedding_type'] = match.group(1)
        meta['color1'] = match.group(4)
        meta['color2'] = match.group(5) if match.group(5) else None

    else:
        print("No match found")
        return

    try:
        if meta['embedding_type'] == 'umap':
            coordinates = adata.obsm['X_umap']
        elif meta['embedding_type'] == 'pca':
            coordinates = adata.obsm['X_pca'][:, 0:2]
        elif meta['embedding_type'] == 'draw_graph':
            coordinates = adata.obsm['X_draw_graph_fa']
        else:
            raise ValueError("Invalid embedding type. Choose either 'umap', 'pca', or 'traj'.")
    except KeyError:
        if meta['embedding_type'] == 'traj':
            raise ValueError("Invalid embedding type. Run draw_graph before plotting trajectory.")
        else:
            raise ValueError(f"The specified embedding '{embedding}' does not exist in adata.obsm.")
            
    # two colors:
    if meta['color2'] != None:
        plot = comparison_plot(adata, coordinates, meta)
    else:
        plot = single_plot(adata, coordinates, meta)
    return plot
        
    
