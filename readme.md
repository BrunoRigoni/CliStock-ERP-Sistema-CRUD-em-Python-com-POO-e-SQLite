# Sistema de Gestão de Estoque e Pedidos (CLI) — Python + SQLite

## Descrição do Projeto

Este projeto é um sistema simples e funcional de gestão de estoque e pedidos, desenvolvido em Python utilizando SQLite como banco de dados. Foi criado com o objetivo de aplicar conceitos fundamentais de programação, banco de dados e arquitetura de software, proporcionando uma experiência real de desenvolvimento de um mini-ERP no terminal.

O sistema conta com duas visões distintas para usuários administradores (ADM) e clientes, permitindo cadastro, autenticação, controle de produtos, criação e visualização de pedidos, tudo em uma interface de linha de comando (CLI) intuitiva.

## Funcionalidades Principais

### Para Administradores (ADM):
- Cadastro, atualização e remoção de produtos no estoque.
- Visualização detalhada dos produtos cadastrados.
- Consulta de todos os pedidos realizados, com informações completas (cliente, produto, quantidade, valor, data).
- Controle automático do estoque após realização de pedidos.

### Para Clientes:
- Visualização dos produtos disponíveis para compra.
- Realização de pedidos com verificação automática de estoque.
- Consulta do histórico de pedidos realizados.

### Geral:
- Cadastro e autenticação de usuários com definição clara de perfis (ADM ou CLIENTE).
- Armazenamento dos dados em banco SQLite local, com persistência.
- Interface limpa e funcional via terminal, com menus organizados e navegação simples.

## Tecnologias Utilizadas

- Python 3.13
- SQLite (banco de dados relacional leve e embutido)
- Bibliotecas padrão do Python (`sqlite3`, `getpass`, `os`)
- Estrutura modular com DAO para abstração do banco

## Estrutura do Projeto

├── main.py # Ponto de entrada do sistema (menu principal)
├── models
│ └── users.py # Modelos e DAO para usuários
├── menus
│ ├── admin_menu.py # Menu e lógica para usuários administradores
│ └── client_menu.py # Menu e lógica para usuários clientes
├── utils
│ └── utils.py # Funções utilitárias (clear, pause)
└── view
└── view_products.py # Visualização formatada dos produtos


## Aprendizados e Desafios

Durante o desenvolvimento, aprofundei meus conhecimentos em:

- Estruturação de projetos Python de forma modular e escalável.
- Manipulação de banco de dados SQLite com comandos SQL para CRUD.
- Implementação de padrão DAO para separar lógica de acesso a dados.
- Controle de fluxo e menus em CLI com tratamento de erros e usabilidade.
- Lógica de negócios para controle de estoque e pedidos.
- Uso de bibliotecas para segurança mínima (entrada de senha oculta).


## Como Executar

1. Clone o repositório:
git clone "https://github.com/BrunoRigoni/CliStock-ERP-Sistema-CRUD-em-Python-com-POO-e-SQLite"

2. Navegue até a pasta do projeto:
cd CliStock-ERP-Sistema-CRUD-em-Python-com-POO-e-SQLite

3. Execute o script principal:
python main.py

4. Siga as instruções no terminal para cadastrar usuários, logar e usar as funcionalidades.

---

## Contato

Bruno Henrique Vicente Calastri Rigoni  
[LinkedIn](https://www.linkedin.com/in/brunohenriquerigoni)  

---

**Este projeto é um passo importante na minha jornada para me tornar um desenvolvedor Python focado em sistemas robustos, escaláveis e com foco em experiência do usuário e segurança.**






