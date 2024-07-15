titulo = 'PERCURSO'
farmacia = '23'
largura_rua = 5
tamanho_casa = 50
colunas = 17
linhas = 7
casas_por_linha = 3
casas_por_coluna = 2
largura_quadra = (casas_por_linha * (tamanho_casa))
altura_quadra = (casas_por_coluna * (tamanho_casa))
largura_jogo = colunas * (tamanho_casa)
largura_tela = largura_jogo + 500
altura_tela = linhas * tamanho_casa
alinhamento_lateral = largura_jogo + 20
posicao_botao_buscar = 60
largura_botao = 90
altura_botao = 30

# Cores
BRANCO = (255, 255, 255)
CINZA_ESCURO = (55, 58, 56)
VERDE = (0, 87, 24)
AMBIENTE = (171, 176, 162)
BEGE = (245, 245, 220)
CINZA = (169, 169, 169)
VERDE_CLARO = (144, 238, 144)
VERMELHO = (255, 0, 0)
AZUL = (79, 144, 242)
PRETO = (0, 0, 0)


mapa = [
    ['rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh'],
    ['rv', '1', '2', '3', 'rv', '4', '5', '6', 'rv', '7', '8', '9', 'rv', '10', '11', '12', 'rv'],
    ['rv', '13', '14', '15', 'rv', '16', '17', '18', 'rv', '19', '20', '21', 'rv', '22', '23', '24', 'rv'],
    ['rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh'],
    ['rv', '25', '26', '27', 'rv', '28', '29', '30', 'rv', '31', '32', '33', 'rv', '34', '35', '36', 'rv'],
    ['rv', '37', '38', '39', 'rv', '40', '41', '42', 'rv', '43', '44', '45', 'rv', '46', '47', '48', 'rv'],
    ['rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh', 'rh']
]
