def transform(df):
    df = df.dropna()
    df['faturamento'] = df['quantidade'] * df['preco']
    return df