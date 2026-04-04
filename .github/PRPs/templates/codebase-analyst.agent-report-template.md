## Analysis: [Component/Feature Name]

### Overview
[2-3 sentence summary of how it works]

### Entry Points
| Location | Purpose |
|---|---|
| `path/to/file.ts:45` | Main handler for X |
| `path/to/other.ts:12` | Called by Y when Z |

### Implementation Flow

#### 1. [First Stage] (`path/file.ts:15-32`)
- What happens at line 15
- Data transformation at line 23
- Outcome at line 32

#### 2. [Second Stage] (`path/other.ts:8-45`)
- Processing logic at line 10
- State change at line 28
- External call at line 40

### Data Flow

```text
[input] → file.ts:45 → other.ts:12 → service.ts:30 → [output]
```

### Patterns Found
| Pattern | Location | Usage |
|---|---|---|
| Repository | `stores/data.ts:10-50` | Data access abstraction |
| Factory | `factories/builder.ts:5` | Creates X instances |

### Configuration
| Setting | Location | Purpose |
|---|---|---|
| `API_KEY` | `config/env.ts:12` | External service auth |
| `RETRY_MAX` | `config/settings.ts:8` | Retry limit for failures |

### Error Handling
| Error Type | Location | Behavior |
|---|---|---|
| ValidationError | `handlers/input.ts:28` | Returns 400, logs warning |
| NetworkError | `services/api.ts:52` | Triggers retry queue |
