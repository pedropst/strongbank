Bootcamp Código[s] | Semifinal

# Strong Bank

Projeto realizado em Python, tanto frontend quanto backend. Para o front, utilizou-se o framework **Streamlit**. Já o backend foi realizado com **Django** e **Django Rest Framework** (DRF). Comunicação entre client side e server side acontece por meio da API.

### Observações e motivações sobre ações tomadas por mim:
1. Utilizei o sistema de autenticação de usuário do Django para dividir os usuário em dois grandes grupos, administradores e usuários comuns.
2. Para determinar o que cada grupo tem acesso ou não, está relacionado ao que abstrai de como seria o funcionamento de um banco. Em resumo, todas as ações sobre a conta (sacar, depositar, etc.) são de única responsabilidade do dono da conta, portanto, administradores não possuem tais permissões. Assim como, toda informação visível ao usuário são somente informações do próprio usuário. Já os adminstradores possuem visibilidade de todas as informações, quando assim desejarem.
3. Resolvi desenvolver o frontend para apresentar melhor a minha ideia, e para colocar em prática a comunicação pela API por meio das **requisições**. A única informação que o frontend possui salva com ele é o `username` e `password` do usuário, para que as autenticações nas outras páginas sejam feitas automaticamente - sem precisa relogar para cada ação. Essa informação é salva e sobrescrita toda vez que um login é confirmado na tela de login, fica salva no arquivo `cookie.json` e que até pelo nome deixa claro o que eu tinha em mente quando decidi armazenar essas informações para serem reutilizadas.
4. O frontend tem como objetivo ser utilizado pelo usuário final, e, portanto, não se comportando corretamente para usuários do grupo administrador. Para esse segundo grupo, recomendo a utilização do Postman ou Insomnia.
5. Optei por fazer raras validações no frontend - quando feitas, foram para tratamento de alguns inputs, deixando a responsabilidade para o backend lidar com as requisições, tentativas de fraudes, etc.

## Frontend
Tem como objetivo simular como seria uma aplicação para um banco digital, feita para ser utilizada pelo funcionário final. Nele é possível acessar páginas para sacar, depositar, transferir, gerenciar cartões, retirar extratos e verificar informações sobre a conta do usuário. Além destas ações que assemelham ao funcionamento de um banco digital, também é possível fazer o cadastro de clientes, criação de contas e de cartão.


## Backend 
Tem como objetivo simular o lado do servidor de um banco digital que disponibiliza por meio dos endpoints da API maneiras de comunicar-se com o server.
Nele foi implementado todas as validações e regras de negócio.

## API - Endpoints
Os endpoints disponíveis e os requisitos para utilizá-los são:

_____ Endpoints SEM autenticação ____
### /user
* Tem como objetivo o CRUD de usuários.
* Verbos: GET, POST, PUT, DELETE
* Requer: `username` `password`
* GET: `{}`
* POST: 
`{
"username":"pedro",
"password":"123456",
"tipo": tipo
}`

Onde tipo, pode ser "A", ou vazio, "". Sendo o primeiro caso para registro de superusers e o segundo para registro de usuários normais. A diferenciação entre esses dois tipos, está nas permissões que cada um tem. Usuários normais conseguem ver somente informações relacionadas ao mesmo. Já admins conseguem ver de todos, contudo, não conseguem exercer "ações" como: sacar, transferir, tirar extrato, depositar.

____ Endpoints COM autenticação ____
### /user/pk/
Tem como objetivo detalhar usuário específico.
* PUT: 
`{
"username":"pedro",
"password":"123456"
}`
* DELETE: `{}`


### /cliente/
* Tem como objetivo o CRUD de clientes.
* Requer: `nome`, `endereco`,  `celular`. 
* GET: `{}`
* POST: `{"username":"pedro","password":"123456","cpf":"03336151133", "tipo": tipo}`

### /cliente/pk/
Tem como objetivo detalhar usuário específico.
* PUT: 
`{
"nome" : "nome",
"endereco" : "endereco",
"celular" : "celular"
}`
* DELETE: `{}`


### /conta/
* Tem como objetivo o CRUD de contas.
* Requer: ~~`doc_cliente`~~, `saldo`, `agencia`
* GET: `{}` -> `{"doc_cliente", "saldo", "agencia", "conta"}` CODE: 200
* POST: `{"doc_cliente": "03336151133", "saldo": 3000, "agencia": "0001"}` -> CODE: 201

### /conta/pk/
* Tem como objetivo detalhar conta específica.
* DELETE: {}

### /saldo
* Tem como objetivo informar saldo disponível na conta.
* GET: `{}` -> `{"saldo": 3000}` CODE: 200

### /sacar/
* Tem como objetivo sacar valor da conta.
* POST: `{"valor": 1000, "senha": "123456", "descricao": "descricao"}` -> CODE: 200

### /depositar/
* Tem como objetivo depositar na conta.
* POST: `{"valor": 2500, "descricao": "descricao"}` -> CODE: 200

### /transferir/
* Tem como objetivo transferir fundos de uma conta para outra.
* POST: `{"doc_destinatario": "04135965788", "valor": 2500, "senha": "123456", "descricao": "descricao"}` -> CODE: 200

### /extrato/
* Tem como objetivo gerar o extrato para um período de data informada.
* POST: `{"dta_inicial": "11/07/2022", "dta_final": "11/07/2022"}` -> [{transacao1}, {transacao2}, ...] CODE 200


### /cartao/
* Tem como objetivo o CRUD de cartões.
* Requer: `dia_vencimento`, `limite_total`, `limite_desbloqueado`, `limite_disponivel`
* GET: -> `{"numeracao": "4138 5810 2586 9874", "mes_validade": "07", "ano_validade": "2030", "limite_total": 5000, "limite_desbloqueado": 3000, "limite_disponivel": 5000, "bloqueado": 0, "cvv":"341"}` CODE 200
* POST -> `{"dia_vencimento": "15", "limite_total": 5000}` CODE 201
* 
### /pagarcredito/
* Tem como objetivo realizar um pagamento com cartão, no modo crédito.
* Requer: `valor`, `parcelas`
* POST -> `{"valor": 600, "parcelas": 12}` CODE: 200

### /pagarcredito/
* Tem como objetivo realizar um pagamento com cartão, no modo débito.
* Requer: `valor`
* POST -> `{"valor": 600}` CODE: 200




https://user-images.githubusercontent.com/67083478/179382539-cb295543-ae8d-4dfc-a30f-0e7dc2e08fe0.mp4

