dados = {
    'E20000172211010218905459': {'nome' : 'Arroz'  , 'codigo' : 'E20000172211010218905459', 'preco' : 5.50, 'stock' : 10},
    'E20000172211010118905454': {'nome' : 'Carne'  , 'codigo' : 'E20000172211010118905454', 'preco' : 20.0, 'stock' : 10},
    'E20000172211011718905474': {'nome' : 'Leite'  , 'codigo' : 'E20000172211011718905474', 'preco' : 6.00, 'stock' : 10},
    'E2000017221101321890548C': {'nome' : 'Ovo'    , 'codigo' : 'E2000017221101321890548C', 'preco' : 0.50, 'stock' : 10},
    'E20000172211009418905449': {'nome' : 'Feijão' , 'codigo' : 'E20000172211009418905449', 'preco' : 9.50, 'stock' : 10},
    'E20000172211012518905484': {'nome' : "Laranja", 'codigo' : 'E20000172211012518905484', 'preco' : 3.00, 'stock' : 10},
    'E20000172211011118905471': {'nome' : "Uva"    , 'codigo' : 'E20000172211011118905471', 'preco' : 7.99, 'stock' : 10},
    'E2000017221101241890547C': {'nome' : "Pera"   , 'codigo' : 'E2000017221101241890547C', 'preco' : 2.50, 'stock' : 10},
    'E2000017221100961890544A': {'nome' : "Kiwi"   , 'codigo' : 'E2000017221100961890544A', 'preco' : 6.75, 'stock' : 10},
}

# {'ip' : status (boleano)}
caixas = {}

# {'ip' : [carrinho]}
carrinhos = {}

# {'data' : dataHoje, 'carrinho' : carrinho}
compras = []