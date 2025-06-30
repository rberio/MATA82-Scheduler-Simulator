# [MATA82] Simulador de Escalonador de Tarefas em Tempo Real
Este projeto consiste em um simulador de eventos discretos para escalonamento de tarefas em tempo real, desenvolvido como requisito para a disciplina MATA82 - Sistemas em Tempo Real. O simulador possui uma interface gráfica interativa que permite ao usuário configurar, executar e analisar o comportamento de diferentes algoritmos de escalonamento em um ambiente com um ou múltiplos processadores.

## 1. Funcionalidades
* Simulação de Múltiplos Algoritmos: Implementação e comparação visual de três algoritmos clássicos de escalonamento:

  - Rate-Monotonic (RM)
  - Earliest Deadline First (EDF)
  - Least Laxity First (LLF)

* Suporte a Múltiplos Processadores: Permite configurar o número de processadores para a simulação, modelando tanto sistemas uniprocessador quanto multiprocessador (escalonamento global).

* Interface Gráfica Intuitiva: Desenvolvido com a biblioteca tkinter, oferecendo uma experiência de uso amigável para configurar tarefas e simulações.

* Visualização com Gráficos de Gantt: Geração de gráficos de Gantt dinâmicos e animados para cada algoritmo, permitindo uma análise visual clara de qual tarefa está executando em cada instante de tempo.

* Métricas de Desempenho: Cálculo e exibição de métricas essenciais para a análise do escalonamento, incluindo:

  - Utilização da CPU
  - Número de Preempções
  - Deadlines Perdidos
  - Tempo de Resposta Médio

* Configuração Flexível de Tarefas: As tarefas podem ser adicionadas manualmente através da interface ou carregadas em lote a partir de arquivos .csv.

* Design Robusto e Escalável:

  - O simulador lida com grandes conjuntos de tarefas (100+) sem esgotar a memória, graças à geração de jobs just-in-time.
  - A interface se adapta a qualquer quantidade de tarefas, com barras de rolagem para a lista e os gráficos.
  - Inclui uma verificação de recursos que avisa o usuário caso ele simule mais processadores do que os disponíveis fisicamente na máquina.

## 2. Tecnologias Utilizadas
- Linguagem: Python 3
- Interface Gráfica: Tkinter (biblioteca padrão do Python)

## 3. Como Executar
1. Certifique-se de que você tem o Python 3 instalado em sua máquina.
2. Clone ou baixe os arquivos do projeto para um diretório local.
3. Abra um terminal ou prompt de comando, navegue até a pasta do projeto.
4. Execute o script principal:
```
python MATA82_SSim_v0628b05.py
```

## 4. Estrutura do Projeto
* `MATA82_SSim_v0628b05.py`: O arquivo principal que contém toda a lógica do simulador e da interface gráfica.
* `tasks_*.csv`: Arquivos de exemplo contendo conjuntos de tarefas que podem ser carregados no simulador.

## 5. Guia de Uso
1. Configuração de Tarefas

No painel esquerdo, na seção "Configuração da Tarefa", você pode definir os parâmetros de uma nova tarefa:

- Nome da Tarefa: Um identificador único para a tarefa.
- Tempo de Computação (C): O tempo que a tarefa leva para ser executada até o fim.
- Período (T): A frequência com que novas instâncias (jobs) da tarefa são liberadas.
- Deadline (D): O prazo máximo, a partir da liberação, que a tarefa tem para concluir sua execução.
- Jitter (J) (opcional): Uma variação no tempo de liberação (atualmente não implementado na lógica principal, mas o campo existe para futuras expansões).

Após preencher os campos, clique em "Adicionar Tarefa".

2. Carregar Tarefas via CSV
Alternativamente, clique em "Carregar CSV" para carregar um conjunto de tarefas de um arquivo. O arquivo `.csv` deve ter o seguinte cabeçalho e formato:

| Name | Computation | Time | Period | Deadline | Jitter |
| ---- | ----------- | ---- | ------ | -------- | ------ |
| Task1| 1.0         | 11.0 | 5.0    | 0.0      |        |
| Task2| 2.0         | 12.0 | 10.0   | 0.0      |        |
| ...  | ...         | ...  | ...    | ...      | ...    |


3. Configuração da Simulação
Na seção "Configuração da Simulação", você pode definir:

- Tempo de Simulação: A duração total (em unidades de tempo) da simulação.
- Número de Processadores: A quantidade de núcleos de processador a serem modelados.

4. Análise dos Resultados
Após clicar em "Executar Simulação", o painel direito será preenchido.

- Gráfico de Gantt: Mostra a linha do tempo de execução. Cada linha horizontal corresponde a uma tarefa. Um bloco colorido indica que a tarefa está sendo executada naquele instante de tempo.
* Painel de Métricas: Fornece um resumo quantitativo:
  - Utilização da CPU: A carga computacional teórica total do conjunto de tarefas (Σ(C/T)). O valor (de X.0) indica a capacidade total do sistema (X = número de processadores).
  - Preempções: Quantas vezes uma tarefa em execução foi interrompida por outra de maior prioridade.
  - Deadlines Perdidos: Quantas instâncias de tarefas não conseguiram terminar antes do seu prazo final. A cor do texto ficará vermelha se houver algum deadline perdido.
  - Tempo de Resposta Médio: O tempo médio entre a liberação de um job e sua conclusão.

## 6. Algoritmos Implementados
1. Rate-Monotonic (RM): Algoritmo de prioridade estática. A prioridade é inversamente proporcional ao período da tarefa (menor período = maior prioridade).
2. Earliest Deadline First (EDF): Algoritmo de prioridade dinâmica. A prioridade é dada à tarefa cujo deadline absoluto está mais próximo no tempo.
3. Least Laxity First (LLF): Algoritmo de prioridade dinâmica. A prioridade é dada à tarefa com a menor "folga" (laxity), calculada como (deadline - tempo_atual - computação_restante).

## 7. Autores
- Carlos Eduardo Lima Botelho Vasconcelos
- Roberio Gomes de Oliveira
