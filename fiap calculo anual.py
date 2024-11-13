def calcular_gs_minima_para_materia(nota_1s, nota_cp_2s, meta_anual):
    contrib_primeiro_semestre = nota_1s * 0.4
    nota_necessaria_segundo_semestre = (meta_anual - contrib_primeiro_semestre) / 0.6
    contrib_cp = nota_cp_2s * 0.4
    nota_necessaria_gs = (nota_necessaria_segundo_semestre - contrib_cp) / 0.6
    
    return round(nota_necessaria_gs, 2)

nota_1s = float(input("Digite a nota do primeiro semestre: \n"))
nota_cp_2s = float(input("Digite a nota TOTAL do CP do segundo semestre: \n"))
meta_anual = float(input("Digite a média anual desejada: \n"))

nota_necessaria_gs = calcular_gs_minima_para_materia(nota_1s, nota_cp_2s, meta_anual)
print(f"Para alcançar uma média anual de {meta_anual}, você precisa de uma nota mínima de {nota_necessaria_gs} na GS do segundo semestre.")
