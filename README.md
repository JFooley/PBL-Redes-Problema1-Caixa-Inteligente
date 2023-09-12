<div align="center">
  <h1>
  Universidade Estadual de Feira de Santana (UEFS)

  Problema 1: Supermercado inteligente
  </h1>

  <h3>
    João Gabriel Lima Almeida
  </h3>

  <p>
  DEPARTAMENTO DE TECNOLOGIA
    
  TEC502 - CONCORRÊNCIA E CONECTIVIDADE
  </p>
</div>

# 1. Introdução
<p style="text-align: justify;">
  Com o avanço e as tecnologias se tornando mais acessíveis, a digitalização de operações antes feitas de forma manual tem se tornado cada vez mais realidade. Durante a pandemia de COVID-19 esse processo se tornou ainda mais intenso, levando muitas áreas a buscarem modernização, não apenas aquelas que possuam uma ligação maior com tecnologia.
  
  Uma área em que a alguns anos vem realizando essa migração é a de supermercados e comércios no geral. A possibilidade de realizar o controle de estoque e vendas via software diminui a abertura para erro humano e torna a operação mais eficiente, além de que as tecnologias de rede e Internet das Coisas (IoT) permitem uma integração de diversos equipamentos em uma única infreestrutura integrada.
  
  Diante disso, este relatório descreve a construção de um sistema em rede para o gerenciamento de um supermercado inteligente, sendo ele proposto pelo problema 1 do MI - Concorrencia e Conectividade. As caracteristicas do sistema são:
  - Todos os caixas são inteligentes e fazem a leitura dos produtos através de um leitur de Radio Frequency Identification (RFID)
  - Todos os caixas estão conectados em uma infraestrutura IoT em nuvem
  - Toda transação e aquisição de informações sobre os produtos deve ser feita através de requisição com protocolo baseado em API REST
  - Cada caixa é representado por um processo rodando em diferentes computadores do laboratório
  - Não é permitido o uso de Frameworks de terceiros pode ser utilizado
  - A adminstração deve ser capaz de ver informações sobre os caixas, bloquear ou liberar um caixa, o histórico de compras, e acompanhar compras em tempo real
  - Um usuário pode iniciar a compra, verificar os itens e pagar a compra
  - Cada tag é associada a um produto e a leitura é feita de forma simultanea

  A metodologia utilizada para o desenvolvimento foi a Problem Based Learning (PBL), através de sessões semanais com a turma onde foram discutidos os requisitos do problema, conceitos importantes e outras questões importantes para o desenvolvimento da solução do problema, neste caso, o software. A linguagem de programação utilizada para a implementação do sistema foi o Python 3.10 e suas bibliotecas nativas
</p>

# 2. Desenvolvimento
<p style="text-align: justify;">
  Considerando os requisitos do problema, decidimos que a arquitetura do sistema devia ser dividida em 4 nós diferentes: Leitor, caixa, servidor intermediário e banco de dados. Representando visualmente os nós e suas conexões, a arquitetura tem a seguinte forma:
</p>

![Arquitetura do sistema.](https://github.com/JFooley/PBL1---Redes/blob/c6e6cae130db4d0e58de4db5f632ed59e80fe40c/Imagens/Arquitetura%20do%20sistema.png)

<p style="text-align: justify;">
  No nível mais alto da rede está o banco de dados que guarda todas as informações utilizadas na operação dos caixas. Ele é responsável por fornecer, através de requisições HTTP, os dados para os níveis abaixo do sistema e receber as solicitações para modificação e criação dos mesmos. Os dados guardados são: estoque de produtos, contendo cada produto com seu respectivo código de tag RFID, preço e quantidade; caixas, que possui endereço de IP de cada caixa conectado a rede e seu status de bloqueio ou não; carrinhos, contendo o endereço IP de cada caixa conectado e os itens atuais presentes no carrinho daquele caixa; compras, que possui o histórico de todas as compras realizadas em todos os caixas em lista, contendo a data da compra e os itens do carrinho. 
  Seguindo o modelo de requisições HTTP, foram implementados 5 rotas do tipo GET e 3 rotas do tipo POST, sendo elas:
  
  - GET
<ol>
  <li>"/" - Lista o estoque de produtos</li>
  <li>"/:ID" - Lista as informações do estoque do produto especificado pelo ID passado como parametro</li>
  <li>"/compras" - Lista o histórico de compras</li>
  <li>"/carrinhos" - Lista os caixas e os seus respectivos carrinhos no momento da requisição</li>
  <li>"/caixas" - Lista todos os caixas e seus estados de bloqueio</li>
</ol>

  - POST
<ol>
  <li>"/comprar" - Verifica se é possivel, realiza a compra dos itens do carrinho e por fim salva ela no histórico</li>
  <li>"/update-caixa" - Atualiza o status do carrinho especificado pelo IP para o status passado na requisição</li>
  <li>"/update-carrinho" - Atualiza os itens do carrinho especificado pelo IP para o passado na requisição</li>
</ol>

  Essas rotas de requisições são utilizadas pelo segundo nível da rede: o servidor intermediário. Neste nível fica um programa responsável por conectar cada um dos caixas ao database, realizando as requisições e devolvendo os dados para quem os solicitou através de uma conexão socket TCP/IP. A existencia desse servidor intermediário tem como finalidade facilitar e organizar melhor o controle dos caixas e simplificar todas as requisições necessárias para cada operação. As rotas GET de histórico de compras, carrinhos atuais, caixas e a de POST de atualizar o status do carrinho não são utilizadas pelo servidor intermediário pois são rotas de administração do sistema. Por não ser o foco do problema, ficou acordado com os tutores que essas rotas seriam acessadas através softwares de teste de API como Postman e Insomnia. Ainda no nível intermediário existe o leitor de indentificação de radiofrequencia (RFID) acoplado a uma placa Raspberry Pi que é responsável por ler as tags e envia-las para o caixa conectado a ele através também de uma conexão socket TCP/IP.
  
  No nível mais baixo da rede estão os caixas, estes separados cada um em uma maquina diferente. Como dito anteriormente, cada caixa realiza duas conexões socket: uma com o servidor intermediário e a outra, quando necessário, com o leitor RFID. Os caixas tem a função de coletar as tags dos produtos lidos, solicitar os dados ao servidor intermediário exibir as informações de cada um deles. Além disso, tem a função de enviar os produtos do carrinho ao servidor intermediário, solicitar a compra e exibir se ela foi realizada ou não.
</p>

# 3. Resultados
<p style="text-align: justify;">
  Ao final do desenvolvimento, o sistema ficou dividido em 4 programas que realizam a função dos 4 nós propostos na arquitetura do sistema.

  - Banco de dados (Database.py)

O nó do banco de dados foi implementado utilizando o módulo http.server nativo do Python. Nele é executado um servidor HTTP que chama os métodos da classe APIHandler, onde estão os métodos GET e POST citados na seção de desenvolvimento. Por não ser o foco do problema, apesar do nome, o banco de dados não é exatamente um banco de dados de armazenamento em massa SQL, apenas listas e dicionários locais na memória que guardam os dados do sistema mas que exercem papel semelhante para o finalidade do problema que é a comunicação em rede. Ainda sim, para evitar quebra da integridade dos dados devido ao paralelismo foi necessário a implementação de zona crítica na parte do código que realiza as alterações propriamente. A imagem abaixo mostra um exemplo do chatlog gerado pelo terminal do banco de dados durante a operação do sistema.
</p>

![Chatlog do banco de dados](https://github.com/JFooley/PBL1---Redes/blob/c6e6cae130db4d0e58de4db5f632ed59e80fe40c/Imagens/Database.png)

<p style="text-align: justify;">
  - Servidor intermediário (Server.py)
  
Como a quantidade de caixas é pequena foi decidido utilizar multithreading para que cada caixa tenha sua própria thread cuidando das operações solicitadas. Dessa forma, uma thread principal roda um servidor socket que fica aguardando por conexões advindas dos caixas, quando essas solicitações de conexões chegam o programa verifica se aquele caixa solicitante está desbloqueado e cria uma nova thread dedicada apenas para ele, onde as requisições são feitas. Por uma questão de depuração e melhor visualização das operações do servidor intermediário, o programa imprime no terminal um chatlog monstrando todas as novas conexões de caixas, as mensagens trocadas (com qual caixa e o conteúdo), desconexões e o motivo delas. A imagem abaixo mostra um exemplo do chatlog durante a operação do sistema.
</p>

![Chatlog do servidor intermediário](https://github.com/JFooley/PBL1---Redes/blob/e01096c0298b7ce453b347df55f350463f1a452b/Imagens/Server.png)

<p style="text-align: justify;">
  - O leitor RFID (Reader.py)

Uma das limitações fisicas da construção do problema é que no laboratório existe apenas um leitor RFID, por esse motivo a operação do leitor foi desenvolvida da seguinte forma: o leitor possui um server socket que fica aguardando por conexões dentro de um looping; quando uma nova solicitação de conexão chega de um caixa o programa aceita, realiza a leitura de todas as tags RFID no alcance do sensor, envia para o caixa solicitante a lista com as tags e logo em seguida fecha a conexão. Dessa forma, o leitor fica alocado a um caixa apenas durante a leitura das tags, podendo atender a qualquer caixa do sistema quando não estiver em uso.

  - Caixas (Cliente.py)

Considerando a função prevista do caixa ele foi implementado da seguinte forma: Após se conectar via socket com o servidor intermediário o caixa solicita ao usuário qual operação ele deseja realizar através de um input pelo teclado; o usuário pode escolher ler os produtos ou confirmar a compra, caso escolha por ler os produtos o caixa realiza uma segunda conexão socket com o leitor RFID, recebe a lista contendo todas as tags no alcance do leitor e envia uma a uma para o servidor intermediário que realiza uma requisição do tipo GET com a rota '/(ID da TAG)' e devolve as informações de cada tag. Essas informações são guardadas no carrinho local do caixa, que no final da leitura é enviado para o database para que atualize o seu estado lá. A comunicação entre o caixa e o servidor intermediário é feita sempre utilizando um dicionário com as chaves "Type" e "Content": na primeira chave é mandado o tipo de conteúdo que o caixa está solicitando, se é um código, uma compra ou um update-carrinho; na segunda chave é enviado o conteúdo, que é interpretado de maneira diferente pelo servidor intermediário a depender do tipo passando na chave "Type".

  - Arquivo de configuração

Devido ao python não possuir uma forma de detectar o IP de rede da máquina onde está sendo executado (Apenas o IP local interno dela), foi criado um arquivo de configuração contendo as variáveis de IP e porta do sistema, já que elas variam de acordo com a maquina que o código está sendo executado. Dessa forma, nenhum código precisa ser alterado além do arquivo de configuração quando for executado em uma maquina diferente.
</p>

# 4. Considerações finais
<p style="text-align: justify;">
  Ao fim, o sistema cumpre todas as funcionalidades propostas pelo problema seguindo também as exigencias e delimitações do mesmo, sendo a unica exceção o requisito de utilizar o serviço de emulação via conteiner Docker. De forma geral, o sistema é capaz de conectar diferentes caixas a rede, realizar leitura dos produtos no alcance do leitor, ver as informações em tempo real e realizar a compra dos produtos, tudo isso com de forma sincronizada sem que haja discrepância nas informações entre os caixas. O banco de dados além de cumprir todas as funções necessárias para a operações dos caixas também oferece interface necessárias para que, através de requisições, o sistema possa ser administrado. A implementação utilizando HTTP server e socket TCP/IP permite que cada um dos nós da arquitetura possam ser executados em diferentes computadores ou até mesmo em um unico, contanto que todos estejam conectado a mesma rede wifi. Vale ressaltar que o sistema prevê casos como a leitura de tags que não existem no banco de dados

  Com relação a parte acadêmica, o desenvolvimento do sistema proposto foi capaz de criar uma compreensão do funcionamento de redes de computadores, comunicação entre diferentes processos independente de linguagem ou hardware através de Socket e também do funcionamento de um servidor HTTP e as questões que permeam esse tipo de tecnologia. Além disso, a construção da rede permitiu compreender o funcionamento da arquitetura TCP/IP, como funcionam as suas diferentes camadas e compreenssão de como funciona a implementação de um protocolo baseado em API REST. A utilização do leitor RFID destacou a importancia da implementação de arquitetura IoT e utilização de harware "não convencional" que fuja do que normalmente é utilizado em um computador. 

  Falando em questão de possiveis melhorias o sistema no sistema, a implementação de um SGBD SQL e a adição de interface gráfica são otimas possibilidades de aprimoramento, principalmente para possibilitar o gerenciamento de forma mais direta sem a necessidade de fazer requisições manuais. Com relação a novas funcionalidades, o sistema poderia incluir novas rotas para possibilitar a alteração das informações dos produtos e até a adição de novos produtos. Outra questão é a adição de novos leitores individuais para cada caixa, permitindo que não 
</p>

# 5. Referencias
<p style="text-align: justify;">
  threading — Thread-based parallelism. Python Software Foundation. 2023. Disponível em: https://docs.python.org/3/library/threading.html. Acesso em: 22 de agosto de 2023.

  http.server — HTTP servers. Python Software Foundation. 2023. Disponível em: https://docs.python.org/3/library/http.server.html. Acesso em: 22 de agosto de 2023.

  json — Codificador e decodificador JSON. Python Software Foundation. 2023. Disponível em: https://docs.python.org/pt-br/3/library/json.html Acesso em: 24 de agosto de 2023.

  socket — Interface de rede de baixo nível. Python Software Foundation. 2023. Disponível em: https://docs.python.org/pt-br/3/library/socket.html Acesso em: 24 de agosto de 2023.

  Requests: HTTP for Humans. Requests. 2023. Disponível em: https://requests.readthedocs.io/en/latest/ Acesso em: 24 de agosto de 2023.
</p>

