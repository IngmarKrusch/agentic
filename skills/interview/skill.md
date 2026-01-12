---
description: "Conduct structured interviews to clarify requirements, explore decisions, solve problems, and produce actionable documents. Use this skill when: (1) exploring requirements before implementation, (2) making architecture or design decisions, (3) investigating problems or debugging, (4) prioritizing work or weighing tradeoffs, (5) designing workflows or processes, or the user says 'interview me', 'let's discuss', 'clarify requirements'. Do NOT use for product specs (use /product-spec), tech specs (use /tech-spec), or bug logging (use /bug)."
argument-hint: "[topic to explore or define]"
---
If not already in plan mode, enter plan mode now. Do not exit plan mode without explicit user approval.

{{#if $ARGUMENTS}}
**Topic to explore:** $ARGUMENTS
{{else}}
**No explicit topic provided.** Ask the user what they want to explore or define.
{{/if}}

## CRITICAL: You MUST Interview First

**Do NOT skip to document creation.** Even if the user provided detailed context, you MUST conduct an interactive, adaptive interview using the AskUserQuestion tool. Reading files or analyzing context is NOT a substitute for asking questions.

Your primary job is to interview me, not to plan. Ask me literally everything needed to fully understand the topic. Make sure your questions are not obvious - they should probe deeper, challenge assumptions, and uncover things I haven't considered.

**Rules:**
- Ask 1-2 questions at a time
- Base questions on my previous answers
- Continue until the topic is thoroughly explored (minimum 3-4 rounds)

## Phase 1: Topic Type Detection

First, determine what type of exploration this is (ask if unclear):

1. **Feature/Spec Definition** - Scope, feature, bugfix, enhancement to be spec'ed
2. **Architecture Decision** - Choosing between technical approaches, technologies, patterns
3. **Problem-Solving** - Understanding and solving a specific problem
4. **Investigation/Research** - Learning about something, gathering information
5. **Prioritization/Tradeoffs** - Choosing between options, weighing criteria
6. **Workflow/Process Design** - How work flows, automation, responsibilities
7. **General Planning** - Any other structured planning need

## Phase 2: Deep, Adaptive Interview

Interview me thoroughly using the AskUserQuestion tool. Adapt questions to the topic type:

**For Feature/Spec Definition:**
- What is the scope and boundaries of this feature?
- How is the functionality supposed to work?
- How does it integrate with existing functionality?
- What are the edge cases and error conditions?
- What are the user flow and UI/UX considerations?
- What tradeoffs or concerns exist?
- Everything else needed to fully define the spec.

**For Architecture Decisions:**
- What decision needs to be made? What is the context?
- What constraints exist (technical, team, timeline)?
- What options have been considered so far?
- What are the evaluation criteria?
- What research is needed before deciding?
- What are the reversibility/cost implications?

**For Problem-Solving:**
- What is the problem exactly? What symptoms are observed?
- What is the desired state?
- What has been tried already?
- What constraints exist?
- What are potential root causes?
- What does success look like?

**For Investigation/Research:**
- What are we trying to learn or understand?
- What do we already know?
- What are the key unknowns?
- Where should we look for information?
- How will we know we have enough info?
- What decisions depend on this research?

**For Prioritization/Tradeoffs:**
- What options are on the table?
- What are the evaluation criteria?
- What constraints exist (time, resources, dependencies)?
- What are the risks of each option?
- What is the cost of reversing a decision?
- Who are the stakeholders affected?

**For Workflow/Process Design:**
- What is the current state (if any)?
- What pain points exist?
- What are the handoffs and responsibilities?
- What should be automated vs manual?
- What are the inputs and outputs?
- How will success be measured?

**For General Planning:**
- What is the goal?
- What are the constraints?
- What are the steps or phases?
- What are the risks?
- How do we verify success?
- What dependencies exist?

## Phase 3: Document Output

Once the interview is complete, create a clear, actionable document.

**For Feature/Spec Definition:**
- Write a spec file (product-spec or tech-spec format)
- Keep it concise but comprehensive
- Avoid code examples unless absolutely necessary
- Ask for filename if not obvious

**For other topic types:**
- Architecture Decision → Decision document with options, criteria, recommendation
- Problem-Solving → Problem statement with analysis and solution approach
- Investigation → Research plan with questions and sources
- Prioritization → Decision matrix or prioritized list with rationale
- Workflow → Process description with responsibilities and steps
- General → Plan document with goals, steps, and success criteria

Ask the user where to write the document if not obvious.