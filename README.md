# Social Network

Este projeto é uma simulação de uma rede social onde os usuários podem:

- Criar contas e fazer login.
- Criar, editar e excluir posts (com suporte para imagem e vídeo).
- Curtir e comentar posts.
- Criar eventos e convidar participantes.
- Criar e gerenciar grupos.
- Seguir outros usuários e enviar mensagens.
- Receber notificações sobre interações (curtidas, comentários, solicitações de seguir, etc).

O projeto foi estruturado de forma modular, dividindo o código em:

- **models**: Definição das classes e seus atributos/métodos.
- **controllers**: Regras de negócio e manipulação dos modelos.
- **views**: Interface interativa (menus) para o usuário.
- **storage.py**: Armazenamento simples utilizando listas globais.
- **tests**: Suíte de testes automatizados utilizando pytest para validar as funcionalidades.

---
### Requisitos

- Python 3.7 ou superior.

## Tutorial de Como Executar
- vá ao diretório principal do arquivo
- rode main.py
- divirta-se


# Descrição das Classes

## 1. Classe User (em `models/user.py`)

### Atributos:
- **`_name`**: Nome do usuário.
- **`_email`**: Email do usuário.
- **`_password`**: Senha do usuário.
- **`_id`**: Identificador único do usuário (atribuído automaticamente com base na quantidade de usuários cadastrados).
- **`_notifications`**: Lista de notificações recebidas pelo usuário.
- **`_followingList`**: Lista de usuários que este usuário segue.
- **`_followersList`**: Lista de usuários que seguem este usuário.
- **`_privacity`**: Booleano que indica se o perfil é privado (`True`) ou público (`False`).
- **`_active`**: Booleano que indica se a conta está ativa (`True`) ou desativada (`False`).

### Métodos:
- **`__init__(self, name, email, password, privacity)`**:  
  Inicializa os atributos do usuário.
- **`__str__(self)`**:  
  Retorna uma string representativa do usuário (ex.: "Nome - Email").
- **`getName(self)` / `setName(self, name)`**:  
  Obtém e atualiza o nome do usuário.
- **`getEmail(self)` / `setEmail(self, email)`**:  
  Obtém e atualiza o email do usuário.
- **`getPassword(self)` / `setPassword(self, password)`**:  
  Obtém e atualiza a senha.
- **`getId(self)`**:  
  Retorna o identificador único do usuário.
- **`isActive(self)`**:  
  Retorna `True` se a conta estiver ativa; caso contrário, `False`.
- **`addNotification(self, notification)`**:  
  Adiciona uma notificação à lista.
- **`getNotifications(self)`**:  
  Retorna a lista de notificações.
- **`follow(self, other_user)`**:  
  Adiciona outro usuário à lista de seguidos e atualiza a lista de seguidores do outro.
- **`getFollowingList(self)` / `getFollowersList(self)`**:  
  Retorna as listas de usuários seguidos e seguidores.
- **`deleteAccount(self)`**:  
  Desativa a conta do usuário e limpa os dados associados.

---

## 2. Classe Post (em `models/post.py`)

### Atributos:
- **`_title`**: Título do post.
- **`_content`**: Conteúdo do post.
- **`_author`**: Usuário que criou o post.
- **`_likes`**: Número de curtidas que o post recebeu.
- **`_comments`**: Lista de comentários do post.
- **`_id`**: Identificador único do post (atribuído automaticamente).
- **`_image`**: URL da imagem associada ao post (opcional).
- **`_video`**: URL do vídeo associado ao post (opcional).

### Métodos:
- **`__init__(self, title, content, author)`**:  
  Inicializa o post com título, conteúdo e autor.
- **`getId(self)`**:  
  Retorna o identificador único do post.
- **`getTitle(self)` / `setTitle(self, title)`**:  
  Obtém e atualiza o título do post.
- **`getContent(self)` / `setContent(self, content)`**:  
  Obtém e atualiza o conteúdo do post.
- **`getAuthor(self)`**:  
  Retorna o autor do post.
- **`getLikes(self)` / `like(self)`**:  
  Obtém o número de curtidas e incrementa a contagem de curtidas.
- **`getComments(self)` / `addComment(self, comment)`**:  
  Obtém a lista de comentários e adiciona um novo comentário.
- **`setImage(self, image_url)` / `getImage(self)`**:  
  Define e obtém a URL da imagem.
- **`setVideo(self, video_url)` / `getVideo(self)`**:  
  Define e obtém a URL do vídeo.
- **`__str__(self)`**:  
  Retorna uma string representativa do post, incluindo autor, título, conteúdo e número de curtidas.

---

## 3. Classe Event (em `models/event.py`)

### Atributos:
- **`_event_name`**: Nome do evento.
- **`_event_date`**: Data do evento.
- **`_event_location`**: Local onde o evento ocorrerá.
- **`_event_description`**: Descrição do evento.
- **`_participants`**: Lista de participantes inscritos no evento.
- **`_id`**: Identificador único do evento (atribuído automaticamente).

### Métodos:
- **`__init__(self, event_name, event_date, event_location, event_description)`**:  
  Inicializa o evento com os dados fornecidos.
- **`__str__(self)`**:  
  Retorna uma string com os detalhes do evento (nome, data, local e descrição).
- **`getId(self)`**:  
  Retorna o identificador único do evento.
- **`getEventName(self)`**:  
  Retorna o nome do evento.
- **`getEventDate(self)`**:  
  Retorna a data do evento.
- **`getParticipants(self)`**:  
  Retorna a lista de participantes.
- **`addParticipant(self, user)`**:  
  Adiciona um usuário à lista de participantes, se ele ainda não estiver inscrito.

---

## 4. Classe Group (em `models/group.py`)

### Atributos:
- **`_name`**: Nome do grupo.
- **`_description`**: Descrição do grupo.
- **`_founder`**: Usuário que fundou o grupo.
- **`_members`**: Lista de membros do grupo (inicia com o fundador).
- **`_posts`**: Lista de posts compartilhados no grupo.
- **`_messages`**: Lista de mensagens trocadas no grupo.

### Métodos:
- **`__init__(self, name, description, founder)`**:  
  Inicializa o grupo, adicionando o fundador como primeiro membro.
- **`__str__(self)`**:  
  Retorna uma string representativa do grupo (ex.: "Nome do Grupo - X Participantes").
- **`getName(self)`**:  
  Retorna o nome do grupo.
- **`getDescription(self)`**:  
  Retorna a descrição do grupo.
- **`getFounder(self)`**:  
  Retorna o usuário fundador do grupo.
- **`getMembers(self)`**:  
  Retorna a lista de membros do grupo.
- **`addMember(self, member)`**:  
  Adiciona um novo membro ao grupo, caso ele não esteja presente.
- **`removeMember(self, member)`**:  
  Remove um membro do grupo, desde que ele não seja o fundador.
