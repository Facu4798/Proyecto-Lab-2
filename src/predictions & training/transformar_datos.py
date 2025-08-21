def transformar_datos(df):

    from add_step import add_step

    #import numpy
    try:
        import numpy as np
    except ImportError:
        import os
        os.system('pip install -U numpy')
        import numpy as np

    #import pipeline
    try:
        from sklearn.pipeline import Pipeline
    except ImportError:
        import os
        os.system('pip install -U scikit-learn')
        from sklearn.pipeline import Pipeline

    #import winsorizer
    try:
        from feature_engine.outliers import Winsorizer
    except ImportError:
        import os
        os.system('pip install -U feature-engine')
        from feature_engine.outliers import Winsorizer

        
    #pipeline definition
    p = Pipeline([],verbose=True)
    from add_step import add_step

    #back + linear + foward
    from transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer1', BLFImputer())

    #volatilidad relativa
    from transformers.volatilidad_rel_transformer import VolatilidadRelativaTransformer
    p = add_step(p, 'volatilidad_rel_transformer', VolatilidadRelativaTransformer())

    #volatilidad ajustada
    from transformers.volatilidad_ajs_transformer import VolatilidadAjustadaTransformer
    p = add_step(p, 'volatilidad_ajs_transformer', VolatilidadAjustadaTransformer())

    #volatilidad absoluta
    from transformers.volatilidad_abs_transformer import VolatilidadAbsolutaTransformer
    p = add_step(p, 'volatilidad_abs_transformer', VolatilidadAbsolutaTransformer())

    #pseudo garch
    from transformers.pseudo_garch_trans import pseudoGarchTransformer
    p = add_step(p, 'pseudo_garch_transformer', pseudoGarchTransformer())

    #ewma volatility
    from transformers.ewma_volatility_trans import ewmaVolatilityTransformer
    p = add_step(p, 'ewma_volatility_transformer', ewmaVolatilityTransformer())

    #volatilidad realizada
    from transformers.volatilidad_realizada_trans import volatilidadRealizadaTransformer
    p = add_step(p, 'volatilidad_realizada_transformer', volatilidadRealizadaTransformer())

    #atr
    from transformers.atr_trans import atrTransformer
    p = add_step(p, 'atr_transformer', atrTransformer(window=14))

    #back + linear + foward
    from transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer2', BLFImputer())
    
    #winsorizacion
    # from feature_engine.outliers import Winsorizer
    # winsor1 = Winsorizer(
    # capping_method='iqr',
    # tail='right',
    # fold=3,
    # variables=['Abs_Var_5d', 'RollingShock_10']
    # )

    # winsor2 = Winsorizer(
    # capping_method='iqr',
    # tail='right',
    # fold=3,
    # variables=['Abs_Var_5d', 'RollingShock_10']
    # )

    # winsor3 = Winsorizer(
    # capping_method='iqr',
    # tail='right',
    # fold=2.5,
    # variables=['EWMA_Volatility', 'RealVol_5d', 'RealVol_20d', 'ATR']
    # )
    # p = add_step(p, 'winsorizer1', winsor1)
    # p = add_step(p, 'winsorizer2', winsor2)
    # p = add_step(p, 'winsorizer3', winsor3)


    #retornos
    from transformers.retornos_trans import retornosTransformer
    p = add_step(p, 'retornos_transformer', retornosTransformer(days=[5,10]))

    #shocks pasados
    from transformers.shocks_pasados_trans import shocksPasadosTransformer
    p = add_step(p, 'shocks_pasados_transformer', shocksPasadosTransformer())

    #close relativo
    from transformers.close_rel_transformer import CloseRelativoTransformer
    p = add_step(p, 'close_rel_transformer', CloseRelativoTransformer())

    #back + linear + foward
    from transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer3', BLFImputer())

    # #winsorizacion

    # winsor4 = Winsorizer(
    # capping_method='iqr',
    # tail='both',
    # fold=1.5,
    # variables=['retorno_porcentaje', 'retorno_porcentaje_5', 'retorno_porcentaje_10', 'Close_rel_25', 'Close_rel_50', 'Close_rel_200']
    # )

    # winsor5 = Winsorizer(
    # capping_method='iqr',
    # tail='right',
    # fold=3,
    # variables=['SquaredRet_1d', 'AbsRet_1d']
    # )

    # p = add_step(p, 'winsorizer4', winsor4)
    # p = add_step(p, 'winsorizer5', winsor5)


    #volume
    from transformers.volume_transformer import VolumeTransformer
    volume1 = VolumeTransformer(window=20)
    volume2 = VolumeTransformer(window=50)
    volume3 = VolumeTransformer(window=200)
    p = add_step(p, 'volume_transformer1', volume1)
    p = add_step(p, 'volume_transformer2', volume2)
    p = add_step(p, 'volume_transformer3', volume3)


    #back + linear + foward
    from transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer4', BLFImputer())

    #winsorizacion

    # winsor6 = Winsorizer(
    # capping_method='iqr',
    # tail='both',
    # fold=1.5,
    # variables=['Volume_rel_25', 'Volume_rel_50', 'Volume_rel_200']
    # )
    # p = add_step(p, 'winsorizer6', winsor6)


    #skew relativo
    # from ..transformers.skew_rel_transformer import SkewRelativaTransformer
    # p = add_step(p, 'skew_rel_transformer', SkewRelativaTransformer())


    #kurtosis relativo
    from transformers.kurtosis_rel_transformer import KurtosisRelativaTransformer
    p = add_step(p, 'kurtosis_rel_transformer', KurtosisRelativaTransformer(window=50))




    #back + linear + foward
    from transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer5', BLFImputer())

    #winsorizacion
    # winsor7 = Winsorizer(
    # capping_method='iqr',
    # tail='both',
    # fold=2,
    # variables=['Skew_rel_50', 'Kurtosis_rel_50']
    # )
    # p = add_step(p, 'winsorizer7', winsor7)


    #bollinger widths
    from transformers.bollinger_width_trans import bollingerWidthTransformer
    p = add_step(p, 'bollinger_width_transformer', bollingerWidthTransformer(window=20, num_std=2))



    #RSI
    from transformers.rsi_transformer import RSITRansformer
    p = add_step(p, 'rsi_transformer', RSITRansformer(window=14))

    #back + linear + foward
    from transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer6', BLFImputer())

    #winsorizacion
    # winsor8 = Winsorizer(
    # capping_method='iqr',
    # tail='right',
    # fold=2.5,
    # variables=['Bollinger_Width', 'RSI']
    # )
    # p = add_step(p, 'winsorizer8', winsor8)


    #max drawdowns
    from transformers.drawdown_transformer import DrawdownTransformer
    p = add_step(p, 'drawdown_transformer', DrawdownTransformer(window=30))


    #back + linear + foward
    from transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer7', BLFImputer())

    #winsorizacion
    # winsor9 = Winsorizer(
    # capping_method='iqr',
    # tail='right',
    # fold=2.5,
    # variables=['Max_Drawdown_30d','Max_Drawdown_30d_shift5', 'Max_Drawdown_30d_shift10']
    # )
    # p = add_step(p, 'winsorizer9', winsor9)

    print("Pipeline steps loaded successfully.")
    p = p.fit(df)
    print("Pipeline fitted successfully.")
    df = p.transform(df)
    print("Data transformed successfully.")

    columns_to_drop = []
    # columns that contain np.inf
    for col in df.columns:
        if (df[col] == np.inf).any():
            columns_to_drop.append(col)

    print("Columns with np.inf values:", columns_to_drop)

    return df,columns_to_drop