# Writing a good `AGENTS.md` (`CLAUDE.md`)

This guide is taken from the [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) blog post and extended with more important and relevant information.

## Principle: LLMs are (mostly) stateless

LLMs are stateless functions. Their weights are frozen by the time they're used for inference, so they don't learn over time. The only thing that the model knows about your codebase is the tokens you put into it.

Similarly, coding agent harnesses such as Claude Code usually require you to manage agents' memory explicitly. AGENTS.md (or CLAUDE.md) is the only file that by default goes into every single conversation you have with the agent.

**This has three important implications**:

1. Coding agents know absolutely nothing about your codebase at the beginning of each session.
2. The agent must be told anything that's important to know about your codebase each time you start a session.
3. `AGENTS.md` is the preferred way of doing this.

## `AGENTS.md` onboards agent to your codebase

Since agent doesn't know anything about your codebase at the beginning of each session, you should use `AGENTS.md` to onboard agent into your codebase. At a high level, this means it should cover:

- **WHAT**: tell agent about the tech, your stack, the project structure. Give agent a map of the codebase. This is especially important in monorepos! Tell agent what the apps are, what the shared packages are, and what everything is for so that it knows where to look for things
- **WHY**: tell agent the purpose of the project and what everything is doing in the repository. What are the purpose and function of the different parts of the project?
- **HOW**: tell agent how it should work on the project. For example, do you use `bun` instead of `node`? You want to include all the information it needs to actually do meaningful work on the project. How can agent verify agent's changes? How can it run tests, typechecks, and compilation steps?

But the way you do this is important! Don't try to stuff every command agent could possibly need to run in your AGENTS.md file - you will get sub-optimal results.

## Creating a good `AGENTS.md` file

The following section provides a number of recommendations on how to write a good `AGENTS.md` file following [context engineering best practices](https://github.com/humanlayer/12-factor-agents/blob/d20c728368bf9c189d6d7aab704744decb6ec0cc/content/factor-03-own-your-context-window.md).

*Your mileage may vary*. Not all of these rules are necessarily optimal for every setup. Like anything else, feel free to break the rules once...

1. you understand when & why it's okay to break them
2. you have a good reason to do so

### Less (instructions) is more

It can be tempting to try and stuff every single command that agent could possibly need to run, as well as your code standards and style guidelines into `AGENTS`.md. **We recommend against this**.

Though the topic hasn't been investigated in an incredibly rigorous manner, [some research](https://arxiv.org/pdf/2507.11538) has been done which indicates the following:

1. **Frontier thinking LLMs can follow ~ 150-200 instructions with reasonable consistency**.  
Smaller models can attend to fewer instructions than larger models, and non-thinking models can attend to fewer instructions than thinking models.
2. **Smaller models get MUCH worse, MUCH more quickly**. Specifically, smaller models tend to exhibit an expotential decay in instruction-following performance as the number of instructions increase, whereas larger frontier thinking models exhibit a linear decay (see below). For this reason, we recommend against using smaller models for multi-step tasks or complicated implementation plans.
3. **LLMs bias towards instructions that are on the peripheries of the prompt**: at the very beginning (the Claude Code system message and `CLAUDE.md`), and at the very end (the most-recent user messages)
4. **As instruction count increases, instruction-following quality decreases uniformly**. This means that as you give the LLM more instructions, it doesn't simply ignore the newer ("further down in the file") instructions - it begins to **ignore all of them uniformly**

Analysis of the Claude Code harness indicates that **Claude Code's system prompt contains ~50 individual instructions**. Depending on the model you're using, that's nearly a third of the instructions your agent can reliably follow already - and that's before rules, plugins, skills, or user messages.

This implies that your `AGENTS.md` file should contain as few instructions as possible - ideally only ones which are universally applicable to your task.

### `AGENTS.md` file length & applicability

All else being equal, **an LLM will perform better on a task when its' context window is full of focused, relevant context** including examples, related files, tool calls, and tool results compared to when its context window has a lot of irrelevant context.

Since `AGENTS.md` goes into every single session, you should ensure that its contents are as universally applicable as possible.

For example, avoid including instructions about (for example) how to structure a new database schema - this won't matter and will distract the model when you're working on something else that's unrelated!

Length-wise, the less is more principle applies as well. While Anthropic does not have an official recommendation on how long your `AGENTS.md` file should be, general consensus is that < 300 lines is best, and shorter is even better.

At HumanLayer, the root `CLAUDE.md` file is less than sixty lines.

### Progressive Disclosure

Writing a concise `AGENTS.md` file that covers everything you want agent to know can be challenging, especially in larger projects.

To address this, we can leverage the principle of **Progressive Disclosure** to ensure that claude only sees task- or project-specific instructions when it needs them.

Instead of including all your different instructions about building your project, running tests, code conventions, or other important context in your `AGENTS.md` file, we recommend keeping task-specific instructions in separate markdown files with self-descriptive names somewhere in your project.

For example:

```
agent_docs/
  |- building_the_project.md
  |- running_tests.md
  |- code_conventions.md
  |- service_architecture.md
  |- database_schema.md
  |- service_communication_patterns.md
```

Then, in your `AGENTS.md` file, you can include a list of these files with a brief description of each, and instruct agent to decide which (if any) are relevant and to read them before it starts working. Or, ask agent to present you with the files it wants to read for aproval first before reading them.

**Prefer pointers to copies**. Don't include code snippets in these files if possible - they will become out-of-date quickly. Instead, include `file:line` references to point agent to the authoritative context.

Conceptually, this is very similar to how [Claude Skills](https://code.claude.com/docs/en/skills) are intended to work, although skills are more focused on tool use than instructions.

### Agent is (not) an expensive linter

One of the most common things that we see people put in their `AGENTS.md` file is code style guidelines. **Never send an LLM to do a linter's job**. LLMs are comparably expensive and *incredibly* slow compared to traditional linters and formatters. We think you should *always use deterministic tools whenever you can*.

Code style guidelines will inevitably add a bunch of instructions and mostly-irrelevant code snippets into your context window, degrading your LLM's performance and instruction-following and eating up your context window.

**LLMs are in-context learners**! If your code follows a certain set of style guidelines or patterns, you should find that armed with a few searches of your codebase (or a good research document!) your agent should tend to follow existing code patterns and conventions without being told to.

If you feel very strongly about this, you might even consider setting up an agent Stop hook that runs your formatter & linter and presents errors to agent for it to fix. Don't make agent find the formatting issues itself.

**Bonus points**: use a linter that can automatically fix issues (HumanLayer likes Biome), and carefully tune your rules about what can safely be auto-fixed for maximum (safe) coverage.

You could also create a Slash Command that includes your code guidelines and which points agent at the changes in version control, or at your `git status`, or similar. This way, you can handle implementation and formatting separately. **You will see better results with both as a result**.

### Don't use /init or auto-generate your `AGENTS.md`

Both Claude Code and other harnesses with OpenCode come with ways to auto-generate your `AGENTS.md` file (or `CLAUDE.md`).

Because `AGENTS.md` goes into every single session with agent, it is one of **the highest leverage points of the harness** - for better or for worse, depending on how you use it.

A bad line of code is a bad line of code. A bad line of an implementation plan has the potential to create a **lot** of bad lines of code. A bad line of a research that misunderstands how the system works has the potential to result in a lot of bad lines in the plan, and therefore a **lot more** bad lines of code as a result.

But the `AGENTS.md` file affects **every single phase of your workflow** and every single artifact produced by it. As a result, we think you should spend some time thinking very carefully about every single line that goes into it:


```
                         Hierarchy of Leverage

             +------------------------------------------+
             | 1 bad line of code == 1 bad line of code |<====+-------------\
             +------------------------------------------+     |             |
                                                              |             |
           +-----------------------------------------------+  |             |
           | 1 bad line of plan == 100 wrong lines of code |--/             |
           |             -> WRONG SOLUTION                 |<=====+---------+
           +-----------------------------------------------+      |         |
                                                                  |         |
        +------------------------------------------------------+  |         |
        | 1 bad line of research == 10-100 wrong lines of plan |--/         |
        |          -> WRONG UNDERSTANDING OF SYSTEM            |<======+----+
        +------------------------------------------------------+       |    |
                                                                       |    |
    +---------------------------------------------------------------+  |    |
    | 1 bad line of specification == 10-100 wrong lines of research |--/    |
    |              -> WRONG UNDERSTANDING OF PROBLEM                |<------+
    +---------------------------------------------------------------+       |
                                                                            |
+------------------------------------------------------------------------+  |
| 1 bad line of `AGENTS.md` affects every single spec, research and plan |--/
|           -> DEGRADATION OF CORE COMPETENCY AND METHODOLOGY            |
+------------------------------------------------------------------------+
```

### Markdown Syntax

These are answers given by [Gemini](https://gemini.google.com/).

- When using ordered lists in markdown use sequential numbering (1., 2., 3.) instead of repeating the same number (1., 1., 1.). This is because while the lists are rendered the same way, the LLM needs clarity. Explicit sequences provide a stronger "ordinal signal". Also, when referencing the certain item it is clearer for both human and AI to see the actual number instead of counting the items.
- Avoid using excessive spaces in the markdown tables. While it may improve readability for humans, every space consumes tokens of context. It is enough to have a single space before and after the content in each cell. Also minimize the separators down to three dashes "| --- | --- |".
- While horisontal spaces are a waste, pay **strong** attention to the empty lines. Those are **strong delimiters** that help the model's attention mechanism reset and focus on the new type of data structure.

   | Element | Empty Line Before? | Empty Line After? | Why? |
   | --- | --- | --- | --- |
   | **Headers** | **Required** | Optional | Defines hierarchy. |
   | **Lists** | **Recommended** | **Recommended** | "Prevents ""bleeding"" into prose." |
   | **Code Blocks** | **Crucial** | **Crucial** | Separates instructions from code logic. |
   | **Tables** | **Recommended** | **Recommended** | Isolates structured data from text. |

- Use **bold** for hard constrainst and primary keywords. Think of bolding as a "High-Priority" flag.
   - **Labels**: Use bolding to name your sections (e.g. **Constraints:**, **Output Format:**).
   - **Negations**: Words like **NOT**, **NEVER**, or **WITHOUT** should be bolded to ensure the model doesn't miss the netative constraint.
   - **Key Variables**: If you define a specific term the AI must use, bolding it helps anchor that term in the model's "memory"."
   **Example**: "You must **NEVER** mention internal project names in the final summary."
- Use **Italics** for style, persona, and nuance. Italics acts as a "soft" signal. They are less about the *what* and more about the *how*.
   - **Tone Instructions**: If you want the AI to be *witty* or *professional*, italics help separate these stylistic descriptors from the actual task.
   - **Meta-Comments**: Use italics for parethetical asides or minor examples that clarify a point without being a "hard-rule".
   - **Subtle Emphasis**: Use them for words that change the *flavor* of a sentence but aren't structural deal-breakers.
   **Example*: "Respond in a *conversational* yet *authoritative* tone."
- Use **Bold + Italics** for critical warnings and "Golden Rules". This is your "Break Glass in Case of Emergency" formatting. If you use it everywhere, it creates massive context pollution because the AI won't know what is actually highest priority.
   - **Absolute Requirements**: Use this for the one or two rules that, if broken, make the entire output useless.
   - **The "Safety" Rule**: Often used for legal or safety boundaries within a prompt.
   **Example**: "***Under no circumstances provide health or medical advice.***"

   | Style | Purpose | Signal Strength | Frequency |
   | --- | --- | --- | --- |
   | **Bold** | Constraints / Labels | High | Frequent |
   | *Italics* | Tone / Nuance | Low | Occasional |
   | ***Both*** | Critical "Do Not Cross" | Extreme | Rare (once per prompt) |

- Use **Blockquotes** as a way to tell the AI, "This information is a separete 'object' or 'package' that I want you to look at, but it is not the instruction itself."
   - **Providing Examples (Few-Shot Prompting)**. This is the most common use. If you want to show the AI how to behave, wrap your examples in blockquotes. It prevents the AI from getting confused and thinking the *example's* content is a new instruction for the *current* task.
   **Example:**

   ```markdown
   Use the following style for your summaries:

   > **Input:** The cat sat on the mat.
   > **Output:** Feline placement confirmed on floor covering.
   ```

   - **Separating Source Material**. If you're asking the AI to analyze a specific piece of text, an email, or a quote, blockquote it. This creates a "container" around the data, which helps the AI distinguish between "Your Directions" and "The Target Data".
   - **Role-Play or Persona Background**. If you have a lengthy description of a persona (e.g. a "Customer Profile" or a "Historical Character"), putting it in a blockquote signals that this is a **background context** rather than the immediate task at hand.
   - **Fight Instruction Drift**. When a prompt is very long, the AI can sometimes forget where your instructions ended and where the data began. By wrapping your data or examples in `>`:

      1. You provide a visual and structural anchor.
      2. You utilize the model's training on Markdown, where `>` usually denotes "quoted" or "external" content.
      3. You make the prompt significantly easier fo *you* to read and maintain.

   - **Using Blockquotes vs. Code Blocks:**

   | Feature | Blockquotes (`>`) | Code Blocks (`` ` ``) |
   | --- | --- | --- |
   | **Best For** | "Prose, examples, quotes, personas." | "Code, JSON, raw data, logs." |
   | **AI Perception** | "This is a special passage of text." | "This is literal data/syntax to be parsed." |
   | **Risk** | The AI might still try to "read" it as text. | The AI strictly treats it as a distinct block of logic. |

- **The "Prompt Pyramid" Strategy**:

   1. **Structure** with Headings (`#`, `##`).
   2. **Organize** with Lists (`*`, `1.`).
   3. **Highlight** with Bolding (`**`).
   4. **Refine** with Italics (`*`).

- ***NEVER use ASCII diagrams to explain logic for AI.*** ASCII diagrams while look good to humans are the nightmare for the AI. They are **Expensive Token Bloat**, **Whitespace Fragile**, and the source of **Instruction Confusion** when AI tries to interpret dashes and slashes as mathematical operators. There efficient alternatives:

   - **Mermaid Syntax**. Most frontier models are trained extensively on code repositories (like GitHub) where **Mermaid.js** is the standard for diagrams. They understand them perfectly and it uses standard token-efficient and semantically clear logic.
   **Instead of ASCII:**
   
   ```text
   +------+                +--------+              +----+
   | User | --(request)--> | Server | --(query)--> | DB |
   +------+                +--------+              +----+
   ```

   **Use Mermaid:**
   
   ````markdown
   ```mermaid
   graph LR
     User -- request --> Server
     Server -- query --> Database
   ```
   ````

   Renders as:

   ```mermaid
   graph LR
     User -- request --> Server
     Server -- query --> Database
   ```

   - **Nested Indented Lists**. For hierarchical logic or simple sequential flows, nothing beats a nested list. It is the most "native" way for an LLM to process order and dependency.

   ```markdown
   - **Step 1**: User Initiation
      - Trigger: Button Click
      - Action: Send POST request to `/api/data`
   - **Step 2**: API Layer
      - Validation: Check Auth Token
      - Next: Forward to Database
   ```

   - **Pseudocode or Logic Blocks**. If the flow is conditional (If/Then), use pseudocode. It removes the ambiguity of "arrows" and replaces them with strict logic.

   ```pseudocode
   FLOW:
   IF user_authenticated:
     GOTO database_fetch
   ELSE:
     RETURN 403_error
   ```

### XML tags in prompts, agents and skills

It's extremely beneficial to use XML tags. While Markdown headers (`#`, `##`) are great for humans, XML-style tags like `<context>` and `<objective>` are like **GPS coordinates** for an AI. Large Language Models are trained heavily on code and documentation where tags are used to define strict boundaries.

1. **The "Container" Effect**: Markdown headers are "one-sided" -- they mark the beginning of a section but not the end. The AI has to guess where the "Context" section ends and the "Instructions" begins. GitHub Copilot often pulls in "neighboring files" and "open tabs" as hidden context. Using tags creates a **high-contrast barrier** between **your prompt instructions**, **highlighted code** and **other pulled-in context**. Combine Markdown and XML tags. Use Markdown for readability (`### Instructions`) and use tags for structural isolation (`<instructions>...</instructions>`).

2. **Common Tag Schema for Copilot Prompts**:

| Tag | Purpose |
| --- | --- |
| `<role>` | Defines the persona (e.g., Senior DevOps, Security Auditor) |
| `<context>` | Provides background on the codebase or the "why" behind the task. |
| `<constraints>` | Lists the "No-Go" zones (e.g., no external libraries, must be ES6) |
| `<task>` | The core action you want performed |
| `<example>` | Few-shot examples to guide the output style |
| `<output>` | Specifies the exact format (JSON, YAML, a specific function) |

3. **Prompt Example**

```markdown
<role>
You are an expert TypeScript developer focusing on performance optimization.
</role>

<context>
The current function handles massive JSON arrays from a legacy API.  
The current bottleneck is the nested mapping logic.
</context>

<task>
Refactor the following code to use a single pass through the data.
</task>

<constraints>
- Do not use Lodash.
- Maintain O(n) time complexity.
</constraints>

<code>
[Insert Code Here]
</code>
```

3. Agents and skills are unique because they use **Tools** (e.g. searching the codebase, running a terminal command). When an agent runs a tool, the result is dumped back into the conversation context. Instruct the agent:

```markdown
"Always wrap the output of your analysis in `<analysis>` tags before calling the next tool."
```

This makes it incredibly easy for the agent to find its own previus thoughts amidst raw logs and search results. In an agent file, you are often managing three distinct "streams" of information:

   - `<persona>`: Who the agent is.
   - `<tools_guidance>`: Precise logic on *how* and *when* to use specific tools (e.g., "Only use `grep` if the file is over 500 lines").
   - `<knowledge>`: Static snippets of documentation or "tribal knowledge" the agent must always remember.

**Example: A Skill Definition (`SKILL.md`):**

```markdown
---
name: migration-pattern
description: Migrating from REST to GraphQL
---

<objective>
Refactor legacy Express.js endpoints to Apollo Server resolvers.
</objective>

<process>
1. Parse the REST route in <input_code>.
2. Define the equivalent GQL schema.
3. Map the database logic into the resolver.
</process>

<knowledge_base>
- Use the 'BaseResolver' class found in /src/shared/base.ts.
- All resolvers must include the @Authorized() decorator.
</knowledge_base>

<rules>
- NEVER modify the database schema during migration.
- DO NOT use any libraries except 'type-graphql'.
</rules>
```

4. **Do not use tags for simple prompts**.

## In Conclusion

1. `AGENTS.md` is for onboarding agent into your codebase. It should define your project's **WHY**, **WHAT**, and **HOW**.
2. **Less (instructions) is more**. While you shouldn't omit necessary instructions, you should include as few instructions as reasonably possible in the file.
3. Keep the contents of your `AGENTS.md` **concise and universally applicable**.
4. Use **Progressive Disclosure** - don't tell agent all the information you could possibly want it to know. Rather, tell it *how to find* important information so that it can find and use it, but only when it needs to to avoid bloating your context window or instruction count.
5. **Syntax matters**. Use markdown syntax strategically to minimize the context pollution and keeping your instructions clear and easy to follow for the model.
6. **Use XML tags in prompts, agents and skills**. If you design tools or agents to handle complex multi-step workflows, XML tags are the best defence against "context collapse". They ensure the AI never forgets it's an agent, even when it's looking at 1,000 lines of error logs.
7. Agent is not a linter. Use linters and code formatters, and use other features like Hooks and Slash Commands as necessary.
8. `AGENTS.md` **is the highest leverage point of the harness**, so avoid auto-generating it. You should carefully craft its contents for best results.
