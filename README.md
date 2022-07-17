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

## Passo a passo
1. Iniciar um ambiente virtual com `python -m venv .venv`.
2. Ativar o ambiente virtual com `.venv\scripts\activate`.
3. Instalar todas as dependências com `pip install -r requirements.txt`.
4. Configurar o arquivo .env com o banco de dados de sua preferência e as credencias do mesmo.
5. Iniciar a API com `python server/manage.py runserver`
6. Iniciar o frontend com `streamlit run client/scripts/app.py`

## API - Endpoints
Os endpoints disponíveis e os requisitos para utilizá-los são:

_____ Endpoints SEM autenticação ____
### /user/
* Tem como objetivo o CRUD de usuários.
* Verbos: POST
* Requer: `username` `password` `email` `tipo`
* POST: 
`{
"username":"pedro",
"password":"123456",
"tipo": tipo
}`

Onde tipo, pode ser "A", ou vazio, "". Sendo o primeiro caso para registro de superusers e o segundo para registro de usuários normais. A diferenciação entre esses dois tipos, está nas permissões que cada um tem. Usuários normais conseguem ver somente informações relacionadas ao mesmo. Já admins conseguem ver de todos, contudo, não conseguem exercer "ações" como: sacar, transferir, tirar extrato, depositar.

* https://user-images.githubusercontent.com/67083478/179382960-9680fa29-73d7-43a4-936b-221d7c3c4249.mp4

### /login/
* Tem como objetivo o CRUD de usuários.
* Verbos: POST
* Requer: `username` `password`
* POST: 
`{
"username":"pedro",
"password":"123456",
}`
* https://user-images.githubusercontent.com/67083478/179382996-b9972a2a-b74e-4d49-9604-2b94dcdead97.mp4



____ Endpoints COM autenticação ____

### /cliente/
* Tem como objetivo o CRUD de clientes.
* Requer: `nome`, `endereco`,  `celular`. 
* GET: `{}`
* POST: `{"nome":"Pedro Henrique", "endereco":"Rua Tijuca, 110", "cpf":"03336681155", "cnpj":"", "tipo": tipo}`
Onde tipo pode ser "PF" para pessoa física e "PJ" para pessoa jurídica.
* https://user-images.githubusercontent.com/67083478/179382675-7b35dcf9-340c-433a-ab99-30a28856e4e7.mp4

### /cliente/pk/
Tem como objetivo detalhar usuário específico.
* DELETE: `{}`


### /conta/
* Tem como objetivo o CRUD de contas.
* Requer: `saldo`, `agencia`
* GET: `{}` -> `{"cliente", "saldo", "agencia", "numero", "tipo"}` CODE: 200
* POST: `{"saldo": 3000, "agencia": "0001"}` -> CODE: 201
* https://user-images.githubusercontent.com/67083478/179382655-0c9ac263-6bd4-4bcb-aa89-b606f886dd94.mp4

### /conta/pk/
Tem como objetivo detalhar conta específica.
* DELETE: `{}`

### /saldo
* Tem como objetivo informar saldo disponível na conta.
* GET: `{}` -> `{"saldo"}` CODE: 200
* https://user-images.githubusercontent.com/67083478/179382635-36d89af1-431b-4691-b859-68fcf4177a9a.mp4

### /sacar/
* Tem como objetivo sacar valor da conta.
* POST: `{"valor": 1000, "senha": "123456", "descricao": "descricao"}` -> CODE: 200
* https://user-images.githubusercontent.com/67083478/179382631-c3c4972a-661c-4052-a159-9da31500d5cb.mp4

### /depositar/
* Tem como objetivo depositar na conta.
* POST: `{"valor": 2500, "descricao": "descricao"}` -> CODE: 200
* https://user-images.githubusercontent.com/67083478/179382624-1b2ab91f-c73d-4020-8f95-29534621af56.mp4

### /transferir/
* Tem como objetivo transferir fundos de uma conta para outra.
* POST: `{"doc_destinatario": "04135965788", "valor": 2500, "senha": "123456", "descricao": "descricao", "agencia":"0001", "numero":"152689"}` -> CODE: 200
* https://user-images.githubusercontent.com/67083478/179382602-2138d349-6181-49b2-94b9-206e525dd5d3.mp4

### /extrato/
* Tem como objetivo gerar o extrato para um período de data informada.
* POST: `{"dta_inicial": "11/07/2022", "dta_final": "11/07/2022"}` -> [{transacao1}, {transacao2}, ...] CODE 200
* https://user-images.githubusercontent.com/67083478/179382599-fbdddade-cc8e-4dd8-acea-6bb91c36c2a6.mp4


### /cartao/
* Tem como objetivo o CRUD de cartões.
* Requer: `dia_vencimento`, `limite_total`
* GET: -> `{"id", "numeracao", "mes_validade", "ano_validade", "limite_total", "limite_desbloqueado", "limite_disponivel", "bloqueado", "cvv", "dia_vencimento"}` CODE 200
* POST: `{"dia_vencimento": "15", "limite_total": 5000}` CODE 201
* https://user-images.githubusercontent.com/67083478/179382587-d7a8993a-110f-4e74-9747-fc05eaecb341.mp4

### /pagarcredito/
* Tem como objetivo realizar um pagamento com cartão, no modo crédito.
* Requer: `valor`, `parcelas`, `descricao`
* POST: `{"valor": 600, "parcelas": 12, "descricao": "Teste 1"}` CODE: 200
* https://user-images.githubusercontent.com/67083478/179382773-1468aae7-0766-43ea-90c3-932dc087ba02.mp4

### /pagardebito/
* Tem como objetivo realizar um pagamento com cartão, no modo débito.
* Requer: `valor`, `descricao`
* POST: `{"valor": 600, "descricao": "Teste 1"}` CODE: 200
* https://user-images.githubusercontent.com/67083478/179382582-e65f25e6-d4e7-418a-b49a-4a03f99119c8.mp4

### /alterarbloqueio/
* Tem como objetivo alternar entre cartão bloqueado e desbloqueado.
* Post: `{}`
* https://user-images.githubusercontent.com/67083478/179383293-a65bf5d2-7077-46ba-a8f0-e3c35583f6b4.mp4
