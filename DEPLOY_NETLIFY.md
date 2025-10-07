# 🚀 Deploy no Netlify - Projeto Flask

Este projeto está **TOTALMENTE CONFIGURADO** para deploy automático no Netlify.

## ✅ Arquivos de Configuração Preparados

- ✅ `requirements.txt` - Dependências Python
- ✅ `runtime.txt` - Versão do Python (3.11)
- ✅ `netlify.toml` - Configurações de build e deploy
- ✅ `_redirects` - Regras de redirecionamento
- ✅ `netlify/functions/app.py` - Função serverless
- ✅ `app.py` - Aplicação Flask configurada para produção
- ✅ `.gitignore` - Arquivos ignorados pelo Git
- ✅ **Repositório Git atualizado e sincronizado**

## 🎯 Passos para Deploy (PRONTO PARA EXECUTAR)

### Via Git (Recomendado) - DEPLOY AUTOMÁTICO

1. **Acesse [Netlify](https://netlify.com)**
2. **Faça login ou crie uma conta**
3. **Clique em "New site from Git"**
4. **Conecte seu repositório GitHub**
5. **Selecione o repositório: `proposta-premium-`**
6. **As configurações serão detectadas automaticamente pelo `netlify.toml`**
7. **Clique em "Deploy site"**

### ⚡ Deploy Instantâneo
- **Build Command**: Configurado automaticamente
- **Publish Directory**: Configurado automaticamente  
- **Functions Directory**: `netlify/functions`
- **Python Version**: 3.11

### Opção 2: Via Drag & Drop

1. **Crie um arquivo ZIP** do projeto (excluindo `venv/` e `__pycache__/`)
2. **No Netlify**:
   - Acesse [netlify.com](https://netlify.com)
   - Arraste e solte o arquivo ZIP na área de deploy

## 🔧 Configurações Importantes

### Variáveis de Ambiente
Se seu projeto usar variáveis de ambiente, configure-as no Netlify:
- Vá em Site settings > Environment variables
- Adicione as variáveis necessárias (ex: `SESSION_SECRET`)

### Domínio Personalizado
- Vá em Site settings > Domain management
- Adicione seu domínio personalizado

## 🧪 Testando o Deploy

Após o deploy, teste todas as rotas:
- `/` (página inicial)
- `/sobre`
- `/cases`
- `/metodologia`
- `/servicos`
- `/investimento`
- `/faq`

## 📝 Estrutura do Projeto

```
projeto/
├── netlify/
│   └── functions/
│       └── app.py          # Função serverless
├── static/                 # Arquivos estáticos
├── templates/              # Templates HTML
├── app.py                  # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── runtime.txt            # Versão Python
├── netlify.toml           # Configurações Netlify
└── _redirects             # Redirecionamentos
```

## 🎉 Pronto!

Seu projeto está totalmente preparado para o Netlify. O deploy deve funcionar automaticamente com as configurações criadas.

### Suporte
Se encontrar algum problema, verifique:
1. Logs de build no Netlify
2. Se todas as dependências estão no `requirements.txt`
3. Se as rotas estão funcionando localmente