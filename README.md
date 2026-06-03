# PropostaDeTermosDeUsoPorImagensCatalogadas

![Build](https://github.com/pedroarcoverde/PropostaDeTermosDeUsoPorImagensCatalogadas/actions/workflows/ci.yml/badge.svg)
![Latest Release](https://img.shields.io/github/v/release/pedroarcoverde/PropostaDeTermosDeUsoPorImagensCatalogadas)

Aplicação ASP.NET Core para testar variantes visuais de termos de uso e coletar telemetria (aceite/rejeição + tempo de leitura).

Principais arquivos
- `ConsentTelemetry.csproj`, `ConsentTelemetry.sln`
- Código: `Controllers/`, `Data/`, `Models/`, `Interfaces/`, `Views/`, `wwwroot/`

Banco de dados
- Banco local SQLite: `consentlogs.db` (arquivo no diretório do projeto).

Pré-requisitos
- .NET 10 SDK instalado: https://dotnet.microsoft.com/en-us/download

Como executar localmente
```powershell
cd "c:caminho do projeto"
dotnet restore
dotnet build
dotnet run --urls http://localhost:5000
# abrir http://localhost:5000 no navegador
```

Endpoints principais
- `POST /api/consent/log` — registra um log (JSON conforme `ConsentLogDto`).
- `GET /api/consent` — lista registros.
- `GET /api/consent/{id}` — obter registro por id.
- `GET /api/health` — health check.

UI
- `http://localhost:5000/` — página de seleção de termo (Index).
- `TermosDeUso` — páginas de termo variante A ou B (acessadas pela seleção).
- `Home/Logs` — painel com tabela dos registros.

Publicar no GitHub
- Repositório público: `PropostaDeTermosDeUsoPorImagensCatalogadas` (já criado).

Comandos úteis
```bash
# ver remotes
git remote -v

# verificar status e últimos commits
git status
git log --oneline -n 5
```

---
Arquivo atualizado pelo assistente para incluir badges e instruções rápidas.
# ConsentTelemetry

API simples para coleta de telemetria de consentimento (ex.: logs de aceite/recusa).

**Arquivo do projeto:** [ConsentTelemetry.csproj](ConsentTelemetry.csproj)
**Solução:** [ConsentTelemetry.sln](ConsentTelemetry.sln)

**Pré-requisitos**
- .NET 10 SDK instalado: https://dotnet.microsoft.com/en-us/download
- SQL Server LocalDB (opcional, o connection string atual usa LocalDB)

**Configuração**
- Ajuste a connection string em [appsettings.json](appsettings.json) se necessário.

**Comandos básicos**
```powershell
cd "c:\caminho do projeto"
dotnet restore
dotnet build
dotnet run
```

Se quiser criar a solution (se ainda não existir):
```powershell
dotnet new sln -n ConsentTelemetry
dotnet sln add ConsentTelemetry.csproj
```
## PropostaDeTermosDeUsoPorImagensCatalogadas

Aplicação ASP.NET Core para testar variantes visuais de termos de uso e coletar telemetria (aceite/rejeição + tempo de leitura).

Arquivos principais
- `ConsentTelemetry.csproj`, `ConsentTelemetry.sln`
- Código: `Controllers/`, `Data/`, `Models/`, `Interfaces/`, `Views/`, `wwwroot/`

Banco de dados
- Banco local SQLite: `consentlogs.db` (arquivo no diretório do projeto).

Pré-requisitos
- .NET 10 SDK instalado: https://dotnet.microsoft.com/en-us/download

Como executar localmente
```powershell
cd "c:caminho do projeto"
dotnet restore
dotnet build
dotnet run --urls http://localhost:5000
# abrir http://localhost:5000 no navegador
```

Endpoints principais
- `POST /api/consent/log` — registra um log (JSON conforme `ConsentLogDto`).
- `GET /api/consent` — lista registros.
- `GET /api/consent/{id}` — obter registro por id.
- `GET /api/health` — health check.

UI
- `http://localhost:5000/` — página de seleção de termo (Index).
- `TermosDeUso` — páginas de termo variante A ou B (acessadas pela seleção).
- `Home/Logs` — painel com tabela dos registros.

Observações sobre Docker
- Este repositório foi simplificado para execução local com SQLite. Removi instruções Docker porque o projeto não necessita de imagem/container para rodar localmente.

Publicar no GitHub
- Nome sugerido do repositório: `PropostaDeTermosDeUsoPorImagensCatalogadas`.

Comandos que vou executar para publicar (ou que você pode executar se preferir autenticado):
```bash
# inicializar repositório local (se ainda não existir)
git init
git add .
git commit -m "Initial: Proposta de termos de uso por imagens catalogadas"

# usar GitHub CLI (opcional) para criar repo público e enviar
# instalar gh: https://cli.github.com/
gh repo create PropostaDeTermosDeUsoPorImagensCatalogadas --public --source=. --remote=origin --push

# ou, se preferir criar manualmente no GitHub e adicionar remote:
git remote add origin https://github.com/<seu-usuario>/PropostaDeTermosDeUsoPorImagensCatalogadas.git
git branch -M main
git push -u origin main
```

Se quiser, eu posso tentar criar o repositório automaticamente usando o `gh` CLI se estiver instalado e autenticado neste ambiente. Caso contrário, posso fornecer instruções passo a passo e o comando `gh` que você pode rodar localmente.

---
Arquivo `README.md` atualizado com as instruções essenciais.
