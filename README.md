# Cálculo de Nota Mínima na GS do Segundo Semestre

Este programa calcula a nota mínima necessária na GS do segundo semestre para atingir uma média anual desejada, considerando as notas do primeiro semestre e do CP do segundo semestre. 

## Estrutura do Cálculo

A média anual é composta das notas do primeiro e segundo semestres, com pesos diferentes:

- **Primeiro semestre**: conta com 40% da nota anual.
- **Segundo semestre**: conta com 60% da nota anual.
  
Dentro de cada semestre:
- **CP** vale 40% da nota do semestre.
- **GS** vale 60% da nota do semestre.

## Exemplo de Uso

Se você tem uma nota do primeiro semestre e uma nota do CP do segundo semestre e deseja alcançar uma média anual específica, o programa calculará a nota mínima necessária na GS do segundo semestre para que a média anual desejada seja atingida.

### Fórmula do Cálculo

1. A contribuição do primeiro semestre para a média anual é calculada como:
   \[
   \text{Contribuição do primeiro semestre} = \text{nota do primeiro semestre} \times 0,4
   \]

2. A contribuição total necessária no segundo semestre é calculada com base na meta anual desejada:
   \[
   \text{Nota necessária no segundo semestre} = \frac{\text{meta anual} - \text{contribuição do primeiro semestre}}{0,6}
   \]

3. A contribuição do CP no segundo semestre é então subtraída, e o restante é atribuído à GS:
   \[
   \text{Nota mínima na GS} = \frac{\text{nota necessária no segundo semestre} - \text{contribuição do CP}}{0,6}
   \]

## Como Usar

### Pré-requisitos

- Python 3.x instalado

### Execução do Programa

1. Clone ou copie este código para um arquivo Python, como `calculo_nota.py`.
2. Execute o arquivo e insira as notas solicitadas:

    ```bash
    python calculo_nota.py
    ```

3. O programa solicitará três valores:
   - Nota do primeiro semestre
   - Nota do CP do segundo semestre
   - Meta de média anual desejada

4. Após inserir esses valores, o programa calculará e exibirá a nota mínima necessária na GS do segundo semestre.

### Exemplo

Para uma meta anual de 60, com as seguintes notas:

- Nota do primeiro semestre: 49.9
- Nota do CP do segundo semestre: 81.75

O programa exibirá:

Para alcançar uma média anual de 60, você precisa de uma nota mínima de 56.72 na GS do segundo semestre.

## Disclaimer

Este programa é fornecido como uma ferramenta de auxílio para cálculo de notas e não garante precisão absoluta. Certifique-se de revisar todos os resultados e consulte fontes adicionais ou profissionais para validar informações críticas. O autor não se responsabiliza por quaisquer consequências decorrentes de eventuais erros nos cálculos ou no uso do programa.
