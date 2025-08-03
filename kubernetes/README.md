# ia-general-chatbot-api - Kubernetes Resources

Este pasta contém o todos os resources do kubernetes relacionados ao arquétipo de aplicações de agentes, a base para todas as aplicações de agentes que será construída.

## Estrutura Geral

O arquivo YAML define variáveis e configurações para serem utilizadas nos templates do Helm, facilitando o deployment e a gestão do microserviço no Kubernetes.

---

## Principais Campos e Explicações

### 1. Informações Básicas

- **nameOverride / fullnameOverride:** Permite sobrescrever o nome padrão do microserviço.
- **replicaCount:** Quantidade de réplicas do pod.

### 2. Imagem Docker

- **image.repository / image.tag:** Especifica o repositório e a tag da imagem Docker. Estes valores podem ser reescritos pela esteira de CI/CD.
- **imagePullSecrets:** Lista de segredos Kubernetes usados para puxar imagens Docker privadas. Devem ser criados previamente no namespace via `kubectl create secret`.

### 3. Comandos e Argumentos

- **command:** Comando que o contêiner executa ao iniciar. Caso não seja especificado, utiliza o comando padrão da imagem Docker.
- **args:** Permite definir argumentos para o comando do contêiner, útil para depuração, como manter o contêiner em loop infinito.

### 4. Portas

- **ports:** Define as portas de rede expostas pelo contêiner, incluindo seu nome, número e protocolo.

### 5. Probes de Saúde

- **livenessProbe:** Sonda que verifica se o aplicativo está rodando. Usa `httpGet` em um caminho e porta definidos, com diversos parâmetros de tempo e tentativas.
- **readinessProbe:** Sonda que verifica se o aplicativo está pronto para receber tráfego. Configuração semelhante à livenessProbe.

### 6. Recursos

- **resources:** Define limites e requisições de CPU e memória para o contêiner, garantindo controle de uso de recursos.

### 7. Configurações de Rede

- **hostAliases:** Permite adicionar entradas ao arquivo `/etc/hosts` do pod, útil para resolver nomes de host específicos.
- **ciliumNetworkPolicy:** Configura políticas de ingress e egress usando Cilium para controle de tráfego de rede.

### 8. Política de Reinício

- **restartPolicy:** Define a política de reinício do contêiner (`Always`, `OnFailure`, `Never`).

### 9. Conta de Serviço

- **serviceAccount:** Permite criar e configurar uma conta de serviço Kubernetes para o pod, incluindo anotações e nome customizado.

### 10. Anotações e Segurança

- **podAnnotations:** Adiciona anotações ao pod.
- **podSecurityContext / securityContext:** Define configurações de segurança para o pod e o contêiner, como IDs de usuário/grupo e permissões.

### 11. Serviço Kubernetes

- **service:** Configura o serviço Kubernetes, incluindo tipo (`ClusterIP`, `NodePort`, etc.) e portas de exposição.

### 12. Rotas Externas e Internas

- **externalRoute / internalRoute:** Configura rotas externas e internas para expor o microserviço, incluindo integração com Gateway API e Envoy Gateway, autenticação JWT, políticas de retry, rate limit, circuit breaker e regras HTTP.

### 13. Autoscaling

- **autoscaling:** Configura o Horizontal Pod Autoscaler (HPA) do Kubernetes, definindo ativação, número mínimo/máximo de réplicas e metas de utilização de CPU/memória.

### 14. Node Selector, Tolerations e Affinity

- **nodeSelector:** Define rótulos de nó para agendamento do pod.
- **tolerations:** Define tolerâncias para agendamento em nós específicos.
- **affinity:** Define afinidade de nó/pod para influenciar o agendamento.

### 15. ConfigMap

- **configMap:** Permite definir pares chave-valor para serem usados como variáveis de ambiente ou arquivos pelo pod.

### 16. Secrets

- **secret:** Permite definir segredos para serem usados como variáveis de ambiente ou arquivos pelo pod. Exemplo de uso para integração com Cloud Secret.

### 17. External Secrets

- **externalSecrets:** Permite integração com provedores externos de secrets, definindo nome, intervalo de atualização e mapeamento de chaves remotas.
