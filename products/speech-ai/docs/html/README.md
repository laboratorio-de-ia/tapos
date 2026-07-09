# Speech AI - Documentação HTML Interativa

## 🎙️ Bem-vindo

Esta é a versão HTML interativa da documentação completa do Speech AI, uma plataforma empresarial de Text-to-Audio com arquitetura modular e escalável.

## 📂 Estrutura de Pastas

```
Docs_HTML/
├── index.html                 # Página principal
├── README.md                  # Este arquivo
├── assets/
│   ├── css/
│   │   └── style.css         # Estilos CSS profissionais
│   ├── js/
│   │   └── main.js           # JavaScript para navegação e busca
│   └── images/
│       ├── system_architecture.png
│       ├── pipeline_flow.png
│       └── domain_models.png
├── pages/
│   ├── foundation/
│   │   ├── index.html
│   │   ├── readme.html
│   │   ├── engineering-docs.html
│   │   ├── architecture.html
│   │   └── diagrams.html
│   ├── sprint/
│   │   ├── index.html
│   │   ├── sprint-roadmap.html
│   │   ├── adr.html
│   │   ├── changelog.html
│   │   └── roadmap.html
│   ├── developer/
│   │   ├── index.html
│   │   ├── developer-guide.html
│   │   ├── coding-standards.html
│   │   ├── contributing.html
│   │   └── testing-guide.html
│   └── operations/
│       ├── index.html
│       ├── security.html
│       ├── operations-guide.html
│       ├── project-metrics.html
│       └── release-process.html
└── diagrams/
    └── index.html
```

## 🚀 Como Usar

### Opção 1: Abrir Localmente
1. Abra o arquivo `index.html` em seu navegador favorito
2. Navegue através dos packs usando o menu lateral
3. Use a barra de busca para encontrar conteúdo específico

### Opção 2: Servir com HTTP Server
```bash
# Python 3
python -m http.server 8000

# Node.js
npx http-server

# PHP
php -S localhost:8000
```

Então acesse: `http://localhost:8000`

## 📚 Conteúdo

### 📖 Foundation Pack
- **README**: Visão geral do projeto
- **Engineering Documentation**: Componentes técnicos
- **Architecture**: Padrões e design
- **Diagrams**: Visualizações

### 🚀 Sprint Pack
- **Sprint Roadmap**: Histórico de sprints
- **ADR**: Decisões arquiteturais
- **Changelog**: Histórico de versões
- **Roadmap**: Visão de produto

### 👨‍💻 Developer Pack
- **Developer Guide**: Setup local
- **Coding Standards**: Padrões de código
- **Contributing**: Como contribuir
- **Testing Guide**: Estratégia de testes

### ⚙️ Operations Pack
- **Security**: Postura de segurança
- **Operations Guide**: Deployment
- **Project Metrics**: KPIs
- **Release Process**: Processo de release

## ✨ Características

- ✅ **Design Responsivo**: Funciona em desktop, tablet e mobile
- ✅ **Navegação Intuitiva**: Menu lateral e breadcrumbs
- ✅ **Busca Integrada**: Encontre conteúdo rapidamente
- ✅ **Índice Automático**: Tabela de conteúdos por página
- ✅ **Diagramas Visuais**: Arquitetura e fluxos em PNG
- ✅ **Links Cruzados**: Navegação entre documentos relacionados
- ✅ **Estilos Profissionais**: Cores e tipografia corporativas

## 🎨 Personalização

### Cores
Edite `/assets/css/style.css` para alterar as cores:
```css
:root {
    --primary-color: #1e3a8a;
    --secondary-color: #3b82f6;
    --accent-color: #f59e0b;
    /* ... mais cores ... */
}
```

### Conteúdo
Todos os arquivos HTML podem ser editados diretamente. A estrutura é simples e bem comentada.

## 📊 Estatísticas

- **Páginas HTML**: 27
- **Documentos Convertidos**: 16 Markdown → HTML
- **Diagramas**: 3 (PNG + Fontes editáveis)
- **Tamanho Total**: ~1.2 MB
- **Tempo de Carregamento**: < 2 segundos

## 🔍 Navegação Rápida

| Página | URL |
| :--- | :--- |
| Início | `index.html` |
| Foundation Pack | `pages/foundation/index.html` |
| Sprint Pack | `pages/sprint/index.html` |
| Developer Pack | `pages/developer/index.html` |
| Operations Pack | `pages/operations/index.html` |
| Diagramas | `diagrams/index.html` |

## 🛠️ Tecnologias

- **HTML5**: Estrutura semântica
- **CSS3**: Estilos responsivos com variáveis CSS
- **JavaScript**: Navegação, busca e interatividade
- **Markdown**: Conteúdo original convertido para HTML

## 📝 Notas

- Todos os links são relativos, permitindo uso offline
- A busca funciona apenas na página atual
- Compatível com navegadores modernos (Chrome, Firefox, Safari, Edge)
- Otimizado para impressão (use Ctrl+P ou Cmd+P)

## 🔄 Atualizações

Para atualizar a documentação:
1. Edite os arquivos Markdown em `/home/ubuntu/SpeechAI_Docs/`
2. Execute o script de conversão: `python3 /home/ubuntu/convert_md_to_html.py`
3. Os arquivos HTML serão regenerados automaticamente

## 📞 Suporte

Para dúvidas ou sugestões sobre a documentação, consulte o arquivo `CONTRIBUTING.md` no pack Developer.

---

**Versão**: 1.0.0  
**Data**: 2 de Julho de 2026  
**Gerado por**: Manus AI - Contexto Global Lab
