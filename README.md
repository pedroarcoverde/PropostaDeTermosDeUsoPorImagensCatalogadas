# Proposta de Representação Visual de Termos de Compromisso

## 📖 Descrição
Este projeto é um artefato de software desenvolvido como parte de um Trabalho de Conclusão de Curso (TCC) no curso de Engenharia da Computação da Universidade de Brasília (UnB). 

O objetivo principal é mitigar a ineficácia dos tradicionais Termos de Uso no ambiente digital — onde a alta densidade textual atua como uma barreira ao consentimento informado — através da aplicação de *Visual Law*, conceitos de Psicologia Cognitiva e Interação Humano-Computador (IHC). A solução propõe uma iconografia padronizada para representar grupos de cláusulas jurídicas, reduzindo a carga cognitiva do usuário e promovendo maior transparência informacional.

## 🏗️ Arquitetura da Solução
O sistema foi estruturado em quatro camadas integradas, garantindo coerência entre a interface (front-end) e as exigências legais (LGPD/GDPR):

1.  **Camada 1 — Catálogo e Taxonomia:** Registro de iconografia versionado que define categorias semânticas para os termos.
2.  **Camada 2 — API de Apresentação (Consent UI Service):** Interface responsiva que utiliza ícones e rótulos claros, implementando avisos *just-in-time*.
3.  **Camada 3 — Mecanismo de Consentimento:** *Consent Ledger* que gerencia a granularidade (opt-in/opt-out) e a retenção de dados.
4.  **Camada 4 — Governança e Auditoria:** Painel dedicado ao DPO (Encarregado de Proteção de Dados) para monitoramento de métricas e trilhas de auditoria.

## 🚀 Funcionalidades
- **Iconografia Semântica:** Mapeamento visual intuitivo para cláusulas complexas.
- **Transparência Informacional:** Redução da carga cognitiva via *Nudges* visuais.
- **Auditoria Facilitada:** Painel de controle para consulta do histórico de consentimentos.
- **Padronização:** Alinhamento com frameworks de privacidade (ISO 29100, NIST Privacy Framework).

## 🛠️ Tecnologias Utilizadas
- **Linguagens:** HTML5, CSS3, JavaScript (ES6+).
- **Estilização:** Tailwind CSS (via CDN).
- **Ícones:** Lucide Icons (via CDN).
- **Gerenciamento de Estado:** Manipulação via *Local Storage* para persistência dos registros de consentimento.

## ⚙️ Como Executar
1. Clone este repositório:
   ```bash
   git clone [https://github.com/pedroarcoverde/PropostaDeTermosDeUsoPorImagensCatalogadas.git](https://github.com/pedroarcoverde/PropostaDeTermosDeUsoPorImagensCatalogadas.git)
   ```
2. Acesse a pasta do projeto.

3. Abra o arquivo index.html (ou o arquivo principal de interface) no seu navegador.

4. Para simular o fluxo de consentimento, interaja com os componentes de interface disponíveis.

## 📚 Referências Teóricas
Este projeto fundamenta-se nos pilares de:
- Visual Law e Legal Design (Hagan, 2020).
- Teoria da Carga Cognitiva (Sweller, 2011).
- Privacidade por Design (Privacy by Design).
- Normativas: LGPD (Brasil), GDPR (União Europeia) e ISO/IEC 29100.

## 📝 Licença
Este projeto é desenvolvido para fins acadêmicos e educacionais.

### Autor: Pedro Arcoverde
### Instituição: Engenharia da Computação - UnB


**Link para o Protótipo:** https://propostatermosdeuso.vercel.app