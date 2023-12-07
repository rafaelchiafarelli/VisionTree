# Árvore da Visão
Repositório da documentação e código relacionado ao projeto.

* Diagrama funcional

Os frutos são cameras PTZ que vasculham o espaço procurando por pessoas.
Quando uma pessoa é encontrada, a cabeça da pessoa é procurada
Quando a cabeça da pessoa é encontrada, ela é fotografada
A foto é processada e exposta nas folhas das árvores
A folha da árvore é um tablet que fica exposto imagens continuamente.

* Partes e funcionais
- CPU --> responsável por processar os vídeos das cameras e fazer o servidor que mantem o fluxo de dados para as folhas
- Tablets --> responsável por mostrar as imagens para os visitantes.
- Cameras --> responsável por capturar as imagens dos visitantes.
- tronco e galhos --> responsável pela estrutura de árvore
- Vazo --> responsável por armazenar o CPU e esconder a infra-estrutura
- Roteador WiFi --> infraestrutura de rede.

* Processos
No CPU ficarão os processos de captura, processamento e busca.
Na camera ficarão o controle de exposição, dia/noite, stream de dados
No Tablet ficará o serviço de captura de imagem da camera do tablet e serviço cliente de streamming.

* Resumo
Serviço de leitura em tempo real de vídeo streamado da camera com 2 canais. O canal de baixa resolução e o de alta resolução.
O canal de baixa resolução será usado para busca do corpo humano, enquanto o canal de alta resolução será usado para busca do rosto. 
    * Trata-se de um mediapipe de pose-estimation. Serão utilizados somente de X e Y do corpo (ombros, pelvis e cabeça)
    * Os pontos do rosto (boca, olhos e nariz) serão confirmados de estarem acima do ombro
    * Da imagem de maior resolução, será extraído o rosto
        - a imagem de menor resolução entrega a região macro do rosto
        - a imagem de maior resolução é recortada na região que sabemos ter o rosto
        - o rosto é processado e todos os 468 pontos são calculados.
    * as imagens dos rostos são mantidas em uma fila e, conforme o cliente faz a leitura da imagem, ela é entregue.
        - a imagem é processada para ter um fundo, ou alguma coisa nesse sentido, como a construção de um Avatar do visitante 
            - efeitos de distorção da imagem são aplicados a cada leitura
            - toda a imagem vai se tornando um borrão e eventualmente se perde o sentido

* Processo de vasculhar por visitantes
    * inicialmente configura-se uma posição inicial e uma posição final
    * para os propósitos dessa obra, somente o Pan deve ser utilizado.
        - há a possibilidade de fazer a varredura.
    * calcula-se quantas "viradas é possível" e grava-se todas essas "viradas"
        - quando as cameras iniciam elas já vão para uma posição inicial. 
        - essa posição inicial é equivalente à X viradas. Então, sabemos que, ao ligar as cameras estão na posição X
        - depois do stream de vídeo estar iniciado, é por que já podemos mandar a camera para a posição zero.
    * se não houver pessoas na posição 0, vai para posição 1 e assim por diante.
        - quando chegar na posição final e estiver habilitada a varredura, faz o movimento de Tilt (usando a mesma lógica de Pan)
    * Se não houver pessoas na posição final, retorna para a posição zero, fazendo a busca por pessoas. 
    * quando encontrar uma pessoa
        * salva a imagem em memória
        * salva os metadados em memória
            - posição da pessoa
            - número de pessoas
            - posição estimada das cabeças
            - pessoa mais próxima
            - data e hora
            - etc

* Processo de vasculhar por rosto.
    * a saída do processo anterior é a gravação de dois arquivos em uma pasta adequada;
    * faz a leitura da imagem, faz a leitura dos metadados
    * os metadados contém a posição provável da cabeça do visitante.
    * faz-se o recorte dessa imagem
    * faz-se o processamento do mediapipe dessa imagem procurando os pontos do rosto 
        - se houver mais de uma pessoa, deve-se estudar a que está mais perto da camera
    * faz-se o processamento dos pontos desse rosto e remove-se somente os pixeis que pentencem ao rosto.
    * gera-se os arquivos de metadados e imagem 
   
* Processo de streamming para os tablet
    * o processo anterior é o processo de geração de uma "semente" a cada interação a semente é germinada com um efeito de transformação. a toda imagem capturada nova, uma nova semente é exposta
    * a germinação é o processamento dessa imagem. 
    * escolhe-se o efeito visual utilizado aleatóriamente.
    * inicia-se a transformação da imagem presente no stream pela imagem atual. 
    * a transformação é da imagem atual para uma imagem nova e da imagem nova para uma imagem sem sentido, totalmente processada. 

* Processo no tablet.
    * o tablet inicia e se coneca ao servidor. 
    * cada tablet terá um end-point para se conectar
