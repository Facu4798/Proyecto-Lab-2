def transformar_datos(df):
    
    from Data.feature_engineering.add_step import add_step

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

    #add missing columns
    if "retorno_porcentaje" not in df.columns:
        df["retorno_porcentaje"] = (df["Close"]-df["Open"])/df["Open"]
    if "retorno" not in df.columns:
        df["retorno"] = df["Close"]-df["Open"]

    #pipeline definition
    p = Pipeline([],verbose=False)

    #back + linear + foward
    from Data.feature_engineering.transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer1', BLFImputer())

    #volatilidad relativa
    from Data.feature_engineering.transformers.volatilidad_rel_transformer import VolatilidadRelativaTransformer
    p = add_step(p, 'volatilidad_rel_transformer', VolatilidadRelativaTransformer())

    #volatilidad ajustada
    from Data.feature_engineering.transformers.volatilidad_ajs_transformer import VolatilidadAjustadaTransformer
    p = add_step(p, 'volatilidad_ajs_transformer', VolatilidadAjustadaTransformer())

    #volatilidad absoluta
    from Data.feature_engineering.transformers.volatilidad_abs_transformer import VolatilidadAbsolutaTransformer
    p = add_step(p, 'volatilidad_abs_transformer', VolatilidadAbsolutaTransformer())

    #pseudo garch
    from Data.feature_engineering.transformers.pseudo_garch_trans import pseudoGarchTransformer
    p = add_step(p, 'pseudo_garch_transformer', pseudoGarchTransformer())

    #ewma volatility
    from Data.feature_engineering.transformers.ewma_volatility_trans import ewmaVolatilityTransformer
    p = add_step(p, 'ewma_volatility_transformer', ewmaVolatilityTransformer())

    #volatilidad realizada
    from Data.feature_engineering.transformers.volatilidad_realizada_trans import volatilidadRealizadaTransformer
    p = add_step(p, 'volatilidad_realizada_transformer', volatilidadRealizadaTransformer())

    #atr
    from Data.feature_engineering.transformers.atr_trans import atrTransformer
    p = add_step(p, 'atr_transformer', atrTransformer(window=14))

    #back + linear + foward
    from Data.feature_engineering.transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer2', BLFImputer())
    
    #retornos
    from Data.feature_engineering.transformers.retornos_trans import retornosTransformer
    p = add_step(p, 'retornos_transformer', retornosTransformer(days=[5,10]))

    #shocks pasados
    from Data.feature_engineering.transformers.shocks_pasados_trans import shocksPasadosTransformer
    p = add_step(p, 'shocks_pasados_transformer', shocksPasadosTransformer())

    #close relativo
    from Data.feature_engineering.transformers.close_rel_transformer import CloseRelativoTransformer
    p = add_step(p, 'close_rel_transformer', CloseRelativoTransformer())

    #back + linear + foward
    from Data.feature_engineering.transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer3', BLFImputer())

    #volume
    from Data.feature_engineering.transformers.volume_transformer import VolumeTransformer
    volume1 = VolumeTransformer(window=20)
    volume2 = VolumeTransformer(window=50)
    volume3 = VolumeTransformer(window=200)
    p = add_step(p, 'volume_transformer1', volume1)
    p = add_step(p, 'volume_transformer2', volume2)
    p = add_step(p, 'volume_transformer3', volume3)


    #back + linear + foward
    from Data.feature_engineering.transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer4', BLFImputer())

    #kurtosis relativo
    from Data.feature_engineering.transformers.kurtosis_rel_transformer import KurtosisRelativaTransformer
    p = add_step(p, 'kurtosis_rel_transformer', KurtosisRelativaTransformer(window=50))




    #back + linear + foward
    from Data.feature_engineering.transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer5', BLFImputer())

    #bollinger widths
    from Data.feature_engineering.transformers.bollinger_width_trans import bollingerWidthTransformer
    p = add_step(p, 'bollinger_width_transformer', bollingerWidthTransformer(window=20, num_std=2))



    #RSI
    from Data.feature_engineering.transformers.rsi_transformer import RSITRansformer
    p = add_step(p, 'rsi_transformer', RSITRansformer(window=14))

    #back + linear + foward
    from Data.feature_engineering.transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer6', BLFImputer())

    #max drawdowns
    from Data.feature_engineering.transformers.drawdown_transformer import DrawdownTransformer
    p = add_step(p, 'drawdown_transformer', DrawdownTransformer(window=30))

    #back + linear + foward
    from Data.feature_engineering.transformers.back_linear_foward_transformer import BLFImputer
    p = add_step(p, 'blf_imputer7', BLFImputer())

    print("Pipeline steps loaded successfully.")
    p.fit(df,y=None)
    print("Pipeline fitted successfully.")
    df = p.transform(df)
    print("Data transformed successfully.")

    columns_to_drop = []
    # columns that contain np.inf
    for col in df.columns:
        if (df[col] == np.inf).any():
            columns_to_drop.append(col)

    return df,columns_to_drop