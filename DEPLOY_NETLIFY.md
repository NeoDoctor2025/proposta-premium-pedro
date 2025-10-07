# Deploy no Netlify - Instruções

## ✅ Projeto Preparado para Deploy

Seu projeto Flask já está configurado para deploy no Netlify! Todos os arquivos necessários foram criados e configurados.

## 📁 Arquivos de Configuração Criados

- ✅ `requirements.txt` - Dependências do Python
- ✅ `runtime.txt` - Versão do Python (3.11)
- ✅ `netlify.toml` - Configurações de build do Netlify
- ✅ `_redirects` - Redirecionamentos para a função serverless
- ✅ `netlify/functions/app.py` - Função serverless para Flask
- ✅ `app.py` - Ajustado para produção

## 🚀 Como Fazer o Deploy

### Opção 1: Via Git (Recomendado)

1. **Inicialize um repositório Git** (se ainda não tiver):
   ```bash
   git init
   git add .
   git commit -m "Preparar projeto para deploy no Netlify"
   ```

2. **Crie um repositório no GitHub/GitLab** e faça push:
   ```bash
   git remote add origin https://github.com/seu-usuario/seu-repositorio.git
   git push -u origin main
   ```

3. **No Netlify**:
   - Acesse [netlify.com](https://netlify.com)
   - Clique em "New site from Git"
   - Conecte seu repositório
   - O Netlify detectará automaticamente as configurações do `netlify.toml`
   - Clique em "Deploy site"

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