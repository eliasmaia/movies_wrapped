def formatar_duracao(minutos):
    try:
        minutos = int(minutos)
        h = minutos // 60
        m = minutos % 60
        return f"{h}h {m:02d}min" if h > 0 else f"{m}min"
    except:
        return "N/A"