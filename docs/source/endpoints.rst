Endpoints
=========

Abaixo estão listados os endpoints da API e seus detalhes.

===================
Criar usuário admin
===================

O primeiro usuário admin deverá ser criado através de linha de comando, uma vez que apenas admins podem criar outros admins.

Para realizar a criação do primeiro usuário, utilizar o seguinte comando:
::

	docker-compose run app sh -c "python manage.py createsuperuser"

Após isso, qualquer usuário admin é capaz de criar outros usuários admin.

--------------------
Endereço do endpoint
--------------------

Para acessar esse endpoint, utilizar o seguinte endereço: api/user/create-superuser

-----------------------
Informações necessárias
-----------------------

Abaixo as informações necessárias para se criar um usuário admin

======== ===========================
Campo    Especificações
======== ===========================
Email    Deve ser um email válido
Password Mínimo 8 caracteres
Name     Obrigatório o preenchimento
======== ===========================

=============
Criar cliente
=============

Esse endpoint permite criar novos clientes. É um endpoint aberto, ou seja, qualquer usuário pode criar sua conta.

--------------------
Endereço do endpoint
--------------------

Para acessar esse endpoint, utilizar o seguinte endereço: api/user/create

-----------------------
Informações necessárias
-----------------------

Abaixo as informações necessárias para se criar um usuário

======== ===========================
Campo    Especificações
======== ===========================
Email    Deve ser um email válido
Password Mínimo 8 caracteres
Name     Obrigatório o preenchimento
======== ===========================

=================
Atualizar cliente
=================

Esse endpoint permite atualizar os dados do cliente autenticado.

--------------------
Endereço do endpoint
--------------------

Para acessar esse endpoint, utilizar o seguinte endereço: api/user/me

-----------------------
Informações necessárias
-----------------------

Não é possível atualizar o email, portanto, apenas os campos abaixos podem ser modificados.

======== ===========================
Campo    Especificações
======== ===========================
Password Mínimo 8 caracteres
Name     Nome do cliente
======== ===========================

===================
Visualizar clientes
===================

Esse endpoint permite visualizar todos os clientes cadastrados. Apenas usuários Admin têm acesso a esse endpoint.

--------------------
Endereço do endpoint
--------------------

Para acessar esse endpoint, utilizar o seguinte endereço: api/user/me

-----------------------
Informações necessárias
-----------------------

Não é possível atualizar o email, portanto, apenas os campos abaixos podem ser modificados.

======== ===========================
Campo    Especificações
======== ===========================
Password Mínimo 8 caracteres
Name     Nome do cliente
======== ===========================

================
Remover clientes
================

Esse endpoint permite remover um cliente. Usuários admin podem remover qualquer usuário, inclusive o próprio. Usuários comuns podem remover apenas o próprio usuário.

--------------------
Endereço do endpoint
--------------------

Para acessar esse endpoint, utilizar o seguinte endereço: api/user/remove

-----------------------
Informações necessárias
-----------------------

É possível remover o próprio usuário, fazendo uma reuqisição para o endpoint sem nenhum parâmetro. 

Para usuários admin, que desejam remover outros usuários, abaixo estão os parâmetros

======== ===================================
Campo    Especificações
======== ===================================
user_id  Id do usuário que se deseja remover
======== ===================================

============================
Cadastrar lista de favoritos
============================

Esse endpoint permite cadastar produtos em uma lista de favoritos. O usuário só pode adicionar produtos na própria lista.

--------------------
Endereço do endpoint
--------------------

Para acessar esse endpoint, utilizar o seguinte endereço: api/wishlist/wishlist

-----------------------
Informações necessárias
-----------------------

Para cadastrar um produto, são necessárias as informações abaixo

======== ========================================================
Campo    Especificações
======== ========================================================
product  Id do produto no formato UUID (deve ser um UUID válido*)
======== ========================================================

* para ser considerado um UUID válido, o produto deve existir em uma API externa. A documentação dessa API encontra-se `nesse link <https://gist.github.com/Bgouveia/9e043a3eba439489a35e70d1b5ea08ec>`_

=============================
Visualizar lista de favoritos
=============================

Esse endpoint permite visualizar a lista de favoritos. O usuário só pode avisualizar a própria lista.

--------------------
Endereço do endpoint
--------------------

Para acessar esse endpoint, utilizar o seguinte endereço: api/wishlist/wishlist

------------------------
Informações apresentadas
------------------------

A lista de produtos apresenta as informações abaixo

======== ========================================================
Campo    Especificações
======== ========================================================
id       Id do item da lista
client   Id do cliente
product  Id do produto
======== ========================================================

=================================================
Visualizar detalhes de item da lista de favoritos
=================================================

Esse endpoint permite visualizar os detalhes de um item da lista de favoritos. Usuários só podem visualizar ítens da própria lista.

--------------------
Endereço do endpoint
--------------------

Para acessar esse endpoint, utilizar o seguinte endereço: api/wishlist/wishlist/<ID-ITEM>

------------------------
Informações apresentadas
------------------------

Os detalhes apresentados são os abaixo

======== ========================================================
Campo    Especificações
======== ========================================================
id       Id do item da lista
client   Informações do cliente conforme tabela abaixo
product  Informações do produto conforme tabela abaixo
======== ========================================================

Dados do cliente

============ ========================================================
Campo        Especificações
============ ========================================================
id           ID do cliente
email        Email do cliente
name         Nome do cliente
============ ========================================================

Dados do produto

============ ========================================================
Campo        Especificações
============ ========================================================
id           ID do produto no formato UUID
price        Preço do produto
image        URL da imagem
brand        Marca
title        Nome do produto
review_score Média dos reviews para este produto (não obrigatório)
============ ========================================================

=====
Login
=====

Para acessar esse endpoint, utilizar o seguinte endereço: api/token

-----------------------
Informações necessárias
-----------------------

Abaixo as informações necessárias para realizar Login

======== ================
Campo    Especificações
======== ================
Email    Email cadastrado
Password Senha cadastrada
======== ================

-------
Retorno
-------

Como retorno de um login, o endpoint envia dois tokens

======== ================================================================
Token    Informações
======== ================================================================
Refresh  Token utilizado para gerar um novo token quando o Access expirar
Access   Token para garantir login (expirável)
======== ================================================================

=============
Refresh Token
=============

Para acessar esse endpoint, utilizar o seguinte endereço: api/token/refresh

É necessário então informar o token de refresh para obter um novo token access.