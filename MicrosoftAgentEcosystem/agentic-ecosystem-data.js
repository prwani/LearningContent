// Microsoft Agentic AI Ecosystem — Content Data
// Schema: ECOSYSTEM_DATA[component][lifecycle][platform] = { summary, paragraphs[], references[] }
// 6 components × 10 lifecycle × 5 platforms = 300 cells

const ECOSYSTEM_DATA = {

// ╔══════════════════════════════════════════════════╗
// ║  SKILLS                                          ║
// ╚══════════════════════════════════════════════════╝
skills: {
    identity: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    source_control_cicd: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    distribution: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: {
            summary: 'Distributing Skills to Open-Source Agent Frameworks on AKS',
            paragraphs: [
                'Microsoft maintains a public skills repository at <a href="https://github.com/microsoft/skills" target="_blank" class="text-purple-600 underline">github.com/microsoft/skills</a>, which contains a <code>marketplace.json</code> manifest enabling discovery and installation of skills. Developers can install skills using the <code>npx skills add microsoft/skills --skill agent-framework-azure-ai-py</code> command. The <code>npx skills</code> CLI is modeled after npm\'s package manager paradigm and is created by Vercel as an open-source project. When a container hosting an open-source agent framework starts on AKS or App Service, it can use the <code>npx</code> command to download and install the required skills at startup, ensuring agents always have the latest skill definitions.',

                'This same pattern can be adapted for enterprise private skills repositories. By mirroring the <code>marketplace.json</code> structure on a private Azure DevOps or GitHub Enterprise repository, organizations can create an "Enterprise Private Skills Repository" with governance layers such as approval workflows, security scanning, and version pinning. The container\'s entrypoint script would reference the private repo URL, authenticate via managed identity or PAT tokens, and pull the approved skill set before the agent begins serving requests.',

                '<strong>Option 2 — Azure Artifacts:</strong> Alternatively, organizations can upload skills as Universal Packages in Azure Artifacts. This approach leverages Azure Artifacts\' built-in versioning, retention policies, and RBAC controls. The agent container\'s startup script uses <code>az artifacts universal download</code> to fetch the skills package, unpack it, and make it available to the agent runtime. This pattern integrates naturally with Azure DevOps pipelines for automated skill publishing and promotion across dev/staging/production feeds.'
            ],
            references: [
                { title: 'Microsoft Skills Repository', url: 'https://github.com/microsoft/skills' },
                { title: 'Skills CLI Documentation', url: 'https://www.npmjs.com/package/skills' },
                { title: 'Agent Skills Browser', url: 'https://microsoft.github.io/skills/' },
                { title: 'Azure Artifacts Universal Packages', url: 'https://learn.microsoft.com/en-us/azure/devops/artifacts/quickstarts/universal-packages' }
            ]
        }
    },
    deployment_hosting: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    discovery: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    observability: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    governance: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    channels: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    extensibility: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    integration: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    }
},

// ╔══════════════════════════════════════════════════╗
// ║  MCP SERVERS                                     ║
// ╚══════════════════════════════════════════════════╝
mcp_servers: {
    identity: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    source_control_cicd: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    distribution: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    deployment_hosting: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    discovery: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: {
            summary: 'MCP Server Discovery via Azure API Center for Foundry Agent Service',
            paragraphs: [
                'Azure API Center provides a centralized platform for inventorying and discovering remote Model Context Protocol (MCP) servers. When using Foundry Agent Service, organizations can register their MCP servers in API Center — including metadata such as server endpoints, supported tools, authentication requirements, and environment configurations. This creates a governed, searchable catalog that Foundry agents can query at runtime to discover which MCP tools are available. The registration process supports both manual entry through the Azure portal and automated registration via Azure API Management sync, making it straightforward to keep the registry current as new MCP servers are deployed.',

                'The private MCP registry pattern in Azure API Center is particularly powerful for enterprises running Foundry Agent Service. Instead of agents discovering tools from uncontrolled public catalogs (which creates security risks), all MCP servers go through a vetting and registration process before being made discoverable. The API Center enforces enterprise authentication (OAuth2 with Entra ID) and can route requests through Azure API Management gateways for additional policy enforcement, auditing, and network security. This ensures that Foundry agents only interact with approved, vetted MCP servers — dramatically reducing the attack surface and eliminating shadow IT risks.',

                'From a practical integration standpoint, Foundry Agent Service can leverage the API Center\'s REST APIs to dynamically query the MCP registry during agent initialization or at runtime. The agent can enumerate available tools, inspect their schemas (via the MCP protocol\'s JSON-RPC 2.0 transport), and selectively connect to the servers that match the current task requirements. This enables a "just-in-time tool discovery" pattern where agents are not hardcoded to specific MCP servers but instead discover them based on context, capability tags, and organizational policies defined in the API Center.'
            ],
            references: [
                { title: 'Inventory and Discover MCP Servers in API Center', url: 'https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server' },
                { title: 'Build Your Private MCP Registry with Azure API Center', url: 'https://techcommunity.microsoft.com/blog/integrationsonazureblog/build-secure-launch-your-private-mcp-registry-with-azure-api-center-/4438016' },
                { title: 'Build and Register MCP Server in Foundry', url: 'https://learn.microsoft.com/en-us/azure/ai-foundry/mcp/build-your-own-mcp-server' },
                { title: 'MCP Registry Demo (Azure Samples)', url: 'https://github.com/Azure-Samples/mcp-registry' }
            ]
        },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    observability: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    governance: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    channels: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    extensibility: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    integration: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    }
},

// ╔══════════════════════════════════════════════════╗
// ║  AGENTS                                          ║
// ╚══════════════════════════════════════════════════╝
agents: {
    identity: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    source_control_cicd: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    distribution: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    deployment_hosting: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    discovery: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: {
            summary: 'Agent Discovery via Azure API Center Agent Registry',
            paragraphs: [
                'Azure API Center provides a centralized platform for discovering, registering, and managing AI agents built on Foundry Agent Service. The agent registry feature supports both first-party agents (built within the organization) and third-party agents, creating a unified catalog where stakeholders can browse agent capabilities, understand their interfaces, and determine the right agent for a given task. Each registered agent includes customizable metadata — such as supported protocols (MCP, A2A), authentication methods, capability descriptions, SLA tiers, and contact information — which dramatically improves discoverability and reduces the overhead of onboarding new agents into enterprise workflows.',

                'For organizations running multiple Foundry Agent Service instances, the API Center agent registry becomes the "phone book" for agent-to-agent interactions. When Agent A needs to delegate a sub-task to another agent, it queries the API Center to discover agents that match the required capabilities, checks their availability and authentication requirements, and establishes a connection using the registered endpoint. This pattern supports the Agent-to-Agent (A2A) protocol that Google and Microsoft jointly developed, enabling cross-platform agent collaboration. The API Center integrates with Azure API Management for private endpoints, ensuring that inter-agent communication remains within the organization\'s network boundary.',

                'The discovery experience extends beyond programmatic access. The API Center portal provides a browsable, searchable UI where business users, architects, and developers can explore the agent catalog without writing code. Teams can tag agents with business domains (e.g., "Finance," "HR," "Customer Support"), compliance classifications, and maturity levels. This metadata-driven approach ensures that as the number of agents grows from tens to hundreds, the organization maintains a clear understanding of its agent landscape and can enforce governance policies at the registry level.'
            ],
            references: [
                { title: 'Agent Registry in Azure API Center', url: 'https://learn.microsoft.com/en-us/azure/api-center/agent-to-agent-overview' },
                { title: 'Empowering Multi-Agent Apps with A2A Protocol', url: 'https://www.microsoft.com/en-us/microsoft-cloud/blog/2025/05/07/empowering-multi-agent-apps-with-the-open-agent2agent-a2a-protocol/' },
                { title: 'Azure API Center Documentation', url: 'https://learn.microsoft.com/en-us/azure/api-center/' },
                { title: 'Google A2A Protocol Announcement', url: 'https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/' }
            ]
        },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    observability: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    governance: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    channels: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    extensibility: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    integration: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    }
},

// ╔══════════════════════════════════════════════════╗
// ║  MODELS                                          ║
// ╚══════════════════════════════════════════════════╝
models: {
    identity: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    source_control_cicd: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    distribution: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    deployment_hosting: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    discovery: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    observability: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    governance: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    channels: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    extensibility: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    integration: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    }
},

// ╔══════════════════════════════════════════════════╗
// ║  TOOLS                                           ║
// ╚══════════════════════════════════════════════════╝
tools: {
    identity: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    source_control_cicd: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    distribution: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    deployment_hosting: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    discovery: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    observability: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    governance: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    channels: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    extensibility: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    integration: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    }
},

// ╔══════════════════════════════════════════════════╗
// ║  PLUGINS                                         ║
// ╚══════════════════════════════════════════════════╝
plugins: {
    identity: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    source_control_cicd: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    distribution: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    deployment_hosting: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    discovery: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    observability: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    governance: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    channels: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    extensibility: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    },
    integration: {
        m365_agent_builder: { summary: '', paragraphs: [], references: [] },
        copilot_studio: { summary: '', paragraphs: [], references: [] },
        foundry_agent_service: { summary: '', paragraphs: [], references: [] },
        foundry_self_hosted: { summary: '', paragraphs: [], references: [] },
        opensource_aks: { summary: '', paragraphs: [], references: [] }
    }
}

};
