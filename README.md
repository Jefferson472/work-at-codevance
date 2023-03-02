<div align="center" id="badges">
    <img src="https://img.shields.io/badge/STATUS-COMPLETED-green"/>
</div>


# Documentação do Projeto Codevance Payments

O projeto Codevance Payments é um gerenciador de pagamentos que permite aos fornecedores acessarem seus pagamentos e solicitar antecipações mediante à taxas baseadas no valor e na quantidade de dias a serem antecipados. O projeto está hospedado na Plataforma Render e pode ser acessado através do link abaixo:

[Codevance Payments](https://codevance-payments.onrender.com)

## Fluxo do Projeto
![Fluxo do Projeto](/docs/codevance-payments-fluxo.jpg)


---
## Instalando e Executando o Projeto
Para executar o projeto localize o arquivo `default.env` e renomei para `.env` fornecendo os valores para as varáveis de ambiente. Se estiver executando local, somente os valores das variáveis `SECRET_KEY` e `CELERY_BROKER_URL` são necessárias.

Execute os comandos abaixo:

1. Instale as dependências do projeto:

    `python -m pip install -r requirements-dev.txt` se estiver rodando local 

    `python -m pip install -r requirements.txt` se estiver rodando em produção

2. Rode as migrações para inicializar o banco de dados:

    `python src/manage.py migrate --settings=setup.settings.local` ou `python src/manage.py migrate --settings=setup.settings.prod`

3. Execute o arquivo `seed.py` para preencher o banco de dados com alguns pagamentos e usuários:

    `python src/manage.py shell < src/seed.py --settings=setup.settings.local`

    Se estiver no powershell utilize o comando:

    `python src/manage.py shell --settings=setup.settings.local --command="exec(open('src\seed.py').read())"`

4. Execute o servidor do Django:

    `python src/manage.py runserver --settings=setup.settings.local` ou `python src/manage.py runserver --settings=setup.settings.prod`

5. Execute o Celery e o Celery Beat. O Celery é responsável pela execução de algumas tarefas de forma assíncronas, neste projeto ele está sendo utilizado para envio de email e criação de logs*. Já o Celery Beat é usado para o agendamento da execução das tarefas, ele é responsável por rodar todos os dias uma função que irá verificar o vencimento dos pagamentos e desativar aqueles que estiverem vencidos.   

	`celery -A setup --workdir src worker -l INFO`

	`celery -A setup --workdir src beat -l INFO`

*O plano free do Render não permite trabalhar com workers, por este motivo, em produção o Celery não está sendo usado. Porém, toda a configuração para a execução de tarefas assíncronas está disponível no código. 

---
## Utilizando o Projeto
O arquivo seed.py, utilizado no item 3 da seção de Instalação, irá fornecer os usuários abaixo e 6 pagamentos de exemplo, sendo um vencido. Ao final da execução irá chamar a função para verificar o os pagamentos vencidos como forma de exemplificação da função.

- admin@test.com: Superusuário Django
- operator@test.com: Pode criar e ver todos os pagamentos, e criar e aprovar antecipações
- supplier@test.com: Pode ver seus pagamentos cadastrados e solicitar antecipações
- supplier2@test.com: Pode ver seus pagamentos cadastrados e solicitar antecipações

A senha de todos usuários é: `test123456`

Acesse `http://localhost:8000/` faça o login com algum dos usuários e solicite uma antecipação. Se estiver com o perfil "Operator" poderá aprovar ou reprovar a requisição. Todas estas ações estarão disponíveis em `http://localhost:8000/logs`.

---
## API Endpoints
### Autenticação
O projeto utiliza autenticação através de JWT, para se autenticar, encaminhe uma requisição do tipo POST para `http://localhost:8000/api/token/` o seguinte conteúdo com um usuário existente:

```json
{
  "email": "email",
  "password": "password"
}
```

Este endpoint irá retorno um json conforme abaixo, utilize o valor da chave "access" em todas as requisições para garantir acesso autenticado:

```json
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```

### Listando e Filtrando Pagamentos
Para visualizar uma lista de pagamentos encaminhe uma requisição do tipo GET para `http://localhost:8000/payments/`. Esta requisição irá retornar o json conforme abaixo:

```json
{
  "id": 2,
  "supplier": 1,
  "description": "Pagamento Teste 2",
  "value": "851.00",
  "date_due": "2023-03-31",
  "is_active": true,
  "created": "2023-03-01T15:13:27.470005-03:00",
  "req_antecipation": {
      "id": 1,
      "payment": 2,
      "requester": 2,
      "request_date": "2023-03-01",
      "fee": "25.53",
      "status": "1",
      "created": "2023-03-01T15:39:05.328825-03:00",
      "updated": "2023-03-01T15:39:54.290121-03:00",
      "antecipation": {
          "id": 1,
          "new_value": "825.47",
          "created": "2023-03-01T15:39:54.332008-03:00",
          "updated": "2023-03-01T15:39:54.332008-03:00",
          "operator": 1,
          "req_antecipation": 1
      }
  }
},
```

Também é possível filtrar o resultado da lista através do endpoint: `http://localhost:8000/payments/status/`. Este endpoint recebe e retorna para os seguintes status:

- unavailable: retorna os pagamentos indiponíveis para antecipação
- avaliable: retorna os pagamento disponíveis para antecipação
- requested: retornar os pagamentos que possuem um pedido de antecipação
- approval: retorna os pagamentos com antecipações aprovadas
- disapproval: retorna os pagamentos com antecipações reprovadas
 
### Solicitando Antecipações
Para solicitar uma antecipação de pagamento com um usuário logado encaminhe uma requisição do tipo POST para `http://localhost:8000/antecipation/create/` com o seguinte conteúdo:

```json
{
  "payment": id,
  "request_date": YYYY-MM-DD
}
```

---
## Testes
Os testes podem ser executados através do comando:

`python src/manage.py test --failfast --settings=setup.settings.local`


---
# Trabalhe na Codevance

A [Codevance](https://codevance.com.br) é uma software house que tem como missão otimizar os resultados e gerar valor ao seu negócio utilizando tecnologia como meio.

Somos especialistas em Python, nosso time atua todo de forma remota e nossos clientes possuem grandes desafios tecnológicos.

Se você:

- Tem sangue no olho e é, ou busca ser, um ótimo programador;
- Tem interesse em crescer profissionalmente;
- É organizado, tem disciplina e autonomia para trabalhar do conforto da sua casa;
- Gosta da linguagem Python ou já utilizou em algum projeto profissional;

Eu te convido a clonar esse repositório, meter a mão na massa e mostrar pra gente as suas qualidades.

Temos vagas para todos os perfis. Não é preciso ter experiência e não fazemos nenhum tipo de distinção.

## Como participar

1. Clone este repositório
1. Siga as instruções abaixo
1. Suba o projeto em algum lugar (heroku, de preferência)
1. Envie um e-mail para ronaldo *dot* oliveira *at* codevance *dot* com *dot* br

## Especificações

Você vai desenvolver um sistema de antecipação de pagamentos.

Imagine que haja uma série de pagamentos a serem feitos por uma empresa no decorrer dos próximos meses, mas a empresa quer fazer um plano com seus fornecedores para fazer estes pagamentos de forma adiantada, concedendo um desconto relacionado a quantidade de dias de diferença entre a data de vencimento original do pagamento e a nova data de pagamento.

O objetivo é fornecer melhor fluxo de caixa ao fornecedor e rentabilizar o caixa da empresa através dos descontos.

Para descobrir o novo valor a ser pago nesta antecipação, o cálculo a ser feito é:

```
NOVO_VALOR = VALOR_ORIGINAL - (VALOR_ORIGINAL * ((3% / 30) * DIFERENCA_DE_DIAS))
```

Vamos a um exemplo prático:

```
DATA DE VENCIMENTO ORIGINAL = 01/10/2019
VALOR ORIGINAL = R$ 1.000,00
NOVA DATA DE VENCIMENTO = 15/09/2019

NOVO VALOR = 1000 - (1000 * ((3% / 30) * 16))
NOVO VALOR = 1000 - (1000 * 0,016)
NOVO VALOR = 1000 - 16

NOVO VALOR = R$ 984,00
```

### Características

- O sistema deve armazenar os pagamentos e suas informações básicas
  - id do pagamento, data de emissão, data de vencimento, valor original, a qual fornecedor pertence, dados cadastrais básicos deste fornecedor, como razão social e CNPJ.
- Para um pagamento ser adiantado, o fornecedor deve fazer uma solicitação, então o operador da empresa escolhe se libera a antecipação ou nega a antecipação. Toda essa movimentação deve ficar armazenada em um log.
  - Essa solicitação pode vir via sistema ou por outras vias. Quando vier por outras vias, o operador da empresa fará a solicitação no sistema.
- O fornecedor deve ter acesso a uma área, através de autenticação via email e senha, onde ele possa solicitar a antecipação de um pagamento. É necessário também que ele veja todos os pagamentos disponíveis para antecipação, todos os pagamentos aguardando liberação, todos os aprovados e todos os negados.
  - Importantíssimo que um fornecedor não veja os pagamentos de outro
- Para cada ação sobre um pagamento (solicitação, liberação, negação) o sistema deve enviar um email ao fornecedor.
  - Este envio de email deve ser feito de forma assíncrona (`celery` é seu amigo)
- Caso um pagamento chegue até sua data de vencimento sem ser antecipado, o mesmo deve ser indisponibilizado para operação, mas mantido no histórico.
  - Fornecedores não podem ver pagamentos indisponibilizados disponíveis para antecipação
- Deve haver uma API Rest básica com dois endpoints:
  - Um endpoint que liste as operações de um fornecedor, que estará autenticado via JWT. Este endpoint deve permitir filtro por estado do pagamento (indisponível, disponível, aguardando confirmação, antecipado, negado)
  - Outro endpoint que será responsável pela solicitação de antecipação de um pagamento. Este endpoint deve receber o identificador do pagamento e, obviamente, um usuário logado só pode solicitar antecipação dos pagamentos associados ao seu usuário.

## Requisitos técnicos

- Utilize Python 3.7 (ou mais recente) como linguagem e PostgreSQL como banco de dados;
- Utilize um framework (dica: com django é mais fácil);
- O código deve estar em inglês (commits podem estar em pt-br);
- O sistema deve estar online, rodando, em algum lugar (dica: com heroku é mais fácil);
- O sistema deve ter testes automatizados (dica: com pytest é mais fácil);
- O repositório deve conter documentação sobre como fazer deployment e como testar;
- Deve conter uma documentação da API;

## Recomendações e dicas

- Caso for utilizar Django, temos [nosso cookiecutter](https://github.com/codevance/cookiecutter-django) que pode servir de ponto de partida (mas não é obrigatório);
- Use boas práticas de programação;
- Modele os dados com cuidado;
- Se preocupe com arquitetura e qualidade de código, não se preocupe com estética (dica: bootstrap é seu amigo).

**Divirta-se!**
