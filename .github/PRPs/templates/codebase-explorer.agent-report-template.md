## Exploration: [Feature/Topic]

### Overview
[2-3 sentence summary of what was found and where]

### File Locations

#### Implementation Files
| File | Purpose |
|------|---------|
| `src/services/feature.ts` | Main service logic |
| `src/handlers/feature-handler.ts` | Request handling |

#### Test Files
| File | Purpose |
|------|---------|
| `src/services/__tests__/feature.test.ts` | Service unit tests |
| `e2e/feature.spec.ts` | End-to-end tests |

#### Configuration
| File | Purpose |
|------|---------|
| `config/feature.json` | Feature settings |

#### Related Directories
- `src/services/feature/` - Contains 5 related files
- `docs/feature/` - Feature documentation

---

### Code Patterns

#### Pattern 1: [Descriptive Name]
**Location**: `src/services/feature.ts:45-67`
**Used for**: [What this pattern accomplishes]

```typescript
// Actual code from the file
export async function createFeature(input: CreateInput): Promise<Feature> {
  const validated = schema.parse(input);
  const result = await repository.create(validated);
  logger.info('Feature created', { id: result.id });
  return result;
}
```

**Key aspects**:

- Validates input with schema
- Uses repository pattern for data access
- Logs after successful creation

#### Pattern 2: [Alternative/Related Pattern]

**Location**: `src/services/other.ts:89-110`
**Used for**: [What this pattern accomplishes]

```typescript
// Another example from the codebase
...
```

---

### Testing Patterns

**Location**: `src/services/__tests__/feature.test.ts:15-45`

```typescript
describe('createFeature', () => {
  it('should create feature with valid input', async () => {
    const input = { name: 'test' };
    const result = await createFeature(input);
    expect(result.id).toBeDefined();
  });

  it('should reject invalid input', async () => {
    await expect(createFeature({})).rejects.toThrow();
  });
});
```

---

### Conventions Observed

- [Naming pattern observed]
- [File organization pattern]
- [Import/export convention]

### Entry Points

| Location | How It Connects |
|----------|-----------------|
| `src/index.ts:23` | Imports feature module |
| `api/routes.ts:45` | Registers feature routes |
