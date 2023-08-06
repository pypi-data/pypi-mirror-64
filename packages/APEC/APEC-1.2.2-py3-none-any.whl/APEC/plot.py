import numpy,pandas,copy,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn
#
global colors
global colors
colors = numpy.array(['pink', 'red', '#377EB8', '#00A020', 'skyblue', 'lightgreen', 'gold',
                      '#FF7F00', '#000066', '#FF3399', '#A65628', '#984EA3', '#999999',
                      '#E41A1C', '#DEDE00', 'b', 'g', 'c', 'm', 'y', 'k', '#808000',
                      '#ADFF2F', '#7CFC00', '#32CD32', '#80FF80', '#00FF7F', '#3CB371',
                      '#007030', '#006400', '#9ACD32', '#6B8E23', '#556B2F', '#66CDAA',
                      '#8FBC8F', '#008080', '#DEB887', '#BC8F8F', '#F4A460', '#B8860B',
                      '#CD853F', '#D2691E', '#8B4513', '#A52A2A', '#778899', '#2F4F4F',
                      '#FFA500', '#FF4500', '#DA70D6', '#FF00FF', '#BA55D3', '#9400D3',
                      '#8B008B', '#9370DB', '#663399', '#4B0082', '#FF69B4', '#FF1493',
                      '#DB7093', '#C71585', '#DDA0DD', '#FF6347', '#BDB76B', '#AA45FF',
                      '#EE82EE', '#FFDAB9', '#8A2BE2', '#7B68EE', '#483D8B', '#3333FF',
                      '#4BAA82', '#FFA07A', '#FA8072', '#CD5C5C', '#B22222', '#8B0000',
                      '#FF7F50', '#7FFF00', '#32CDFF', '#98FB98', '#00FA9A', '#2E8B57',
                      '#228B22', '#00FFFF', '#AFEEEE', '#7FFFD4', '#40E0D0', '#00CED1',
                      '#5F9EA0', '#4682B4', '#ADD8E6', '#87CEFA', '#6495ED', '#00BFFF',
                      '#1E90FF', '#4169E1', '#00008B', '#191970', '#D2B48C', '#DAA520'])
#
def weighted_tsne(matrix, clusters, rs, wt, perplexity, learnRate):
    cell_types = list(set(clusters['cluster']))
    adjusted = copy.deepcopy(matrix)
    for ctype in cell_types:
        cluster_cells = numpy.where(clusters['cluster']==ctype)[0]
        weight = adjusted[cluster_cells, :].mean(axis=0) * float(wt)
        adjusted[cluster_cells, :] = numpy.array([x+weight for x in adjusted[cluster_cells, :]])
#    if matrix.shape[0]<=10000:
#        from sklearn.manifold import TSNE
#        tsne_result = TSNE(n_components=2, random_state=rs).fit_transform(adjusted)
#    else:
    from MulticoreTSNE import MulticoreTSNE as McTSNE
    tsne_result = McTSNE(n_components=2, random_state=rs, perplexity=perplexity, learning_rate=learnRate).fit_transform(adjusted)
    return tsne_result
#
#
def define_files(project, matrix_type, cell_label):
    if matrix_type=='APEC':
        reads_file = project+'/matrix/normalized_Accesson_reads.csv'
#        reads_file = project+'/matrix/Accesson_reads.csv'
    elif matrix_type=='chromVAR':
        reads_file = project+'/result/deviation_chromVAR.csv'
    else:
        print("Error: wrong <matrix_type>, should be 'APEC' or 'chromVAR' !")
        sys.exit()
    cluster_file = project+'/result/cluster_by_'+matrix_type+'.csv'
    cells_file = project+'/matrix/filtered_cells.csv'
    return reads_file, cells_file, cluster_file
#
#
def plot_tsne(project,
              matrix_type='APEC',   # ='APEC' or 'chromVAR'
              rs=0,    # random_state for tSNE
              wt=0.2,     # Weight coefficient
              corr='no',
              perplexity=30,
              learnRate=200
              ):
    """
    project:        Path to the project folder.
    matrix_type:    Type of input matrix, can be 'APEC' or 'chromVAR', default='APEC'.
                    If matrix_type='APEC', it will use accesson matrix yielded by clustering.cluster_byAccesson();
                    if matrix_type='chromVAR', it will use deviation matrix yielded by clustering.cluster_byMotif().
    rs:             Random state seed for TSNE analysis, default=0.
    wt:             Weight coefficient for TSNE analysis, default=0.2.
    """
    cell_label = 'notes'
    reads_file, cells_file, cluster_file = define_files(project, matrix_type, cell_label)
    reads_df = pandas.read_csv(reads_file, sep=',', index_col=0,
                               engine='c', na_filter=False, low_memory=False)
    if matrix_type=='chromVAR': reads_df = reads_df.T
    cells_df = pandas.read_csv(cells_file, sep='\t', index_col=0)
    cluster_df = pandas.read_csv(cluster_file, sep='\t', index_col=0)
    reads_df, cluster_df = reads_df.loc[cells_df.index.values], cluster_df.loc[cells_df.index.values]
    if corr=='no':
        tsne_result = weighted_tsne(reads_df.values, cluster_df, rs, wt, perplexity, learnRate)
    else:
        tsne_result = weighted_tsne(reads_df.T.corr().values, cluster_df, rs, wt, perplexity, learnRate)
    tsne_df = pandas.DataFrame(tsne_result, index=cells_df.index, columns=['TSNE1', 'TSNE2'])
    out_tsne = project+'/result/TSNE_by_'+matrix_type+'.csv'
    tsne_df.to_csv(out_tsne, sep='\t')
#
    cTypes = list(set(cells_df[cell_label]))
    cTypes.sort()
    fig1, axes = plt.subplots(1, figsize=(15,15))
    for ict,ct in enumerate(cTypes):
        index = numpy.where(cells_df[cell_label]==ct)[0]
        axes.scatter(tsne_result[index, 0], tsne_result[index, 1], c=colors[ict], label=ct, s=50)
    axes.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    outfig1 = project+'/figure/TSNE_by_'+matrix_type+'_with_'+cell_label+'_label.pdf'
    fig1.savefig(outfig1, bbox_inches='tight')
    plt.close()
#
    cTypes = list(set(cluster_df['cluster']))
    cTypes.sort()
    fig2, axes = plt.subplots(1, figsize=(15,15))
    for ict,ct in enumerate(cTypes):
        index = numpy.where(cluster_df['cluster']==ct)[0]
        axes.scatter(tsne_result[index, 0], tsne_result[index, 1], c=colors[ict], label=ct, s=50)
    axes.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    outfig2 = project+'/figure/TSNE_by_'+matrix_type+'_with_cluster_label.pdf'
    fig2.savefig(outfig2, bbox_inches='tight')
    plt.close()
    print('plot_tsne output files:')
    print(out_tsne)
    print(outfig1)
    print(outfig2)
    return
#
#
def plot_umap(project,
              matrix_type='APEC',   # ='APEC' or 'chromVAR'
              rs=0    # random_state for UMAP
              ):
    """
    project:        Path to the project folder.
    matrix_type:    Type of input matrix, can be 'APEC' or 'chromVAR', default='APEC'.
                    If matrix_type='APEC', it will use accesson matrix yielded by clustering.cluster_byAccesson();
                    if matrix_type='chromVAR', it will use deviation matrix yielded by clustering.cluster_byMotif().
    rs:             Random state seed for UMAP analysis, default=0.
    """
    cell_label = 'notes'
    import umap
    reads_file, cells_file, cluster_file = define_files(project, matrix_type, cell_label)
    reads_df = pandas.read_csv(reads_file, sep=',', index_col=0,
                             engine='c', na_filter=False, low_memory=False)
    cells_df = pandas.read_csv(cells_file, sep='\t', index_col=0)
    cluster_df = pandas.read_csv(cluster_file, sep='\t', index_col=0)
    if matrix_type=='chromVAR': reads_df = reads_df.T
    reads_df = reads_df.loc[cells_df.index.values]
    umap_result = umap.UMAP(n_components=2, random_state=rs).fit_transform(reads_df.values)
    umap_df = pandas.DataFrame(umap_result, index=cells_df.index, columns=['UMAP1', 'UMAP2'])
    out_umap = project+'/result/UMAP_by_'+matrix_type+'.csv'
    umap_df.to_csv(out_umap, sep='\t')
#
    cTypes = list(set(cells_df[cell_label]))
    cTypes.sort()
    fig1, axes = plt.subplots(1, figsize=(15,15))
    for ict,ct in enumerate(cTypes):
        index = numpy.where(cells_df[cell_label]==ct)[0]
        axes.scatter(umap_result[index, 0], umap_result[index, 1], c=colors[ict], label=ct, s=50)
    axes.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    outfig1 = project+'/figure/UMAP_by_'+matrix_type+'_with_'+cell_label+'_label.pdf'
    fig1.savefig(outfig1, bbox_inches='tight')
    plt.close()
#
    cTypes = list(set(cluster_df['cluster']))
    cTypes.sort()
    fig2, axes = plt.subplots(1, figsize=(15,15))
    for ict,ct in enumerate(cTypes):
        index = numpy.where(cluster_df['cluster']==ct)[0]
        axes.scatter(umap_result[index, 0], umap_result[index, 1], c=colors[ict], label=ct, s=50)
    axes.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    outfig2 = project+'/figure/UMAP_by_'+matrix_type+'_with_cluster_label.pdf'
    fig2.savefig(outfig2, bbox_inches='tight')
    plt.close()
    print('plot_umap output files:')
    print(out_umap)
    print(outfig1)
    print(outfig2)
    return
#
#
def correlation(project,
                matrix_type='APEC',   # ='APEC' or 'chromVAR'
                cell_label='notes',   # ='notes' or 'cluster'
                method='ward',
                metric='euclidean',
                clip=[-1,1],   # =[min,max]
                connect='no'
                ):
    """
    project:        Path to the project folder.
    matrix_type:    Type of input matrix, can be 'APEC' or 'chromVAR', default='APEC'.
                    If matrix_type='APEC', it will use accesson matrix yielded by clustering.cluster_byAccesson();
                    if matrix_type='chromVAR', it will use deviation matrix yielded by clustering.cluster_byMotif().
    cell_label:     Color labels for cells, can be 'notes' or 'cluster', default='notes'.
                    If cell_label='cluster', it will use clustering result of clustering.cluster_byAccesson().
    method:         The "method" parameter for scipy funcion pdist, can be 'ward', 'average', 'single', default='ward'.
    metric:         The "metric" parameter for scipy funcion pdist, default='euclidean', see scipy website for more details.
    clip:           Clip range for the heatmap colorbar, can be [min, max], default=[-1, 1].
    connect:        Whether to use the connectivity matrix to build cell-cell correlation, default='no'.
    """
    import seaborn
    reads_file, cells_file, cluster_file = define_files(project, matrix_type, cell_label)
    reads_df = pandas.read_csv(reads_file, sep=',', index_col=0,
                               engine='c', na_filter=False, low_memory=False)
    if cell_label=='notes':
        cells_file = project+'/matrix/filtered_cells.csv'
    else:
        cells_file = project+'/result/cluster_by_'+matrix_type+'.csv'
    cells_df = pandas.read_csv(cells_file, sep='\t', index_col=0)
    if matrix_type=='chromVAR':
        reads_df = reads_df.T
    elif matrix_type!='APEC':
        print("Error: wrong input parameter for <matrix_type> !")
        sys.exit()
    reads_df = reads_df.loc[cells_df.index.values]
#
    cTypes = list(set(cells_df[cell_label]))
    cTypes.sort()
    lut = dict(zip(cTypes, colors[:len(cTypes)]))
    row_colors = cells_df[cell_label].map(lut)
    cmap = seaborn.diverging_palette(h_neg=210, h_pos=350, s=90, l=30, as_cmap=True)
    seaborn.set(font_scale=1.2)
    if connect=='yes':
        from sklearn.neighbors import kneighbors_graph
        connect = kneighbors_graph(reads_df.values, n_neighbors=20, include_self=False)
        connectivity = 0.5*(connect + connect.T)
        corr = numpy.corrcoef(connectivity.A)
    else:
        corr = numpy.corrcoef(reads_df.values)
    corr_df = pandas.DataFrame(corr, index=reads_df.index, columns=reads_df.index)
    fig0 = seaborn.clustermap(corr_df, method=method, metric=metric, cmap=cmap,
                              row_colors=row_colors, figsize=(20,20), vmin=clip[0], vmax=clip[1])
    plt.setp(fig0.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
    plt.setp(fig0.ax_heatmap.xaxis.get_majorticklabels(), rotation=90)
    outfig = project+'/figure/cell_cell_correlation_by_'+matrix_type+'_with_'+cell_label+'_label.png'
    fig0.savefig(outfig, bbox_inches='tight')
    plt.close()
    print('correlation output files:')
    print(outfig)
    return
#
#
def plot_trajectory(project,
                    cell_label='notes',   # ='notes', 'cluster', 'State'
                    angles=[30,30]    # =[alpha, beta]
                    ):
    """
    project:        Path to the project folder.
    cell_label:     Color labels for cells, can be 'notes' or 'cluster', default='notes'.
    angles:         Rotation angles for 3D trajectory, e.g. [100,20], default=[30,30].
    """
    if cell_label=='notes':
        cells_file = project+'/matrix/filtered_cells.csv'
        cells_df = pandas.read_csv(cells_file, sep='\t', index_col=0)
    elif cell_label=='cluster':
        cells_file = project+'/result/cluster_by_APEC.csv'
        cells_df = pandas.read_csv(cells_file, sep='\t', index_col=0)
    elif cell_label=='State':
        cells_file = project+'/result/monocle_trajectory.csv'
        cells_df = pandas.read_csv(cells_file, sep=',', index_col=0)
    else:
        print("Error: wrong <cell_label>, should be 'notes' or 'cluster' !")
        sys.exit()
    reduced_df = pandas.read_csv(project+'/result/monocle_reduced_dimension.csv', sep=',', index_col=0)
    fig = plt.figure(1, figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    cell_types = list(set(list(cells_df[cell_label].values)))
    cell_types.sort()
    for itype,ctype in enumerate(cell_types):
        cells = cells_df.loc[cells_df[cell_label]==ctype].index.values
        ax.scatter(reduced_df.loc[1,cells], reduced_df.loc[2,cells], reduced_df.loc[3,cells],
                   c=colors[itype], edgecolors='none', s=20, label=cell_types[itype])
    ax.view_init(angles[0], angles[1])
    ax.set_xlim(reduced_df.iloc[0].min()-0.02, reduced_df.iloc[0].max()+0.02)
    ax.set_ylim(reduced_df.iloc[1].min()-0.02, reduced_df.iloc[1].max()+0.02)
    ax.set_zlim(reduced_df.iloc[2].min()-0.02, reduced_df.iloc[2].max()+0.02)
    ax.legend(fontsize=20, bbox_to_anchor=(1.0, 1.0))
    outfig = project+'/figure/pseudotime_trajectory_with_'+cell_label+'_label.pdf'
    fig.savefig(outfig, bbox_inches='tight')
    plt.close()
    print('plot_trajectory output files:')
    print(outfig)
    return
#
#
def plot_feature(project,
                 space='tsne',   # ='tsne' or 'umap' or 'trajectory'
                 feature='accesson',   # ='accesson' or 'motif' or 'gene'
                 matrix_type='APEC',   # ='APEC' or 'chromVAR'
                 name='1',    # = name of accesson/motif/gene
                 clip='none',    # = None or [min,max]
                 angles=[30,30],    # = [alpha, beta]
                 ):
    """
    project:        Path to the project folder.
    space:          In which space we draw the feature, can be 'tsne' or 'umap' or 'trajectory', default='tsne'.
                    If space='tsne', run plot.plot_tsne() first;
                    if space='umap', run plot.plot_umap() first;
                    if space='trajectory', run generate.monocle_trajectory() first.
    feature:        Type of the feature, can be 'accesson' or 'motif' or 'gene', default='accesson'.
                    If feature='accesson', run clustering.cluster_byAccesson() first;
                    if feature='motif', run clustering.cluster_byMotif() first;
                    if feature='gene', run generate.gene_expression() first.
    matrix_type:    Type of input matrix for tSNE/UMAP, can be 'APEC' or 'chromVAR', default='APEC'.
                    If matrix_type='APEC', it will use tSNE/UMAP result of APEC;
                    if matrix_type='chromVAR', it will use tSNE/UMAP result of chromVAR.
    name:           Name of the feature.
                    If feature='accesson', name=accesson number, i.e. '1';
                    if feature='motif', name=motif symbol, i.e. 'GATA1';
                    if feature='gene', name=gene symbol, i.e. 'CD36'.
    clip:           Clip range for the input matrix, can be [min, max] or 'none', default='none'.
    angles:         Rotation angles for 3D trajectory, e.g. [100,20], default=[30,30].
    """
    if space=='trajectory':
        space_df = pandas.read_csv(project+'/result/monocle_reduced_dimension.csv', sep=',', index_col=0).T
    else:
        space_df = pandas.read_csv(project+'/result/'+space.upper()+'_by_'+matrix_type+'.csv', sep='\t', index_col=0)
    matrix, cells = space_df.values, space_df.index.values
    if feature=='motif':
        reads_df = pandas.read_csv(project+'/result/deviation_chromVAR.csv', sep=',', index_col=0,
                                   engine='c', na_filter=False, low_memory=False).T
        motifs = []
        for tf in reads_df.columns.values:
            names = tf.split('-')[:-1]
            if name in names: motifs.append(tf)
        print(motifs)
        if len(motifs)==0:
            print("No corresponding motif "+name+"!")
            sys.exit()
        else:
            reads = reads_df.loc[cells, motifs].values.sum(axis=1)
    elif feature=='gene':
        reads_df = pandas.read_csv(project+'/matrix/genes_scored_by_TSS_peaks.csv', sep=',', index_col=0,
                                   engine='c', na_filter=False, low_memory=False)
        gene = list(set([name]).intersection(set(reads_df.columns.values)))
        if len(gene)==0:
            print("No corresponding gene "+name+"!")
            sys.exit()
        else:
            reads = reads_df.loc[cells, gene].values.sum(axis=1)
    elif feature=='accesson':
        reads_df = pandas.read_csv(project+'/matrix/Accesson_reads.csv', sep=',', index_col=0,
                   engine='c', na_filter=False, low_memory=False)
        normal = numpy.array([x/x.sum()*10000 for x in reads_df.values])
        reads_df = pandas.DataFrame(normal, index=reads_df.index, columns=reads_df.columns)
        reads = reads_df.loc[cells, name].values
#    print(reads.shape)
    order = numpy.argsort(reads)
    if clip!='none':
        reads = numpy.clip(reads, clip[0], clip[1])
#
    if space=='trajectory':
        clist = ['blue', 'silver', 'red']
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list('mylist', clist, N=256)
        fig1 = plt.figure(1, figsize=(12,10))
        ax = fig1.add_subplot(111, projection='3d')
        im = ax.scatter(matrix[order,0], matrix[order,1], matrix[order,2], cmap=cmap, c=reads[order], edgecolors='none', s=10)
        ax.view_init(angles[0], angles[1])
        cbar = plt.colorbar(im, shrink=0.15, ticks=[reads.min(), reads.max()], aspect=8)
        cbar.ax.set_yticklabels([round(reads.min(),2), round(reads.max(),2)])
        width = matrix[:,0].max()-matrix[:,0].min()
        height = matrix[:,1].max()-matrix[:,1].min()
        rad = matrix[:,2].max()-matrix[:,2].min()
        ax.set_xlim((matrix[:,0].min()-0.01*width, matrix[:,0].max()+0.01*width))
        ax.set_ylim((matrix[:,1].min()-0.01*height, matrix[:,1].max()+0.01*height))
        ax.set_zlim((matrix[:,2].min()-0.01*rad, matrix[:,2].max()+0.01*rad))
        ax.set_zticks([])
    else:
        clist = ['steelblue', 'cornsilk', 'red']
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list('mylist', clist, N=256)
        fig1 = plt.figure(1, figsize=(6,5))
        ax = fig1.add_subplot(111)
        im = ax.scatter(matrix[order,0], matrix[order,1],  cmap=cmap, c=reads[order], edgecolors='none', s=10)
        cbar = plt.colorbar(im, shrink=0.15, ticks=[reads.min(), reads.max()], aspect=8)
        cbar.ax.set_yticklabels([round(reads.min(),2), round(reads.max(),2)])
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(feature+'    '+name)
    outfig = project+'/figure/'+feature+'_'+name+'_on_'+space+'_by_'+matrix_type+'.pdf'
    fig1.savefig(outfig, bbox_inches='tight')
    plt.close()
    print('plot_feature output files:')
    print(outfig)
    return
#
#
#
