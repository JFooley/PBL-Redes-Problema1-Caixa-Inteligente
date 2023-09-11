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
  - Todos os caixas são inteligentes e fazem a leitura dos produtos através de um leituro RFID
  - Todos os caixas estão conectados em uma infraestrutura IoT em nuvem
  - Toda transação e aquisição de informações sobre os produtos deve ser feita através de requisição com protocolo baseado em API REST
  - Cada caixa é representado por um processo rodando em diferentes computadores do laboratório
  - Não é permitido o uso de Frameworks de terceiros pode ser utilizado
  - A adminstração deve ser capaz de ver informações sobre os caixas, bloquear ou liberar um caixa, o histórico de compras, e acompanhar compras em tempo real
  - Um usuário pode iniciar a compra, verificar os itens e pagar a compra;

  A metodologia utilizada para o desenvolvimento foi a Problem Based Learning (PBL), através de sessões semanais com a turma onde foram discutidos os requisitos do problema, conceitos importantes e outras questões importantes para o desenvolvimento da solução do problema, neste caso, o software.
</p>

# 2. Desenvolvimento
<p style="text-align: justify;">
  Considerando os requisitos do problema, decidimos que a arquitetura do sistema devia ser dividida em 4 nós diferentes: Leitor, caixa, servidor intermediário e banco de dados. Representando visualmente os nós e suas conexões, a arquitetura tem a seguinte forma:
  (INSERIR A IMAGEM)
  
  No nível mais alto da rede está o banco de dados que guarda todas as informações utilizadas na operação dos caixas. Ele é responsável por fornecer, através de requisições HTTP, os dados para os níveis abaixo do sistema e receber as solicitações para modificação e criação dos mesmos. Os dados guardados são: estoque de produtos, contendo cada produto com seu respectivo código de tag RFID, preço e quantidade; caixas, que possui endereço de IP de cada caixa conectado a rede e seu status de bloqueio ou não; carrinhos, contendo o endereço IP de cada caixa conectado e os itens atuais presentes no carrinho daquele caixa; compras, que possui o histórico de todas as compras realizadas em todos os caixas em lista, contendo a data da compra e os itens do carrinho. 
  Seguindo o modelo de requisições HTTP, foram implementados 5 rotas do tipo GET e 3 rotas do tipo POST, sendo elas:
  - GET
<ol>
  <li>"/" - Lista o estoque de produtos</li>
  <li>"/:ID" - Lista as informações do estoque do produto especificado pelo ID passado como parametro</li>
  <li>"/compras" - Lista o histórico de compras</li>
  <li>"/carrinhos" - Lista os caixas e os seus respectivos carrinhos no momento da requisição</li>
  <li>"/caixas" - Lista todos os caixas e seus estados de bloqueio</li>
  - POST
</ol>
</p>

