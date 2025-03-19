📌 Lion Hub - Rede Social Interativa no Terminal

O Lion Hub é um sistema de rede social interativa baseado em menus no terminal. Ele permite que os usuários criem contas, publiquem posts, interajam com outros usuários, enviem mensagens privadas, sigam perfis e muito mais, tudo sem a necessidade de uma interface gráfica.

⸻

🌜 Funcionalidades Implementadas

O projeto foi desenvolvido para cobrir diversas funcionalidades essenciais de uma rede social. Abaixo está um comparativo entre as funcionalidades inicialmente desejadas e o que foi implementado:

✅ Funcionalidades Concluídas:

✔ Gerenciamento de Contas de Usuário:
	•	Registro e login de usuários
	•	Atualização de nome e senha
	•	Exibição do perfil do usuário
	•	Configurações de privacidade

✔ Criação e Gerenciamento de Posts:
	•	Criar, editar e excluir posts
	•	Suporte a textos, imagens e vídeos
	•	Listagem e exibição de posts

✔ Sistema de Seguidores:
	•	Seguir e deixar de seguir usuários
	•	Aceitar ou recusar solicitações de seguidores
	•	Listar seguidores e seguidos

✔ Mensagens Privadas:
	•	Enviar e receber mensagens privadas
	•	Visualizar histórico de conversas
	•	Marcar mensagens como lidas
	•	Excluir mensagens

✔ Criação e Gerenciamento de Grupos:
	•	Criar e excluir grupos
	•	Editar informações do grupo
	•	Gerenciar privacidade do grupo

✔ Sistema de Notificações:
	•	Notificações para curtidas, comentários, novos seguidores, etc.
	•	Marcar notificações como lidas
	•	Excluir notificações

✔ Gerenciamento de Curtidas e Comentários:
	•	Curtir e descurtir posts
	•	Criar e excluir comentários em posts

✔ Criação e Gerenciamento de Eventos:
	•	Criar, editar e excluir eventos
	•	Visualizar detalhes de eventos
	•	Configurar eventos como públicos ou privados

⸻

❌ Funcionalidades Não Implementadas e Justificativas:

✖ Moderação e Filtros de Conteúdo:
	•	A moderação automática de conteúdo não foi implementada devido à ausência de um sistema avançado de análise de texto e IA. Geralmente em redes sociais, a quebra de diretrizes para casos graves ocorre de maneira manual, como houve com o X e Instagram.

⸻

🛠 Como Executar o Projeto

1️⃣ Configurar o Ambiente
	•	Certifique-se de ter o Python 3.10+ instalado
	•	Instale as dependências necessárias:

pip install -r requirements.txt



2️⃣ Configurar o Banco de Dados
	•	Certifique-se de ter o PostgreSQL instalado e rodando
	•	Crie um banco de dados chamado social_network
	•	Execute o seguinte script SQL no pgAdmin para criar as tabelas:

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    privacidade BOOLEAN DEFAULT TRUE
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    midia TEXT,
    data_criacao TIMESTAMP DEFAULT NOW()
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    autor_id INT REFERENCES users(id) ON DELETE CASCADE,
    conteudo TEXT NOT NULL,
    data_criacao TIMESTAMP DEFAULT NOW()
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES users(id) ON DELETE CASCADE,
    post_id INT REFERENCES posts(id) ON DELETE CASCADE
);

CREATE TABLE followers (
    id SERIAL PRIMARY KEY,
    seguidor_id INT REFERENCES users(id) ON DELETE CASCADE,
    seguido_id INT REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(seguidor_id, seguido_id)
);

CREATE TABLE follow_requests (
    id SERIAL PRIMARY KEY,
    seguidor_id INT REFERENCES users(id) ON DELETE CASCADE,
    seguido_id INT REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(seguidor_id, seguido_id)
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    remetente_id INT REFERENCES users(id) ON DELETE CASCADE,
    destinatario_id INT REFERENCES users(id) ON DELETE CASCADE,
    conteudo TEXT NOT NULL,
    lida BOOLEAN DEFAULT FALSE,
    data_criacao TIMESTAMP DEFAULT NOW()
);

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES users(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    objeto_id INT NOT NULL,
    lida BOOLEAN DEFAULT FALSE,
    data_criacao TIMESTAMP DEFAULT NOW()
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    owner_id INT REFERENCES users(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    privacidade BOOLEAN DEFAULT TRUE
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    owner_id INT REFERENCES users(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    data DATE NOT NULL,
    localizacao TEXT NOT NULL,
    privacidade BOOLEAN DEFAULT TRUE
);


3️⃣ Executar o Sistema
	•	Para iniciar o menu interativo, basta rodar:
  pip install psycopg2
  cd backend
  python main.py



⸻

🏢 Estrutura do Projeto

lion_hub/
️│── app/
️│   ├── models/         # Modelos das entidades (User, Post, Comment, etc.)
️│   ├── database.py     # Conexão com o banco de dados
️│   └── main.py         # Menu principal do sistema
️│── README.md           # Documentação do projeto



⸻

📚 Pilares da Programação Orientada a Objetos

🔒 Encapsulamento
	•	Os atributos das classes estão encapsulados usando atributos privados (__atributo).
	•	A classe User protege senhas armazenadas usando hashing.

📚 Herança
	•	BaseModel serve como classe base para todas as entidades do sistema.
	•	Post, Comment, Like, Message, Notification, Group e Event herdam BaseModel.

🎨 Abstração
	•	BaseModel é uma classe abstrata que define um modelo padrão para outras classes.

⸻
